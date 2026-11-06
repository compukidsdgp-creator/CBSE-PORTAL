(function(){
  const script=document.currentScript;
  const rootUrl=new URL('.',script.src);
  const homeUrl=new URL('index.html',rootUrl).href;
  const body=document.body;
  if(!body)return;

  // Inject portal-zones.css once if not already loaded
  if(!document.querySelector('link[href*="portal-zones"]')){
    const lnk=document.createElement('link');
    lnk.rel='stylesheet';lnk.href=new URL('portal-zones.css',rootUrl).href;
    document.head.appendChild(lnk);
  }

  if(!document.querySelector('.portal-backbar')){
    const bar=document.createElement('nav');
    bar.className='portal-backbar';
    bar.setAttribute('aria-label','Portal navigation');
    bar.innerHTML='<span class="portal-brand">CBSEMOCK</span><button type="button" id="portal-back">← Back</button><a href="'+homeUrl+'">⌂ Main Home</a><a href="'+new URL("news.html",rootUrl).href+'" aria-label="CBSE News and Updates">📰 News</a><a href="'+new URL("weekly-focus/weekly-focus-prod.html",rootUrl).href+'" aria-label="Weekly Focus">🎯 Weekly Focus</a>';
    body.insertBefore(bar,body.firstChild);
    bar.querySelector('#portal-back').addEventListener('click',function(){
      if(document.referrer && new URL(document.referrer).origin===location.origin && history.length>1) history.back();
      else location.href=homeUrl;
    });
  }

  function makeAd(id,where){
    if(document.getElementById(id))return;
    const wrap=document.createElement('div');
    wrap.className='portal-ad';
    wrap.id=id==='ad-leader-top'?'ad-leader-top-wrap':'ad-leader-bottom-wrap';
    const inner=document.createElement('div');inner.className='portal-ad-inner';inner.id=id;
    wrap.appendChild(inner);
    if(where==='top')body.insertBefore(wrap,body.firstChild);
    else body.appendChild(wrap);
  }
  makeAd('ad-leader-top','top');
  makeAd('ad-leader-bottom','bottom');
})();