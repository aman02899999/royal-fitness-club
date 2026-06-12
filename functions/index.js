'use strict';

/**
 * functions/index.js — Firebase Cloud Functions
 * Royal Fitness Club SaaS Platform
 *
 * Endpoints:
 *   createRazorpayOrder    — creates a server-side Razorpay order (subscription)
 *   verifyRazorpayPayment  — verifies payment signature and activates subscription
 *   createPDFOrder         — creates a Razorpay order for PDF purchase
 *   recordPDFPurchase      — verifies payment signature and writes pdf_purchases
 *   razorpayWebhook        — handles Razorpay webhook events
 *   expireSubscriptions    — daily sweep to downgrade expired subscriptions
 *   createMember           — admin-only: creates Auth user + Firestore member doc
 *   generateAIMealPlan     — AI-powered Indian meal plan via ChatGPT (OpenAI)
 *
 * Secrets (set once via Firebase CLI, stored in Google Secret Manager):
 *   firebase functions:secrets:set RAZORPAY_KEY_ID
 *   firebase functions:secrets:set RAZORPAY_KEY_SECRET
 *   firebase functions:secrets:set RAZORPAY_WEBHOOK_SECRET
 *   firebase functions:secrets:set OPENAI_API_KEY
 *
 * ⚠️  NEVER commit real credentials to source control.
 */

const functions = require('firebase-functions');
const { defineSecret } = require('firebase-functions/params');
const admin = require('firebase-admin');
const Razorpay = require('razorpay');
const crypto = require('crypto');
const cors = require('cors')({ origin: true });
const OpenAI = require('openai');

admin.initializeApp();

// ---------------------------------------------------------------------------
// Secret definitions — values resolved at function invocation time
// ---------------------------------------------------------------------------
const RZP_KEY_ID = defineSecret('RAZORPAY_KEY_ID');
const RZP_KEY_SECRET = defineSecret('RAZORPAY_KEY_SECRET');
const RZP_WEBHOOK_SECRET = defineSecret('RAZORPAY_WEBHOOK_SECRET');
const OPENAI_API_KEY = defineSecret('OPENAI_API_KEY');

// Lazily creates a Razorpay instance inside a function invocation where
// secrets are available. Must NOT be called at module load time.
const getRazorpay = () => new Razorpay({
  key_id: RZP_KEY_ID.value(),
  key_secret: RZP_KEY_SECRET.value(),
});

// ---------------------------------------------------------------------------
// Plan amounts (in paise — 1 INR = 100 paise)
// ---------------------------------------------------------------------------
const PLAN_AMOUNTS = {
  royal_pro: 49900,    // ₹499
  royal_elite: 199900, // ₹1999
};

// ---------------------------------------------------------------------------
// PDF product catalog
// ---------------------------------------------------------------------------
const PDF_CATALOG = {
  anabolic_full_guide: { amount: 29900, name: 'Anabolic Full Guide' },
  fitness_mindset:     { amount: 29900, name: 'Fitness & Mindset Guidance' },
};

// ---------------------------------------------------------------------------
// createRazorpayOrder — HTTPS Callable
// ---------------------------------------------------------------------------
exports.createRazorpayOrder = functions
  .runWith({ secrets: [RZP_KEY_ID, RZP_KEY_SECRET] })
  .https.onCall(async (data, context) => {
    if (!context.auth) {
      throw new functions.https.HttpsError('unauthenticated', 'You must be logged in to create a payment order.');
    }

    const { plan } = data;
    const uid = context.auth.uid;
    const amount = PLAN_AMOUNTS[plan];

    if (!amount) {
      throw new functions.https.HttpsError('invalid-argument', `Invalid plan "${plan}". Valid options: royal_pro, royal_elite.`);
    }

    try {
      const order = await getRazorpay().orders.create({
        amount,
        currency: 'INR',
        receipt: `rfc_${uid}_${Date.now()}`,
        notes: { uid, plan },
      });

      await admin.firestore().collection('payment_orders').doc(order.id).set({
        orderId: order.id,
        uid,
        plan,
        amount,
        currency: 'INR',
        status: 'created',
        createdAt: admin.firestore.FieldValue.serverTimestamp(),
      });

      console.log('[createRazorpayOrder] Order created:', order.id, uid, plan);
      return { orderId: order.id, amount, currency: 'INR', keyId: RZP_KEY_ID.value() };
    } catch (err) {
      console.error('[createRazorpayOrder] Error:', err);
      throw new functions.https.HttpsError('internal', 'Failed to create Razorpay order. Please try again.');
    }
  });

