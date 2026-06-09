/**
 * functions/index.js — Firebase Cloud Functions
 * Royal Fitness Club SaaS Platform
 *
 * Backend Razorpay integration providing three endpoints:
 *
 *   createRazorpayOrder    — HTTPS Callable: creates a server-side Razorpay order
 *   verifyRazorpayPayment  — HTTPS Callable: verifies payment signature and activates subscription
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
 *   payment.captured  — activates/confirms the user's plan
 *   payment.failed    — marks the order as failed
 *   (subscription.cancelled is logged but not yet actioned)
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
          const { uid, plan } = orderDoc.data();

          // Recalculate expiry from capture time
          const expiryDate = new Date();
          expiryDate.setDate(expiryDate.getDate() + 30);
          const expiryTimestamp = admin.firestore.Timestamp.fromDate(expiryDate);

          const webhookAt = admin.firestore.FieldValue.serverTimestamp();

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
        // TODO: call window.SubscriptionService.cancelSubscription() or replicate
        // its logic here (update subscriptions/{id} status and downgrade user plan).
        console.log('[razorpayWebhook] subscription.cancelled received (not yet handled):', payload?.id);
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
      // Return 200 so Razorpay doesn't retry indefinitely on our internal errors.
      return res.json({ received: true, error: err.message });
    }
  });
});
