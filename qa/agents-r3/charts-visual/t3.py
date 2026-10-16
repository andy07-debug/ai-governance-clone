import json, base64, io
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'; URL='file://'+ROOT+'/clone/index.html'
JOBS=[('01-llm-analytics',916.8,268),('05b-traffic-project-usage',440.4,300),('05d-traffic-statistics',440.4,300)]
errs=[]
with sync_playwright() as pw:
    b=pw.chromium.launch()
    pg=b.new_page(viewport={'width':1920,'height':936}); pg.on('pageerror', lambda e: errs.append(str(e)))
    for v,w,h in JOBS:
        pg.goto(URL+'#'+v); pg.wait_for_timeout(1300)
        r=pg.evaluate("""([w,h])=>{const cv=document.querySelector('canvas[data-chart]'); const p=cv.parentElement; const cs=getComputedStyle(p);
          const padX=parseFloat(cs.paddingLeft)+parseFloat(cs.paddingRight);
          p.style.width=(w+padX+parseFloat(cs.borderLeftWidth)+parseFloat(cs.borderRightWidth))+'px'; p.style.flex='none'; return padX;}""",[w,h])
        pg.wait_for_timeout(1500)
        info=pg.evaluate("""()=>{const cv=document.querySelector('canvas[data-chart]'); const r=cv.getBoundingClientRect(); return [r.width,r.height,cv.width,cv.height, cv.toDataURL()]}""")
        print(v, info[:4])
        img=Image.open(io.BytesIO(base64.b64decode(info[4].split(',')[1]))).convert('RGBA')
        img.save('render-%s.png'%v[:3])
        ref=Image.open(ROOT+'/qa/charts/%s-0.png'%v).convert('RGBA')
        print(' ref size', ref.size, 'render size', img.size)
        if ref.size!=img.size: continue
        A=np.asarray(img).astype(int); R=np.asarray(ref).astype(int)
        # composite on white
        def onw(X): a=X[...,3:4]/255.; return X[...,:3]*a+255*(1-a)
        d=np.abs(onw(A)-onw(R)).sum(2)
        big=d>40; vbig=d>150
        print(' pixels >40:', big.sum(), ' >150:', vbig.sum(), 'max', d.max())
        ys,xs=np.nonzero(vbig)
        if len(xs): print('  >150 bbox x',xs.min(),xs.max(),'y',ys.min(),ys.max())
        m=np.full(d.shape+(3,),235,np.uint8); m[big]=[255,160,160]; m[vbig]=[255,0,0]
        Image.fromarray(m).save('diff-%s.png'%v[:3])
    print('ERRS',errs); b.close()