// ---------------------------------------------------------------------------
// verifyRazorpayPayment — HTTPS Callable
// ---------------------------------------------------------------------------
exports.verifyRazorpayPayment = functions
  .runWith({ secrets: [RZP_KEY_SECRET] })
  .https.onCall(async (data, context) => {
    if (!context.auth) {
      throw new functions.https.HttpsError('unauthenticated', 'You must be logged in to verify a payment.');
    }

    const { orderId, paymentId, signature, plan } = data;
    const uid = context.auth.uid;

    if (!orderId || !paymentId || !signature || !plan) {
      throw new functions.https.HttpsError('invalid-argument', 'orderId, paymentId, signature, and plan are all required.');
    }

    const expectedSignature = crypto
      .createHmac('sha256', RZP_KEY_SECRET.value())
      .update(`${orderId}|${paymentId}`)
      .digest('hex');

    if (expectedSignature !== signature) {
      console.warn('[verifyRazorpayPayment] Signature mismatch for order:', orderId);
      throw new functions.https.HttpsError('invalid-argument', 'Payment signature verification failed. The payment may have been tampered with.');
    }

    try {
      const db = admin.firestore();
      const batch = db.batch();
      const now = admin.firestore.FieldValue.serverTimestamp();

      const expiryDate = new Date();
      expiryDate.setDate(expiryDate.getDate() + 30);
      const expiryTimestamp = admin.firestore.Timestamp.fromDate(expiryDate);
      const amountInRupees = plan === 'royal_pro' ? 499 : 1999;

      const subRef = db.collection('subscriptions').doc();
      batch.set(subRef, {
        uid, plan, status: 'active',
        amount: amountInRupees, currency: 'INR',
        razorpayOrderId: orderId, razorpayPaymentId: paymentId,
        startDate: now, expiryDate: expiryTimestamp,
        createdAt: now, updatedAt: now,
      });

      batch.update(db.collection('users').doc(uid), {
        plan, subscriptionId: subRef.id, expiryDate: expiryTimestamp, updatedAt: now,
      });

      batch.update(db.collection('payment_orders').doc(orderId), {
        status: 'paid', paymentId, verifiedAt: now,
      });

      await batch.commit();
      console.log('[verifyRazorpayPayment] Subscription activated:', subRef.id, uid, plan);
      return { success: true, subscriptionId: subRef.id };
    } catch (err) {
      console.error('[verifyRazorpayPayment] Firestore batch error:', err);
      throw new functions.https.HttpsError('internal', 'Payment verified but subscription activation failed. Contact support with payment ID: ' + paymentId);
    }
  });

// ---------------------------------------------------------------------------
// createPDFOrder — HTTPS Callable
// ---------------------------------------------------------------------------
exports.createPDFOrder = functions
  .runWith({ secrets: [RZP_KEY_ID, RZP_KEY_SECRET] })
  .https.onCall(async (data, context) => {
    if (!context.auth) {
      throw new functions.https.HttpsError('unauthenticated', 'You must be logged in.');
    }

    const uid = context.auth.uid;
    const itemId = data.itemId || 'anabolic_full_guide';

    if (!PDF_CATALOG[itemId]) {
      throw new functions.https.HttpsError('invalid-argument', `Unknown product: ${itemId}`);
    }
    const { amount } = PDF_CATALOG[itemId];

    const existing = await admin.firestore()
      .collection('pdf_purchases').doc(uid)
      .collection('items').doc(itemId).get();
    if (existing.exists) {
      throw new functions.https.HttpsError('already-exists', 'You have already purchased this guide.');
    }

    let order;
    try {
      order = await getRazorpay().orders.create({
        amount,
        currency: 'INR',
        receipt: `pdf_${uid.slice(-8)}_${Date.now()}`,
        notes: { uid, itemId },
      });
    } catch (err) {
      console.error('[createPDFOrder] Razorpay order error:', err);
      throw new functions.https.HttpsError('internal', 'Could not create payment order. Please try again.');
    }

    await admin.firestore().collection('payment_orders').doc(order.id).set({
      uid, itemId, type: 'pdf_purchase',
      amount, currency: 'INR', status: 'pending',
      razorpayOrderId: order.id,
      createdAt: admin.firestore.FieldValue.serverTimestamp(),
    });

    console.log('[createPDFOrder] Order created:', order.id, uid, itemId);
    return { orderId: order.id, keyId: RZP_KEY_ID.value(), amount, currency: 'INR' };
  });

