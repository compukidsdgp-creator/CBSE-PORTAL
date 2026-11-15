/**
 * CBSEMock.org.in — Ad blocks (vendor / direct-sponsor banners)
 * ==============================================================
 * Settings live in ads-config.json and are edited from the admin panel
 * (https://cbsemock.org.in/admin/). Do not edit slot data here.
 *
 *  • A slot with  active: true  and an image shows the sponsor's banner.
 *  • An empty slot shows a "Your ad here" box ONLY when  show_placeholders  is true.
 *    With it false (the default) every empty box — including the hard-coded
 *    "ADVERTISEMENT · RESERVED SPACE" boxes in the labs — is hidden and the
 *    layout closes up. Keep it false while the site is under AdSense review.
 *
 * Slot sizes: leaderboard 728×90 · sidebar 300×75 · inline 580×90
 */
(function () {
  var SCRIPT = document.currentScript ? document.currentScript.src : new URL('ads.js', location.href).href;
  var CONFIG_URL = new URL('ads-config.json', SCRIPT).href;
  var SLOT_FOR_ID = {
    'ad-leader-top': 'leaderboard_top', 'ad-leader-bottom': 'leaderboard_bottom',
    'ad-left-1': 'sidebar_left_1', 'ad-left-2': 'sidebar_left_2', 'ad-left-3': 'sidebar_left_3',
    'ad-right-1': 'sidebar_right_1', 'ad-right-2': 'sidebar_right_2', 'ad-right-3': 'sidebar_right_3',
    'ad-inline-1': 'inline_1', 'ad-inline-2': 'inline_2'
  };
  var PLACEHOLDER_CLASSES = ['ad-slot', 'adslot', 'adinline', 'ad'];
  var PLACEHOLDER_TEXT = /advertisement|reserved advertising|reserved space|advertise here|your ad here/i;
  var WRAPPERS = '.ad-leader, .ad-inline-wrap, .ad-sidebar-col';

  // Hide placeholder boxes straight away (no flash); revealed only if the config asks for them.
  var css = document.createElement('style');
  css.textContent =
    'html:not(.cbse-ads-ph) .ad-slot:not(.cbse-ad-live), html:not(.cbse-ads-ph) .adslot:not(.cbse-ad-live){display:none!important}' +
    '.cbse-ad-hidden{display:none!important}' +
    '.ad-page-wrap.cbse-no-rails{grid-template-columns:minmax(0,1fr)!important}' +
    '.ad-page-wrap.cbse-no-rails .ad-main-col{grid-column:1!important}' +
    '.ad-page-wrap.cbse-no-rails .ad-leader{grid-column:1!important}';
  (document.head || document.documentElement).appendChild(css);

  function placeholder(slot, contact) {
    var d = document.createElement('div');
    d.style.cssText = 'width:100%;box-sizing:border-box;border:2px dashed #c9a227;border-radius:8px;' +
      'background:linear-gradient(135deg,#1a3a6b11,#c9a22711);display:flex;flex-direction:column;' +
      'align-items:center;justify-content:center;padding:10px 8px;margin:8px 0;text-align:center;' +
      'font-family:Inter,sans-serif;color:#1a3a6b;gap:4px';
    d.innerHTML = '<span style="font-size:18px">📢</span>' +
      '<span style="font-size:11px;font-weight:700;letter-spacing:.5px">YOUR AD HERE</span>' +
      '<span style="font-size:10px;color:#666">' + (slot.label || '') + '</span>' +
      '<a href="mailto:' + contact + '" style="font-size:10px;color:#1a3a6b;font-weight:600;margin-top:2px;">' + contact + '</a>';
    return d;
  }

  function banner(slot) {
    var a = document.createElement('a');
    a.href = slot.url || '#';
    a.target = '_blank';
    a.rel = 'noopener sponsored';
    a.style.cssText = 'display:block;width:100%;margin:8px 0;';
    var img = document.createElement('img');
    img.src = new URL(slot.img, SCRIPT).href;
    img.alt = slot.alt || 'Sponsored';
    img.loading = 'lazy';
    img.style.cssText = 'width:100%;height:auto;display:block;border-radius:6px;';
    a.appendChild(img);
    return a;
  }

  function hasClass(el, list) {
    for (var i = 0; i < list.length; i++) if (el.classList.contains(list[i])) return true;
    return false;
  }

  function apply(cfg) {
    var slots = cfg.slots || {};
    var showPh = !!cfg.show_placeholders;
    var contact = cfg.contact || 'ads@cbsemock.org.in';
    if (showPh) document.documentElement.classList.add('cbse-ads-ph');

    // 1. Vendor slots (#ad-…)
    Object.keys(SLOT_FOR_ID).forEach(function (id) {
      var box = document.getElementById(id);
      if (!box) return;
      var slot = slots[SLOT_FOR_ID[id]] || {};
      box.innerHTML = '';
      if (slot.active && slot.img) {
        box.appendChild(banner(slot));
        box.classList.add('cbse-ad-live');
        var w = box.closest('.ad-slot, .adslot'); if (w) w.classList.add('cbse-ad-live');
      } else if (showPh) {
        box.appendChild(placeholder(slot, contact));
      } else {
        box.classList.add('cbse-ad-hidden');
      }
    });

    // 2. Wrappers whose vendor boxes are all empty → hide, and close up the grid
    document.querySelectorAll(WRAPPERS).forEach(function (w) {
      var boxes = w.querySelectorAll('[id^="ad-"]');
      if (!boxes.length) return;
      var live = false;
      boxes.forEach(function (b) { if (b.classList.contains('cbse-ad-live') || (showPh && b.firstChild)) live = true; });
      w.classList.toggle('cbse-ad-hidden', !live);
    });
    document.querySelectorAll('.ad-page-wrap').forEach(function (p) {
      var rails = p.querySelectorAll('.ad-sidebar-col');
      var anyVisible = false;
      rails.forEach(function (r) { if (!r.classList.contains('cbse-ad-hidden')) anyVisible = true; });
      p.classList.toggle('cbse-no-rails', rails.length > 0 && !anyVisible);
    });

    // 3. Hard-coded "ADVERTISEMENT · RESERVED SPACE" boxes (labs) — no vendor behind them
    if (!showPh) {
      document.querySelectorAll('div, aside, section').forEach(function (el) {
        if (!hasClass(el, PLACEHOLDER_CLASSES) || el.classList.contains('cbse-ad-live')) return;
        if (el.querySelector('ins.adsbygoogle, [id^="ad-"].cbse-ad-live')) return;
        if (PLACEHOLDER_TEXT.test(el.textContent || '') || el.classList.contains('ad-slot') || el.classList.contains('adslot')) {
          el.classList.add('cbse-ad-hidden');
        }
      });
    }
  }

  var DEFAULTS = { show_placeholders: false, slots: {} };
  var bust = Math.floor(Date.now() / 300000);          // re-read the config at most every 5 minutes
  var cfgPromise = fetch(CONFIG_URL + '?v=' + bust, { cache: 'no-cache' })
    .then(function (r) { return r.ok ? r.json() : DEFAULTS; })
    .catch(function () { return DEFAULTS; });

  function run() { cfgPromise.then(apply); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run);
  else run();
})();
