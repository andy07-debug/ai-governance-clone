import base64, io, numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'; URL='file://'+ROOT+'/clone/index.html'
OUT=ROOT+'/qa/agents-r3/skeptic-bar192/'
def white(X): a=X[...,3:4]/255.; return X[...,:3]*a+255*(1-a)
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
    for v in ['05b-traffic-project-usage','05d-traffic-statistics']:
        pg.goto(URL+'#'+v); pg.wait_for_timeout(1300)
        info=pg.evaluate("""()=>{const cv=document.querySelector('canvas[data-chart]'); const p=cv.parentElement; const r=p.getBoundingClientRect(); return [cv.dataset.chart, r.width, r.height, cv.width, cv.height, devicePixelRatio]}""")
        print(v, 'before pin', info)
        pg.evaluate("""()=>{const cv=document.querySelector('canvas[data-chart]'); const p=cv.parentElement; p.style.width='440.4px'; p.style.height='300px'; p.style.flex='none';}""")
        pg.wait_for_timeout(1500)
        print(' after pin', pg.evaluate("()=>{const cv=document.querySelector('canvas[data-chart]');return [cv.width,cv.height]}"))
        R=white(np.asarray(Image.open(ROOT+'/qa/charts/%s-0.png'%v).convert('RGBA')).astype(float))
        base=pg.evaluate("()=>Chart.getChart(document.querySelector('canvas[data-chart]')).data.datasets[0].data.slice()")
        def render(d):
            u=pg.evaluate("(d)=>{const c=Chart.getChart(document.querySelector('canvas[data-chart]')); c.data.datasets[0].data=d; c.update('none'); return [c.canvas.toDataURL(), c.scales.y.max]}", d)
            A=white(np.asarray(Image.open(io.BytesIO(base64.b64decode(u[0].split(',')[1]))).convert('RGBA')).astype(float))
            return A,u[1]
        for d in (base, [x if i!=2 else x-1 for i,x in enumerate(base)], [x if i!=2 else x-2 for i,x in enumerate(base)]):
            A,ym=render(d); D=np.abs(A-R).sum(2)
            ys,xs=np.where(D>150)
            print(' ',d,'sum',int(D.sum()),'>150',int((D>150).sum()),'ymax',ym, 'rows',sorted(set(ys.tolist()))[:10], (xs.min(),xs.max()) if len(xs) else None)
        # column profile of bar 2 around top: capture vs shipped
        A,_=render(base)
        cx=215
        print('  capture col',cx,[int(R[y,cx].sum()) for y in range(60,70)])
        print('  shipped col',cx,[int(A[y,cx].sum()) for y in range(60,70)])
        A2,_=render([x if i!=2 else x-1 for i,x in enumerate(base)])
        print('  192     col',cx,[int(A2[y,cx].sum()) for y in range(60,70)])
        # restore and tooltip
        render(base)
        pt=pg.evaluate("()=>{const c=Chart.getChart(document.querySelector('canvas[data-chart]'));const m=c.getDatasetMeta(0).data[2];const r=c.canvas.getBoundingClientRect();return [r.left+m.x, r.top+m.y+20]}")
        pg.mouse.move(*pt); pg.wait_for_timeout(700)
        print('  tooltip', pg.evaluate("()=>{const c=Chart.getChart(document.querySelector('canvas[data-chart]'));const t=c.tooltip;return [t.title, t.body&&t.body.map(b=>b.lines)]}"))
    print('errors',errs)
    b.close()
