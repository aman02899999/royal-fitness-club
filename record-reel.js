const puppeteer = require('/opt/node22/lib/node_modules/puppeteer');
const path = require('path');
const fs = require('fs');

const CHROME = '/root/.cache/puppeteer/chrome/linux-149.0.7827.22/chrome-linux64/chrome';
const REEL_HTML = 'file://' + path.resolve(__dirname, 'reel.html');
const FRAMES_DIR = path.resolve(__dirname, 'reel-frames');
const FPS = 30;
const DURATION_MS = 20000;
const TOTAL_FRAMES = FPS * (DURATION_MS / 1000); // 600
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
  await page.goto(REEL_HTML, { waitUntil: 'networkidle0', timeout: 30000 });

  // Wait for fonts to load
  await page.waitForFunction(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 2000));

  console.log(`Capturing ${TOTAL_FRAMES} frames at ${FPS}fps...`);

  for (let i = 0; i < TOTAL_FRAMES; i++) {
    const timeMs = Math.round((i / FPS) * 1000);
    const delayVal = -timeMs + 'ms';

    await page.evaluate((t) => {
      document.documentElement.style.setProperty('--t', t);
    }, delayVal);

    // Small settle time for first frame
    if (i === 0) await new Promise(r => setTimeout(r, 100));

    const framePath = path.join(FRAMES_DIR, 'f' + String(i + 1).padStart(4, '0') + '.png');
    await page.screenshot({ path: framePath, type: 'png' });

    if (i % 30 === 0) {
      process.stdout.write(`  Frame ${i + 1}/${TOTAL_FRAMES} (t=${timeMs}ms)\n`);
    }
  }

  await browser.close();
  console.log(`\nDone! ${TOTAL_FRAMES} frames saved to ${FRAMES_DIR}`);
  console.log(`\nRun ffmpeg to stitch:`);
  console.log(`ffmpeg -r 30 -i reel-frames/f%04d.png -vcodec libx264 -pix_fmt yuv420p -crf 18 -movflags +faststart reel.mp4`);
}

main().catch(err => { console.error(err); process.exit(1); });
