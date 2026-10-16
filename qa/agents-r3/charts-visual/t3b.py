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
        for val in [193,192.5,192,191]:
            u=pg.evaluate("""(val)=>{const c=Chart.getChart(document.querySelector('canvas[data-chart]')); c.data.datasets[0].data[2]=val; c.update('none'); return [c.canvas.toDataURL(), c.scales.y.getPixelForValue(0)-c.scales.y.getPixelForValue(1)]}""", val)
            A=np.asarray(Image.open(io.BytesIO(base64.b64decode(u[0].split(',')[1]))).convert('RGBA')).astype(int)
            d=np.abs(onw(A)-onw(R)).sum(2)
            print(v[:3], val, 'px/unit %.3f'%u[1], '>40', (d>40).sum(), '>150', (d>150).sum(), 'sum', int(d.sum()))
    b.close()
