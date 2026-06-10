/**
 * analyticsService.js — Event Analytics & Admin Reporting Service
 * Royal Fitness Club SaaS Platform
 *
 * Uses Firebase v10 compat SDK (loaded via CDN script tags).
 * Exposes window.AnalyticsService with all analytics and reporting operations.
 *
 * Depends on: firebase/app, firebase/auth, firebase/firestore (compat CDN)
 *
 * Collection layout:
 *   analytics/{uid}/events/{auto-id}   — per-user event stream
 *   global_analytics/{eventName}       — aggregated event counters
 *   users/{uid}                        — lastLogin, createdAt, plan fields
 *   subscriptions/{subId}              — amount, status, createdAt fields
 *   progress_logs/{uid}/logs/{auto-id} — calculator results
 *   measurements/{uid}/logs/{auto-id}  — body measurements
 *   activity/{uid}                     — streak counter
 *
 * Load order in index.html:
 *   1. firebase-app-compat.js
 *   2. firebase-auth-compat.js
 *   3. firebase-firestore-compat.js
 *   4. <firebase init script>
 *   5. analyticsService.js  ← this file
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

  /** @returns {firebase.firestore.FieldValue} */
  function increment(n) {
    return firebase.firestore.FieldValue.increment(n);
  }

  /**
   * Returns a Date set to midnight (00:00:00.000) UTC for a given offset.
   * @param {number} [daysAgo=0] - Days to subtract from today
   * @returns {Date}
   */
  function utcMidnight(daysAgo) {
    var d = new Date();
    d.setUTCHours(0, 0, 0, 0);
    if (daysAgo) d.setUTCDate(d.getUTCDate() - daysAgo);
    return d;
  }

  /**
   * Converts a Firestore Timestamp or raw value to a JS Date, or null.
   * @param {*} val
   * @returns {Date|null}
   */
  function toDate(val) {
    if (!val) return null;
    if (typeof val.toDate === 'function') return val.toDate();
    return new Date(val);
  }

  /**
   * Formats a Date to 'dd MMM' (e.g. "09 Jun").
   * @param {Date} date
   * @returns {string}
   */
  function formatDdMmm(date) {
    var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    var dd = String(date.getDate()).padStart(2, '0');
    return dd + ' ' + months[date.getMonth()];
  }

  // ---------------------------------------------------------------------------
  // Session ID management
  // ---------------------------------------------------------------------------

  var _sessionId = null;

  /**
   * Returns (or creates) a session-scoped ID persisted in sessionStorage.
   * A new ID is generated whenever the browser tab is closed and reopened.
   * @returns {string}
   */
  function getSessionId() {
    if (_sessionId) return _sessionId;

    try {
      var stored = sessionStorage.getItem('rfc_session_id');
      if (stored) {
        _sessionId = stored;
        return _sessionId;
      }
    } catch (_) {
      // sessionStorage unavailable (e.g. private browsing with restrictions)
    }

    // Generate a new session ID: timestamp + random hex
    _sessionId = Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 10);

    try {
      sessionStorage.setItem('rfc_session_id', _sessionId);
    } catch (_) {
      // Ignore — in-memory fallback is still usable
    }

    return _sessionId;
  }

  // ---------------------------------------------------------------------------
  // Public API
  // ---------------------------------------------------------------------------

  window.AnalyticsService = {

    /**
     * Tracks an arbitrary user event.
     *
     * Writes to:
     *   analytics/{uid}/events/{auto-id}  — full event payload
     *   global_analytics/{eventName}      — increments count, updates lastSeen
     *
     * Silently no-ops when no authenticated user is present, so callers do not
     * need to guard against unauthenticated state.
     *
     * Recognised event names (not enforced — others are accepted):
     *   'calculator_used', 'meal_plan_viewed', 'pro_modal_opened',
     *   'subscription_started', 'profile_updated', 'measurement_saved',
     *   'pdf_exported', 'physio_used', 'login', 'register', 'view'
     *
     * @param {string} eventName          - Identifier for the event type
     * @param {Object} [properties={}]    - Arbitrary key/value metadata
     * @returns {Promise<void>}
     */
    async trackEvent(eventName, properties) {
      if (properties === undefined) properties = {};
      try {
        var user = firebase.auth().currentUser;
        if (!user) return;

        var uid = user.uid;
        var eventDoc = {
          event: eventName,
          properties: properties,
          timestamp: serverTimestamp(),
          sessionId: getSessionId(),
        };

        var globalDoc = {
          count: increment(1),
          lastSeen: serverTimestamp(),
        };

        // Fire both writes concurrently — neither depends on the other
        await Promise.all([
          db()
            .collection('analytics')
            .doc(uid)
            .collection('events')
            .add(eventDoc),
          db()
            .collection('global_analytics')
            .doc(eventName)
            .set(globalDoc, { merge: true }),
        ]);
      } catch (err) {
        // Analytics must never break the caller
        console.error('[AnalyticsService] trackEvent error:', err);
      }
    },

    /**
     * Returns (or creates) the session ID for the current browser tab session.
     * Persisted in sessionStorage so it survives page navigations within the
     * same tab but resets on tab close.
     *
     * @returns {string}
     */
    getSessionId: getSessionId,

    /**
     * Counts Daily Active Users (DAU): users whose `lastLogin` timestamp is
     * greater than or equal to today's midnight UTC.
     *
     * @returns {Promise<number>}
     */
    async getDAU() {
      try {
        var since = firebase.firestore.Timestamp.fromDate(utcMidnight(0));
        var snap = await db()
          .collection('users')
          .where('lastLogin', '>=', since)
          .get();
        return snap.size;
      } catch (err) {
        console.error('[AnalyticsService] getDAU error:', err);
        return 0;
      }
    },

    /**
     * Counts Monthly Active Users (MAU): users whose `lastLogin` timestamp is
     * within the last 30 days.
     *
     * @returns {Promise<number>}
     */
    async getMAU() {
      try {
        var since = firebase.firestore.Timestamp.fromDate(utcMidnight(30));
        var snap = await db()
          .collection('users')
          .where('lastLogin', '>=', since)
          .get();
        return snap.size;
      } catch (err) {
        console.error('[AnalyticsService] getMAU error:', err);
        return 0;
      }
    },

    /**
     * Counts new user registrations in the last 7 days.
     *
     * @returns {Promise<number>}
     */
    async getNewUsersThisWeek() {
      try {
        var since = firebase.firestore.Timestamp.fromDate(utcMidnight(7));
        var snap = await db()
          .collection('users')
          .where('createdAt', '>=', since)
          .get();
        return snap.size;
      } catch (err) {
        console.error('[AnalyticsService] getNewUsersThisWeek error:', err);
        return 0;
      }
    },

    /**
     * Builds a comprehensive admin analytics report.
     *
     * Reads are parallelised where possible. All sub-queries have individual
     * error guards so a single failing sub-query never breaks the full report.
     *
     * @returns {Promise<{
     *   dau: number,
     *   mau: number,
     *   totalUsers: number,
     *   proUsers: number,
     *   freeUsers: number,
     *   newThisWeek: number,
     *   newThisMonth: number,
     *   proConversionRate: string,
     *   topEvents: Array<{event: string, count: number}>,
     *   planDistribution: {free: number, royal_pro: number, royal_elite: number},
     *   revenueThisMonth: number,
     *   retentionRate: string
     * }>}
     */
    async getAdminReport() {
      var DEFAULT = {
        dau: 0,
        mau: 0,
        totalUsers: 0,
        proUsers: 0,
        freeUsers: 0,
        newThisWeek: 0,
        newThisMonth: 0,
        proConversionRate: '0.0%',
        topEvents: [],
        planDistribution: { free: 0, royal_pro: 0, royal_elite: 0 },
        revenueThisMonth: 0,
        retentionRate: '—',
      };

      try {
        var thirtyDaysAgo = firebase.firestore.Timestamp.fromDate(utcMidnight(30));
        var sevenDaysAgo  = firebase.firestore.Timestamp.fromDate(utcMidnight(7));
        var todayMidnight = firebase.firestore.Timestamp.fromDate(utcMidnight(0));

        // Start of current calendar month (local)
        var now = new Date();
        var startOfMonth = new Date(now.getFullYear(), now.getMonth(), 1);
        var startOfMonthTs = firebase.firestore.Timestamp.fromDate(startOfMonth);

        // Parallelise all top-level reads
        var results = await Promise.allSettled([
          /* 0 */ db().collection('users').get(),
          /* 1 */ db().collection('users').where('lastLogin', '>=', todayMidnight).get(),
          /* 2 */ db().collection('users').where('lastLogin', '>=', thirtyDaysAgo).get(),
          /* 3 */ db().collection('users').where('createdAt', '>=', sevenDaysAgo).get(),
          /* 4 */ db().collection('users').where('createdAt', '>=', thirtyDaysAgo).get(),
          /* 5 */ db().collection('global_analytics').orderBy('count', 'desc').limit(10).get(),
          /* 6 */ db()
                    .collection('subscriptions')
                    .where('status', 'in', ['active', 'completed'])
                    .where('createdAt', '>=', startOfMonthTs)
                    .get(),
        ]);

        // Helper: safely extract .value from allSettled result
        function val(idx) {
          return results[idx].status === 'fulfilled' ? results[idx].value : null;
        }

        // --- Users collection aggregation ---
        var usersSnap = val(0);
        var totalUsers = 0;
        var proUsers = 0;
        var freeUsers = 0;
        var planDistribution = { free: 0, royal_pro: 0, royal_elite: 0 };

        if (usersSnap) {
          totalUsers = usersSnap.size;
          usersSnap.forEach(function (doc) {
            var plan = doc.data().plan || 'free';
            if (plan === 'royal_pro') {
              proUsers++;
              planDistribution.royal_pro++;
            } else if (plan === 'royal_elite') {
              proUsers++;
              planDistribution.royal_elite++;
            } else {
              freeUsers++;
              planDistribution.free++;
            }
          });
        }

        // --- Active user counts ---
        var dau         = val(1) ? val(1).size : 0;
        var mau         = val(2) ? val(2).size : 0;
        var newThisWeek = val(3) ? val(3).size : 0;
        var newThisMonth = val(4) ? val(4).size : 0;

        // --- Conversion rate ---
        var proConversionRate = totalUsers > 0
          ? (proUsers / totalUsers * 100).toFixed(1) + '%'
          : '0.0%';

        // --- Top events ---
        var topEvents = [];
        var globalSnap = val(5);
        if (globalSnap) {
          globalSnap.forEach(function (doc) {
            topEvents.push({ event: doc.id, count: doc.data().count || 0 });
          });
          // Already ordered by count desc from the query; re-sort client-side as
          // a safety measure in case Firestore ordering differs.
          topEvents.sort(function (a, b) { return b.count - a.count; });
        }

        // --- Revenue this month ---
        var revenueThisMonth = 0;
        var revenueSnap = val(6);
        if (revenueSnap) {
          revenueSnap.forEach(function (doc) {
            revenueThisMonth += (doc.data().amount || 0);
          });
        }

        return {
          dau: dau,
          mau: mau,
          totalUsers: totalUsers,
          proUsers: proUsers,
          freeUsers: freeUsers,
          newThisWeek: newThisWeek,
          newThisMonth: newThisMonth,
          proConversionRate: proConversionRate,
          topEvents: topEvents,
          planDistribution: planDistribution,
          revenueThisMonth: revenueThisMonth,
          retentionRate: '—',
        };
      } catch (err) {
        console.error('[AnalyticsService] getAdminReport error:', err);
        return DEFAULT;
      }
    },

    /**
     * Convenience wrapper that calls trackEvent with section metadata.
     * Use this for lightweight section-view instrumentation without polluting
     * the event namespace with arbitrary section strings.
     *
     * @param {string} sectionName - e.g. 'calculator', 'meal_plan', 'profile'
     * @returns {Promise<void>}
     */
    async trackView(sectionName) {
      return window.AnalyticsService.trackEvent('view', { section: sectionName });
    },

    /**
     * Returns a personal activity summary for a given user.
     *
     * Reads (in parallel):
     *   progress_logs/{uid}/logs  — calculator history count
     *   measurements/{uid}/logs  — measurement history count
     *   activity/{uid}           — streak and lastCheckin
     *
     * @param {string} uid
     * @returns {Promise<{
     *   totalCalculations: number,
     *   totalMeasurements: number,
     *   lastActive: Date|null,
     *   streakDays: number
     * }>}
     */
    async getUserActivity(uid) {
      var DEFAULT = {
        totalCalculations: 0,
        totalMeasurements: 0,
        lastActive: null,
        streakDays: 0,
      };

      try {
        if (!uid) return DEFAULT;

        var results = await Promise.allSettled([
          /* 0 */ db().collection('progress_logs').doc(uid).collection('logs').get(),
          /* 1 */ db().collection('measurements').doc(uid).collection('logs').get(),
          /* 2 */ db().collection('activity').doc(uid).get(),
        ]);

        var calcSnap    = results[0].status === 'fulfilled' ? results[0].value : null;
        var measSnap    = results[1].status === 'fulfilled' ? results[1].value : null;
        var activityDoc = results[2].status === 'fulfilled' ? results[2].value : null;

        var totalCalculations = calcSnap ? calcSnap.size : 0;
        var totalMeasurements = measSnap ? measSnap.size : 0;
        var streakDays = 0;
        var lastActive = null;

        if (activityDoc && activityDoc.exists) {
          var data = activityDoc.data();
          streakDays = data.streak || 0;
          lastActive = toDate(data.lastCheckin || data.updatedAt);
        }

        return {
          totalCalculations: totalCalculations,
          totalMeasurements: totalMeasurements,
          lastActive: lastActive,
          streakDays: streakDays,
        };
      } catch (err) {
        console.error('[AnalyticsService] getUserActivity error:', err);
        return DEFAULT;
      }
    },

  };

  console.log('[AnalyticsService] loaded');
})();
