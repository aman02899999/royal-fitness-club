/**
 * subscriptionService.js — Subscription Management Service
 * Royal Fitness Club SaaS Platform
 *
 * Uses Firebase v10 compat SDK (loaded via CDN script tags).
 * Exposes window.SubscriptionService with all subscription-related operations.
 *
 * Depends on: firebase/app, firebase/auth, firebase/firestore (compat CDN)
 *
 * Load order in index.html:
 *   1. firebase-app-compat.js
 *   2. firebase-auth-compat.js
 *   3. firebase-firestore-compat.js
 *   4. <firebase init script that calls firebase.initializeApp(config)>
 *   5. auth.js
 *   6. userService.js
 *   7. subscriptionService.js  ← this file
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
   * Preferred over client-side Date objects for consistency across time zones.
   * @returns {firebase.firestore.FieldValue}
   */
  function serverTimestamp() {
    return firebase.firestore.FieldValue.serverTimestamp();
  }

  /**
   * Returns a Firestore Timestamp that is `days` calendar days from now.
   * Used for trialEnd / expiryDate fields where an absolute future date is needed
   * at write-time (serverTimestamp cannot be used for computed future dates).
   * @param {number} days
   * @returns {firebase.firestore.Timestamp}
   */
  function timestampDaysFromNow(days) {
    const d = new Date();
    d.setDate(d.getDate() + days);
    return firebase.firestore.Timestamp.fromDate(d);
  }

  /**
   * Converts a Firestore QuerySnapshot to a plain array of objects,
   * injecting the document ID as `id` on each item.
   * @param {firebase.firestore.QuerySnapshot} snap
   * @returns {Object[]}
   */
  function snapToArray(snap) {
    return snap.docs.map((doc) => ({ id: doc.id, ...doc.data() }));
  }

  // ---------------------------------------------------------------------------
  // Public API
  // ---------------------------------------------------------------------------

  window.SubscriptionService = {

    /**
     * Plan catalogue.
     *
     * Consumers may read this map directly to build pricing/feature UI without
     * duplicating plan details. The `currency` field is present on all plans
     * for consistency (free plan returns 0 with INR denomination).
     */
    PLANS: {
      free: {
        name: 'Free',
        price: 0,
        currency: 'INR',
        features: ['calculator', 'meal_plan_basic'],
      },
      royal_pro: {
        name: 'Royal Pro',
        price: 499,
        currency: 'INR',
        features: [
          'all_free',
          'meal_plan_full',
          'tracker',
          'pdf_export',
          'progress_photos',
        ],
      },
      royal_elite: {
        name: 'Royal Elite',
        price: 1999,
        currency: 'INR',
        features: [
          'all_pro',
          'coaching',
          'custom_plan',
          'priority_support',
        ],
      },
    },

    /**
     * Creates a new subscription document in `subscriptions/{subId}` and
     * updates the user's `plan` field in `users/{uid}`.
     *
     * New subscriptions always start with `status: 'trial'`.
     * Trial window  : 7 days from creation.
     * Billing period: 30 days from creation.
     *
     * Uses a Firestore batch write so both documents succeed or fail together.
     *
     * @param {string} uid                          - Firebase Auth UID
     * @param {string} plan                         - 'royal_pro' | 'royal_elite'
     * @param {{method?: string, orderId?: string, paymentId?: string}} [paymentData={}]
     * @returns {Promise<{subId: string, subscription: Object}>}
     */
    async createSubscription(uid, plan, paymentData = {}) {
      try {
        const planDetails = window.SubscriptionService.PLANS[plan];
        if (!planDetails) throw new Error(`[SubscriptionService] Unknown plan: ${plan}`);

        const subRef = db().collection('subscriptions').doc();
        const subId = subRef.id;

        const subscription = {
          uid,
          plan,
          planName: planDetails.name,
          status: 'trial',
          amount: planDetails.price,
          currency: planDetails.currency || 'INR',
          startDate: serverTimestamp(),
          trialEnd: timestampDaysFromNow(7),
          expiryDate: timestampDaysFromNow(30),
          paymentMethod: paymentData.method || 'card',
          razorpayOrderId: paymentData.orderId || null,
          razorpayPaymentId: paymentData.paymentId || null,
          createdAt: serverTimestamp(),
          updatedAt: serverTimestamp(),
        };

        const batch = db().batch();

        // Write the new subscription document
        batch.set(subRef, subscription);

        // Sync plan onto the user document
        batch.update(db().collection('users').doc(uid), {
          plan,
          subscriptionId: subId,
          expiryDate: timestampDaysFromNow(30),
          updatedAt: serverTimestamp(),
        });

        await batch.commit();

        console.log('[SubscriptionService] createSubscription:', uid, plan, subId);
        return { subId, subscription };
      } catch (err) {
        console.error('[SubscriptionService] createSubscription error:', err);
        throw err;
      }
    },

    /**
     * Retrieves the user's current active or trial subscription.
     * Returns the most recently created matching document, or null if none exists.
     *
     * @param {string} uid
     * @returns {Promise<Object|null>}
     */
    async getSubscription(uid) {
      try {
        const snap = await db()
          .collection('subscriptions')
          .where('uid', '==', uid)
          .where('status', 'in', ['active', 'trial'])
          .orderBy('createdAt', 'desc')
          .limit(1)
          .get();

        if (snap.empty) return null;
        const doc = snap.docs[0];
        return { id: doc.id, ...doc.data() };
      } catch (err) {
        console.error('[SubscriptionService] getSubscription error:', err);
        return null;
      }
    },

    /**
     * Cancels the user's active/trial subscription and downgrades their plan
     * to 'free'. Both writes are batched for atomicity.
     *
     * @param {string} uid
     * @returns {Promise<void>}
     */
    async cancelSubscription(uid) {
      try {
        const sub = await window.SubscriptionService.getSubscription(uid);
        if (!sub) {
          console.warn('[SubscriptionService] cancelSubscription: no active subscription for', uid);
          return;
        }

        const batch = db().batch();

        batch.update(db().collection('subscriptions').doc(sub.id), {
          status: 'cancelled',
          cancelledAt: serverTimestamp(),
          updatedAt: serverTimestamp(),
        });

        batch.update(db().collection('users').doc(uid), {
          plan: 'free',
          subscriptionId: null,
          updatedAt: serverTimestamp(),
        });

        await batch.commit();

        console.log('[SubscriptionService] cancelSubscription:', uid, sub.id);
      } catch (err) {
        console.error('[SubscriptionService] cancelSubscription error:', err);
        throw err;
      }
    },

    /**
     * Returns a detailed status object for the user's current plan.
     *
     * Reads both the `users/{uid}` document (for the plan field) and the
     * subscriptions collection (for expiry/days-left), then derives `isPro`,
     * `isElite`, and `isActive` from their combination.
     *
     * @param {string} uid
     * @returns {Promise<{plan: string, isPro: boolean, isElite: boolean, isActive: boolean, expiryDate: Date|null, daysLeft: number, subscription: Object|null}>}
     */
    async checkPlanStatus(uid) {
      const DEFAULT = {
        plan: 'free',
        isPro: false,
        isElite: false,
        isActive: false,
        expiryDate: null,
        daysLeft: 0,
        subscription: null,
      };

      try {
        const [userSnap, sub] = await Promise.all([
          db().collection('users').doc(uid).get(),
          window.SubscriptionService.getSubscription(uid),
        ]);

        if (!userSnap.exists) return DEFAULT;

        const plan = (userSnap.data().plan) || 'free';

        let expiryDate = null;
        let daysLeft = 0;

        if (sub && sub.expiryDate) {
          expiryDate = sub.expiryDate.toDate
            ? sub.expiryDate.toDate()
            : new Date(sub.expiryDate);
          daysLeft = Math.max(
            0,
            Math.ceil((expiryDate - Date.now()) / (1000 * 60 * 60 * 24))
          );
        }

        const isActive = !!sub &&
          ['active', 'trial'].includes(sub.status) &&
          daysLeft > 0;

        return {
          plan,
          isPro: isActive && ['royal_pro', 'royal_elite'].includes(plan),
          isElite: isActive && plan === 'royal_elite',
          isActive,
          expiryDate,
          daysLeft,
          subscription: sub,
        };
      } catch (err) {
        console.error('[SubscriptionService] checkPlanStatus error:', err);
        return DEFAULT;
      }
    },

    /**
     * Returns all subscription documents for a user ordered by `createdAt`
     * descending. Useful for billing history and support audit trails.
     *
     * @param {string} uid
     * @returns {Promise<Object[]>}
     */
    async getSubscriptionHistory(uid) {
      try {
        const snap = await db()
          .collection('subscriptions')
          .where('uid', '==', uid)
          .orderBy('createdAt', 'desc')
          .get();

        return snapToArray(snap);
      } catch (err) {
        console.error('[SubscriptionService] getSubscriptionHistory error:', err);
        return [];
      }
    },

    /**
     * Convenience shorthand: activates a 7-day free trial for the given user.
     * Delegates entirely to createSubscription (which always sets status:'trial').
     *
     * @param {string} uid
     * @param {string} [plan='royal_pro'] - Plan to trial; defaults to royal_pro
     * @returns {Promise<{subId: string, subscription: Object}>}
     */
    async activateTrialForUser(uid, plan = 'royal_pro') {
      try {
        return await window.SubscriptionService.createSubscription(uid, plan, {
          method: 'trial',
        });
      } catch (err) {
        console.error('[SubscriptionService] activateTrialForUser error:', err);
        throw err;
      }
    },

    /**
     * Returns true if the user currently has an active or trial subscription
     * on the `royal_pro` or `royal_elite` plan, false otherwise.
     *
     * @param {string} uid
     * @returns {Promise<boolean>}
     */
    async isProUser(uid) {
      try {
        const status = await window.SubscriptionService.checkPlanStatus(uid);
        return status.isPro;
      } catch (err) {
        console.error('[SubscriptionService] isProUser error:', err);
        return false;
      }
    },

    // -------------------------------------------------------------------------
    // Admin / reporting helpers (bonus — not in core spec)
    // -------------------------------------------------------------------------

    /**
     * Admin: directly updates fields on a subscription document.
     *
     * @param {string} subId   - Subscription document ID
     * @param {Object} updates - Fields to update
     * @returns {Promise<void>}
     */
    async adminUpdateSubscription(subId, updates) {
      try {
        await db().collection('subscriptions').doc(subId).update({
          ...updates,
          updatedAt: serverTimestamp(),
        });
        console.log('[SubscriptionService] adminUpdateSubscription:', subId);
      } catch (err) {
        console.error('[SubscriptionService] adminUpdateSubscription error:', err);
        throw err;
      }
    },

    /**
     * Admin: returns all subscriptions, optionally filtered by status.
     *
     * @param {string|null} [statusFilter=null] - e.g. 'active', 'trial', 'cancelled'
     * @param {number}      [limitN=100]        - Maximum results to return
     * @returns {Promise<Object[]>}
     */
    async getAllSubscriptions(statusFilter = null, limitN = 100) {
      try {
        let query = db()
          .collection('subscriptions')
          .orderBy('createdAt', 'desc')
          .limit(limitN);

        if (statusFilter) {
          query = query.where('status', '==', statusFilter);
        }

        const snap = await query.get();
        return snapToArray(snap);
      } catch (err) {
        console.error('[SubscriptionService] getAllSubscriptions error:', err);
        return [];
      }
    },

    /**
     * Admin: returns the sum of all `amount` fields across active and completed
     * subscriptions. For a production revenue dashboard, consider a Cloud Function
     * with aggregated counters to avoid full-collection reads.
     *
     * @returns {Promise<number>} Total revenue in INR (paise-free integer)
     */
    async getTotalRevenue() {
      try {
        const snap = await db()
          .collection('subscriptions')
          .where('status', 'in', ['active', 'completed'])
          .get();

        return snap.docs.reduce((sum, doc) => sum + (doc.data().amount || 0), 0);
      } catch (err) {
        console.error('[SubscriptionService] getTotalRevenue error:', err);
        return 0;
      }
    },
  };

  console.log('[SubscriptionService] loaded');
})();