// ---------------------------------------------------------------------------
// recordPDFPurchase — HTTPS Callable
// ---------------------------------------------------------------------------
exports.recordPDFPurchase = functions
  .runWith({ secrets: [RZP_KEY_SECRET] })
  .https.onCall(async (data, context) => {
    if (!context.auth) {
      throw new functions.https.HttpsError('unauthenticated', 'You must be logged in.');
    }

    const { orderId, paymentId, signature } = data;
    const itemId = data.itemId || 'anabolic_full_guide';
    const uid = context.auth.uid;

    if (!PDF_CATALOG[itemId]) {
      throw new functions.https.HttpsError('invalid-argument', `Unknown product: ${itemId}`);
    }
    if (!orderId || !paymentId || !signature) {
      throw new functions.https.HttpsError('invalid-argument', 'orderId, paymentId, and signature are all required.');
    }

    const expectedSig = crypto
      .createHmac('sha256', RZP_KEY_SECRET.value())
      .update(`${orderId}|${paymentId}`)
      .digest('hex');

    if (expectedSig !== signature) {
      console.warn('[recordPDFPurchase] Signature mismatch — orderId:', orderId);
      throw new functions.https.HttpsError('invalid-argument', 'Payment signature verification failed.');
    }

    const db = admin.firestore();
    const now = admin.firestore.FieldValue.serverTimestamp();
    const batch = db.batch();
    const amountRupees = Math.round(PDF_CATALOG[itemId].amount / 100);

    batch.set(
      db.collection('pdf_purchases').doc(uid).collection('items').doc(itemId),
      { uid, itemId, orderId, paymentId, amount: amountRupees, currency: 'INR', purchasedAt: now }
    );
    batch.update(db.collection('payment_orders').doc(orderId), {
      status: 'paid', paymentId, verifiedAt: now,
    });

    await batch.commit();
    console.log('[recordPDFPurchase] PDF purchased:', uid, itemId, paymentId);
    return { success: true };
  });

