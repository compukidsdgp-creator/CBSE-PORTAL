const {chromium}=require('playwright');const fs=require('fs');
(async()=>{ /* writes per-page paper question lists */const b=await chromium.launch();const files=fs.readdirSync('.').filter(f=>/^cbse-class-1[02]-.*\.html$/.test(f));const out={};
for(const f of files){const p=await b.newPage();await p.route(/^https?:/,r=>r.abort());
 try{await p.goto('file://'+process.cwd()+'/'+f,{waitUntil:'load'});await p.waitForTimeout(300);
 const res=await p.evaluate(()=>{
  const key=o=>{if(typeof o==='string')return o;const t=o.q||o.question||o.text||o.passage||o.title||o.stem;return typeof t==='string'?t:JSON.stringify(o)};
  function leaves(x,acc){if(Array.isArray(x)){x.forEach(y=>leaves(y,acc))}else if(x&&typeof x==='object'){if(x.q||x.question||x.text||x.passage||x.stem)acc.push(key(x));else Object.values(x).forEach(y=>leaves(y,acc))}else if(typeof x==='string'&&x.length>25)acc.push(x);return acc}
  const papers=[];
  if(typeof buildPaper==='function'){for(let n=0;n<15;n++){try{papers.push(leaves(buildPaper(n),[]))}catch(e){papers.push(['ERR '+e.message])}}}
  else if(typeof pick==='function'&&typeof render==='function'){const orig=pick;let cur=null;window.pick=function(){const r=orig.apply(this,arguments);if(cur)leaves(r,cur);return r};
   for(let n=0;n<15;n++){cur=[];try{render(n)}catch(e){cur.push('ERR '+e.message)}papers.push(cur)}}
  return papers});
 out[f]=res}catch(e){out[f]={err:e.message}}await p.close()}
fs.writeFileSync(process.argv[2],JSON.stringify(out));await b.close()})();
// Usage: node tools/mock_overlap_audit.js OUT.json   (run from the repo root), then:
//        python3 tools/mock_overlap_report.py OUT.json
