# Deployment Scripts

These scripts deploy Firebase resources directly via REST APIs, bypassing the Firebase CLI
permission requirements. Use them when the service account lacks `serviceusage.googleapis.com`
access (standard Firebase service accounts).

## Prerequisites

Set the service account key path:
```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/sa-key.json
```

Install dependencies (uses functions/node_modules):
```bash
cd functions && npm ci
```

## Scripts

### deploy-rules.js — Deploy Firestore security rules
```bash
node scripts/deploy-rules.js
```
Deploys `firestore.rules` to the `cloud.firestore` release.

### deploy-extras.js — Deploy Storage rules + Firestore indexes
```bash
node scripts/deploy-extras.js
```
Deploys `storage.rules` and all indexes in `firestore.indexes.json`.

## When to use

Run these manually after the GitHub Actions deploy if storage rules or Firestore indexes
fail to deploy due to service account permissions. The main workflow handles hosting,
Firestore rules, and Functions automatically.
