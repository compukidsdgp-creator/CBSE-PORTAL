/* CBSEMock — small "follow us" card
   Slides in at the bottom-left once a visitor has shown some interest
   (scrolled 40% of the page, or stayed 30 seconds). It never covers the page,
   has a close button, and stays away for 14 days after it is closed
   (30 days after a follow button is tapped).
   Add ?follow=preview to any page address to see it at once.
   LIVE = false  -> only shows with ?follow=preview (owner's preview).
   LIVE = true   -> shows to every visitor by the rules above. */
(function () {
  var LIVE = false;
  var KEY = 'cbsemock_follow_card_until';
  var preview = /[?&]follow=preview\b/.test(location.search);
  function snoozed() {
    try { return Date.now() < Number(localStorage.getItem(KEY) || 0); } catch (e) { return false; }
  }
  function snooze(days) {
    try { localStorage.setItem(KEY, String(Date.now() + days * 864e5)); } catch (e) {}
  }
  if (!preview && (!LIVE || snoozed())) return;

  var LINKS = [
    { name: 'Telegram', sub: 'Every new paper, instantly', href: 'https://t.me/cbsemockportal', bg: '#229ED9',
      icon: 'M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.894 8.221-1.97 9.28c-.145.658-.537.818-1.084.508l-3-2.21-1.447 1.394c-.16.16-.295.295-.605.295l.213-3.053 5.56-5.023c.242-.213-.054-.333-.373-.12L7.178 13.4l-2.95-.924c-.64-.203-.658-.64.136-.954l11.566-4.458c.538-.196 1.006.128.832.941z' },
    { name: 'Instagram', sub: 'Formula reels & tips', href: 'https://www.instagram.com/cbsemock/',
      bg: 'linear-gradient(45deg,#f09433,#e6683c 25%,#dc2743 50%,#cc2366 75%,#bc1888)',
      icon: 'M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z' },
    { name: 'Facebook', sub: 'News & daily posts', href: 'https://www.facebook.com/profile.php?id=61596243964780', bg: '#1877f2',
      icon: 'M24 12.073C24 5.41 18.627 0 12 0S0 5.41 0 12.073C0 18.1 4.388 23.094 10.125 24v-8.437H7.078v-3.49h3.047V9.41c0-3.025 1.792-4.697 4.533-4.697 1.312 0 2.686.235 2.686.235v2.97h-1.514c-1.491 0-1.956.93-1.956 1.886v2.269h3.328l-.532 3.49h-2.796V24C19.612 23.094 24 18.1 24 12.073z' }
  ];

  var css =
    '#cmFollow{position:fixed;left:16px;bottom:88px;z-index:99990;width:292px;max-width:calc(100vw - 96px);' +
    'background:#0f2347;color:#fff;border:1px solid rgba(232,204,106,.55);border-radius:16px;padding:14px 14px 12px;' +
    'box-shadow:0 14px 34px rgba(0,0,0,.32);font-family:Inter,system-ui,Arial,sans-serif;' +
    'transform:translateY(24px);opacity:0;pointer-events:none;transition:transform .35s ease,opacity .35s ease}' +
    '#cmFollow.on{transform:none;opacity:1;pointer-events:auto}' +
    '#cmFollow h4{margin:0 26px 2px 0;font-size:.95rem;font-weight:700;color:#e8cc6a;line-height:1.25}' +
    '#cmFollow p{margin:0 0 10px;font-size:.76rem;color:rgba(255,255,255,.78);line-height:1.4}' +
    '#cmFollow .cmx{position:absolute;top:6px;right:6px;width:30px;height:30px;border:0;border-radius:50%;background:rgba(255,255,255,.1);' +
    'color:#fff;font-size:18px;line-height:1;cursor:pointer}#cmFollow .cmx:hover{background:rgba(255,255,255,.22)}' +
    '#cmFollow a{display:flex;align-items:center;gap:10px;text-decoration:none;color:#fff;border-radius:11px;padding:8px 11px;margin-top:7px}' +
    '#cmFollow a:hover{filter:brightness(1.08)}#cmFollow a b{display:block;font-size:.84rem;line-height:1.2}' +
    '#cmFollow a span{display:block;font-size:.7rem;opacity:.9;line-height:1.25}#cmFollow svg{flex:none}' +
    '@media(max-width:480px){#cmFollow{left:10px;bottom:86px;padding:12px 12px 10px}#cmFollow p{margin-bottom:4px}' +
    '#cmFollow .cml{display:flex;gap:6px}#cmFollow a{flex:1;flex-direction:column;gap:4px;padding:9px 4px;text-align:center}' +
    '#cmFollow a span{display:none}#cmFollow a b{font-size:.74rem}}' +
    '@media(prefers-reduced-motion:reduce){#cmFollow{transition:none}}' +
    '@media print{#cmFollow{display:none}}';

  var shown = false, card;
  function close(days) {
    if (!card) return;
    card.classList.remove('on');
    if (!preview) snooze(days);
    setTimeout(function () { if (card && card.parentNode) card.parentNode.removeChild(card); card = null; }, 400);
  }
  function show() {
    if (shown) return; shown = true;
    window.removeEventListener('scroll', onScroll);
    var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
    card = document.createElement('aside');
    card.id = 'cmFollow'; card.setAttribute('aria-label', 'Follow CBSEMock');
    var h = '<button class="cmx" type="button" aria-label="Close">&times;</button>' +
            '<h4>Never miss a free paper</h4><p>New mock papers every Mon, Wed &amp; Fri. Follow us to get them first.</p><div class="cml">';
    LINKS.forEach(function (l) {
      h += '<a href="' + l.href + '" target="_blank" rel="noopener" style="background:' + l.bg + '">' +
           '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="' + l.icon + '"/></svg>' +
           '<div><b>' + l.name + '</b><span>' + l.sub + '</span></div></a>';
    });
    card.innerHTML = h + '</div>';
    document.body.appendChild(card);
    card.querySelector('.cmx').addEventListener('click', function () { close(14); });
    Array.prototype.forEach.call(card.querySelectorAll('a'), function (a) {
      a.addEventListener('click', function () {
        if (window.gtag) { try { gtag('event', 'follow_card_click', { network: a.querySelector('b').textContent }); } catch (e) {} }
        close(30);
      });
    });
    document.addEventListener('keydown', function esc(e) {
      if (e.key === 'Escape') { close(14); document.removeEventListener('keydown', esc); }
    });
    requestAnimationFrame(function () { requestAnimationFrame(function () { card.classList.add('on'); }); });
  }
  function onScroll() {
    var doc = document.documentElement;
    var max = doc.scrollHeight - window.innerHeight;
    if (max > 0 && window.scrollY / max >= 0.4) show();
  }
  function start() {
    if (preview) { show(); return; }
    window.addEventListener('scroll', onScroll, { passive: true });
    setTimeout(show, 30000);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
