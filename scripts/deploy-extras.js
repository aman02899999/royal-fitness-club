// Deploy Storage rules + Firestore indexes via REST APIs using the service account
const fs = require('fs');
const path = require('path');
const { GoogleAuth } = require(path.join('/home/user/royal-fitness-club/functions/node_modules', 'google-auth-library'));

const PROJECT = 'royal-fitness-club-7adc1';
const BUCKET = 'royal-fitness-club-7adc1.firebasestorage.app';

async function main() {
  const auth = new GoogleAuth({
    keyFile: process.env.GOOGLE_APPLICATION_CREDENTIALS,
    scopes: ['https://www.googleapis.com/auth/cloud-platform', 'https://www.googleapis.com/auth/firebase'],
  });
  const client = await auth.getClient();
  const token = (await client.getAccessToken()).token;
  const headers = { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' };

  // --- Storage rules ---
  const rulesBase = `https://firebaserules.googleapis.com/v1/projects/${PROJECT}`;
  const storageSource = fs.readFileSync('/home/user/royal-fitness-club/storage.rules', 'utf8');
  let res = await fetch(`${rulesBase}/rulesets`, {
    method: 'POST', headers,
    body: JSON.stringify({ source: { files: [{ name: 'storage.rules', content: storageSource }] } }),
  });
  if (!res.ok) {
    console.error('Storage ruleset create failed:', res.status, await res.text());
  } else {
    const ruleset = await res.json();
    const relId = `firebase.storage/${BUCKET}`;
    const releaseName = `projects/${PROJECT}/releases/${relId}`;
    res = await fetch(`${rulesBase}/releases/${encodeURIComponent(relId)}`, {
      method: 'PATCH', headers,
      body: JSON.stringify({ release: { name: releaseName, rulesetName: ruleset.name } }),
    });
    if (res.status === 404) {
      res = await fetch(`${rulesBase}/releases`, {
        method: 'POST', headers,
        body: JSON.stringify({ name: releaseName, rulesetName: ruleset.name }),
      });
    }
    if (!res.ok) console.error('Storage release failed:', res.status, await res.text());
    else console.log('Storage rules deployed:', (await res.json()).name);
  }

  // --- Firestore indexes ---
  const indexes = JSON.parse(fs.readFileSync('/home/user/royal-fitness-club/firestore.indexes.json', 'utf8')).indexes;
  for (const idx of indexes) {
    const url = `https://firestore.googleapis.com/v1/projects/${PROJECT}/databases/(default)/collectionGroups/${idx.collectionGroup}/indexes`;
    const body = {
      queryScope: idx.queryScope,
      fields: idx.fields.map(f => ({ fieldPath: f.fieldPath, order: f.order })),
    };
    res = await fetch(url, { method: 'POST', headers, body: JSON.stringify(body) });
    const txt = await res.text();
    if (res.ok) console.log(`Index created on ${idx.collectionGroup}:`, idx.fields.map(f => f.fieldPath).join(','));
    else if (res.status === 409) console.log(`Index already exists on ${idx.collectionGroup}:`, idx.fields.map(f => f.fieldPath).join(','));
    else console.error(`Index failed (${res.status}) on ${idx.collectionGroup}:`, txt.slice(0, 300));
  }
}

main().catch((e) => { console.error(e); process.exit(1); });
