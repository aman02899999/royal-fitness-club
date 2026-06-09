/**
 * auth.js — Firebase Authentication Service
 * Royal Fitness Club SaaS Platform
 *
 * Uses Firebase v10 compat SDK (loaded via CDN script tags).
 * Exposes window.AuthService with all auth-related operations.
 *
 * Depends on: firebase/app, firebase/auth, firebase/firestore (compat CDN)
 */

(function () {
  'use strict';

  // ---------------------------------------------------------------------------
  // Helpers
  // ---------------------------------------------------------------------------

  /**
   * Returns a Firestore server timestamp via the compat SDK.
   * @returns {firebase.firestore.FieldValue}
   */
  function serverTimestamp() {
    return firebase.firestore.FieldValue.serverTimestamp();
  }

  /**
   * Shorthand references (resolved at call-time so the CDN scripts are already
   * loaded before any function executes).
   */
  function auth() {
    return firebase.auth();
  }

  function db() {
    return firebase.firestore();
  }

  // ---------------------------------------------------------------------------
  // Internal helpers
  // ---------------------------------------------------------------------------

  /**
   * Fetches a user document from Firestore.
   * @param {string} uid
   * @returns {Promise<Object|null>}
   */
  async function fetchUserData(uid) {
    try {
      const snap = await db().collection('users').doc(uid).get();
      return snap.exists ? snap.data() : null;
    } catch (err) {
      console.error('[AuthService] fetchUserData error:', err);
      return null;
    }
  }

  /**
   * Builds a normalised session object returned by loginUser / onAuthStateChanged.
   * @param {firebase.User} user
   * @param {Object} userData
   * @returns {{user: firebase.User, userData: Object, isAdmin: boolean, isPro: boolean}}
   */
  function buildSession(user, userData) {
    const isAdmin = userData ? userData.role === 'admin' : false;
    const isPro =
      userData
        ? ['royal_pro', 'royal_elite'].includes(userData.plan)
        : false;
    return { user, userData, isAdmin, isPro };
  }

  // ---------------------------------------------------------------------------
  // Public API
  // ---------------------------------------------------------------------------

  window.AuthService = {

    /**
     * Registers a new Firebase Auth user and creates the corresponding
     * Firestore document in the `users` collection.
     *
     * @param {string} name     - Display name
     * @param {string} email    - Email address
     * @param {string} phone    - Phone number
     * @param {string} password - Password
     * @returns {Promise<{user: firebase.User, userData: Object}>}
     */
    async registerUser(name, email, phone, password) {
      try {
        const credential = await auth().createUserWithEmailAndPassword(email, password);
        const user = credential.user;

        // Optionally set display name on the Auth profile
        await user.updateProfile({ displayName: name });

        const userData = {
          uid: user.uid,
          name,
          email,
          phone: phone || '',
          role: 'member',
          status: 'active',
          plan: 'free',
          createdAt: serverTimestamp(),
          updatedAt: serverTimestamp(),
          lastLogin: serverTimestamp(),
        };

        await db().collection('users').doc(user.uid).set(userData);

        console.log('[AuthService] registerUser success:', user.uid);
        return { user, userData };
      } catch (err) {
        console.error('[AuthService] registerUser error:', err);
        throw err;
      }
    },

    /**
     * Signs in an existing user with email and password.
     * Updates the `lastLogin` timestamp in Firestore on success.
     *
     * @param {string} email
     * @param {string} password
     * @returns {Promise<{user: firebase.User, userData: Object, isAdmin: boolean, isPro: boolean}>}
     */
    async loginUser(email, password) {
      try {
        const credential = await auth().signInWithEmailAndPassword(email, password);
        const user = credential.user;

        // Update last login timestamp (non-blocking — fire and forget is fine)
        db()
          .collection('users')
          .doc(user.uid)
          .update({ lastLogin: serverTimestamp(), updatedAt: serverTimestamp() })
          .catch((err) => console.warn('[AuthService] lastLogin update warning:', err));

        const userData = await fetchUserData(user.uid);

        // Persist lightweight flags for legacy localStorage consumers
        if (userData) {
          localStorage.setItem('bm_user', JSON.stringify({ uid: user.uid, name: userData.name, email }));
          if (['royal_pro', 'royal_elite'].includes(userData.plan)) {
            localStorage.setItem('bm_pro', '1');
          }
        }

        const session = buildSession(user, userData);
        console.log('[AuthService] loginUser success:', user.uid);
        return session;
      } catch (err) {
        console.error('[AuthService] loginUser error:', err);
        throw err;
      }
    },

    /**
     * Legacy / simplified sign-in flow used by the current UI (name + email + phone,
     * no password field). This does NOT create a real Firebase Auth account.
     *
     * Instead it:
     *  1. Creates or updates a document in the `pending_users` collection.
     *  2. Sets window.pendingUser for the UI to consume.
     *  3. Mirrors the data to localStorage so the rest of the app keeps working.
     *
     * When the user is ready to upgrade to a full account, call registerUser().
     *
     * @param {string} name
     * @param {string} email
     * @param {string} phone
     * @returns {Promise<Object>} pendingUser object
     */
    async loginWithName(name, email, phone) {
      try {
        const pendingId = btoa(email.toLowerCase().trim()).replace(/=/g, '');

        const pendingData = {
          id: pendingId,
          name: name || '',
          email: email || '',
          phone: phone || '',
          plan: 'free',
          status: 'active',
          role: 'member',
          updatedAt: serverTimestamp(),
        };

        const docRef = db().collection('pending_users').doc(pendingId);
        const snap = await docRef.get();

        if (!snap.exists) {
          pendingData.createdAt = serverTimestamp();
          await docRef.set(pendingData);
        } else {
          await docRef.update({
            name: name || snap.data().name,
            phone: phone || snap.data().phone,
            updatedAt: serverTimestamp(),
          });
        }

        const resolved = { ...pendingData, id: pendingId };

        // Expose globally so the UI can react immediately
        window.pendingUser = resolved;

        // Keep legacy localStorage bridge alive
        localStorage.setItem('bm_user', JSON.stringify({ uid: pendingId, name, email }));

        console.log('[AuthService] loginWithName (pending user):', pendingId);
        return resolved;
      } catch (err) {
        console.error('[AuthService] loginWithName error:', err);
        throw err;
      }
    },

    /**
     * Signs the current user out of Firebase Auth and clears all local state.
     *
     * @returns {Promise<void>}
     */
    async logoutUser() {
      try {
        await auth().signOut();

        // Clear legacy localStorage flags
        localStorage.removeItem('bm_user');
        localStorage.removeItem('bm_pro');
        localStorage.removeItem('bm_sub');

        // Clear pending user reference
        window.pendingUser = null;

        console.log('[AuthService] logoutUser: signed out');
      } catch (err) {
        console.error('[AuthService] logoutUser error:', err);
        throw err;
      }
    },

    /**
     * Subscribes to Firebase Auth state changes.
     * The callback receives a session object (or null on sign-out).
     *
     * @param {function({user, userData, isAdmin, isPro}|null): void} callback
     * @returns {function} Unsubscribe function
     */
    onAuthStateChanged(callback) {
      return auth().onAuthStateChanged(async (user) => {
        if (!user) {
          callback(null);
          return;
        }

        try {
          const userData = await fetchUserData(user.uid);
          callback(buildSession(user, userData));
        } catch (err) {
          console.error('[AuthService] onAuthStateChanged fetch error:', err);
          callback(buildSession(user, null));
        }
      });
    },

    /**
     * Returns the currently authenticated Firebase user, or null.
     *
     * @returns {firebase.User|null}
     */
    getCurrentUser() {
      return auth().currentUser;
    },

    /**
     * Checks whether a given UID belongs to an admin.
     * Reads the `role` field from Firestore.
     *
     * @param {string} uid
     * @returns {Promise<boolean>}
     */
    async checkAdmin(uid) {
      try {
        const userData = await fetchUserData(uid);
        return userData ? userData.role === 'admin' : false;
      } catch (err) {
        console.error('[AuthService] checkAdmin error:', err);
        return false;
      }
    },

    /**
     * Sends a password-reset email to the specified address.
     *
     * @param {string} email
     * @returns {Promise<void>}
     */
    async resetPassword(email) {
      try {
        await auth().sendPasswordResetEmail(email);
        console.log('[AuthService] resetPassword: email sent to', email);
      } catch (err) {
        console.error('[AuthService] resetPassword error:', err);
        throw err;
      }
    },

    /**
     * Updates the password of the currently authenticated user.
     * The user must have signed in recently; call reauthentication first if
     * Firebase throws `auth/requires-recent-login`.
     *
     * @param {string} newPassword
     * @returns {Promise<void>}
     */
    async updatePassword(newPassword) {
      try {
        const user = auth().currentUser;
        if (!user) throw new Error('No authenticated user');
        await user.updatePassword(newPassword);
        console.log('[AuthService] updatePassword: password updated');
      } catch (err) {
        console.error('[AuthService] updatePassword error:', err);
        throw err;
      }
    },
  };

  console.log('[AuthService] loaded');
})();