// ---------------------------------------------------------------------------
// razorpayWebhook — HTTPS Request
// ---------------------------------------------------------------------------
exports.razorpayWebhook = functions
  .runWith({ secrets: [RZP_WEBHOOK_SECRET] })
  .https.onRequest((req, res) => {
    cors(req, res, async () => {
      if (req.method !== 'POST') return res.status(405).send('Method Not Allowed');

      const webhookSecret = RZP_WEBHOOK_SECRET.value();
      const incomingSignature = req.headers['x-razorpay-signature'];

      if (webhookSecret) {
        if (!incomingSignature) {
          console.warn('[razorpayWebhook] Missing x-razorpay-signature header');
          return res.status(400).send('Missing signature header');
        }
        const hmac = crypto
          .createHmac('sha256', webhookSecret)
          .update(JSON.stringify(req.body))
          .digest('hex');
        if (hmac !== incomingSignature) {
          console.warn('[razorpayWebhook] Invalid webhook signature');
          return res.status(400).send('Invalid signature');
        }
      }

      const event = req.body.event;
      const paymentEntity = req.body.payload?.payment?.entity;
      const payload = paymentEntity || req.body.payload?.subscription?.entity;
      console.log('[razorpayWebhook] Received event:', event);

      const db = admin.firestore();

      try {
        if (event === 'payment.captured') {
          const orderId = paymentEntity?.order_id;
          if (!orderId) return res.json({ received: true });

          const orderDoc = await db.collection('payment_orders').doc(orderId).get();
          if (orderDoc.exists) {
            const { uid, plan, status } = orderDoc.data();
            const webhookAt = admin.firestore.FieldValue.serverTimestamp();

            if (status === 'paid' || status === 'captured') {
              await db.collection('payment_orders').doc(orderId).update({ webhookAt });
              return res.json({ received: true });
            }

            const expiryDate = new Date();
            expiryDate.setDate(expiryDate.getDate() + 30);
            const expiryTimestamp = admin.firestore.Timestamp.fromDate(expiryDate);

            await db.collection('users').doc(uid).update({ plan, updatedAt: webhookAt, expiryDate: expiryTimestamp });
            await db.collection('payment_orders').doc(orderId).update({ status: 'captured', webhookAt });
            console.log('[razorpayWebhook] payment.captured: user plan updated:', uid, plan);
          }
        } else if (event === 'payment.failed') {
          const orderId = paymentEntity?.order_id;
          if (orderId) {
            await db.collection('payment_orders').doc(orderId).update({
              status: 'failed',
              failureReason: paymentEntity?.error_description || 'Unknown error',
              webhookAt: admin.firestore.FieldValue.serverTimestamp(),
            });
          }
        } else if (event === 'subscription.cancelled') {
          const razorSubId = payload?.id;
          if (razorSubId) {
            const subSnap = await db.collection('subscriptions')
              .where('razorpaySubscriptionId', '==', razorSubId).limit(1).get();
            if (!subSnap.empty) {
              const subDoc = subSnap.docs[0];
              const uid = subDoc.data().uid;
              const batch = db.batch();
              batch.update(subDoc.ref, { status: 'cancelled', cancelledAt: admin.firestore.FieldValue.serverTimestamp() });
              if (uid) batch.update(db.collection('users').doc(uid), { plan: 'free', updatedAt: admin.firestore.FieldValue.serverTimestamp() });
              await batch.commit();
              console.log('[razorpayWebhook] subscription.cancelled:', uid, razorSubId);
            }
          }
        } else {
          console.log('[razorpayWebhook] Unhandled event:', event);
        }

        return res.json({ received: true });
      } catch (err) {
        console.error('[razorpayWebhook] Error for event', event, ':', err);
        return res.json({ received: true, error: err.message });
      }
    });
  });

// ---------------------------------------------------------------------------
// expireSubscriptions — Scheduled (daily, no secrets needed)
// ---------------------------------------------------------------------------
exports.expireSubscriptions = functions.pubsub
  .schedule('every 24 hours')
  .timeZone('Asia/Kolkata')
  .onRun(async () => {
    const db = admin.firestore();
    const now = admin.firestore.Timestamp.now();

    const snap = await db.collection('subscriptions')
      .where('status', 'in', ['active', 'trial'])
      .where('expiryDate', '<=', now)
      .get();

    if (snap.empty) { console.log('[expireSubscriptions] No expired subscriptions.'); return null; }

    let batch = db.batch();
    let ops = 0;
    const commits = [];

    for (const doc of snap.docs) {
      const { uid } = doc.data();
      batch.update(doc.ref, { status: 'expired', updatedAt: admin.firestore.FieldValue.serverTimestamp() });
      batch.update(db.collection('users').doc(uid), { plan: 'free', subscriptionId: null, updatedAt: admin.firestore.FieldValue.serverTimestamp() });
      ops += 2;
      if (ops >= 450) { commits.push(batch.commit()); batch = db.batch(); ops = 0; }
    }
    if (ops > 0) commits.push(batch.commit());
    await Promise.all(commits);

    console.log('[expireSubscriptions] Expired', snap.size, 'subscriptions.');
    return null;
  });

