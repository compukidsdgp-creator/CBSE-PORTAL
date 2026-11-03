/**
 * search.js — Universal subject/topic search for cbsemock.org.in
 * Drop a <div id="cbse-search"></div> anywhere and include this script.
 * No server, no build step — pure client-side.
 */
(function(){
'use strict';

// ── Subject index ─────────────────────────────────────────────────────────────
const SUBJECTS = [
  // Class X
  { title:'Mathematics Standard', cls:'X', file:'resources/maths-x.html',
    tags:'maths algebra geometry trigonometry statistics probability quadratic equations' },
  { title:'Mathematics Basic', cls:'X', file:'resources/maths-basic-x.html',
    tags:'maths basic class 10 arithmetic mensuration' },
  { title:'Science', cls:'X', file:'resources/science-x.html',
    tags:'science physics chemistry biology class 10 light electricity carbon' },
  { title:'Social Science', cls:'X', file:'resources/sst-x.html',
    tags:'social science history geography civics economics class 10 india' },
  { title:'English Language & Literature', cls:'X', file:'resources/english-ll-x.html',
    tags:'english literature grammar first flight footprints class 10' },
  { title:'English Communicative', cls:'X', file:'resources/english-comm-x.html',
    tags:'english communicative writing comprehension class 10' },
  { title:'Hindi Course A', cls:'X', file:'resources/hindi-a-x.html',
    tags:'hindi course a kshitij kritika sparsh sanchayan class 10' },
  { title:'Computer Applications', cls:'X', file:'resources/comp-app-x.html',
    tags:'computer applications html css python class 10 coding' },
  { title:'Artificial Intelligence', cls:'X', file:'resources/ai-x.html',
    tags:'artificial intelligence AI machine learning python data class 10' },
  // Class XII
  { title:'Mathematics', cls:'XII', file:'resources/maths-xii.html',
    tags:'maths calculus matrices determinants integration vectors class 12 differentiation' },
  { title:'Physics', cls:'XII', file:'resources/physics-xii.html',
    tags:'physics electricity magnetism optics modern physics class 12 wave' },
  { title:'Chemistry', cls:'XII', file:'resources/chemistry-xii.html',
    tags:'chemistry organic inorganic physical solutions electrochemistry class 12' },
  { title:'Biology', cls:'XII', file:'resources/biology-xii.html',
    tags:'biology genetics evolution ecology reproduction class 12 botany zoology' },
  { title:'English Core', cls:'XII', file:'resources/english-xii.html',
    tags:'english core flamingo vistas writing class 12 literature grammar' },
  { title:'Computer Science', cls:'XII', file:'resources/cs-xii.html',
    tags:'computer science python sql networking class 12 programming database' },
  { title:'Economics', cls:'XII', file:'resources/economics-xii.html',
    tags:'economics microeconomics macroeconomics gdp demand supply market class 12' },
  { title:'Accountancy', cls:'XII', file:'resources/accountancy-xii.html',
    tags:'accountancy partnership company accounts balance sheet cash flow class 12' },
  { title:'Business Studies', cls:'XII', file:'resources/business-xii.html',
    tags:'business studies management marketing consumer protection class 12 directing controlling' },
];

// ── Scoring: title match scores higher ───────────────────────────────────────
function score(subject, query) {
  const q = query.toLowerCase().trim();
  if (!q) return 0;
  const words = q.split(/\s+/);
  let s = 0;
  for (const w of words) {
    if (subject.title.toLowerCase().includes(w)) s += 10;
    if (subject.cls === w.toUpperCase()) s += 8;
    if (subject.tags.includes(w)) s += 3;
  }
  return s;
}

// ── Render ────────────────────────────────────────────────────────────────────
function render(results, query) {
  const base = document.getElementById('cbse-search');
  if (!base) return;
  const list = base.querySelector('.cs-results');
  if (!list) return;
  if (!query.trim()) { list.innerHTML=''; list.hidden=true; return; }
  if (results.length === 0) {
    list.innerHTML = '<div class="cs-empty">No subjects found for "'+query+'"</div>';
    list.hidden = false; return;
  }
  list.innerHTML = results.map(s => `
    <a class="cs-result" href="${s.file}">
      <span class="cs-badge cs-badge--${s.cls==='X'?'x':'xii'}">${s.cls}</span>
      <span class="cs-name">${s.title}</span>
      <span class="cs-arrow">→</span>
    </a>`).join('');
  list.hidden = false;
}

// ── Search ────────────────────────────────────────────────────────────────────
function doSearch(query) {
  const scored = SUBJECTS
    .map(s => ({ ...s, _s: score(s, query) }))
    .filter(s => s._s > 0)
    .sort((a,b) => b._s - a._s)
    .slice(0, 8);
  render(scored, query);
}

// ── Mount ─────────────────────────────────────────────────────────────────────
function mount() {
  const base = document.getElementById('cbse-search');
  if (!base) return;

  base.innerHTML = `
<div class="cs-wrap">
  <div class="cs-input-row">
    <span class="cs-icon">🔍</span>
    <input class="cs-input" type="search" placeholder="Search subject or topic… (e.g. Maths XII, carbon, partnership)" autocomplete="off" spellcheck="false">
  </div>
  <div class="cs-results" hidden></div>
</div>
<style>
.cs-wrap{position:relative;max-width:620px;margin:0 auto}
.cs-input-row{display:flex;align-items:center;background:#fff;border:2px solid #00b4d8;border-radius:12px;padding:10px 16px;gap:10px;box-shadow:0 4px 18px rgba(0,180,216,.15)}
.cs-icon{font-size:1.2rem;flex-shrink:0}
.cs-input{flex:1;border:none;outline:none;font-size:1rem;background:transparent;color:#1a202c;font-family:inherit}
.cs-results{position:absolute;left:0;right:0;top:calc(100% + 6px);background:#fff;border:1px solid #dde3ea;border-radius:12px;box-shadow:0 8px 28px rgba(0,0,0,.12);z-index:200;overflow:hidden}
.cs-result{display:flex;align-items:center;gap:10px;padding:11px 16px;text-decoration:none;color:#1a202c;border-bottom:1px solid #f1f5f9;transition:background .15s}
.cs-result:last-child{border-bottom:none}
.cs-result:hover{background:#f0fbff}
.cs-badge{font-size:.68rem;font-weight:700;padding:2px 8px;border-radius:20px;flex-shrink:0}
.cs-badge--x{background:#c0392b;color:#fff}
.cs-badge--xii{background:#6b21a8;color:#fff}
.cs-name{flex:1;font-size:.92rem;font-weight:600}
.cs-arrow{color:#00b4d8;font-size:1rem}
.cs-empty{padding:14px 16px;font-size:.88rem;color:#64748b}
@media(prefers-color-scheme:dark){
  .cs-input-row{background:#161b22;border-color:#00b4d8}
  .cs-input{color:#e6edf3}
  .cs-results{background:#161b22;border-color:#30363d}
  .cs-result{color:#e6edf3;border-bottom-color:#30363d}
  .cs-result:hover{background:#1c2733}
}
</style>`;

  const input = base.querySelector('.cs-input');
  input.addEventListener('input', e => doSearch(e.target.value));
  input.addEventListener('keydown', e => {
    if (e.key==='Escape') { input.value=''; render([], ''); }
  });
  // close on outside click
  document.addEventListener('click', e => {
    if (!base.contains(e.target)) render([], '');
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', mount);
} else {
  mount();
}

})();
