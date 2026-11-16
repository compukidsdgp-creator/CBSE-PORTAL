// Mobile legibility / tap-target fixer.
// For each page: on a phone viewport, find text under 12px and tap targets under 24px tall, then write
// per-page CSS (inside <!-- MOBILE-FIX:START/END --> in <head>) that lifts exactly those elements.
// A selector is only used when EVERY element it matches on that page needs the fix, so nothing
// that is already larger ever shrinks.   node tools/mobile_fix.js <base-url> <file>...
const {chromium, devices} = require('playwright');
const fs = require('fs');
const [base, ...files] = process.argv.slice(2);
const START = '<!-- MOBILE-FIX:START -->', END = '<!-- MOBILE-FIX:END -->';

(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({...devices['Pixel 5']});
  for (const f of files) {
    let html = fs.readFileSync(f, 'utf8');
    if (html.includes(START)) html = html.slice(0, html.indexOf(START)) + html.slice(html.indexOf(END) + END.length);
    fs.writeFileSync(f, html);                       // audit the page without an old fix
    const p = await ctx.newPage();
    await p.route(/^https?:\/\/(?!127\.0\.0\.1)/, r => r.abort());
    try { await p.goto(base + '/' + encodeURI(f), {timeout: 30000, waitUntil: 'load'}); } catch (e) {}
    await p.waitForTimeout(600);
    const res = await p.evaluate(() => {
      const esc = s => CSS.escape(s);
      const okCls = c => c && !/^(active|open|on|show|hidden|selected|is-|js-)/.test(c) && c.length < 40;
      function sel(el) {                      // short, stable selector: up to 3 levels anchored on id/class
        const parts = [];
        let e = el, depth = 0;
        while (e && e.nodeType === 1 && e !== document.body && depth < 3) {
          let s = e.tagName.toLowerCase();
          if (e.id && !/\d{3,}/.test(e.id)) { parts.unshift('#' + esc(e.id) + (parts.length ? '' : '')); break; }
          const cls = [...e.classList].filter(okCls).slice(0, 2);
          if (cls.length) s += cls.map(c => '.' + esc(c)).join('');
          parts.unshift(s);
          if (cls.length && depth >= 1) break;
          e = e.parentElement; depth++;
        }
        return parts.join(' > ');
      }
      const vis = el => { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
        return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; };
      // small text
      const small = new Map();
      const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      const seen = new Set();
      while (w.nextNode()) {
        const n = w.currentNode; if (!n.textContent.trim()) continue;
        const el = n.parentElement; if (!el || seen.has(el) || el.closest('svg,script,style,noscript')) continue; seen.add(el);
        if (!vis(el)) continue;
        if (parseFloat(getComputedStyle(el).fontSize) < 11.95) { const s = sel(el); if (s) small.set(s, true); }
      }
      const fontSel = [];
      for (const s of small.keys()) {
        let all; try { all = [...document.querySelectorAll(s)]; } catch (e) { continue; }
        if (all.length && all.every(x => !vis(x) || parseFloat(getComputedStyle(x).fontSize) < 11.95)) fontSel.push(s);
      }
      // tap targets (links in running text are exempt, as in Lighthouse)
      const tapMap = new Map();
      document.querySelectorAll('a[href],button,select,input:not([type=hidden]),[role=button]').forEach(el => {
        if (!vis(el) || el.closest('svg')) return;
        const r = el.getBoundingClientRect();
        if (r.height >= 24) return;
        const par = el.parentElement;
        if (par && el.tagName === 'A' && !el.closest('footer,nav,header,.crumb,.breadcrumb') && /^(P|LI|TD|SPAN|EM|SMALL|LABEL|DD)$/.test(par.tagName)) {
          const own = (el.textContent || '').trim().length, all = (par.textContent || '').trim().length;
          if (all > own + 25) return;               // inline link inside a sentence
        }
        let s = sel(el); if (!s) return;
        const need = Math.ceil((24 - r.height) / 2) + 1;
        try {                                   // shared selector also hits big targets → narrow it by href
          const all = [...document.querySelectorAll(s)];
          if (!all.every(x => !vis(x) || x.getBoundingClientRect().height < 24) && el.getAttribute('href'))
            s = s + '[href="' + el.getAttribute('href').replace(/"/g, '\\"') + '"]';
        } catch (e) {}
        tapMap.set(s, Math.max(need, tapMap.get(s) || 0));
      });
      const tapSel = [];
      for (const [s, need] of tapMap) {
        let all; try { all = [...document.querySelectorAll(s)]; } catch (e) { continue; }
        if (all.every(x => !vis(x) || x.getBoundingClientRect().height < 24)) tapSel.push([s, Math.min(need, 8)]);
      }
      return {fontSel, tapSel};
    });
    await p.close();
    if (!res.fontSel.length && !res.tapSel.length) { console.log('clean', f); continue; }
    let css = '@media (max-width:768px){';
    if (res.fontSel.length) css += res.fontSel.map(s => 'html body ' + s).join(',') + '{font-size:12px!important;}';
    const byPad = {};
    for (const [s, n] of res.tapSel) (byPad[n] = byPad[n] || []).push('html body ' + s);
    for (const n in byPad) css += byPad[n].join(',') + `{padding-top:${n}px!important;padding-bottom:${n}px!important;}`;
    css += '}';
    const block = `${START}<style id="mobile-fix">${css}</style>${END}`;
    html = fs.readFileSync(f, 'utf8');
    const i = html.search(/<\/head>/i);
    html = html.slice(0, i) + block + '\n' + html.slice(i);
    fs.writeFileSync(f, html);
    console.log('fixed', f, res.fontSel.length, 'text rules,', res.tapSel.length, 'tap rules');
  }
  await b.close();
})();
