const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({
    executablePath: '/home/isyarharun/.cache/ms-playwright/chromium_headless_shell-1228/chrome-headless-shell-linux64/chrome-headless-shell',
  });
  for (const url of ['http://127.0.0.1:8080/', 'http://127.0.0.1:8080/en/']) {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    await page.goto(url, { waitUntil: 'networkidle' });
    const m = await page.evaluate(() => {
      const res = performance.getEntriesByType('resource');
      const byType = {};
      let total = 0;
      for (const r of res) {
        const size = r.transferSize || 0;
        total += size;
        const t = r.initiatorType;
        byType[t] = (byType[t] || 0) + size;
      }
      return {
        requests: res.length,
        totalKB: Math.round(total / 1024),
        byTypeKB: Object.fromEntries(Object.entries(byType).map(([k, v]) => [k, Math.round(v / 1024)])),
        h1: document.querySelectorAll('h1').length,
        imgs: [...document.images].length,
        imgsNoAlt: [...document.images].filter((i) => !i.hasAttribute('alt')).length,
        title: document.title,
        lang: document.documentElement.lang,
        height: document.documentElement.scrollHeight,
      };
    });
    console.log(url, JSON.stringify(m));
    await page.close();
  }
  await browser.close();
})();
