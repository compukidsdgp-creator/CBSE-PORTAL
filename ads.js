/**
 * CBSEMock.org.in — Ad Configuration
 * ====================================
 * To add a client ad:
 *   1. Place their image in the ads/ folder
 *   2. Update the slot below with img, url, alt
 *   3. Push to GitHub — goes live in ~2 minutes
 *
 * To remove an ad, set: active: false
 * Slot sizes:
 *   leaderboard : 728×90 px  (top and bottom, full width)
 *   sidebar     : 300×75 px  (left & right panels, 6×1.5 inch equivalent)
 *   inline      : 580×90 px  (between question blocks)
 */

const CBSE_ADS_SCRIPT_URL = document.currentScript ? document.currentScript.src : new URL('ads.js', location.href).href;
const CBSE_ADS = {

  /* ── TOP LEADERBOARD ─────────────────────────────── */
  leaderboard_top: {
    active: false,
    img:    "ads/leaderboard-top.jpg",
    url:    "#",
    alt:    "Advertise here — 728×90 — cbsemock.org.in",
    label:  "Top Banner · 728×90"
  },

  /* ── BOTTOM LEADERBOARD ──────────────────────────── */
  leaderboard_bottom: {
    active: false,
    img:    "ads/leaderboard-bottom.jpg",
    url:    "#",
    alt:    "Advertise here — 728×90 — cbsemock.org.in",
    label:  "Bottom Banner · 728×90"
  },

  /* ── LEFT SIDEBAR (top → bottom) ─────────────────── */
  sidebar_left_1: {
    active: false,
    img:    "ads/sidebar-left-1.jpg",
    url:    "#",
    alt:    "Advertise here — cbsemock.org.in",
    label:  "Left Panel 1 · 300×75"
  },
  sidebar_left_2: {
    active: false,
    img:    "ads/sidebar-left-2.jpg",
    url:    "#",
    alt:    "Advertise here — cbsemock.org.in",
    label:  "Left Panel 2 · 300×75"
  },
  sidebar_left_3: {
    active: false,
    img:    "ads/sidebar-left-3.jpg",
    url:    "#",
    alt:    "Advertise here — cbsemock.org.in",
    label:  "Left Panel 3 · 300×75"
  },

  /* ── RIGHT SIDEBAR (top → bottom) ────────────────── */
  sidebar_right_1: {
    active: false,
    img:    "ads/sidebar-right-1.jpg",
    url:    "#",
    alt:    "Advertise here — cbsemock.org.in",
    label:  "Right Panel 1 · 300×75"
  },
  sidebar_right_2: {
    active: false,
    img:    "ads/sidebar-right-2.jpg",
    url:    "#",
    alt:    "Advertise here — cbsemock.org.in",
    label:  "Right Panel 2 · 300×75"
  },
  sidebar_right_3: {
    active: false,
    img:    "ads/sidebar-right-3.jpg",
    url:    "#",
    alt:    "Advertise here — cbsemock.org.in",
    label:  "Right Panel 3 · 300×75"
  },

  /* ── INLINE (injected between question blocks) ────── */
  inline_1: {
    active: false,
    img:    "ads/inline-1.jpg",
    url:    "#",
    alt:    "Advertise here — cbsemock.org.in",
    label:  "Inline 1 · 580×90"
  },
  inline_2: {
    active: false,
    img:    "ads/inline-2.jpg",
    url:    "#",
    alt:    "Advertise here — cbsemock.org.in",
    label:  "Inline 2 · 580×90"
  }
};

/* ── Render engine (do not edit below this line) ────── */
(function () {
  function placeholder(slot) {
    var d = document.createElement('div');
    d.style.cssText = [
      'width:100%','box-sizing:border-box',
      'border:2px dashed #c9a227','border-radius:8px',
      'background:linear-gradient(135deg,#1a3a6b11,#c9a22711)',
      'display:flex','flex-direction:column',
      'align-items:center','justify-content:center',
      'padding:10px 8px','margin:8px 0','text-align:center',
      'font-family:Inter,sans-serif','color:#1a3a6b','gap:4px'
    ].join(';');
    d.innerHTML =
      '<span style="font-size:18px">📢</span>' +
      '<span style="font-size:11px;font-weight:700;letter-spacing:.5px">YOUR AD HERE</span>' +
      '<span style="font-size:10px;color:#666">' + slot.label + '</span>' +
      '<a href="mailto:ads@cbsemock.org.in" style="font-size:10px;color:#1a3a6b;font-weight:600;margin-top:2px;">ads@cbsemock.org.in</a>';
    return d;
  }

  function renderAd(slotKey, container) {
    var slot = CBSE_ADS[slotKey];
    if (!slot || !container) return;
    if (slot.active && slot.img) {
      var a = document.createElement('a');
      a.href = slot.url || '#';
      a.target = '_blank';
      a.rel = 'noopener sponsored';
      a.style.cssText = 'display:block;width:100%;margin:8px 0;';
      var img = document.createElement('img');
      img.src = new URL(slot.img, CBSE_ADS_SCRIPT_URL).href;
      img.alt = slot.alt || '';
      img.style.cssText = 'width:100%;height:auto;display:block;border-radius:6px;';
      a.appendChild(img);
      container.appendChild(a);
    } else {
      container.appendChild(placeholder(slot));
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    // Leaderboards
    renderAd('leaderboard_top',    document.getElementById('ad-leader-top'));
    renderAd('leaderboard_bottom', document.getElementById('ad-leader-bottom'));
    // Sidebars
    ['1','2','3'].forEach(function(n){
      renderAd('sidebar_left_'  + n, document.getElementById('ad-left-'  + n));
      renderAd('sidebar_right_' + n, document.getElementById('ad-right-' + n));
    });
    // Inline
    renderAd('inline_1', document.getElementById('ad-inline-1'));
    renderAd('inline_2', document.getElementById('ad-inline-2'));
  });
})();
