// Export the deck to a 1920x1080 PDF, one slide per page, links kept clickable.
// Usage: node tools/export-pdf.js [url] [out.pdf]
// Serve the repo first, e.g. `python3 -m http.server 8765`.
const { chromium } = require('playwright');

const url = process.argv[2] || 'http://localhost:8765/';
const out = process.argv[3] || 'Breadboarding Workshop 2026.pdf';

(async () => {
  const browser = await chromium.launch(
    process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {}
  );
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));

  await page.goto(url, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.emulateMedia({ media: 'print' });
  await page.pdf({
    path: out,
    width: '1920px',
    height: '1080px',
    printBackground: true,
    margin: { top: 0, right: 0, bottom: 0, left: 0 },
  });
  await browser.close();

  if (errors.length) {
    console.error('Page errors:\n' + errors.join('\n'));
    process.exitCode = 1;
  }
  console.log('Wrote ' + out);
})();
