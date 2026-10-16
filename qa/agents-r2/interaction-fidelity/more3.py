from playwright.sync_api import sync_playwright
URL='file:///Users/kumaraniket/Desktop/AI Governance Clone/clone/index.html'
with sync_playwright() as pw:
    br=pw.chromium.launch(); pg=br.new_page(viewport={'width':1920,'height':936})
    for v in ['05b-traffic-project-usage','05d-traffic-statistics']:
        pg.goto('about:blank'); pg.goto(URL+'#'+v); pg.wait_for_timeout(300)
        r=pg.evaluate("""()=>{const bs=[...document.querySelectorAll('[data-panel]:last-of-type button')].filter(b=>b.textContent.trim()==='more');const out=[];
          bs.forEach((b,i)=>{const entry=b.closest('.px-3.py-2'); const before=[...document.querySelectorAll('.line-clamp-2')]; b.click(); const after=new Set(document.querySelectorAll('.line-clamp-2'));
           const ch=before.filter(e=>!after.has(e)); const ok=ch.length===1&&entry.contains(ch[0]); const h=ch[0]?Math.round(ch[0].getBoundingClientRect().height):0; b.click(); const back=entry.querySelector('p').classList.contains('line-clamp-2');
           if(!ok||!back) out.push({i,ch:ch.length,ok,back}); });
          // also: other clamped lines with no more button (overflowing?)
          const clamps=[...document.querySelectorAll('[data-panel]:last-of-type .line-clamp-2')]; const noBtn=clamps.filter(c=>{const e=c.parentElement; return ![...e.querySelectorAll('button')].some(b=>/^(more|less)$/.test(b.textContent.trim()))});
          return {n:bs.length, bad:out, clamps:clamps.length, noBtn:noBtn.map(c=>[c.tagName,c.className.slice(0,60),c.scrollHeight>c.clientHeight+1,c.textContent.slice(0,50)])}}""")
        print(v,r)
    br.close()
