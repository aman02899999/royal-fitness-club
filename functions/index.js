/**
 * functions/index.js — Firebase Cloud Functions
 * Royal Fitness Club SaaS Platform
 *
 * Backend Razorpay integration providing five endpoints:
 *
 *   createRazorpayOrder    — HTTPS Callable: creates a server-side Razorpay order (subscription)
 *   verifyRazorpayPayment  — HTTPS Callable: verifies payment signature and activates subscription
 *   createPDFOrder         — HTTPS Callable: creates a ₹299 Razorpay order for PDF purchase
 *   recordPDFPurchase      — HTTPS Callable: verifies payment signature and writes pdf_purchases
 *   razorpayWebhook        — HTTPS Request:  handles Razorpay webhook events
 *
 * Deploy:
 *   firebase deploy --only functions
 *
 * Set Razorpay credentials before deploying:
 *   firebase functions:config:set \
 *     razorpay.key_id="rzp_live_XXXXXXXXXXXXXXXX" \
 *     razorpay.key_secret="XXXXXXXXXXXXXXXXXXXXXXXX" \
 *     razorpay.webhook_secret="XXXXXXXXXXXXXXXXXXXXXXXX"
 *
 * For local development with the emulator, create a .runtimeconfig.json:
 *   {
 *     "razorpay": {
 *       "key_id": "rzp_test_PLACEHOLDER",
 *       "key_secret": "test_secret_PLACEHOLDER",
 *       "webhook_secret": ""
 *     }
 *   }
 *
 * ⚠️  IMPORTANT: Never commit real Razorpay credentials to source control.
 */

'use strict';

const functions = require('firebase-functions');
const admin = require('firebase-admin');
const Razorpay = require('razorpay');
const crypto = require('crypto');
const cors = require('cors')({ origin: true });

admin.initializeApp();

// ---------------------------------------------------------------------------
// Razorpay SDK initialisation
// ---------------------------------------------------------------------------

/**
 * Razorpay instance, configured from Firebase Functions runtime config.
 *
 * Set credentials via:
 *   firebase functions:config:set razorpay.key_id="..." razorpay.key_secret="..."
 *
 * Fallback placeholder values are used in local emulator runs only.
 * ⚠️  Replace placeholder strings with real keys — never commit real keys.
 */
const razorpay = new Razorpay({
  key_id: functions.config().razorpay?.key_id || 'rzp_test_PLACEHOLDER',
  key_secret: functions.config().razorpay?.key_secret || 'test_secret_PLACEHOLDER',
});

// ---------------------------------------------------------------------------
// Plan amounts (in paise — 1 INR = 100 paise)
// ---------------------------------------------------------------------------

const PLAN_AMOUNTS = {
  royal_pro: 49900,    // ₹499
  royal_elite: 199900, // ₹1999
};

// ---------------------------------------------------------------------------
// createRazorpayOrder — HTTPS Callable
// ---------------------------------------------------------------------------

/**
 * Creates a Razorpay order on the server and records it in Firestore.
 *
 * Input  (data):  { plan: 'royal_pro' | 'royal_elite', uid: string }
 * Output:         { orderId: string, amount: number, currency: 'INR', keyId: string }
 *
 * The returned `keyId` is the public Razorpay key that the client uses to open
 * the checkout modal. Sending it from the server means the client never needs
 * to hard-code or manage the key itself.
 *
 * Firestore writes:
 *   payment_orders/{order.id} — status:'created', uid, plan, amount
 */
exports.createRazorpayOrder = functions.https.onCall(async (data, context) => {
  // Authentication guard
  if (!context.auth) {
    throw new functions.https.HttpsError(
      'unauthenticated',
      'You must be logged in to create a payment order.'
    );
  }

  const { plan } = data;
  const uid = context.auth.uid;

  // Validate plan
  const amount = PLAN_AMOUNTS[plan];
  if (!amount) {
    throw new functions.https.HttpsError(
      'invalid-argument',
      `Invalid plan "${plan}". Valid options: royal_pro, royal_elite.`
    );
  }

  try {
    // Create order with Razorpay
    const order = await razorpay.orders.create({
      amount,
      currency: 'INR',
      receipt: `rfc_${uid}_${Date.now()}`,
      notes: {
        uid,
        plan,
      },
    });

    // Persist order details for later verification and webhook reconciliation
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

    return {
      orderId: order.id,
      amount,
      currency: 'INR',
      keyId: functions.config().razorpay?.key_id || 'rzp_test_PLACEHOLDER',
    };
  } catch (err) {
    console.error('[createRazorpayOrder] Error:', err);
    throw new functions.https.HttpsError(
      'internal',
      'Failed to create Razorpay order. Please try again.'
    );
  }
});

