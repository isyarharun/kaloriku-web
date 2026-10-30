const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({
    executablePath: '/home/isyarharun/.cache/ms-playwright/chromium_headless_shell-1228/chrome-headless-shell-linux64/chrome-headless-shell',
  });
  const shots = [
    { name: 'desktop-hero', url: 'http://127.0.0.1:8080/', w: 1440, h: 900, full: false },
    { name: 'desktop-full', url: 'http://127.0.0.1:8080/', w: 1440, h: 900, full: true },
    { name: 'mobile-full', url: 'http://127.0.0.1:8080/', w: 390, h: 844, full: true },
    { name: 'en-hero', url: 'http://127.0.0.1:8080/en/', w: 1440, h: 900, full: false },
  ];
  for (const s of shots) {
    const page = await browser.newPage({ viewport: { width: s.w, height: s.h }, deviceScaleFactor: 1 });
    await page.emulateMedia({ reducedMotion: 'reduce' });
    page.on('response', (r) => { if (r.status() >= 400) console.log('HTTP', r.status(), r.url()); });
    page.on('pageerror', (e) => console.log('JS ERROR', e.message));
    await page.goto(s.url, { waitUntil: 'networkidle' });
    await page.waitForTimeout(400);
    await page.evaluate(async () => {
      const step = window.innerHeight * 0.8;
      for (let y = 0; y < document.body.scrollHeight; y += step) {
        window.scrollTo(0, y);
        await new Promise((r) => setTimeout(r, 60));
      }
      window.scrollTo(0, 0);
    });
    await page.waitForTimeout(300);
    await page.screenshot({ path: `/tmp/${s.name}.png`, fullPage: s.full });
    if (!s.full) {
      const h = await page.evaluate(() => document.documentElement.scrollHeight);
      console.log(s.name, 'page height', h);
    }
    await page.close();
  }
  await browser.close();
})();
