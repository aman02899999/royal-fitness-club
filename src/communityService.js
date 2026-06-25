/**
 * communityService.js — Community Leaderboard Service
 * Royal Fitness Club SaaS Platform
 *
 * Uses Firebase v10 compat SDK (loaded via CDN script tags).
 * Exposes window.CommunityService with leaderboard operations.
 *
 * Collection layout:
 *   leaderboard/{uid} — one flat doc per member, written by the member
 *     { name, beastScore, streak, plan, updatedAt }
 *
 * Privacy: only the display name (first name + last initial) is published,
 * never email/phone. Members write their own entry; all authenticated
 * members may read the board (enforced in firestore.rules).
 *
 * Load order in index.html: after firebase init, alongside other services.
 */

(function () {
  'use strict';

  /** @returns {firebase.firestore.Firestore} */
  function db() {
    return firebase.firestore();
  }

  /** @returns {firebase.firestore.FieldValue} */
  function serverTimestamp() {
    return firebase.firestore.FieldValue.serverTimestamp();
  }

  /**
   * Reduces a full name to a privacy-safe display name:
   * "Aman Sharma" → "Aman S."  /  "Priya" → "Priya"
   * @param {string} fullName
   * @returns {string}
   */
  function displayName(fullName) {
    const parts = (fullName || 'Beast').trim().split(/\s+/);
    if (parts.length === 1) return parts[0];
    return parts[0] + ' ' + parts[parts.length - 1][0].toUpperCase() + '.';
  }

  window.CommunityService = {

    /**
     * Creates or updates the member's leaderboard entry.
     * Only the provided numeric fields are merged, so a streak update never
     * clobbers an existing beastScore and vice versa.
     *
     * @param {string} uid
     * @param {{name?: string, beastScore?: number, streak?: number, plan?: string}} data
     * @returns {Promise<void>}
     */
    async updateEntry(uid, data) {
      try {
        if (!uid) return;

        const entry = { updatedAt: serverTimestamp() };
        if (data.name !== undefined) entry.name = displayName(data.name);
        if (typeof data.beastScore === 'number') entry.beastScore = data.beastScore;
        if (typeof data.streak === 'number') entry.streak = data.streak;
        if (data.plan !== undefined) entry.plan = data.plan;

        await db().collection('leaderboard').doc(uid).set(entry, { merge: true });
        console.log('[CommunityService] updateEntry:', uid);
      } catch (err) {
        // Leaderboard writes must never break the calling feature
        console.error('[CommunityService] updateEntry error:', err);
      }
    },

    /**
     * Fetches the top leaderboard entries ordered by the given field.
     *
     * @param {string} [orderField='beastScore'] - 'beastScore' | 'streak'
     * @param {number} [limitN=50]
     * @returns {Promise<Object[]>} Array of { uid, name, beastScore, streak, plan }
     */
    async getLeaderboard(orderField, limitN) {
      if (orderField === undefined) orderField = 'beastScore';
      if (limitN === undefined) limitN = 50;
      try {
        const snap = await db()
          .collection('leaderboard')
          .orderBy(orderField, 'desc')
          .limit(limitN)
          .get();

        return snap.docs.map((doc) => ({ uid: doc.id, ...doc.data() }));
      } catch (err) {
        console.error('[CommunityService] getLeaderboard error:', err);
        return [];
      }
    },

    /**
     * Returns the member's 1-based rank on the board for the given field,
     * or null if they have no entry yet. Counts docs with a strictly higher
     * value, so ties share the same rank.
     *
     * @param {string} uid
     * @param {string} [orderField='beastScore']
     * @returns {Promise<number|null>}
     */
    async getUserRank(uid, orderField) {
      if (orderField === undefined) orderField = 'beastScore';
      try {
        const mySnap = await db().collection('leaderboard').doc(uid).get();
        if (!mySnap.exists || typeof mySnap.data()[orderField] !== 'number') return null;

        const higherQuery = db()
          .collection('leaderboard')
          .where(orderField, '>', mySnap.data()[orderField]);

        // count() aggregate costs 1 read per 1000 matching docs instead of
        // fetching every higher-ranked document.
        if (typeof higherQuery.count === 'function') {
          const agg = await higherQuery.count().get();
          return agg.data().count + 1;
        }

        const higher = await higherQuery.get();
        return higher.size + 1;
      } catch (err) {
        console.error('[CommunityService] getUserRank error:', err);
        return null;
      }
    },

    /**
     * Real-time leaderboard subscription via onSnapshot.
     * Returns an unsubscribe function — call it to stop listening.
     *
     * @param {string} [orderField='beastScore']
     * @param {number} [limitN=50]
     * @param {function(Object[]): void} callback - called with entries array on every change
     * @returns {function} unsubscribe
     */
    subscribeLeaderboard(orderField, limitN, callback) {
      if (orderField === undefined) orderField = 'beastScore';
      if (limitN === undefined) limitN = 50;
      try {
        const unsub = db()
          .collection('leaderboard')
          .orderBy(orderField, 'desc')
          .limit(limitN)
          .onSnapshot(
            (snap) => {
              const entries = snap.docs.map((doc) => ({ uid: doc.id, ...doc.data() }));
              try { callback(entries); } catch (e) { console.error('[CommunityService] subscribeLeaderboard callback error:', e); }
            },
            (err) => { console.error('[CommunityService] subscribeLeaderboard error:', err); }
          );
        return unsub;
      } catch (err) {
        console.error('[CommunityService] subscribeLeaderboard setup error:', err);
        return function () {};
      }
    },

    /**
     * Removes the member's entry from the leaderboard (privacy opt-out).
     *
     * @param {string} uid
     * @returns {Promise<void>}
     */
    async removeEntry(uid) {
      try {
        await db().collection('leaderboard').doc(uid).delete();
        console.log('[CommunityService] removeEntry:', uid);
      } catch (err) {
        console.error('[CommunityService] removeEntry error:', err);
        throw err;
      }
    },
  };

  console.log('[CommunityService] loaded');
})();