// ---------------------------------------------------------------------------
// createMember — Admin-only Callable (no secrets needed)
// ---------------------------------------------------------------------------
exports.createMember = functions.https.onCall(async (data, context) => {
  if (!context.auth) throw new functions.https.HttpsError('unauthenticated', 'Must be logged in.');

  const callerDoc = await admin.firestore().collection('users').doc(context.auth.uid).get();
  if (!callerDoc.exists || callerDoc.data().role !== 'admin') {
    throw new functions.https.HttpsError('permission-denied', 'Admin role required.');
  }

  const { name, email, password, phone, membershipExpiry } = data;
  if (!name || !email || !password) throw new functions.https.HttpsError('invalid-argument', 'name, email and password are required.');
  if (password.length < 6) throw new functions.https.HttpsError('invalid-argument', 'Password must be at least 6 characters.');
  if (!membershipExpiry) throw new functions.https.HttpsError('invalid-argument', 'membershipExpiry is required.');

  const userRecord = await admin.auth().createUser({ email, password, displayName: name });
  const uid = userRecord.uid;
  const expiryDate = new Date(membershipExpiry);

  await admin.firestore().collection('users').doc(uid).set({
    uid, name, email, phone: phone || '',
    role: 'member', plan: 'free', status: 'active',
    membershipExpiry: admin.firestore.Timestamp.fromDate(expiryDate),
    createdAt: admin.firestore.FieldValue.serverTimestamp(),
    updatedAt: admin.firestore.FieldValue.serverTimestamp(),
    lastLogin: admin.firestore.FieldValue.serverTimestamp(),
  });

  console.log('[createMember] Created member:', uid, email);
  return { uid };
});

