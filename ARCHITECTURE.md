# Royal Fitness Club — Architecture

**India's Most Advanced Gym SaaS Platform**

> Single-file frontend SPA · Firebase backend · Razorpay payments · PWA-ready

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Tech Stack](#2-tech-stack)
3. [Repository Layout](#3-repository-layout)
4. [Frontend Architecture](#4-frontend-architecture)
5. [Authentication & Access Control](#5-authentication--access-control)
6. [Data Architecture](#6-data-architecture)
7. [Payment Integration (Razorpay)](#7-payment-integration-razorpay)
8. [Cloud Functions](#8-cloud-functions)
9. [Admin Panel](#9-admin-panel)
10. [Feature Catalogue](#10-feature-catalogue)
11. [Security Model](#11-security-model)
12. [PWA & Offline](#12-pwa--offline)
13. [Deployment](#13-deployment)
14. [Secrets & Environment Variables](#14-secrets--environment-variables)
15. [Key Constants & IDs](#15-key-constants--ids)
16. [Data-Flow Diagrams](#16-data-flow-diagrams)

---

## 1. Project Overview

Royal Fitness Club (RFC) is a **fitness SaaS platform** targeting Indian gym-goers and fitness enthusiasts. It combines:

- A **member-facing Progressive Web App** (`index.html`) with 20+ interactive tools
- A **admin control panel** (`admin.html`) for gym management
- **Firebase** for auth, database, hosting, and serverless functions
- **Razorpay** for Indian payment processing (subscriptions + one-time purchases)

The entire frontend is a **single HTML file** (~500 KB) that loads Firebase via CDN and renders everything client-side. There is no frontend build step, no bundler, and no framework — intentionally keeping the deployment surface minimal.

---

## 2. Tech Stack

| Layer | Technology |
|---|---|
| Hosting | Firebase Hosting (CDN + custom headers) |
| Auth | Firebase Authentication (email/password) |
| Database | Cloud Firestore (NoSQL) |
| File Storage | Firebase Storage |
| Backend Logic | Firebase Cloud Functions (Node.js 18) |
| Payments | Razorpay (orders + webhook verification) |
| Secrets | Google Secret Manager (via Firebase Functions secrets) |
| Frontend | Vanilla HTML/CSS/JavaScript (no framework) |
| Fonts | Google Fonts (Bebas Neue, Barlow Condensed, Inter) |
| PWA | Service Worker + Web App Manifest |
| Firebase SDK | Firebase JS SDK v10 (compat mode) loaded via CDN |

---

## 3. Repository Layout

```
royal-fitness-club/
│
├── index.html            ← Main SPA (entire user-facing app, ~500KB)
├── admin.html            ← Admin control panel
├── 404.html              ← Custom Firebase Hosting error page
├── sw.js                 ← Service Worker (PWA offline cache)
├── manifest.json         ← PWA Web App Manifest
├── firebase.js           ← Firebase config reference (safe to commit)
├── firebase.json         ← Firebase Hosting / Functions / Firestore config
├── .firebaserc           ← Firebase project alias
├── firestore.rules       ← Firestore security rules
├── firestore.indexes.json← Firestore composite indexes
├── storage.rules         ← Firebase Storage security rules
├── ARCHITECTURE.md       ← This file
│
├── functions/
│   ├── index.js          ← All Firebase Cloud Functions
│   └── package.json      ← Functions dependencies (firebase-functions, razorpay, cors)
│
├── icons/                ← PWA icon set (72px → 512px)
├── generated_pdfs/       ← Pre-generated PDF guides (served as static files)
├── posters/              ← Marketing poster images
├── scripts/              ← Utility scripts (not deployed)
├── src/                  ← Source utilities (not deployed via firebase.json ignore)
│
└── *.py                  ← PDF generation scripts (local tooling, not deployed)
```

**Deployed files** (controlled by `firebase.json` `ignore` list):
- `index.html`, `admin.html`, `404.html`, `sw.js`, `manifest.json`
- `icons/`, `generated_pdfs/`, `posters/`
- Python scripts, `src/`, `scripts/`, `functions/` are **excluded** from hosting

---

## 4. Frontend Architecture

### 4.1 Single-File SPA Pattern

`index.html` contains everything:

```
index.html
├── <head>             CSS variables, all styles (~600 lines)
├── Firebase SDK       CDN: firebase-app-compat, auth, firestore, analytics
├── Razorpay SDK       CDN: checkout.razorpay.com/v1/checkout.js
├── <body>             All HTML sections (profile, tools, store, arena…)
└── <script>           All application JavaScript (~6000 lines)
```

There is **no routing library**. Sections are `display:none` by default and revealed by toggling CSS classes or inline styles. Navigation links use anchor hash (`href="#arena"`) for scroll, and profile/modals use `display:block/none` toggling.

### 4.2 Section Map

| Section ID | Purpose |
|---|---|
| `#home` | Hero banner with live counters |
| `#profile` | Member dashboard (shown when logged in) |
| `#plans` | Pricing cards |
| `#calculator` | Beast Score + TDEE calculator |
| `#mealplan` | Formula-based AI meal planner |
| `#roadmap` | 12-week transformation roadmap |
| `#bodyfat` | Body fat calculator |
| `#calculators` | BMR / water / ideal weight calculators |
| `#physio` | Physio assessment (pain / posture / mobility / recovery) |
| `#dashboard` | Transformation dashboard with charts |
| `#tracker` | Workout + habit tracker |
| `#workoutlog` | Workout history log |
| `#arena` | Tiger Leaderboard |
| `#challenges` | Paid fitness challenges |
| `#bloodreport` | AI blood report diagnosis |
| `#courses` | Certification courses store |
| `#store` | PDF guides + bundle deals |

### 4.3 State Management

All runtime state lives in:

1. **Module-level `let` variables** — `user`, `isPro`, `lastRes`, `currentSplit`, etc.
2. **`localStorage`** — wallet, referral, challenges, courses, blood reports, workout logs
3. **Firebase Auth state** — `firebase.auth().onAuthStateChanged()`
4. **Firestore** — user profile, subscriptions, purchases, physio scores, leaderboard

### 4.4 Key Global Variables

```javascript
let user        // Firebase Auth user object (null = logged out)
let isPro       // boolean — user has active Pro plan
let lastRes     // result object from last calculator run
let currentSplit // current workout split ('ppl', 'upper_lower', etc.)
```

### 4.5 Core Function Patterns

```javascript
// Auth gate — most tool functions start with this pattern
if (!user) { forceLogin(); return; }
if (!isPro) { openModal('promodal'); return; }

// Toast notifications
toast('message')              // green success
toast('message', 'gold')      // amber warning
toast('message', true)        // red error

// Modal system
openModal('modalId')
closeModal('modalId')

// Profile system
openProfile()    // shows #profile section
closeProfile()   // hides #profile section
applyUser()      // renders everything for logged-in user
```

---

## 5. Authentication & Access Control

### 5.1 Login Flow

```
User clicks "Login"
      ↓
Firebase Auth (email + password)
      ↓
onAuthStateChanged fires
      ↓
applyUser() called
  ├─ Fetches Firestore /users/{uid}
  ├─ Sets isPro based on plan + expiryDate
  ├─ Renders profile card, wallet, leaderboard rank
  ├─ Calls checkLoginBonus() → ₹20 daily credit
  └─ Renders wallet + leaderboard
```

### 5.2 Registration Flow

```
User submits register form
      ↓
firebase.auth().createUserWithEmailAndPassword()
      ↓
registerWithCode() validates membership code
      ↓
Firestore /users/{uid} document created
      ↓
If referral code entered → creditReferrer() called
  ├─ Referrer gets ₹100 in wallet
  └─ New user gets ₹50 signup bonus
```

### 5.3 Access Tiers

| Tier | Condition | Access |
|---|---|---|
| **Guest** | Not logged in | Hero, pricing, leaderboard (read-only), blood report demo |
| **Free Member** | Logged in, `plan === 'free'` | Calculator, basic tools |
| **Pro Member** | Logged in, `plan === 'pro'`, `expiryDate` not past | All tools, PDF downloads, challenges join, courses |
| **Admin** | `admin.html` session, hardcoded credential check | Full admin panel |

---

## 6. Data Architecture

### 6.1 Firestore Collections

```
/users/{uid}
  ├── uid, name, email, phone
  ├── plan: 'free' | 'pro' | 'elite'
  ├── role: 'member' | 'admin'
  ├── expiryDate: Timestamp
  ├── gymMember: boolean
  ├── memberCode: string (used membership code)
  └── /renewals/{id} (subcollection)

/subscriptions/{subId}
  ├── uid, plan, status: 'active'|'cancelled'|'expired'
  ├── amount, currency
  ├── razorpayOrderId, razorpayPaymentId
  └── startDate, expiryDate

/codes/{code}
  ├── used: boolean
  └── usedBy: uid | null

/payment_orders/{orderId}
  ├── uid, plan|itemId, type: 'subscription'|'pdf_purchase'
  ├── amount, currency, status
  └── razorpayOrderId, paymentId

/pdf_purchases/{uid}/items/{itemId}
  └── uid, itemId, orderId, paymentId, amount, purchasedAt

/pdf_catalog/{itemId}
  └── name, description, price, fileUrl

/measurements/{uid}/logs/{logId}
  └── date, waist, chest, arms, hips, thigh

/progress_logs/{uid}/logs/{logId}
  └── bmi, bmr, tdee, score, goal, date

/activity/{uid}
  └── streak, lastWorkout, workoutCount

/physio_summary/{uid}
  └── recovery, posture, mobility scores

/physio_logs/{uid}/logs/{logId}
  └── assessment history

/leaderboard/{uid}
  └── name, city, tigerScore, streak, etc.

/announcements/{aid}
  └── title, body, createdAt (admin-written)

/pending_payments/{orderId}
  └── temporary payment state before webhook

/global_analytics/{eventName}
  └── count (aggregated event counters)

/ai_rate_limits/{uid_date}
  └── count (Cloud Function writes only)
```

### 6.2 localStorage Schema

All client-side persistence uses `localStorage`. Keys are namespaced:

| Key Pattern | Contents |
|---|---|
| `rfc_wallet_{uid}_data` | `{ balance, txns: [{id, ts, amount, desc, type, status}] }` |
| `rfc_refcode_{uid}` | Unique referral code string `RFC-XXXXXX` |
| `rfc_lb_date_{uid}` | Date string of last daily login bonus |
| `rfc_ref_count_{uid}` | Number of successful referrals |
| `rfc_referrals_{uid}` | Array of referral objects |
| `rfc_redeem_reqs_{uid}` | Array of UPI redemption requests |
| `rfc_ch_joined_{uid}` | Array of joined challenge IDs |
| `rfc_ch_prog_{uid}_{chId}` | `{ days, logs: [dateStrings] }` |
| `rfc_ch_pts_{chId}` | Participant count for a challenge |
| `rfc_challenges` | Override array for challenges (set by admin) |
| `rfc_courses` | Override array for courses (set by admin) |
| `rfc_purchased_{uid}` | Array of purchased course IDs |
| `rfc_blood_reports_{uid}` | Last 10 blood report results |
| `rfc_adm_*` | Admin panel data (members, blogs, faqs, pricing, etc.) |
| `rfc_newsletter` | Newsletter subscriber emails (main site) |

### 6.3 Admin localStorage (`rfc_adm_*`)

The admin panel persists all CMS content under `rfc_adm_` prefixed keys:

| Key | Contents |
|---|---|
| `rfc_adm_members` | Member array (demo/offline management) |
| `rfc_adm_features` | Feature/USP cards for homepage |
| `rfc_adm_testimonials` | Testimonial cards |
| `rfc_adm_blogs` | Blog post array |
| `rfc_adm_pricing` | Pricing plan array |
| `rfc_adm_faqs` | FAQ array |
| `rfc_adm_newsletter` | Admin-managed subscriber list |
| `rfc_adm_redemptions` | Wallet redemption requests |
| `rfc_adm_referrals` | Referral records |
| `rfc_adm_codes` | Generated access code history |
| `rfc_adm_activity` | Admin activity log (last 50 actions) |
| `rfc_adm_challenges_adm` | Challenge definitions (CRUD) |
| `rfc_adm_courses_adm` | Course definitions (CRUD) |
| `rfc_adm_seeded` | Boolean — prevents re-seeding defaults |

---

## 7. Payment Integration (Razorpay)

### 7.1 Architecture Principle

- **Key ID** (`rzp_live_SzivmCT3vTvTAK`) — public, safe in client JS and git
- **Key Secret** — **NEVER** in client code; stored only as Firebase Secret `RAZORPAY_KEY_SECRET`
- **Webhook Secret** — stored only as Firebase Secret `RAZORPAY_WEBHOOK_SECRET`
- All signature verification happens **server-side** in Cloud Functions

### 7.2 Subscription Payment Flow

```
Client                        Cloud Function              Razorpay
  │                               │                          │
  ├─ createRazorpayOrder({plan}) ─►│                          │
  │                               ├─ razorpay.orders.create()►│
  │                               │◄─── { orderId, amount } ──┤
  │◄────── { orderId, keyId } ────┤                          │
  │                               │                          │
  ├─ new Razorpay({ key, amount }).open() ──────────────────►│
  │◄──────────── { paymentId, signature } ───────────────────┤
  │                               │                          │
  ├─ verifyRazorpayPayment({...}) ►│                          │
  │                               ├─ HMAC-SHA256 verify      │
  │                               ├─ Write /subscriptions    │
  │                               ├─ Update /users/{uid}     │
  │◄────── { success: true } ─────┤                          │
  │                               │                          │
  │    (async backup path)        │◄── webhook: payment.captured
  │                               ├─ Re-verify + update plan │
```

### 7.3 PDF Purchase Flow

Same pattern as subscription but calls `createPDFOrder` + `recordPDFPurchase`. After verification, `pdf_purchases/{uid}/items/{itemId}` is written. The client checks this collection to gate PDF download buttons.

### 7.4 Challenge / Course Payments (Client-side only)

Challenge entry fees and course purchases use Razorpay **client-side only** for the demo implementation (no Cloud Function verification). The `handler` callback directly writes to localStorage. For production, these should be routed through a Cloud Function like the subscription flow.

---

## 8. Cloud Functions

All functions live in `functions/index.js`. Deployed to Firebase Functions Node.js 18.

| Function | Type | Trigger | Purpose |
|---|---|---|---|
| `createRazorpayOrder` | Callable | Client | Creates Razorpay order for subscriptions |
| `verifyRazorpayPayment` | Callable | Client | Verifies signature, activates subscription |
| `createPDFOrder` | Callable | Client | Creates Razorpay order for PDF purchase |
| `recordPDFPurchase` | Callable | Client | Verifies signature, writes pdf_purchases |
| `razorpayWebhook` | HTTP | Razorpay | Handles payment.captured / failed / cancelled events |
| `expireSubscriptions` | Scheduled | every 24h (IST) | Sweeps expired subscriptions → sets plan='free' |
| `createMember` | Callable | Admin | Creates Firebase Auth user + Firestore doc |
| `deleteMember` | Callable | Admin | Deletes Auth user + Firestore doc |

### Secrets Required

```bash
firebase functions:secrets:set RAZORPAY_KEY_ID
firebase functions:secrets:set RAZORPAY_KEY_SECRET
firebase functions:secrets:set RAZORPAY_WEBHOOK_SECRET
```

### Deploy

```bash
cd functions && firebase deploy --only functions
```

---

## 9. Admin Panel

`admin.html` is a standalone SPA with session-based auth (no Firebase Auth — credential check is hardcoded).

**Credentials:** `admin@royalfitnessclub.com` / `RFC@Admin2025`

**Session:** `sessionStorage.setItem('rfc_admin_auth', '1')` — cleared on browser close.

### Tab Structure

| Tab | Key Features |
|---|---|
| **Dashboard** | Stat cards (members, pro, pending payouts, referrals, subscribers, active); recent members; pending redemptions; activity feed |
| **Members** | Search/filter table; add/edit/suspend/delete members; plan badges |
| **Code Gen** | Generate 10 access codes per plan type; expiry control; code status table |
| **Redemptions** | UPI payout requests from user wallets; approve/reject (syncs back to user wallet localStorage) |
| **Referrals** | Referral tracking from user-side `rfc_referrals_*` keys; mark credited; referral leaderboard |
| **Newsletter** | Subscriber list merged from admin + main site (`rfc_newsletter`); CSV export; add/remove |
| **Features** | CRUD for homepage feature/USP cards (emoji, title, description, order) |
| **Blogs** | CRUD blog posts (title, category, author, read time, cover image, excerpt, full content, status) |
| **Pricing** | CRUD pricing plans (name, price, duration, badge, feature list, highlight flag) |
| **FAQs** | CRUD FAQs (question, answer, category, order); reset-to-defaults danger zone |
| **Challenges** | CRUD fitness challenges (status, entry fee, dates, prizes, rules, gradient); participant + revenue stats |
| **Courses** | CRUD certification courses (modules, PDF URLs, banner, pricing); PDF material manager |

### Admin → Main Site Data Sync

When admin saves challenges or courses, changes are written to two keys simultaneously:
- `rfc_adm_challenges_adm` / `rfc_adm_courses_adm` — admin panel's own store
- `rfc_challenges` / `rfc_courses` — keys that `index.html` reads directly

This means changes appear on the main site **instantly** (same browser session) without any server roundtrip.

---

## 10. Feature Catalogue

### Member-Facing Features

| Feature | Section | Auth Required | Pro Required |
|---|---|---|---|
| Beast Score Calculator | `#calculator` | Yes | No |
| TDEE / BMR / Macro Calculator | `#calculator` | Yes | No |
| AI Meal Planner (formula-based) | `#mealplan` | Yes | No |
| 12-Week Roadmap | `#roadmap` | No | No |
| Body Fat Calculator | `#bodyfat` | No | No |
| BMR / Water / Ideal Weight | `#calculators` | No | No |
| Physio Assessment | `#physio` | Yes | No |
| Transformation Dashboard | `#dashboard` | Yes | No |
| Workout + Habit Tracker | `#tracker` | Yes | No |
| Workout History Log | `#workoutlog` | Yes | No |
| Tiger Leaderboard | `#arena` | No (read) | No |
| Wallet & Referrals | Profile | Yes | No |
| **Blood Report Diagnosis** | `#bloodreport` | No | No |
| **Fitness Challenges** | `#challenges` | Yes (to join) | No |
| **Certification Courses** | `#courses` | Yes (to buy) | No |
| PDF Guides Store | `#store` | Yes | No |
| Bundle Deals | `#store` | Yes | No |

### Engagement / Monetisation Mechanics

| Mechanic | Trigger | Value |
|---|---|---|
| Daily Login Bonus | First login each calendar day | ₹20 wallet credit |
| Referral Credit | New user purchases Pro with your code | ₹100 to referrer |
| Referral Signup Bonus | New user who used a referral code | ₹50 wallet credit |
| Challenge Join Bonus | Any challenge entry fee paid | ₹50 wallet credit |
| Wallet Redemption | Balance ≥ ₹500 | UPI payout (admin approval) |
| Tiger Leaderboard | Monthly competition | ₹8k / ₹4.5k / ₹2.5k supplements |

### Tiger Score Formula

```
TigerScore = (streak × 10) + (workouts × 5) + (checkins × 8) + (referrals × 50) + (photos × 20)
```

Daily shuffle (fairness factor):
```javascript
shuffle = Math.abs(Math.sin(dayNum * 1.618 + rank * 2.718) * 8) | 0
```

---

## 11. Security Model

### Firestore Rules Summary

| Collection | Read | Write |
|---|---|---|
| `codes` | Public | Admin (create/delete); Auth user (mark used) |
| `users/{uid}` | Self only | Self (restricted fields); Admin (all) |
| `subscriptions` | Owner | Owner (cancel only); Admin |
| `measurements`, `progress_logs`, `activity`, `physio_*` | Owner | Owner |
| `pdf_purchases/{uid}` | Owner | Admin / Cloud Functions |
| `pdf_catalog` | Auth users | Admin |
| `leaderboard` | Auth users | Owner |
| `announcements` | Auth users | Admin |
| `payment_orders` | Owner | Admin / Cloud Functions |
| `global_analytics` | Admin | Any auth user |
| `ai_rate_limits` | Owner | Cloud Functions only |

### Client-Side Security

- Firebase client config values (API key, project ID) are **safe to commit** — Firebase security is enforced by Firestore Rules and Auth restrictions, not config secrecy
- Razorpay Key ID (`rzp_live_SzivmCT3vTvTAK`) is public — safe in JS
- Key Secret and Webhook Secret are **never** in client code
- Admin panel uses hardcoded credential check (not Firebase Auth) — suitable for single-admin setup; for multi-admin, migrate to Firebase custom claims

### Firebase Hosting Headers

All responses include:
```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Cache-Control: max-age=86400  (JS/CSS assets)
```

### Storage Rules

Progress photos: owner read/write only, max 5 MB, images only. Everything else denied.

---

## 12. PWA & Offline

### Service Worker (`sw.js`)

- Cache name: `rfc-v2`
- **Install**: pre-caches `index.html`, `admin.html`, `404.html`, `manifest.json`, icons
- **Activate**: cleans up old cache versions
- **Fetch**: cache-first for same-origin GET requests; skips Firebase/Razorpay/Google API calls

### Manifest (`manifest.json`)

- `display: standalone` — full-screen app experience
- Theme color: `#e8001d` (RFC red)
- Background: `#070707` (near-black)
- 8 icon sizes (72px → 512px)
- 3 shortcuts: AI Meal Planner, Beast Score, Knowledge Store

### PWA Install

Works on Chrome (Android/Desktop), Safari (iOS 16.4+). Users can "Add to Home Screen" for native-like experience.

---

## 13. Deployment

### Firebase Hosting

```bash
# Deploy hosting only
firebase deploy --only hosting

# Deploy everything
firebase deploy

# Deploy functions only
cd functions && firebase deploy --only functions
```

### What Gets Deployed

The `firebase.json` `ignore` list excludes: Python scripts, `src/`, `scripts/`, `functions/`, `README.md`, `generated_pdfs/`, `posters/`, hidden files.

**Deployed:** `index.html`, `admin.html`, `404.html`, `sw.js`, `manifest.json`, `icons/`

### Hosting URL

`https://royal-fitness-club-7adc1.web.app` (primary)
`https://royalfitnessclub.in` (custom domain, if configured)

### Clean URL Rewrite

`/admin` → `admin.html` (via `firebase.json` rewrite rule)

---

## 14. Secrets & Environment Variables

| Secret | Location | Use |
|---|---|---|
| `RAZORPAY_KEY_SECRET` | Firebase Secret Manager | Server-side HMAC-SHA256 signature verification |
| `RAZORPAY_WEBHOOK_SECRET` | Firebase Secret Manager | Webhook request verification |
| `RAZORPAY_KEY_ID` | Firebase Secret Manager | Returned to client from Cloud Function (not hardcoded in Functions, uses live key) |

### Setting Secrets

```bash
firebase functions:secrets:set RAZORPAY_KEY_SECRET
# Prompts for value — obtain from Razorpay Dashboard → Settings → API Keys

firebase functions:secrets:set RAZORPAY_WEBHOOK_SECRET
# Prompts for value — obtain from Razorpay Dashboard → Webhooks → Secret
```

### What Is Safe to Commit

| Value | Safe? | Reason |
|---|---|---|
| Firebase config (apiKey, projectId, etc.) | ✅ Yes | Protected by Firestore Rules, not secret |
| Razorpay Key ID `rzp_live_SzivmCT3vTvTAK` | ✅ Yes | Public key — identifies merchant only |
| Razorpay Key Secret | ❌ Never | Signs requests — exposure = full payment forgery |
| Webhook Secret | ❌ Never | Verifies Razorpay webhooks |
| Admin credentials in admin.html | ⚠️ Dev only | Should move to env var or Firebase custom claims for production |

---

## 15. Key Constants & IDs

| Constant | Value | Location |
|---|---|---|
| Firebase Project ID | `royal-fitness-club-7adc1` | `.firebaserc`, `firebase.json` |
| Firebase App ID | `1:116269953135:web:e9c815a1e62788fbd05d9a` | `firebase.js` |
| Razorpay Live Key ID | `rzp_live_SzivmCT3vTvTAK` | `index.html` (JS) |
| Admin Email | `admin@royalfitnessclub.com` | `admin.html` (JS) |
| Admin Password | `RFC@Admin2025` | `admin.html` (JS) |
| Plan: Pro Monthly | `royal_pro` / ₹499 | `functions/index.js` |
| Plan: Elite | `royal_elite` / ₹1,999 | `functions/index.js` |
| PDF: Anabolic Guide | `anabolic_full_guide` / ₹299 | `functions/index.js` |
| PDF: Fitness & Mindset | `fitness_mindset` / ₹299 | `functions/index.js` |
| PWA Cache Version | `rfc-v2` | `sw.js` |
| localStorage Namespace | `rfc_` / `rfc_adm_` | `index.html`, `admin.html` |

---

## 16. Data-Flow Diagrams

### User Login → Full App State

```
Firebase Auth ──onAuthStateChanged──► applyUser()
                                          │
                              ┌───────────┼───────────────┐
                              ▼           ▼               ▼
                    Firestore         localStorage     DOM Updates
                  /users/{uid}     rfc_wallet_{uid}   profile card
                   plan, expiry    rfc_refcode_{uid}  wallet balance
                   gymMember       rfc_lb_date_{uid}  referral code
                                                       nav user pill
                                                       leaderboard rank
```

### Blood Report Diagnosis Flow

```
User Input (upload/manual)
         │
         ▼
  brRunAnalysis(vals, gender)
         │
    2.8s animation
         │
         ▼
  BLOOD_MARKERS.forEach()
    ├─ brGetStatus(id, val, gender) → 'ok'|'low'|'high'|'warn'
    ├─ Calculate deviation from midpoint → health score contribution
    └─ Render color-coded marker card
         │
         ▼
  Generate recommendations from BLOOD_RECS map
  (keyed by markerId_status, e.g. 'vitd_low', 'testo_low')
         │
         ▼
  Health Score 0–100
  + Save to rfc_blood_reports_{uid} (localStorage, last 10)
```

### Admin → Main Site Sync (Challenges / Courses)

```
Admin edits challenge/course
         │
         ▼
  saveChallenge() / saveCourse()
         │
    ┌────┴────┐
    ▼         ▼
rfc_adm_    rfc_challenges /    ← same localStorage, different key
challenges_adm  rfc_courses
(admin store)  (main site reads)
                     │
                     ▼
             index.html getChallenges()
             reads rfc_challenges
             falls back to DEFAULT_CHALLENGES
```

### Razorpay Payment (Production Path)

```
index.html                functions/index.js           Razorpay
    │                           │                          │
    ├─ createRazorpayOrder ────►│                          │
    │                           ├─ orders.create() ───────►│
    │◄──── { orderId } ─────────┤◄──── { id } ─────────────┤
    │                           │                          │
    ├─ Razorpay checkout popup ─────────────────────────►  │
    │◄──── paymentId + signature ──────────────────────── │
    │                           │                          │
    ├─ verifyRazorpayPayment ──►│                          │
    │                           ├─ HMAC verify             │
    │                           ├─ Write Firestore          │
    │◄──── { success } ─────────┤                          │
    │                           │                          │
    │         (async)           │◄── webhook: payment.captured
    │                           ├─ Double-write safety      │
    │                           └─ Update user plan        │
```

---

*Last updated: June 2026 · Branch: `claude/royal-fitness-saas-refactor-87s2ul`*
