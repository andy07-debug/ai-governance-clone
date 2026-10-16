from playwright.sync_api import sync_playwright
import numpy as np
from PIL import Image
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
OUT='/Users/kumaraniket/Desktop/AI Governance Clone/qa/agents/analytics+firewall+events'
ANIM='*,*::before,*::after{animation-duration:0s!important;animation-delay:0s!important;transition:none!important;caret-color:transparent!important}'
cfg=[('01-llm-analytics','.min-h-0.flex-1.overflow-y-auto',[0,700,1400,1965]),('02-firewall','.flex-1.overflow-y-auto.p-6',[0,344]),('03-live-events',None,[0])]
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    for v,sel,offs in cfg:
        for o in offs:
            imgs=[]
            for kind,url in [('clone','file://'+ROOT+'/clone/index.html#'+v),('base','file://'+ROOT+'/qa/base/'+v+'.html')]:
                pg.goto(url); pg.add_style_tag(content=ANIM); pg.wait_for_timeout(500)
                if sel: pg.evaluate(f"(o)=>{{const a=document.querySelectorAll('{sel}');a[a.length-1].scrollTop=o}}", o)
                pg.wait_for_timeout(200)
                p=f'{OUT}/cmp-{v}-{o}-{kind}.png'; pg.screenshot(path=p); imgs.append(np.asarray(Image.open(p).convert('RGB')).astype(int))
            d=np.abs(imgs[0]-imgs[1]).sum(2)>30
            # restrict to right panel
            dr=d[:,866:]
            ys,xs=np.nonzero(dr)
            print(v,o,'diff% right',round(100*dr.mean(),3), 'bbox', (xs.min()+866,ys.min(),xs.max()+866,ys.max()) if len(xs) else None)
            Image.fromarray((d*255).astype('uint8')).save(f'{OUT}/diffmask-{v}-{o}.png')
    b.close()
