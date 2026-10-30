const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({
    executablePath: '/home/isyarharun/.cache/ms-playwright/chromium_headless_shell-1228/chrome-headless-shell-linux64/chrome-headless-shell',
  });
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
  await page.goto('http://127.0.0.1:8080/scripts/og.html', { waitUntil: 'networkidle' });
  await page.waitForTimeout(500);
  await page.screenshot({ path: '/home/isyarharun/Documents/projects/kaloriku-web/assets/img/og.jpg', type: 'jpeg', quality: 90 });
  console.log('og.jpg written');
  await browser.close();
})();
