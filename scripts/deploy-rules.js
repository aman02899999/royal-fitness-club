// Deploy Firestore rules via the Firebase Rules REST API using the service account
const fs = require('fs');
const path = require('path');
const { GoogleAuth } = require(path.join('/home/user/royal-fitness-club/functions/node_modules', 'google-auth-library'));

const PROJECT = 'royal-fitness-club-7adc1';
const RULES_FILE = '/home/user/royal-fitness-club/firestore.rules';

async function main() {
  const auth = new GoogleAuth({
    keyFile: process.env.GOOGLE_APPLICATION_CREDENTIALS,
    scopes: ['https://www.googleapis.com/auth/cloud-platform', 'https://www.googleapis.com/auth/firebase'],
  });
  const client = await auth.getClient();
  const token = (await client.getAccessToken()).token;
  const base = `https://firebaserules.googleapis.com/v1/projects/${PROJECT}`;
  const headers = { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' };

  const source = fs.readFileSync(RULES_FILE, 'utf8');

  // 1. Create a new ruleset (this also validates/compiles the rules)
  let res = await fetch(`${base}/rulesets`, {
    method: 'POST',
    headers,
    body: JSON.stringify({ source: { files: [{ name: 'firestore.rules', content: source }] } }),
  });
  if (!res.ok) { console.error('Ruleset create failed:', res.status, await res.text()); process.exit(1); }
  const ruleset = await res.json();
  console.log('Ruleset created:', ruleset.name);

  // 2. Point the cloud.firestore release at the new ruleset
  const releaseName = `projects/${PROJECT}/releases/cloud.firestore`;
  res = await fetch(`${base}/releases/cloud.firestore`, {
    method: 'PATCH',
    headers,
    body: JSON.stringify({ release: { name: releaseName, rulesetName: ruleset.name } }),
  });
  if (res.status === 404) {
    // No release yet — create one
    res = await fetch(`${base}/releases`, {
      method: 'POST',
      headers,
      body: JSON.stringify({ name: releaseName, rulesetName: ruleset.name }),
    });
  }
  if (!res.ok) { console.error('Release update failed:', res.status, await res.text()); process.exit(1); }
  console.log('Firestore rules deployed:', (await res.json()).name);
}

main().catch((e) => { console.error(e); process.exit(1); });
