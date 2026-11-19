// Mobile audit for virtual labs: at phone widths, report page-level horizontal overflow, elements that stick
// out of the viewport (outside scrollable containers), tiny text, small tap targets, oversized fixed widths
// and console errors.   node tools/lab_mobile_audit.js <base-url> <out.json> <file>...
const {chromium, devices} = require('playwright');
const fs = require('fs');
const [base, out, ...files] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch();
  const res = [];
  for (const [label, dev] of [['360', {viewport: {width: 360, height: 740}, deviceScaleFactor: 1, isMobile: true, hasTouch: true}], ['390', devices['Pixel 5']]]) {
    const ctx = await b.newContext(dev);
    for (const f of files) {
      const p = await ctx.newPage(); const errs = [];
      p.on('pageerror', e => errs.push(e.message));
      await p.route(/^https?:\/\/(?!127\.0\.0\.1)/, r => r.abort());
      try { await p.goto(base + '/' + encodeURI(f), {timeout: 30000, waitUntil: 'load'}); } catch (e) { errs.push('load: ' + e.message); }
      await p.waitForTimeout(500);
      const r = await p.evaluate(() => {
        const W = innerWidth, doc = document.documentElement.scrollWidth - W;
        const clipped = el => { for (let e = el.parentElement; e && e !== document.body; e = e.parentElement) { const o = getComputedStyle(e).overflowX; if (o === 'auto' || o === 'scroll' || o === 'hidden' || o === 'clip') return true; } return false; };
        const name = el => el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + (typeof el.className === 'string' && el.className.trim() ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '');
        const over = [], small = [], taps = [];
        for (const el of document.body.querySelectorAll('*')) {
          const cs = getComputedStyle(el); if (cs.display === 'none' || cs.visibility === 'hidden' || cs.position === 'fixed') continue;
          const rc = el.getBoundingClientRect(); if (!rc.width || !rc.height) continue;
          if ((rc.right > W + 1 || rc.left < -1) && !clipped(el) && !(el.closest('svg') && el.tagName.toLowerCase() !== 'svg')) over.push(name(el) + ' ' + Math.round(rc.left) + '→' + Math.round(rc.right));
          const fs_ = parseFloat(cs.fontSize);
          if (fs_ < 12 && [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 2) && !el.closest('svg')) small.push(name(el) + ' ' + fs_ + 'px');
          if (el.matches('button,input:not([type=hidden]),select,[role=button],a.btn,.btn,.chip') && (rc.height < 32 || rc.width < 32)) taps.push(name(el) + ' ' + Math.round(rc.width) + 'x' + Math.round(rc.height));
        }
        return {doc, over: [...new Set(over)].slice(0, 8), nOver: over.length, small: [...new Set(small)].slice(0, 5), nSmall: small.length, taps: [...new Set(taps)].slice(0, 5), nTaps: taps.length};
      });
      res.push({file: f, w: label, errs: errs.slice(0, 3), ...r});
      await p.close();
    }
    await ctx.close();
  }
  fs.writeFileSync(out, JSON.stringify(res, null, 1));
  await b.close();
})();
