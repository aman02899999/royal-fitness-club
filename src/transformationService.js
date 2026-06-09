/**
 * transformationService.js — Transformation Data Persistence Service
 * Royal Fitness Club SaaS Platform
 *
 * Uses Firebase v10 compat SDK (loaded via CDN script tags).
 * Exposes window.TransformationService with all transformation-data operations.
 *
 * Depends on: firebase/firestore (compat CDN)
 *
 * Collection layout:
 *   progress_logs/{uid}/logs/{auto-id}  — calculator results
 *   measurements/{uid}/logs/{auto-id}   — body measurement entries
 *   activity/{uid}                      — streak, workouts, hydration
 *   physio_logs/{uid}/logs/{auto-id}    — physio score history
 *   physio_summary/{uid}                — latest physio scores (single doc)
 *   users/{uid}                         — lastCalculation timestamp
 *
 * Load order in index.html:
 *   1. firebase-app-compat.js
 *   2. firebase-firestore-compat.js
 *   3. <firebase init script>
 *   4. transformationService.js  ← this file
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
   * Rounds a numeric value to `decimals` decimal places.
   * Returns 0 if the value is falsy or not a finite number.
   *
   * @param {*}      val
   * @param {number} [decimals=0]
   * @returns {number}
   */
  function round(val, decimals) {
    if (!val && val !== 0) return 0;
    var n = parseFloat(val);
    if (!isFinite(n)) return 0;
    var factor = Math.pow(10, decimals || 0);
    return Math.round(n * factor) / factor;
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
   * Formats a Date object to 'dd MMM' string (e.g. "09 Jun").
   * @param {Date} [date]
   * @returns {string}
   */
  function formatDdMmm(date) {
    var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    var d = date || new Date();
    var dd = String(d.getDate()).padStart(2, '0');
    return dd + ' ' + months[d.getMonth()];
  }

  /**
   * Converts a measurements object to numbers, skipping non-numeric values.
   * Input values are typically strings from HTML inputs.
   *
   * @param {Object} measurements - Raw string measurements
   * @returns {Object}            - Parsed numeric measurements
   */
  function parseMeasurements(measurements) {
    var out = {};
    var fields = ['waist', 'chest', 'arms', 'hips', 'thigh'];
    fields.forEach(function (key) {
      var v = parseFloat(measurements[key]);
      out[key] = isFinite(v) ? v : 0;
    });
    return out;
  }

  // ---------------------------------------------------------------------------
  // Public API
  // ---------------------------------------------------------------------------

  window.TransformationService = {

    /**
     * Saves a calculator result to `progress_logs/{uid}/logs/{auto-id}`.
     *
     * Also updates `users/{uid}.lastCalculation` with a server timestamp so
     * the user document always reflects the most recent activity.
     *
     * The `result` object is the `lastRes` value from index.html and must
     * contain at minimum: bmi, bmr, tdee, targetCals, bf, score, goal, diet,
     * weight, height, age, macros:{prot, carb, fat}.
     *
     * @param {string} uid    - Firebase Auth UID
     * @param {Object} result - Calculator output from lastRes
     * @returns {Promise<string|null>} Auto-generated document ID, or null on error
     */
    async saveCalculationResult(uid, result) {
      try {
        if (!uid || !result) return null;

        var doc = {
          uid:        uid,
          bmi:        round(result.bmi, 1),
          bmr:        Math.round(result.bmr  || 0),
          tdee:       Math.round(result.tdee || 0),
          calories:   result.targetCals || 0,
          bodyFat:    round(result.bf, 1),
          beastScore: result.score  || 0,
          goal:       result.goal   || null,
          diet:       result.diet   || null,
          weight:     result.weight || null,
          height:     result.height || null,
          age:        result.age    || null,
          macros: {
            prot: result.macros ? (result.macros.prot || 0) : 0,
            carb: result.macros ? (result.macros.carb || 0) : 0,
            fat:  result.macros ? (result.macros.fat  || 0) : 0,
          },
          date:      serverTimestamp(),
          timestamp: serverTimestamp(),
        };

        var docRef = await db()
          .collection('progress_logs')
          .doc(uid)
          .collection('logs')
          .add(doc);

        // Best-effort update — do not block on or throw from this
        try {
          await db().collection('users').doc(uid).update({
            lastCalculation: serverTimestamp(),
          });
        } catch (updateErr) {
          console.warn('[TransformationService] lastCalculation update failed:', updateErr);
        }

        console.log('[TransformationService] saveCalculationResult:', uid, docRef.id);
        return docRef.id;
      } catch (err) {
        console.error('[TransformationService] saveCalculationResult error:', err);
        return null;
      }
    },

    /**
     * Returns the single most recent calculation result for a user.
     *
     * Reads the latest document from `progress_logs/{uid}/logs` ordered by
     * `timestamp` descending with limit 1.
     *
     * @param {string} uid
     * @returns {Promise<Object|null>} Document data (with injected `id`) or null
     */
    async getLastCalculation(uid) {
      try {
        if (!uid) return null;

        var snap = await db()
          .collection('progress_logs')
          .doc(uid)
          .collection('logs')
          .orderBy('timestamp', 'desc')
          .limit(1)
          .get();

        if (snap.empty) return null;
        var doc = snap.docs[0];
        return { id: doc.id, ...doc.data() };
      } catch (err) {
        console.error('[TransformationService] getLastCalculation error:', err);
        return null;
      }
    },

    /**
     * Returns calculation history for progress chart rendering.
     *
     * Each entry is a lightweight projection containing only the fields needed
     * for chart display: date, bmi, bodyFat, beastScore, calories, weight.
     *
     * @param {string} uid
     * @param {number} [limitN=30] - Maximum entries to return (most recent first)
     * @returns {Promise<Array<{date: Date|null, bmi: number, bodyFat: number, beastScore: number, calories: number, weight: number|null}>>}
     */
    async getCalculationHistory(uid, limitN) {
      if (limitN === undefined) limitN = 30;
      try {
        if (!uid) return [];

        var snap = await db()
          .collection('progress_logs')
          .doc(uid)
          .collection('logs')
          .orderBy('timestamp', 'desc')
          .limit(limitN)
          .get();

        return snap.docs.map(function (doc) {
          var d = doc.data();
          return {
            date:       toDate(d.timestamp || d.date),
            bmi:        d.bmi        || 0,
            bodyFat:    d.bodyFat    || 0,
            beastScore: d.beastScore || 0,
            calories:   d.calories   || 0,
            weight:     d.weight     || null,
          };
        });
      } catch (err) {
        console.error('[TransformationService] getCalculationHistory error:', err);
        return [];
      }
    },

    /**
     * Saves a body measurement entry to `measurements/{uid}/logs/{auto-id}`.
     *
     * Input values (waist, chest, arms, hips, thigh) are accepted as strings
     * from HTML inputs and are coerced to numbers before storage. A human-
     * readable `dateStr` field ('dd MMM') is computed at write time.
     *
     * @param {string} uid          - Firebase Auth UID
     * @param {{waist?: string, chest?: string, arms?: string, hips?: string, thigh?: string}} measurements
     * @returns {Promise<string|null>} Auto-generated document ID, or null on error
     */
    async saveMeasurement(uid, measurements) {
      try {
        if (!uid || !measurements) return null;

        var parsed = parseMeasurements(measurements);

        var docRef = await db()
          .collection('measurements')
          .doc(uid)
          .collection('logs')
          .add({
            ...parsed,
            date:    serverTimestamp(),
            dateStr: formatDdMmm(new Date()),
          });

        console.log('[TransformationService] saveMeasurement:', uid, docRef.id);
        return docRef.id;
      } catch (err) {
        console.error('[TransformationService] saveMeasurement error:', err);
        return null;
      }
    },

    /**
     * Returns measurement history for a user ordered by date descending.
     *
     * @param {string} uid
     * @param {number} [limitN=10] - Maximum entries to return
     * @returns {Promise<Object[]>}
     */
    async getMeasurementHistory(uid, limitN) {
      if (limitN === undefined) limitN = 10;
      try {
        if (!uid) return [];

        var snap = await db()
          .collection('measurements')
          .doc(uid)
          .collection('logs')
          .orderBy('date', 'desc')
          .limit(limitN)
          .get();

        return snap.docs.map(function (doc) {
          return { id: doc.id, ...doc.data() };
        });
      } catch (err) {
        console.error('[TransformationService] getMeasurementHistory error:', err);
        return [];
      }
    },

    /**
     * Saves or updates activity data for a user in `activity/{uid}`.
     *
     * The document is merged so existing fields not present in `data` are
     * preserved. If the incoming streak is higher than the persisted streak,
     * `lastCheckin` is refreshed to the server timestamp to record the
     * moment the streak advanced.
     *
     * @param {string} uid
     * @param {{streak: number, wk: number, hy: number}} data
     *   streak — current streak in days
     *   wk     — workout sessions completed
     *   hy     — hydration-goal days met
     * @returns {Promise<void>}
     */
    async saveActivityData(uid, data) {
      try {
        if (!uid || !data) return;

        var docRef = db().collection('activity').doc(uid);

        // Read current streak to decide whether to bump lastCheckin
        var existingSnap = await docRef.get();
        var previousStreak = existingSnap.exists
          ? (existingSnap.data().streak || 0)
          : 0;

        var payload = {
          streak:        data.streak      || 0,
          workouts:      data.wk          || 0,
          hydrationDays: data.hy          || 0,
          updatedAt:     serverTimestamp(),
        };

        if ((data.streak || 0) > previousStreak) {
          payload.lastCheckin = serverTimestamp();
        }

        await docRef.set(payload, { merge: true });

        console.log('[TransformationService] saveActivityData:', uid);
      } catch (err) {
        console.error('[TransformationService] saveActivityData error:', err);
      }
    },

    /**
     * Returns activity data for a user from `activity/{uid}`.
     * Falls back to zero-valued defaults when the document does not yet exist.
     *
     * @param {string} uid
     * @returns {Promise<{streak: number, workouts: number, hydrationDays: number}>}
     */
    async getActivityData(uid) {
      var DEFAULT = { streak: 0, workouts: 0, hydrationDays: 0 };
      try {
        if (!uid) return DEFAULT;

        var snap = await db().collection('activity').doc(uid).get();
        if (!snap.exists) return DEFAULT;

        var d = snap.data();
        return {
          streak:        d.streak        || 0,
          workouts:      d.workouts      || 0,
          hydrationDays: d.hydrationDays || 0,
        };
      } catch (err) {
        console.error('[TransformationService] getActivityData error:', err);
        return DEFAULT;
      }
    },

    /**
     * Saves physio assessment scores.
     *
     * Writes to two locations atomically via a Firestore batch:
     *   physio_logs/{uid}/logs/{auto-id}  — immutable history entry
     *   physio_summary/{uid}              — mutable latest-scores document
     *
     * @param {string} uid
     * @param {{posture: number, mobility: number, recovery: number}} scores - 0–100 values
     * @returns {Promise<void>}
     */
    async savePhysioScores(uid, scores) {
      try {
        if (!uid || !scores) return;

        var logRef = db()
          .collection('physio_logs')
          .doc(uid)
          .collection('logs')
          .doc(); // auto-ID

        var summaryRef = db().collection('physio_summary').doc(uid);

        var logEntry = {
          posture:   scores.posture   || 0,
          mobility:  scores.mobility  || 0,
          recovery:  scores.recovery  || 0,
          timestamp: serverTimestamp(),
        };

        var summaryEntry = {
          posture:   scores.posture   || 0,
          mobility:  scores.mobility  || 0,
          recovery:  scores.recovery  || 0,
          updatedAt: serverTimestamp(),
        };

        var batch = db().batch();
        batch.set(logRef, logEntry);
        batch.set(summaryRef, summaryEntry, { merge: true });
        await batch.commit();

        console.log('[TransformationService] savePhysioScores:', uid);
      } catch (err) {
        console.error('[TransformationService] savePhysioScores error:', err);
      }
    },

    /**
     * Returns the latest physio scores for a user from `physio_summary/{uid}`.
     * Falls back to zero-valued defaults when the document does not yet exist.
     *
     * @param {string} uid
     * @returns {Promise<{posture: number, mobility: number, recovery: number}>}
     */
    async getPhysioScores(uid) {
      var DEFAULT = { posture: 0, mobility: 0, recovery: 0 };
      try {
        if (!uid) return DEFAULT;

        var snap = await db().collection('physio_summary').doc(uid).get();
        if (!snap.exists) return DEFAULT;

        var d = snap.data();
        return {
          posture:  d.posture  || 0,
          mobility: d.mobility || 0,
          recovery: d.recovery || 0,
        };
      } catch (err) {
        console.error('[TransformationService] getPhysioScores error:', err);
        return DEFAULT;
      }
    },

    /**
     * Returns a complete transformation summary suitable for profile display.
     *
     * All sub-reads are parallelised and individually guarded. A failure in
     * any one sub-read returns null/defaults for that section rather than
     * failing the entire summary.
     *
     * @param {string} uid
     * @returns {Promise<{
     *   lastCalculation: Object|null,
     *   measurementCount: number,
     *   calculationCount: number,
     *   activityData: {streak: number, workouts: number, hydrationDays: number},
     *   physioScores: {posture: number, mobility: number, recovery: number}
     * }>}
     */
    async getTransformationSummary(uid) {
      var DEFAULT = {
        lastCalculation:  null,
        measurementCount: 0,
        calculationCount: 0,
        activityData:     { streak: 0, workouts: 0, hydrationDays: 0 },
        physioScores:     { posture: 0, mobility: 0, recovery: 0 },
      };

      try {
        if (!uid) return DEFAULT;

        var results = await Promise.allSettled([
          /* 0 */ window.TransformationService.getLastCalculation(uid),
          /* 1 */ db().collection('measurements').doc(uid).collection('logs').get(),
          /* 2 */ db().collection('progress_logs').doc(uid).collection('logs').get(),
          /* 3 */ window.TransformationService.getActivityData(uid),
          /* 4 */ window.TransformationService.getPhysioScores(uid),
        ]);

        function resolved(idx, fallback) {
          return results[idx].status === 'fulfilled' ? results[idx].value : fallback;
        }

        var lastCalculation  = resolved(0, null);
        var measSnap         = resolved(1, null);
        var calcSnap         = resolved(2, null);
        var activityData     = resolved(3, DEFAULT.activityData);
        var physioScores     = resolved(4, DEFAULT.physioScores);

        return {
          lastCalculation:  lastCalculation,
          measurementCount: measSnap ? measSnap.size : 0,
          calculationCount: calcSnap ? calcSnap.size : 0,
          activityData:     activityData     || DEFAULT.activityData,
          physioScores:     physioScores     || DEFAULT.physioScores,
        };
      } catch (err) {
        console.error('[TransformationService] getTransformationSummary error:', err);
        return DEFAULT;
      }
    },

  };

  console.log('[TransformationService] loaded');
})();