// ---------------------------------------------------------------------------
// generateAIMealPlan — Authenticated Callable
// Calls ChatGPT (gpt-4o-mini) to generate a personalised Indian meal plan.
// Requires OPENAI_API_KEY secret (set via: firebase functions:secrets:set OPENAI_API_KEY)
// Rate-limited: max 5 AI plans per user per day via Firestore counter.
// ---------------------------------------------------------------------------
exports.generateAIMealPlan = functions
  .runWith({ secrets: [OPENAI_API_KEY], timeoutSeconds: 60, memory: '256MB' })
  .https.onCall(async (data, context) => {
    if (!context.auth) {
      throw new functions.https.HttpsError('unauthenticated', 'You must be logged in to generate a meal plan.');
    }

    const uid = context.auth.uid;
    const { targetCals, macros, goal, diet, dietStyle, healthConditions, age, weight, gender, mealFreq } = data;

    if (!targetCals || !macros || !goal || !diet) {
      throw new functions.https.HttpsError('invalid-argument', 'targetCals, macros, goal, and diet are required.');
    }

    // Rate limit: max 5 AI plans per user per day
    const db = admin.firestore();
    const today = new Date().toISOString().slice(0, 10);
    const rateLimitRef = db.collection('ai_rate_limits').doc(`${uid}_${today}`);
    const rateLimitDoc = await rateLimitRef.get();
    const usageCount = rateLimitDoc.exists ? (rateLimitDoc.data().count || 0) : 0;

    if (usageCount >= 5) {
      throw new functions.https.HttpsError('resource-exhausted', 'You have reached the daily limit of 5 AI meal plans. Please try again tomorrow.');
    }

    const DIET_LABELS = { veg: 'Pure Vegetarian (no eggs, no meat)', nonveg: 'Non-Vegetarian (includes chicken, fish, eggs)', egget: 'Eggetarian (eggs, dairy, no meat)', keto: 'Ketogenic (very low carb, high fat)' };
    const GOAL_LABELS = { loss: 'Fat Loss — calorie deficit', gain: 'Muscle Gain — lean bulk', maintain: 'Maintenance / Body Recomposition' };
    const healthNote = Array.isArray(healthConditions) && healthConditions.length ? `Health conditions: ${healthConditions.join(', ')}.` : '';
    const meals = mealFreq || 3;

    const prompt = `You are a certified Indian sports nutritionist creating a personalised single-day meal plan.

CLIENT PROFILE:
- Gender: ${gender || 'not specified'}, Age: ${age || '—'}, Weight: ${weight || '—'} kg
- Goal: ${GOAL_LABELS[goal] || goal}
- Diet: ${DIET_LABELS[diet] || diet}
- Diet style: ${dietStyle || 'balanced'}
- ${healthNote}
- Daily targets: ${targetCals} kcal | ${macros.prot}g protein | ${macros.carb}g carbs | ${macros.fat}g fat
- Meals per day: ${meals}

INSTRUCTIONS:
1. Use only authentic Indian foods and dishes (dal, roti, rice, sabzi, paneer, chicken, eggs, etc.)
2. Each meal must include: meal name, 2-4 specific ingredients with quantities, macros, and a one-line reason
3. Total calories must sum within ±80 kcal of ${targetCals}
4. Strictly respect the diet type — no meat for veg/egget, very low carbs for keto
5. If health conditions are present, adjust accordingly (e.g. no refined sugar for diabetic, no soy for thyroid)
6. Return ONLY a JSON array — no markdown, no extra text

JSON format (array of ${meals} meal objects):
[
  {
    "meal": "Breakfast",
    "time": "7:30 AM",
    "name": "Dish name",
    "items": [{"name": "Ingredient", "qty": "80g"}],
    "kcal": 450,
    "prot": 35,
    "carb": 40,
    "fat": 12,
    "reason": "One-line reason this meal fits the goal"
  }
]`;

    try {
      const client = new OpenAI({ apiKey: OPENAI_API_KEY.value() });
      const response = await client.chat.completions.create({
        model: 'gpt-4o-mini',
        max_tokens: 1500,
        messages: [{ role: 'user', content: prompt }],
      });

      const raw = response.choices[0]?.message?.content || '[]';
      // Strip any accidental markdown fences
      const jsonStr = raw.replace(/```json?\n?/gi, '').replace(/```/g, '').trim();
      let plan;
      try {
        plan = JSON.parse(jsonStr);
      } catch {
        console.error('[generateAIMealPlan] JSON parse error. Raw response:', raw);
        throw new functions.https.HttpsError('internal', 'AI returned invalid JSON. Please try again.');
      }

      if (!Array.isArray(plan) || plan.length === 0) {
        throw new functions.https.HttpsError('internal', 'AI returned an empty meal plan. Please try again.');
      }

      // Persist rate limit counter
      await rateLimitRef.set({ uid, date: today, count: usageCount + 1, updatedAt: admin.firestore.FieldValue.serverTimestamp() }, { merge: true });

      console.log('[generateAIMealPlan] Generated plan for', uid, '— meals:', plan.length);
      return { plan, generatedAt: Date.now() };

    } catch (err) {
      if (err instanceof functions.https.HttpsError) throw err;
      console.error('[generateAIMealPlan] OpenAI API error:', err.message);
      throw new functions.https.HttpsError('internal', 'AI service temporarily unavailable. Your database plan is still active.');
    }
  });

// ---------------------------------------------------------------------------
// deleteMember — Admin-only Callable
// Deletes the Firebase Auth user AND the Firestore user document
// ---------------------------------------------------------------------------
exports.deleteMember = functions.https.onCall(async (data, context) => {
  if (!context.auth) throw new functions.https.HttpsError('unauthenticated', 'Must be logged in.');

  const callerDoc = await admin.firestore().collection('users').doc(context.auth.uid).get();
  if (!callerDoc.exists || callerDoc.data().role !== 'admin') {
    throw new functions.https.HttpsError('permission-denied', 'Admin role required.');
  }

  const { uid } = data;
  if (!uid) throw new functions.https.HttpsError('invalid-argument', 'uid is required.');
  if (uid === context.auth.uid) throw new functions.https.HttpsError('invalid-argument', 'Cannot delete your own account.');

  // Delete Firebase Auth user (ignore if already gone)
  try { await admin.auth().deleteUser(uid); } catch (e) {
    if (e.code !== 'auth/user-not-found') throw e;
  }

  // Delete Firestore document
  await admin.firestore().collection('users').doc(uid).delete();

  console.log('[deleteMember] Deleted member:', uid);
  return { success: true };
});