// ---------------------------------------------------------------------------
// verifyRazorpayPayment — HTTPS Callable
// ---------------------------------------------------------------------------

/**
 * Verifies the Razorpay payment signature and, on success, atomically:
 *   1. Creates a subscription document in `subscriptions/{subId}`.
 *   2. Updates `users/{uid}` with the new plan, subscriptionId, and expiryDate.
 *   3. Marks `payment_orders/{orderId}` as paid.
 *
 * Signature verification uses HMAC-SHA256 over "orderId|paymentId" with the
 * Razorpay key_secret. This prevents spoofed payment confirmations.
 *
 * Input  (data):  { orderId: string, paymentId: string, signature: string, plan: string }
 * Output:         { success: true, subscriptionId: string }
 */
exports.verifyRazorpayPayment = functions.https.onCall(async (data, context) => {
  // Authentication guard
  if (!context.auth) {
    throw new functions.https.HttpsError(
      'unauthenticated',
      'You must be logged in to verify a payment.'
    );
  }

  const { orderId, paymentId, signature, plan } = data;
  const uid = context.auth.uid;

  // Validate required fields
  if (!orderId || !paymentId || !signature || !plan) {
    throw new functions.https.HttpsError(
      'invalid-argument',
      'orderId, paymentId, signature, and plan are all required.'
    );
  }

  // ---------------------------------------------------------------------------
  // Signature verification
  // ---------------------------------------------------------------------------
  const keySecret = functions.config().razorpay?.key_secret || 'test_secret_PLACEHOLDER';

  const expectedSignature = crypto
    .createHmac('sha256', keySecret)
    .update(`${orderId}|${paymentId}`)
    .digest('hex');

  if (expectedSignature !== signature) {
    console.warn('[verifyRazorpayPayment] Signature mismatch for order:', orderId);
    throw new functions.https.HttpsError(
      'invalid-argument',
      'Payment signature verification failed. The payment may have been tampered with.'
    );
  }

  // ---------------------------------------------------------------------------
  // Firestore batch write — subscription + user + order update
  // ---------------------------------------------------------------------------
  try {
    const db = admin.firestore();
    const batch = db.batch();
    const now = admin.firestore.FieldValue.serverTimestamp();

    // Subscription expiry: 30 days from today
    const expiryDate = new Date();
    expiryDate.setDate(expiryDate.getDate() + 30);
    const expiryTimestamp = admin.firestore.Timestamp.fromDate(expiryDate);

    // Derive rupee amount from paise for the subscription record
    const amountInRupees = plan === 'royal_pro' ? 499 : 1999;

    // 1. New subscription document
    const subRef = db.collection('subscriptions').doc();
    batch.set(subRef, {
      uid,
      plan,
      status: 'active',
      amount: amountInRupees,
      currency: 'INR',
      razorpayOrderId: orderId,
      razorpayPaymentId: paymentId,
      startDate: now,
      expiryDate: expiryTimestamp,
      createdAt: now,
      updatedAt: now,
    });

    // 2. Update user document
    batch.update(db.collection('users').doc(uid), {
      plan,
      subscriptionId: subRef.id,
      expiryDate: expiryTimestamp,
      updatedAt: now,
    });

    // 3. Mark payment order as paid
    batch.update(db.collection('payment_orders').doc(orderId), {
      status: 'paid',
      paymentId,
      verifiedAt: now,
    });

    await batch.commit();

    console.log('[verifyRazorpayPayment] Subscription activated:', subRef.id, uid, plan);

    return { success: true, subscriptionId: subRef.id };
  } catch (err) {
    console.error('[verifyRazorpayPayment] Firestore batch error:', err);
    throw new functions.https.HttpsError(
      'internal',
      'Payment verified but subscription activation failed. Contact support with your payment ID: ' + paymentId
    );
  }
});

// ---------------------------------------------------------------------------
// expireSubscriptions — Scheduled (daily)
// ---------------------------------------------------------------------------

