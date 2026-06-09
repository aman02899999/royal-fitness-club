/**
 * razorpayService.js — Razorpay Payment Integration
 * Royal Fitness Club SaaS Platform
 *
 * Client-side Razorpay checkout integration using the Firebase v10 compat SDK.
 * Exposes window.RazorpayService with the full payment flow:
 *   loadScript → createOrder → openCheckout → completePayment
 *
 * Depends on: firebase/firestore (compat CDN), window.SubscriptionService
 *
 * Load order in index.html:
 *   1. firebase-app-compat.js
 *   2. firebase-auth-compat.js
 *   3. firebase-firestore-compat.js
 *   4. <firebase init script that calls firebase.initializeApp(config)>
 *   5. subscriptionService.js
 *   6. razorpayService.js  ← this file
 *
 * The Razorpay checkout script is loaded lazily on first checkout:
 *   https://checkout.razorpay.com/v1/checkout.js
 *
 * ⚠️  IMPORTANT: Replace KEY_ID below with your real key from the Razorpay
 *     dashboard before going live. Test keys start with "rzp_test_", live
 *     keys start with "rzp_live_".
 */

(function () {
  'use strict';

  // ---------------------------------------------------------------------------
  // Helpers
  // ---------------------------------------------------------------------------

  /** @returns {firebase.firestore.Firestore} */
  function db() {
    return firebase.firestore();
  }

  /**
   * Returns a Firestore server-side timestamp via the compat SDK.
   * @returns {firebase.firestore.FieldValue}
   */
  function serverTimestamp() {
    return firebase.firestore.FieldValue.serverTimestamp();
  }

  // ---------------------------------------------------------------------------
  // Public API
  // ---------------------------------------------------------------------------

  window.RazorpayService = {

    /**
     * Razorpay API Key ID.
     *
     * ⚠️  REPLACE THIS VALUE with your actual key from:
     *     https://dashboard.razorpay.com/app/keys
     *
     * Test keys  → rzp_test_XXXXXXXXXXXXXXXX  (no real money moved)
     * Live keys  → rzp_live_XXXXXXXXXXXXXXXX  (real transactions)
     */
    KEY_ID: 'rzp_test_PLACEHOLDER',

    /**
     * Plan catalogue — prices in INR, amounts are whole rupees (not paise).
     * Paise conversion (×100) is applied when opening the Razorpay modal.
     */
    PLANS: {
      royal_pro: {
        name: 'Royal Pro',
        amount: 499,
        currency: 'INR',
        interval: 'monthly',
      },
      royal_elite: {
        name: 'Royal Elite',
        amount: 1999,
        currency: 'INR',
        interval: 'monthly',
      },
    },

    // -------------------------------------------------------------------------
    // Script loader
    // -------------------------------------------------------------------------

    /**
     * Dynamically loads the Razorpay checkout script if it has not been loaded
     * yet. Safe to call multiple times — resolves immediately on subsequent
     * calls once the script is present in the DOM.
     *
     * @returns {Promise<boolean>} Resolves true on successful load, false on error.
     */
    async loadScript() {
      return new Promise((resolve) => {
        // Already loaded — nothing to do.
        if (window.Razorpay) {
          resolve(true);
          return;
        }

        const existingScript = document.querySelector(
          'script[src="https://checkout.razorpay.com/v1/checkout.js"]'
        );
        if (existingScript) {
          // Script tag exists but Razorpay global may still be initialising;
          // wait for its load event.
          existingScript.addEventListener('load', () => resolve(true));
          existingScript.addEventListener('error', () => resolve(false));
          return;
        }

        const script = document.createElement('script');
        script.src = 'https://checkout.razorpay.com/v1/checkout.js';
        script.async = true;

        script.onload = () => {
          console.log('[RazorpayService] Checkout script loaded');
          resolve(true);
        };

        script.onerror = () => {
          console.error('[RazorpayService] Failed to load checkout script');
          resolve(false);
        };

        document.head.appendChild(script);
      });
    },

    // -------------------------------------------------------------------------
    // Order creation
    // -------------------------------------------------------------------------

    /**
     * Creates a pending payment record in Firestore under
     * `pending_payments/{orderId}` and returns the order details.
     *
     * NOTE: This implementation generates a client-side order ID because there
     * is no backend yet. Once the Firebase Cloud Function `createRazorpayOrder`
     * is deployed (see functions/index.js), replace this method body with a
     * call to that function so Razorpay generates a real server-side order ID:
     *
     *   const fn = firebase.functions().httpsCallable('createRazorpayOrder');
     *   const { data } = await fn({ plan, uid });
     *   return data;
     *
     * @param {string} plan - 'royal_pro' | 'royal_elite'
     * @param {string} uid  - Firebase Auth UID of the purchasing user
     * @returns {Promise<{orderId: string, amount: number, currency: string}>}
     */
    async createOrder(plan, uid) {
      try {
        const planDetails = window.RazorpayService.PLANS[plan];
        if (!planDetails) {
          throw new Error(`[RazorpayService] Unknown plan: ${plan}`);
        }

        // Client-side order ID — replace with server-generated ID when backend
        // Cloud Function is live.
        const orderId = `rfc_local_${uid}_${Date.now()}`;

        await db().collection('pending_payments').doc(orderId).set({
          orderId,
          uid,
          plan,
          amount: planDetails.amount,
          currency: planDetails.currency,
          status: 'pending',
          createdAt: serverTimestamp(),
        });

        console.log('[RazorpayService] createOrder:', orderId, plan);
        return {
          orderId,
          amount: planDetails.amount,
          currency: planDetails.currency,
        };
      } catch (err) {
        console.error('[RazorpayService] createOrder error:', err);
        throw err;
      }
    },

    // -------------------------------------------------------------------------
    // Checkout flow
    // -------------------------------------------------------------------------

    /**
     * Runs the full Razorpay checkout flow:
     *   1. Loads the Razorpay checkout script.
     *   2. Creates a pending order in Firestore.
     *   3. Opens the Razorpay payment modal pre-filled with user details.
     *   4. On successful payment, calls completePayment() to activate the
     *      subscription and update Firestore records.
     *
     * @param {string} plan                             - 'royal_pro' | 'royal_elite'
     * @param {string} uid                              - Firebase Auth UID
     * @param {{ name: string, email: string, phone: string }} userData - User contact details for prefill
     * @returns {Promise<Object>} Resolves with payment + subscription data on
     *   success; rejects if the user dismisses the modal or payment fails.
     */
    async openCheckout(plan, uid, userData) {
      try {
        const planDetails = window.RazorpayService.PLANS[plan];
        if (!planDetails) {
          throw new Error(`[RazorpayService] Unknown plan: ${plan}`);
        }

        // Step 1: ensure the Razorpay checkout script is available.
        const scriptLoaded = await window.RazorpayService.loadScript();
        if (!scriptLoaded) {
          throw new Error('[RazorpayService] Could not load Razorpay checkout script. Check your internet connection.');
        }

        // Step 2: create the order record.
        const { orderId, amount, currency } = await window.RazorpayService.createOrder(plan, uid);

        // Step 3: open the modal and wait for the user's action.
        return new Promise((resolve, reject) => {
          const options = {
            // ⚠️  KEY_ID must be set to your real Razorpay key — see top of file.
            key: window.RazorpayService.KEY_ID,

            // Razorpay expects paise (rupees × 100).
            amount: amount * 100,

            currency,

            name: 'Royal Fitness Club',
            description: `${planDetails.name} Subscription`,

            // No hosted logo URL configured — set to an empty string.
            image: '',

            // order_id should be the Razorpay server-side order ID.
            // Until the Cloud Function is live this is the local orderId.
            order_id: orderId,

            prefill: {
              name: userData.name || '',
              email: userData.email || '',
              contact: userData.phone || '',
            },

            theme: {
              color: '#e8001d',
            },

            modal: {
              ondismiss: () => {
                console.log('[RazorpayService] Checkout modal dismissed by user');
                reject(new Error('Payment cancelled by user'));
              },
            },

            /**
             * Called by Razorpay after a successful payment authorisation.
             * The response object contains:
             *   - razorpay_payment_id  : unique payment ID
             *   - razorpay_order_id    : the order ID passed above
             *   - razorpay_signature   : HMAC-SHA256 signature for server-side verification
             *
             * @param {{ razorpay_payment_id: string, razorpay_order_id: string, razorpay_signature: string }} response
             */
            handler: async (response) => {
              try {
                console.log('[RazorpayService] Payment authorised:', response.razorpay_payment_id);
                const result = await window.RazorpayService.completePayment(plan, uid, response);
                resolve(result);
              } catch (handlerErr) {
                console.error('[RazorpayService] completePayment error in handler:', handlerErr);
                reject(handlerErr);
              }
            },
          };

          const rzp = new window.Razorpay(options);
          rzp.open();
        });
      } catch (err) {
        console.error('[RazorpayService] openCheckout error:', err);
        throw err;
      }
    },

    // -------------------------------------------------------------------------
    // Post-payment processing
    // -------------------------------------------------------------------------

    /**
     * Called after Razorpay confirms a successful payment authorisation.
     * Performs three writes in sequence:
     *   1. Marks the pending_payments record as 'completed'.
     *   2. Creates a subscription via window.SubscriptionService.createSubscription().
     *   3. Updates the users/{uid} plan field.
     *
     * For production use, consider moving signature verification (step 0) into
     * the `verifyRazorpayPayment` Cloud Function before committing to Firestore.
     *
     * @param {string} plan                    - 'royal_pro' | 'royal_elite'
     * @param {string} uid                     - Firebase Auth UID
     * @param {{ razorpay_payment_id: string, razorpay_order_id: string, razorpay_signature: string }} paymentResponse
     *   Raw response object from the Razorpay handler callback.
     * @returns {Promise<{ subId: string, subscription: Object, paymentId: string }>}
     */
    async completePayment(plan, uid, paymentResponse) {
      try {
        const { razorpay_payment_id, razorpay_order_id, razorpay_signature } = paymentResponse;

        // 1. Update the pending_payments record.
        await db().collection('pending_payments').doc(razorpay_order_id).update({
          status: 'completed',
          paymentId: razorpay_payment_id,
          signature: razorpay_signature,
          completedAt: serverTimestamp(),
        });

        // 2. Create the subscription document (also syncs plan onto users/{uid}).
        const { subId, subscription } = await window.SubscriptionService.createSubscription(
          uid,
          plan,
          {
            method: 'razorpay',
            orderId: razorpay_order_id,
            paymentId: razorpay_payment_id,
          }
        );

        // 3. The users/{uid}.plan field is already written by createSubscription,
        //    but we also update the raw payment reference here for auditability.
        await db().collection('users').doc(uid).update({
          plan,
          lastPaymentId: razorpay_payment_id,
          updatedAt: serverTimestamp(),
        });

        console.log('[RazorpayService] completePayment: subscription activated', subId);
        return { subId, subscription, paymentId: razorpay_payment_id };
      } catch (err) {
        console.error('[RazorpayService] completePayment error:', err);
        throw err;
      }
    },

    // -------------------------------------------------------------------------
    // Signature verification
    // -------------------------------------------------------------------------

    /**
     * Stub for client-side payment signature verification.
     *
     * Real HMAC-SHA256 signature verification MUST be done server-side
     * (requires the Razorpay key_secret which must never be exposed to the
     * browser). This stub logs the IDs and returns true so the client-side
     * flow is unblocked during development.
     *
     * TODO: Replace with a call to the `verifyRazorpayPayment` Cloud Function
     * once it is deployed:
     *
     *   const fn = firebase.functions().httpsCallable('verifyRazorpayPayment');
     *   const { data } = await fn({ orderId, paymentId, signature, plan });
     *   return data.success;
     *
     * @param {string} paymentId  - razorpay_payment_id from the handler response
     * @param {string} orderId    - razorpay_order_id from the handler response
     * @param {string} signature  - razorpay_signature from the handler response
     * @returns {Promise<boolean>} Always resolves true in this stub implementation.
     */
    async verifyPayment(paymentId, orderId, signature) {
      try {
        // TODO: implement via Firebase Function — see functions/index.js
        console.log('[RazorpayService] verifyPayment (stub):', { paymentId, orderId, signature });
        return true;
      } catch (err) {
        console.error('[RazorpayService] verifyPayment error:', err);
        return false;
      }
    },
  };

  console.log('[RazorpayService] loaded');
})();
