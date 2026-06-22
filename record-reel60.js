const puppeteer = require('/opt/node22/lib/node_modules/puppeteer');
const path = require('path');
const fs = require('fs');

const CHROME = '/root/.cache/puppeteer/chrome/linux-149.0.7827.22/chrome-linux64/chrome';
const REEL_HTML = 'file://' + path.resolve(__dirname, 'reel60.html');
const FRAMES_DIR = path.resolve(__dirname, 'reel60-frames');
const FPS = 30;
const DURATION_MS = 60000;
const TOTAL_FRAMES = FPS * (DURATION_MS / 1000); // 1800
const WIDTH = 1080;
const HEIGHT = 1920;

async function main() {
  if (!fs.existsSync(FRAMES_DIR)) fs.mkdirSync(FRAMES_DIR, { recursive: true });

  console.log(`Launching browser...`);
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: true,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-gpu',
      '--window-size=' + WIDTH + ',' + HEIGHT,
    ],
  });

  const page = await browser.newPage();
  await page.setViewport({ width: WIDTH, height: HEIGHT, deviceScaleFactor: 1 });

  console.log(`Loading reel...`);
  await page.goto(REEL_HTML, { waitUntil: 'networkidle0', timeout: 45000 });
  await page.waitForFunction(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 2000));

  console.log(`Capturing ${TOTAL_FRAMES} frames at ${FPS}fps (${DURATION_MS/1000}s)...`);

  for (let i = 0; i < TOTAL_FRAMES; i++) {
    const timeMs = Math.round((i / FPS) * 1000);
    const delayVal = -timeMs + 'ms';

    await page.evaluate((t) => {
      document.documentElement.style.setProperty('--t', t);
    }, delayVal);

    if (i === 0) await new Promise(r => setTimeout(r, 100));

    const framePath = path.join(FRAMES_DIR, 'f' + String(i + 1).padStart(4, '0') + '.png');
    await page.screenshot({ path: framePath, type: 'png' });

    if (i % 60 === 0) {
      const sec = (timeMs / 1000).toFixed(1);
      process.stdout.write(`  Frame ${i + 1}/${TOTAL_FRAMES} (t=${sec}s)\n`);
    }
  }

  await browser.close();
  console.log(`\nDone! ${TOTAL_FRAMES} frames saved to ${FRAMES_DIR}`);
}

main().catch(err => { console.error(err); process.exit(1); });