/**
 * Daily sweep that downgrades expired subscriptions.
 *
 * Finds subscriptions with status 'active' or 'trial' whose expiryDate has
 * passed, marks each 'expired', and resets the owning user's plan to 'free'.
 * Without this, a single payment would grant the plan indefinitely — the
 * client derives isPro from users/{uid}.plan and nothing else flips it.
 *
 * Requires composite index: subscriptions (status ASC, expiryDate ASC).
 */
exports.expireSubscriptions = functions.pubsub
  .schedule('every 24 hours')
  .timeZone('Asia/Kolkata')
  .onRun(async () => {
    const db = admin.firestore();
    const now = admin.firestore.Timestamp.now();

    const snap = await db
      .collection('subscriptions')
      .where('status', 'in', ['active', 'trial'])
      .where('expiryDate', '<=', now)
      .get();

    if (snap.empty) {
      console.log('[expireSubscriptions] No expired subscriptions.');
      return null;
    }

    // Batches cap at 500 ops; each expiry uses 2 (subscription + user).
    let batch = db.batch();
    let ops = 0;
    const commits = [];

    for (const doc of snap.docs) {
      const { uid } = doc.data();

      batch.update(doc.ref, {
        status: 'expired',
        updatedAt: admin.firestore.FieldValue.serverTimestamp(),
      });
      batch.update(db.collection('users').doc(uid), {
        plan: 'free',
        subscriptionId: null,
        updatedAt: admin.firestore.FieldValue.serverTimestamp(),
      });

      ops += 2;
      if (ops >= 450) {
        commits.push(batch.commit());
        batch = db.batch();
        ops = 0;
      }
    }
    if (ops > 0) commits.push(batch.commit());
    await Promise.all(commits);

    console.log('[expireSubscriptions] Expired', snap.size, 'subscriptions.');
    return null;
  });

// ---------------------------------------------------------------------------
// razorpayWebhook — HTTPS Request
// ---------------------------------------------------------------------------

/**
 * Handles incoming Razorpay webhook events.
 *
 * Configure the webhook URL in the Razorpay dashboard:
 *   https://dashboard.razorpay.com/app/webhooks
 *   URL: https://<region>-royal-fitness-club-7adc1.cloudfunctions.net/razorpayWebhook
 *
 * Set the webhook secret:
 *   firebase functions:config:set razorpay.webhook_secret="XXXXXXXX"
 *
 * Handled events:
 *   payment.captured       — activates/confirms the user's plan
 *   payment.failed         — marks the order as failed
 *   subscription.cancelled — downgrades user plan to free, marks sub cancelled
 */
