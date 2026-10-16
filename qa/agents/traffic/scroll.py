import os
from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
URL='file://'+ROOT+'/clone/index.html'
VIEWS=['05-traffic','05a-traffic-projects','05b-traffic-project-usage','05c-traffic-model-config','05d-traffic-statistics','05e-traffic-applications','05f-traffic-errorlogs']
OUT=os.path.dirname(os.path.abspath(__file__))
JS="""() => { const out=[]; document.querySelectorAll('#root *').forEach((e,i)=>{const s=getComputedStyle(e); if((/(auto|scroll)/.test(s.overflowY)&&e.scrollHeight>e.clientHeight+2)||(/(auto|scroll)/.test(s.overflowX)&&e.scrollWidth>e.clientWidth+2)){const r=e.getBoundingClientRect(); e.setAttribute('data-qa-scroll',i); out.push({i, cls:e.className.toString().slice(0,90), sh:e.scrollHeight, ch:e.clientHeight, sw:e.scrollWidth, cw:e.clientWidth, x:Math.round(r.x), y:Math.round(r.y), w:Math.round(r.width), h:Math.round(r.height), oy:s.overflowY, ox:s.overflowX});}}); 
 const imgs=[...document.querySelectorAll('#root img')].filter(i=>!i.complete||i.naturalWidth==0).map(i=>i.src.slice(0,80));
 const docScroll=[document.documentElement.scrollHeight, document.documentElement.clientHeight, document.documentElement.scrollWidth];
 return {out, imgs, docScroll}; }"""
if __name__=="__main__":
 with sync_playwright() as pw:
     b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
     for v in VIEWS:
         pg.goto(URL+'#'+v); pg.wait_for_timeout(500)
         r=pg.evaluate(JS)
         print('=====',v, 'broken imgs',r['imgs'],'doc',r['docScroll'])
         for s in r['out']: print('  ',s)
         for s in r['out']:
             if s['x']>870 and s['sh']>s['ch']+2:
                 pg.evaluate(f"document.querySelector('[data-qa-scroll=\"{s['i']}\"]').scrollTop=1e6")
         pg.wait_for_timeout(200)
         pg.screenshot(path=f'{OUT}/{v}-bottom.png')
     b.close()
