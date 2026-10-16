import os, numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'; URL='file://'+ROOT+'/clone/index.html'
ANIM_OFF = '*,*::before,*::after{animation-duration:0s!important;animation-delay:0s!important;transition:none!important;caret-color:transparent!important}'
views=sorted(f[:-4] for f in os.listdir(ROOT+'/qa/clone') if f.endswith('.png'))
errs=[]
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936}); pg.on('pageerror', lambda e: errs.append(str(e)))
    for v in views:
        if v.startswith('08-'): continue
        pg.goto(URL+'#'+v); pg.add_style_tag(content=ANIM_OFF); pg.wait_for_timeout(1600)
        p='shots/%s.png'%v; pg.screenshot(path=p)
        a=np.asarray(Image.open(p).convert('RGB')).astype(int); c=np.asarray(Image.open(ROOT+'/qa/clone/%s.png'%v).convert('RGB')).astype(int)
        if a.shape!=c.shape: print(v,'shape',a.shape,c.shape); continue
        d=np.abs(a-c).sum(2)>30
        ys,xs=np.nonzero(d)
        print(v, 'diff%%=%.3f'%(100*d.mean()), ('bbox x%d-%d y%d-%d'%(xs.min(),xs.max(),ys.min(),ys.max())) if len(xs) else '')
        if len(xs):
            m=(a*0.35+255*0.65).astype(np.uint8); m[d]=[255,0,0]; Image.fromarray(m).save('shots/diff-%s.png'%v)
    print('ERRS',errs); b.close()
