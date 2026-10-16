import json
from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
URL='file://'+ROOT+'/clone/index.html'
views=['00-home','07a-shell-mode-dropdown','07b-shell-hamburger','07c-shell-projects']
JS="""()=>{const out=[];const els=[...document.querySelectorAll('button,a,[role=button],li,.cursor-pointer,input,textarea,.p-dropdown,svg[class*=cursor]')];
for(const e of els){const r=e.getBoundingClientRect(); if(r.width<2||r.height<2) continue; if(r.bottom<0||r.top>936||r.right<0||r.left>1920) continue;
const cx=r.left+r.width/2, cy=r.top+r.height/2; const top=document.elementFromPoint(cx,cy); if(!top||!(e===top||e.contains(top))) continue;
out.push({tag:e.tagName,txt:(e.innerText||e.placeholder||e.title||e.getAttribute('aria-label')||'').replace(/\\s+/g,' ').trim().slice(0,40),cls:(e.className&&e.className.baseVal!==undefined?e.className.baseVal:e.className||'').slice(0,50),title:e.title||'',x:Math.round(cx),y:Math.round(cy)})}
return out}"""
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    errs=[]
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: errs.append(m.text) if m.type=='error' else None)
    for v in views:
        pg.goto(URL+'#'+v); pg.wait_for_timeout(300)
        items=pg.evaluate(JS)
        # dedupe by coordinate
        seen=set(); its=[]
        for it in items:
            k=(it['x']//6,it['y']//6)
            if k in seen: continue
            seen.add(k); its.append(it)
        print('=====',v,len(its))
        for it in its:
            pg.goto(URL+'#'+v); pg.reload(); pg.wait_for_timeout(200)
            before=pg.evaluate("document.getElementById('mount').innerHTML.length")
            pg.mouse.click(it['x'],it['y']); pg.wait_for_timeout(200)
            h=pg.evaluate('location.hash.slice(1)')
            after=pg.evaluate("document.getElementById('mount').innerHTML.length")
            res = ('NAV->'+h) if h!=v else ('domchg' if after!=before else 'nothing')
            print(f"  {res:32s} {it['tag']:6s} ({it['x']},{it['y']}) '{it['txt']}' title='{it['title']}' cls={it['cls'][:40]}")
    print('errors',errs)
    b.close()
