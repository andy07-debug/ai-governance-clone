import base64, io, numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'; URL='file://'+ROOT+'/clone/index.html'
def onw(X): a=X[...,3:4]/255.; return X[...,:3]*a+255*(1-a)
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    for v in ['05b-traffic-project-usage','05d-traffic-statistics']:
        pg.goto(URL+'#'+v); pg.wait_for_timeout(1300)
        pg.evaluate("""()=>{const cv=document.querySelector('canvas[data-chart]'); const p=cv.parentElement; p.style.width='440.4px'; p.style.flex='none';}""")
        pg.wait_for_timeout(1500)
        R=np.asarray(Image.open(ROOT+'/qa/charts/%s-0.png'%v).convert('RGBA')).astype(int)
        base=pg.evaluate("()=>Chart.getChart(document.querySelector('canvas[data-chart]')).data.datasets[0].data.slice()")
        def score(data):
            u=pg.evaluate("""(d)=>{const c=Chart.getChart(document.querySelector('canvas[data-chart]')); c.data.datasets[0].data=d; c.update('none'); return c.canvas.toDataURL()}""", data)
            A=np.asarray(Image.open(io.BytesIO(base64.b64decode(u.split(',')[1]))).convert('RGBA')).astype(int)
            d=np.abs(onw(A)-onw(R)).sum(2); return int(d.sum()), int((d>150).sum()), int((d>40).sum())
        best=list(base)
        for i in range(6):
            res={}
            for dv in (-2,-1,0,1,2):
                t=list(best); t[i]=base[i]+dv; res[base[i]+dv]=score(t)
            k=min(res,key=lambda x:res[x][0]); best[i]=k
            print(v[:3],'bar',i,res,'-> best',k)
        print(v[:3],'shipped',base,score(base),'best',best,score(best))
    b.close()
