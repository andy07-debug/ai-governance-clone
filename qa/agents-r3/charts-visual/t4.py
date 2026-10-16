import json
from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'; URL='file://'+ROOT+'/clone/index.html'
errs=[]
TT="""()=>{const c=Chart.getChart(document.querySelector('canvas[data-chart]')); const t=c.tooltip; return {op:t.opacity, title:t.title, body:(t.body||[]).map(b=>b.lines.join('|')), x:t.x, y:t.y, w:t.width, cw:c.width, ch:c.height}}"""
PTS="""()=>{const c=Chart.getChart(document.querySelector('canvas[data-chart]')); const r=c.canvas.getBoundingClientRect(); return c.getDatasetMeta(0).data.map(e=>{const p=e.getProps(['x','y','base']); return [r.left+p.x, r.top+(p.base!==undefined? (p.y+p.base)/2 : p.y)]})}"""
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936}); pg.on('pageerror', lambda e: errs.append(str(e)))
    for v in ['01-llm-analytics','05b-traffic-project-usage','05d-traffic-statistics']:
        pg.goto(URL+'#'+v); pg.wait_for_timeout(1300)
        for mode in ('normal','fs'):
            if mode=='fs': pg.locator('[title="Toggle Fullscreen"]').first.click(); pg.wait_for_timeout(1300)
            pts=pg.evaluate(PTS); out=[]
            for i,(x,y) in enumerate(pts):
                pg.mouse.move(x,y); pg.wait_for_timeout(450); t=pg.evaluate(TT); out.append((t['title'],t['body'],round(t['op'],2)))
                if i==len(pts)-1: pg.screenshot(path='tt-%s-%s.png'%(v[:3],mode))
            print(v[:3],mode,out)
            pg.mouse.move(5,5); pg.wait_for_timeout(500); print('  after leave op', pg.evaluate(TT)['op'])
        pg.locator('[title="Toggle Fullscreen"]').first.click()
    print('ERRS',errs); b.close()
