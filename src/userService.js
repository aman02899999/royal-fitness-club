/**
 * userService.js — Firestore User CRUD & Progress Service
 * Royal Fitness Club SaaS Platform
 *
 * Uses Firebase v10 compat SDK (loaded via CDN script tags).
 * Exposes window.UserService with all user-data operations.
 *
 * Depends on: firebase/firestore (compat CDN)
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

  /** @returns {firebase.firestore.FieldValue} */
  function serverTimestamp() {
    return firebase.firestore.FieldValue.serverTimestamp();
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

  window.UserService = {

    /**
     * Creates or merges a Firestore user document at `users/{uid}`.
     *
     * @param {string} uid
     * @param {Object} data - Fields to store
     * @returns {Promise<void>}
     */
    async createUser(uid, data) {
      try {
        await db().collection('users').doc(uid).set(data, { merge: true });
        console.log('[UserService] createUser:', uid);
      } catch (err) {
        console.error('[UserService] createUser error:', err);
        throw err;
      }
    },

    /**
     * Retrieves a user document from `users/{uid}`.
     *
     * @param {string} uid
     * @returns {Promise<Object|null>} User data or null if not found
     */
    async getUser(uid) {
      try {
        const snap = await db().collection('users').doc(uid).get();
        return snap.exists ? { id: snap.id, ...snap.data() } : null;
      } catch (err) {
        console.error('[UserService] getUser error:', err);
        return null;
      }
    },

    /**
     * Updates specific fields on a user document and refreshes `updatedAt`.
     *
     * @param {string} uid
     * @param {Object} data - Fields to update
     * @returns {Promise<void>}
     */
    async updateUser(uid, data) {
      try {
        await db()
          .collection('users')
          .doc(uid)
          .update({ ...data, updatedAt: serverTimestamp() });
        console.log('[UserService] updateUser:', uid);
      } catch (err) {
        console.error('[UserService] updateUser error:', err);
        throw err;
      }
    },

    /**
     * Permanently deletes a user document (admin use only).
     * Does NOT delete the Firebase Auth account — call Admin SDK for that.
     *
     * @param {string} uid
     * @returns {Promise<void>}
     */
    async deleteUser(uid) {
      try {
        await db().collection('users').doc(uid).delete();
        console.log('[UserService] deleteUser:', uid);
      } catch (err) {
        console.error('[UserService] deleteUser error:', err);
        throw err;
      }
    },

    /**
     * Returns a paginated list of users ordered by `createdAt` descending.
     *
     * @param {number} [limitN=50]          - Page size
     * @param {firebase.firestore.DocumentSnapshot|null} [lastDoc=null] - Cursor for next page
     * @returns {Promise<{users: Object[], lastDoc: firebase.firestore.DocumentSnapshot|null, total: number}>}
     */
    async getAllUsers(limitN = 50, lastDoc = null) {
      try {
        let query = db()
          .collection('users')
          .orderBy('createdAt', 'desc')
          .limit(limitN);

        if (lastDoc) {
          query = query.startAfter(lastDoc);
        }

        const snap = await query.get();
        const users = snapToArray(snap);
        const newLastDoc = snap.docs.length > 0 ? snap.docs[snap.docs.length - 1] : null;

        // Total count (lightweight — uses a separate aggregation-style query)
        // Firestore doesn't support COUNT natively in the compat SDK without
        // aggregation queries, so we return the fetched length as `total` here.
        // Replace with AggregateQuery if needed for accurate counts.
        return {
          users,
          lastDoc: newLastDoc,
          total: users.length,
        };
      } catch (err) {
        console.error('[UserService] getAllUsers error:', err);
        return { users: [], lastDoc: null, total: 0 };
      }
    },

    /**
     * Searches users by name or email using a client-side filter.
     * Fetches up to 200 records, then filters in-memory.
     *
     * @param {string} query - Search term
     * @returns {Promise<Object[]>}
     */
    async searchUsers(query) {
      try {
        const term = (query || '').toLowerCase().trim();
        if (!term) return [];

        const snap = await db()
          .collection('users')
          .orderBy('createdAt', 'desc')
          .limit(200)
          .get();

        const all = snapToArray(snap);
        return all.filter(
          (u) =>
            (u.name && u.name.toLowerCase().includes(term)) ||
            (u.email && u.email.toLowerCase().includes(term))
        );
      } catch (err) {
        console.error('[UserService] searchUsers error:', err);
        return [];
      }
    },

    /**
     * Updates the subscription plan and status of a user.
     *
     * @param {string} uid
     * @param {string} plan   - e.g. 'free', 'royal_pro', 'royal_elite'
     * @param {string} status - e.g. 'active', 'trial', 'suspended'
     * @returns {Promise<void>}
     */
    async updateUserPlan(uid, plan, status) {
      try {
        await db()
          .collection('users')
          .doc(uid)
          .update({ plan, status, updatedAt: serverTimestamp() });
        console.log('[UserService] updateUserPlan:', uid, plan, status);
      } catch (err) {
        console.error('[UserService] updateUserPlan error:', err);
        throw err;
      }
    },

    /**
     * Suspends a user account by setting `status` to `'suspended'`.
     *
     * @param {string} uid
     * @returns {Promise<void>}
     */
    async suspendUser(uid) {
      try {
        await db()
          .collection('users')
          .doc(uid)
          .update({ status: 'suspended', updatedAt: serverTimestamp() });
        console.log('[UserService] suspendUser:', uid);
      } catch (err) {
        console.error('[UserService] suspendUser error:', err);
        throw err;
      }
    },

    /**
     * Reactivates a suspended user account.
     *
     * @param {string} uid
     * @returns {Promise<void>}
     */
    async activateUser(uid) {
      try {
        await db()
          .collection('users')
          .doc(uid)
          .update({ status: 'active', updatedAt: serverTimestamp() });
        console.log('[UserService] activateUser:', uid);
      } catch (err) {
        console.error('[UserService] activateUser error:', err);
        throw err;
      }
    },

    /**
     * Returns aggregate user statistics computed from the `users` collection.
     * Reads all documents — use sparingly (consider a Cloud Function for large datasets).
     *
     * @returns {Promise<{totalUsers: number, proUsers: number, freeUsers: number, suspended: number, newThisMonth: number}>}
     */
    async getUserStats() {
      try {
        const snap = await db().collection('users').get();
        const users = snapToArray(snap);

        const now = new Date();
        const startOfMonth = new Date(now.getFullYear(), now.getMonth(), 1);

        let proUsers = 0;
        let freeUsers = 0;
        let suspended = 0;
        let newThisMonth = 0;

        users.forEach((u) => {
          if (['royal_pro', 'royal_elite'].includes(u.plan)) {
            proUsers++;
          } else {
            freeUsers++;
          }

          if (u.status === 'suspended') suspended++;

          // createdAt may be a Firestore Timestamp or already a Date
          const created = u.createdAt
            ? u.createdAt.toDate
              ? u.createdAt.toDate()
              : new Date(u.createdAt)
            : null;

          if (created && created >= startOfMonth) newThisMonth++;
        });

        return {
          totalUsers: users.length,
          proUsers,
          freeUsers,
          suspended,
          newThisMonth,
        };
      } catch (err) {
        console.error('[UserService] getUserStats error:', err);
        return { totalUsers: 0, proUsers: 0, freeUsers: 0, suspended: 0, newThisMonth: 0 };
      }
    },

    /**
     * Saves a calculator result (BMI / BMR / TDEE / Beast Score) to
     * `progress_logs/{uid}/logs/` as a new timestamped document.
     *
     * @param {string} uid
     * @param {{bmi: number, bmr: number, tdee: number, bodyFat: number, beastScore: number, calories: number, goal: string, diet: string}} result
     * @returns {Promise<string>} New document ID
     */
    async saveCalculatorResult(uid, result) {
      try {
        const docRef = await db()
          .collection('progress_logs')
          .doc(uid)
          .collection('logs')
          .add({
            date: serverTimestamp(),
            bmi: result.bmi || null,
            bmr: result.bmr || null,
            tdee: result.tdee || null,
            bodyFat: result.bodyFat || null,
            beastScore: result.beastScore || null,
            calories: result.calories || null,
            goal: result.goal || null,
            diet: result.diet || null,
            createdAt: serverTimestamp(),
          });

        console.log('[UserService] saveCalculatorResult:', uid, docRef.id);
        return docRef.id;
      } catch (err) {
        console.error('[UserService] saveCalculatorResult error:', err);
        throw err;
      }
    },

    /**
     * Saves a body measurement entry to `measurements/{uid}/logs/`.
     *
     * @param {string} uid
     * @param {Object} measurement - e.g. { chest, waist, hips, weight, ... }
     * @returns {Promise<string>} New document ID
     */
    async saveMeasurement(uid, measurement) {
      try {
        const docRef = await db()
          .collection('measurements')
          .doc(uid)
          .collection('logs')
          .add({
            date: serverTimestamp(),
            ...measurement,
            createdAt: serverTimestamp(),
          });

        console.log('[UserService] saveMeasurement:', uid, docRef.id);
        return docRef.id;
      } catch (err) {
        console.error('[UserService] saveMeasurement error:', err);
        throw err;
      }
    },

    /**
     * Retrieves the 10 most recent measurement entries for a user.
     *
     * @param {string} uid
     * @returns {Promise<Object[]>}
     */
    async getMeasurements(uid) {
      try {
        const snap = await db()
          .collection('measurements')
          .doc(uid)
          .collection('logs')
          .orderBy('date', 'desc')
          .limit(10)
          .get();

        return snapToArray(snap);
      } catch (err) {
        console.error('[UserService] getMeasurements error:', err);
        return [];
      }
    },

    /**
     * Saves or merges activity data (streak, workouts, hydration) to `activity/{uid}`.
     *
     * @param {string} uid
     * @param {{streak: number, workouts: number, hydrationDays: number}} activityData
     * @returns {Promise<void>}
     */
    async saveActivityData(uid, activityData) {
      try {
        await db()
          .collection('activity')
          .doc(uid)
          .set(
            { ...activityData, updatedAt: serverTimestamp() },
            { merge: true }
          );
        console.log('[UserService] saveActivityData:', uid);
      } catch (err) {
        console.error('[UserService] saveActivityData error:', err);
        throw err;
      }
    },

    /**
     * Retrieves the activity document for a user from `activity/{uid}`.
     *
     * @param {string} uid
     * @returns {Promise<Object|null>}
     */
    async getActivityData(uid) {
      try {
        const snap = await db().collection('activity').doc(uid).get();
        return snap.exists ? { id: snap.id, ...snap.data() } : null;
      } catch (err) {
        console.error('[UserService] getActivityData error:', err);
        return null;
      }
    },
  };

  console.log('[UserService] loaded');
})();