exports.razorpayWebhook = functions.https.onRequest((req, res) => {
  cors(req, res, async () => {
    // Only accept POST requests
    if (req.method !== 'POST') {
      return res.status(405).send('Method Not Allowed');
    }

    // ---------------------------------------------------------------------------
    // Webhook signature verification
    // ---------------------------------------------------------------------------
    const webhookSecret = functions.config().razorpay?.webhook_secret || '';
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
    const subscriptionEntity = req.body.payload?.subscription?.entity;
    const payload = paymentEntity || subscriptionEntity;

    console.log('[razorpayWebhook] Received event:', event);

    const db = admin.firestore();

    try {
      // -----------------------------------------------------------------------
      // payment.captured — payment successfully captured by Razorpay
      // -----------------------------------------------------------------------
      if (event === 'payment.captured') {
        const orderId = paymentEntity?.order_id;

        if (!orderId) {
          console.warn('[razorpayWebhook] payment.captured: missing order_id in payload');
          return res.json({ received: true });
        }

        const orderDoc = await db.collection('payment_orders').doc(orderId).get();

        if (orderDoc.exists) {
          const { uid, plan, status } = orderDoc.data();
          const webhookAt = admin.firestore.FieldValue.serverTimestamp();

          // Idempotency: verifyRazorpayPayment already activated this order
          // ('paid'), or a previous webhook delivery handled it ('captured').
          // Record the delivery but do not re-apply the plan or regress status.
          if (status === 'paid' || status === 'captured') {
            await db.collection('payment_orders').doc(orderId).update({ webhookAt });
            console.log('[razorpayWebhook] payment.captured: order already processed, skipping:', orderId);
            return res.json({ received: true });
          }

          // Recalculate expiry from capture time
          const expiryDate = new Date();
          expiryDate.setDate(expiryDate.getDate() + 30);
          const expiryTimestamp = admin.firestore.Timestamp.fromDate(expiryDate);

          // Update user plan
          await db.collection('users').doc(uid).update({
            plan,
            updatedAt: webhookAt,
            expiryDate: expiryTimestamp,
          });

          // Mark order as captured
          await db.collection('payment_orders').doc(orderId).update({
            status: 'captured',
            webhookAt,
          });

          console.log('[razorpayWebhook] payment.captured: user plan updated:', uid, plan);
        } else {
          console.warn('[razorpayWebhook] payment.captured: order not found in Firestore:', orderId);
        }
      }

      // -----------------------------------------------------------------------
      // payment.failed — payment was declined or errored
      // -----------------------------------------------------------------------
      else if (event === 'payment.failed') {
        const orderId = paymentEntity?.order_id;

        if (orderId) {
          await db.collection('payment_orders').doc(orderId).update({
            status: 'failed',
            failureReason: paymentEntity?.error_description || 'Unknown error',
            webhookAt: admin.firestore.FieldValue.serverTimestamp(),
          });
          console.log('[razorpayWebhook] payment.failed: order marked failed:', orderId);
        } else {
          console.warn('[razorpayWebhook] payment.failed: missing order_id in payload');
        }
      }

      // -----------------------------------------------------------------------
      // subscription.cancelled — Razorpay subscription cancelled
      // -----------------------------------------------------------------------
      else if (event === 'subscription.cancelled') {
        const subEntity = payload?.subscription?.entity || payload;
        const razorSubId = subEntity?.id;
        if (!razorSubId) {
          console.warn('[razorpayWebhook] subscription.cancelled: missing subscription id');
        } else {
          // Find the matching Firestore subscription doc by Razorpay subscription id
          const subSnap = await db.collection('subscriptions')
            .where('razorpaySubscriptionId', '==', razorSubId)
            .limit(1).get();

          if (!subSnap.empty) {
            const subDoc = subSnap.docs[0];
            const uid = subDoc.data().uid;
            const batch = db.batch();

            batch.update(subDoc.ref, {
              status: 'cancelled',
              cancelledAt: admin.firestore.FieldValue.serverTimestamp(),
              webhookAt: admin.firestore.FieldValue.serverTimestamp(),
            });

            if (uid) {
              batch.update(db.collection('users').doc(uid), {
                plan: 'free',
                updatedAt: admin.firestore.FieldValue.serverTimestamp(),
              });
            }

            await batch.commit();
            console.log('[razorpayWebhook] subscription.cancelled: downgraded uid', uid, 'sub', razorSubId);
          } else {
            console.warn('[razorpayWebhook] subscription.cancelled: no Firestore doc for sub', razorSubId);
          }
        }
      }

      // -----------------------------------------------------------------------
      // Unhandled event — log and acknowledge
      // -----------------------------------------------------------------------
      else {
        console.log('[razorpayWebhook] Unhandled event type:', event);
      }

      return res.json({ received: true });
    } catch (err) {
      console.error('[razorpayWebhook] Handler error for event', event, ':', err);
      return res.json({ received: true, error: err.message });
    }
  });
});

// ---------------------------------------------------------------------------
// createMember — Admin-only Callable
// ---------------------------------------------------------------------------

/**
 * Creates a Firebase Auth user + Firestore member document.
 * Called from the admin dashboard when enrolling a new gym member.
 *
 * Input:  { name, email, password, phone?, membershipExpiry (ISO string) }
 * Output: { uid }
 *
 * Only callable by admin users (verified via Firestore role check).
 */
// ---------------------------------------------------------------------------
// PDF product catalog — shared by createPDFOrder + recordPDFPurchase
// ---------------------------------------------------------------------------
const PDF_CATALOG = {
  anabolic_full_guide:  { amount: 29900, name: 'Anabolic Full Guide' },
  fitness_mindset:      { amount: 29900, name: 'Fitness & Mindset Guidance' },
};

// ---------------------------------------------------------------------------
// createPDFOrder — HTTPS Callable
// ---------------------------------------------------------------------------

/**
 * Creates a server-side Razorpay order for any PDF product.
 * Input:  { itemId }  — must be a key in PDF_CATALOG (defaults to anabolic_full_guide)
 * Output: { orderId, keyId, amount, currency }
 */
