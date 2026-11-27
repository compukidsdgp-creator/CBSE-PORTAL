/* CBSEMock — floating share buttons (WhatsApp + Facebook) + a YouTube subscribe button, same look as the share-fab on the mock-paper pages.
   Added to pages by share_tags.py (<script src="/share-fab.js" defer>). Does nothing if the page already has its own
   .share-fab-wrap, is a draft/noindex page, or is printed. */
(function () {
  if (document.querySelector('.share-fab-wrap')) return;
  var robots = document.querySelector('meta[name="robots"]');
  if (robots && /noindex/i.test(robots.content)) return;

  var url = location.href.split('#')[0];
  var title = (document.title || 'CBSEMock').replace(/\s*\|\s*.*$/, '');
  var text = title + ' — free on CBSEMock';
  var WA = 'M16 2C8.28 2 2 8.28 2 16c0 2.44.65 4.73 1.78 6.72L2 30l7.5-1.75A13.94 13.94 0 0016 30c7.72 0 14-6.28 14-14S23.72 2 16 2zm0 25.5a11.44 11.44 0 01-5.84-1.6l-.42-.25-4.45 1.04 1.06-4.33-.28-.45A11.46 11.46 0 014.5 16C4.5 9.6 9.6 4.5 16 4.5S27.5 9.6 27.5 16 22.4 27.5 16 27.5zm6.3-8.56c-.34-.17-2.02-1-2.33-1.11-.32-.11-.55-.17-.78.17-.23.34-.89 1.11-1.09 1.34-.2.23-.4.26-.74.09-.34-.17-1.44-.53-2.74-1.69-1.01-.9-1.7-2.01-1.9-2.35-.2-.34-.02-.52.15-.69.15-.15.34-.4.51-.6.17-.2.23-.34.34-.57.11-.23.06-.43-.03-.6-.09-.17-.78-1.88-1.07-2.57-.28-.67-.57-.58-.78-.59h-.67c-.23 0-.6.09-.91.43-.32.34-1.2 1.17-1.2 2.86s1.23 3.32 1.4 3.55c.17.23 2.42 3.7 5.87 5.19.82.35 1.46.56 1.96.72.82.26 1.57.22 2.16.13.66-.1 2.02-.83 2.31-1.62.28-.8.28-1.48.2-1.62-.09-.14-.32-.23-.66-.4z';
  var FB = 'M29 16C29 8.82 23.18 3 16 3S3 8.82 3 16c0 6.49 4.75 11.87 10.97 12.84V19.7H10.4V16h3.57v-3.1c0-3.52 2.1-5.47 5.31-5.47 1.54 0 3.14.28 3.14.28v3.46h-1.77c-1.74 0-2.28 1.08-2.28 2.19V16h3.89l-.62 3.7h-3.27v9.14C24.25 27.87 29 22.49 29 16z';

  var YT = 'M31.33 8.25a4.02 4.02 0 0 0-2.83-2.85C26.01 4.73 16 4.73 16 4.73s-10.01 0-12.5.67a4.02 4.02 0 0 0-2.83 2.85C0 10.76 0 16 0 16s0 5.24.67 7.75a4.02 4.02 0 0 0 2.83 2.85c2.49.67 12.5.67 12.5.67s10.01 0 12.5-.67a4.02 4.02 0 0 0 2.83-2.85C32 21.24 32 16 32 16s0-5.24-.67-7.75zM12.73 20.76V11.24L21.09 16l-8.36 4.76z';
  var css =
    '.share-fab-wrap{position:fixed;bottom:28px;right:16px;z-index:1000;display:flex;flex-direction:column;gap:10px;align-items:center}' +
    '.share-fab{position:relative;display:flex;align-items:center;justify-content:center;width:48px;height:48px;border-radius:50%;border:none;' +
    'cursor:pointer;text-decoration:none;box-shadow:0 4px 14px rgba(0,0,0,.35);transition:transform .18s,box-shadow .18s}' +
    '.share-fab:hover{transform:scale(1.12);box-shadow:0 6px 20px rgba(0,0,0,.45)}' +
    '.share-fab.wa{background:#25D366}.share-fab.fb{background:#1877F2}.share-fab.yt{background:#FF0000}' +
    '.share-fab .fab-tooltip{position:absolute;right:58px;background:rgba(20,20,40,.85);color:#fff;font:600 .7rem Inter,system-ui,sans-serif;' +
    'white-space:nowrap;padding:4px 9px;border-radius:6px;opacity:0;pointer-events:none;transition:opacity .2s}' +
    '.share-fab:hover .fab-tooltip{opacity:1}' +
    '@media(max-width:767px){.share-fab-wrap{bottom:calc(14px + env(safe-area-inset-bottom,0px));right:10px;gap:8px}' +
    '.share-fab{width:42px;height:42px;opacity:.92}.share-fab .fab-tooltip{display:none}}' +
    '@media print{.share-fab-wrap{display:none!important}}';

  function btn(cls, href, path, label) {
    return '<a class="share-fab ' + cls + '" href="' + href + '" target="_blank" rel="noopener" aria-label="' + label + '">' +
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="24" height="24" fill="#fff" aria-hidden="true"><path d="' + path + '"/></svg>' +
      '<span class="fab-tooltip">' + label + '</span></a>';
  }

  function mount() {
    if (document.querySelector('.share-fab-wrap')) return;
    var st = document.createElement('style');
    st.textContent = css;
    document.head.appendChild(st);
    var w = document.createElement('div');
    w.className = 'share-fab-wrap';
    w.innerHTML =
      btn('wa', 'https://wa.me/?text=' + encodeURIComponent(text + ' ' + url), WA, 'Share on WhatsApp') +
      btn('fb', 'https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(url), FB, 'Share on Facebook') +
      btn('yt', 'https://www.youtube.com/@CBSEMOCK?sub_confirmation=1', YT, 'Subscribe on YouTube');
    w.addEventListener('click', function (e) {
      var a = e.target.closest('a');
      if (!a || !window.gtag) return;
      try {
        if (a.classList.contains('yt')) gtag('event', 'youtube_subscribe_click', { item_id: location.pathname });
        else gtag('event', 'share', { method: a.classList.contains('wa') ? 'whatsapp' : 'facebook', item_id: location.pathname });
      } catch (x) {}
    });
    document.body.appendChild(w);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount); else mount();
})();
