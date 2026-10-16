import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
URL='file://'+ROOT+'/clone/index.html'
VIEWS=['05-traffic','05a-traffic-projects','05b-traffic-project-usage','05c-traffic-model-config','05d-traffic-statistics','05e-traffic-applications','05f-traffic-errorlogs']
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    for v in VIEWS:
        pg.goto(URL+'#'+v); pg.wait_for_timeout(800)
        pg.screenshot(path=f'now-{v}.png')
        A=np.asarray(Image.open(f'{ROOT}/qa/base/{v}.png').convert('RGB')).astype(int)
        B=np.asarray(Image.open(f'now-{v}.png').convert('RGB')).astype(int)
        if A.shape!=B.shape: print(v,'shape',A.shape,B.shape); continue
        m=(np.abs(A-B).sum(2)>60)
        ys,xs=np.nonzero(m)
        rows=np.nonzero(m.any(1))[0]
        # group rows into bands
        bands=[];
        for r in rows:
            if bands and r-bands[-1][1]<=8: bands[-1][1]=r
            else: bands.append([r,r])
        out=[]
        for a,b2 in bands:
            cols=np.nonzero(m[a:b2+1].any(0))[0]; out.append((int(cols.min()),int(a),int(cols.max()),int(b2), int(m[a:b2+1].sum())))
        out=sorted(out,key=lambda t:-t[4])[:8]
        print(v,'diff%',round(m.mean()*100,3),out)
        Image.fromarray((np.where(m[...,None],[255,0,0],B*0.4+150)).astype('uint8')).save(f'diff-{v}.png')
    b.close()
