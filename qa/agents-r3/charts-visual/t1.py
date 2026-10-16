import os, json
from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
URL='file://'+ROOT+'/clone/index.html'
INFO = r"""() => {
  const inst = Object.values(Chart.instances);
  const cvs = [...document.querySelectorAll('canvas[data-chart]')];
  return { state: window.__cloneState(), hash: location.hash, nInst: inst.length, nCanvas: cvs.length,
    attached: inst.map(c => document.contains(c.canvas)),
    charts: cvs.map(cv => { const c = Chart.getChart(cv); if (!c) return {id: cv.dataset.chart, none: true};
      const r = cv.getBoundingClientRect(); const p = cv.parentElement.getBoundingClientRect();
      const cs = getComputedStyle(cv.parentElement);
      const ctx = cv.getContext('2d'); const d = ctx.getImageData(0,0,cv.width,cv.height).data; let n=0; for (let k=3;k<d.length;k+=4) if (d[k]>0) n++;
      return { id: cv.dataset.chart, labels: c.data.labels, data: c.data.datasets[0].data, ymax: c.scales.y.max, yticks: c.scales.y.ticks.map(t=>t.value),
        cssW: r.width, cssH: r.height, bw: cv.width, bh: cv.height, parentContentW: p.width - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight),
        parentContentH: p.height - parseFloat(cs.paddingTop) - parseFloat(cs.paddingBottom), chartW: c.width, chartH: c.height, painted: n, dpr: c.currentDevicePixelRatio }; }) };
}"""
errs=[]
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: m.type in ('error','warning') and errs.append(m.text))
    def info(tag):
        pg.wait_for_timeout(1300); r=pg.evaluate(INFO); print(tag, json.dumps(r)); return r
    for v in ['01-llm-analytics','05b-traffic-project-usage','05d-traffic-statistics']:
        pg.goto(URL+'#'+v); info('deeplink '+v)
    # in-app nav
    pg.goto(URL); pg.wait_for_timeout(500)
    home = lambda: pg.locator('main button[title="Back to home"], main span.p-1.text-indigo-600').first.click()
    for i in range(2):
        pg.get_by_text('LLM Studio Analytics', exact=True).click(); info('nav01 #%d'%i)
        home(); info('home after 01')
        pg.get_by_text('Traffic Analysis', exact=True).click(); pg.wait_for_timeout(300)
        pg.locator('main').get_by_text('Statistics', exact=True).first.click(); info('nav05d #%d'%i)
        pg.locator('main .p-breadcrumb-home').first.click(); pg.wait_for_timeout(300)
        pg.locator('main').get_by_text('Projects', exact=True).first.click(); pg.wait_for_timeout(300)
        pg.get_by_role('button', name='View Usage').first.click(); info('nav05b #%d'%i)
        pg.go_back(); pg.wait_for_timeout(300); pg.go_forward(); info('back/fwd 05b #%d'%i)
        pg.go_back(); pg.go_back(); pg.go_back(); pg.wait_for_timeout(300); info('back x3 -> ?')
        pg.go_forward(); info('fwd')
        home(); pg.wait_for_timeout(300)
    print('ERRS', errs)
    b.close()