exports.createPDFOrder = functions.https.onCall(async (data, context) => {
  if (!context.auth) {
    throw new functions.https.HttpsError('unauthenticated', 'You must be logged in.');
  }

  const uid = context.auth.uid;
  const itemId = data.itemId || 'anabolic_full_guide';

  if (!PDF_CATALOG[itemId]) {
    throw new functions.https.HttpsError('invalid-argument', `Unknown product: ${itemId}`);
  }
  const { amount } = PDF_CATALOG[itemId];

  // Idempotency — already purchased
  const existing = await admin.firestore()
    .collection('pdf_purchases').doc(uid)
    .collection('items').doc(itemId).get();
  if (existing.exists) {
    throw new functions.https.HttpsError('already-exists', 'You have already purchased this guide.');
  }

  let order;
  try {
    order = await razorpay.orders.create({
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
    uid,
    itemId,
    type: 'pdf_purchase',
    amount,
    currency: 'INR',
    status: 'pending',
    razorpayOrderId: order.id,
    createdAt: admin.firestore.FieldValue.serverTimestamp(),
  });

  console.log('[createPDFOrder] Order created:', order.id, uid, itemId);
  return {
    orderId: order.id,
    keyId: functions.config().razorpay?.key_id || 'rzp_test_PLACEHOLDER',
    amount,
    currency: 'INR',
  };
});

// ---------------------------------------------------------------------------
// recordPDFPurchase — HTTPS Callable
// ---------------------------------------------------------------------------

/**
 * Verifies the Razorpay payment signature for any PDF product and, on success:
 *   1. Writes pdf_purchases/{uid}/items/{itemId}
 *   2. Marks payment_orders/{orderId} as paid
 *
 * Input:  { orderId, paymentId, signature, itemId }
 * Output: { success: true }
 */
exports.recordPDFPurchase = functions.https.onCall(async (data, context) => {
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

  const keySecret = functions.config().razorpay?.key_secret || 'test_secret_PLACEHOLDER';
  const expectedSig = crypto
    .createHmac('sha256', keySecret)
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
    status: 'paid',
    paymentId,
    verifiedAt: now,
  });

  await batch.commit();

  console.log('[recordPDFPurchase] PDF purchased and recorded:', uid, itemId, paymentId);
  return { success: true };
});

// ---------------------------------------------------------------------------
// createMember — Admin-only Callable
// ---------------------------------------------------------------------------

exports.createMember = functions.https.onCall(async (data, context) => {
  // Verify caller is authenticated
  if (!context.auth) {
    throw new functions.https.HttpsError('unauthenticated', 'Must be logged in.');
  }

  // Verify caller is an admin
  const callerDoc = await admin.firestore().collection('users').doc(context.auth.uid).get();
  if (!callerDoc.exists || callerDoc.data().role !== 'admin') {
    throw new functions.https.HttpsError('permission-denied', 'Admin role required.');
  }

  const { name, email, password, phone, membershipExpiry } = data;

  if (!name || !email || !password) {
    throw new functions.https.HttpsError('invalid-argument', 'name, email and password are required.');
  }
  if (password.length < 6) {
    throw new functions.https.HttpsError('invalid-argument', 'Password must be at least 6 characters.');
  }
  if (!membershipExpiry) {
    throw new functions.https.HttpsError('invalid-argument', 'membershipExpiry is required.');
  }

  // Create Firebase Auth user
  const userRecord = await admin.auth().createUser({
    email,
    password,
    displayName: name,
  });

  const uid = userRecord.uid;
  const expiryDate = new Date(membershipExpiry);

  // Create Firestore member document
  await admin.firestore().collection('users').doc(uid).set({
    uid,
    name,
    email,
    phone: phone || '',
    role: 'member',
    plan: 'free',
    status: 'active',
    membershipExpiry: admin.firestore.Timestamp.fromDate(expiryDate),
    createdAt: admin.firestore.FieldValue.serverTimestamp(),
    updatedAt: admin.firestore.FieldValue.serverTimestamp(),
    lastLogin: admin.firestore.FieldValue.serverTimestamp(),
  });

  console.log('[createMember] Created member:', uid, email, 'expires:', expiryDate.toISOString());
  return { uid };
});
