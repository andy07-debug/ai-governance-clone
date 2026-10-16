"""Recover the exact data behind the captured chart bitmaps by re-rendering them with the live app's
Chart.js 4.5.1 config and fitting values to minimise the pixel difference."""
import os, json, base64
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b64 = lambda p: base64.b64encode(open(os.path.join(ROOT, p), 'rb').read()).decode()

HARNESS = r"""
async ({img, w, h, cfgSrc, fit}) => {
  document.body.innerHTML = `<div id=box style="position:relative;width:${w}px;height:${h}px"><canvas id=c></canvas></div>`;
  const ref = await new Promise(r => { const i = new Image(); i.onload = () => r(i); i.src = 'data:image/png;base64,' + img; });
  const rc = document.createElement('canvas'); rc.width = ref.width; rc.height = ref.height;
  const rx = rc.getContext('2d'); rx.drawImage(ref, 0, 0); const R = rx.getImageData(0, 0, rc.width, rc.height).data;
  const cfg = (new Function('return ' + cfgSrc))();
  cfg.options.animation = false; cfg.options.devicePixelRatio = 1;
  if (fit.yMax) cfg.options.scales.y.max = fit.yMax;
  const chart = new Chart(document.getElementById('c'), cfg);
  const cv = document.getElementById('c');
  const diff = (x0, x1) => { chart.update('none'); const D = cv.getContext('2d').getImageData(0, 0, cv.width, cv.height).data;
    let s = 0; const W = cv.width;
    for (let y = 0; y < cv.height; y++) for (let x = (x0 ?? 0); x < (x1 ?? W); x++) { const k = (y * W + x) * 4;
      s += Math.abs(D[k]-R[k]) + Math.abs(D[k+1]-R[k+1]) + Math.abs(D[k+2]-R[k+2]) + Math.abs(D[k+3]-R[k+3]); }
    return s; };
  const data = chart.data.datasets[0].data;
  const log = [];
  for (let pass = 0; pass < 3; pass++) {
    for (const i of fit.indices) {
      const xc = Math.round(chart.scales.x.getPixelForValue(i)); const x0 = Math.max(0, xc - fit.halfWin), x1 = Math.min(cv.width, xc + fit.halfWin);
      let best = data[i], bestS = diff(x0, x1);
      for (let step of fit.steps) {
        let improved = true;
        while (improved) { improved = false;
          for (const cand of [best - step, best + step]) { if (cand < 0) continue; data[i] = cand; const s = diff(x0, x1); if (s < bestS) { bestS = s; best = cand; improved = true; } }
          data[i] = best; }
      }
      data[i] = Math.round(best / fit.quantum) * fit.quantum;
      log.push([pass, i, data[i]]);
    }
  }
  if (fit.yMax) { delete chart.options.scales.y.max; }
  const total = diff();
  const D2 = cv.getContext('2d').getImageData(0,0,cv.width,cv.height); const out = new ImageData(cv.width, cv.height);
  for (let k=0;k<D2.data.length;k+=4){ const d=Math.abs(D2.data[k]-R[k])+Math.abs(D2.data[k+1]-R[k+1])+Math.abs(D2.data[k+2]-R[k+2])+Math.abs(D2.data[k+3]-R[k+3]);
    const g = 255 - Math.min(255, (R[k+3]? (R[k]+R[k+1]+R[k+2])/3 : 255)) ; out.data[k]= d>40?255:230; out.data[k+1]=d>40?0:230; out.data[k+2]=d>40?0:230; out.data[k+3]=255; }
  const oc=document.createElement('canvas'); oc.width=cv.width; oc.height=cv.height; oc.getContext('2d').putImageData(out,0,0);
  const diffPng = oc.toDataURL().split(',')[1]; const renderPng = cv.toDataURL().split(',')[1]; const nonzero = (() => { const D = cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data; let n=0; for (let k=0;k<D.length;k+=4){ if (Math.abs(D[k]-R[k])+Math.abs(D[k+1]-R[k+1])+Math.abs(D[k+2]-R[k+2])+Math.abs(D[k+3]-R[k+3])>40) n++; } return n; })();
  return { diffPng, renderPng, size: [cv.width, cv.height], ref: [rc.width, rc.height], data: data.slice(), total, pixelsOff: nonzero, yMax: chart.scales.y.max };
}
"""

LINE_CFG = r"""{
  type: 'line',
  data: { labels: ['10/09','10/10','10/11','10/12','10/13','10/14','10/15'],
    datasets: [{ data: [530.0280780000003,45.579979,19.359871999999996,604.7357749999993,549.7861160000002,541.9825619999998,150],
      borderColor:'#7549F2', backgroundColor:'rgba(117, 73, 242, 0.12)', pointBackgroundColor:'#5928ED', pointBorderColor:'#ffffff',
      pointBorderWidth:2, pointRadius:4, pointHoverRadius:6, borderWidth:3, fill:true, tension:0.35 }] },
  options: { responsive:true, maintainAspectRatio:false, interaction:{intersect:false, mode:'index'}, plugins:{legend:{display:false}},
    scales: {
      x: { title:{display:true,text:'Date',color:'#64748b',font:{weight:'bold'}}, grid:{display:false}, ticks:{color:'#64748b'} },
      y: { beginAtZero:true, title:{display:true,text:'Cost (USD)',color:'#64748b',font:{weight:'bold'}}, grid:{color:'#e2e8f0'},
           ticks:{color:'#64748b', callback: v => '$' + Number(v).toLocaleString('en-US')} } } }
}"""

BAR_CFG = r"""{
  type: 'bar',
  data: { labels: ['11:11','11:12','11:13','11:14','11:15','11:16'],
    datasets: [{ label:'Total Requests', data:[130,170,190,200,175,150],
      backgroundColor: Array(6).fill('rgba(99, 102, 241, 0.6)'), borderColor: Array(6).fill('rgb(99, 102, 241)'), borderWidth: 1 }] },
  options: { maintainAspectRatio:false, plugins:{legend:{display:false}},
    scales: {
      x: { ticks:{color:'#666', maxRotation:45, autoSkip:true, maxTicksLimit:16}, grid:{color:'#eee'}, title:{display:true,text:'Time',color:'#999',font:{size:11}} },
      y: { beginAtZero:true, ticks:{color:'#666'}, grid:{color:'#eee'}, title:{display:true,text:'Requests',color:'#999',font:{size:11}} } } }
}"""

JOBS = [
  ('01-llm-analytics', 'qa/charts/01-llm-analytics-0.png', 916.8, 268, LINE_CFG, {'indices': [6], 'steps': [64, 16, 4, 1, 0.25, 0.05], 'quantum': 0.01, 'halfWin': 60}),
  ('05b-traffic-project-usage', 'qa/charts/05b-traffic-project-usage-0.png', 440.4, 300, BAR_CFG, {'indices': [0,1,2,3,4,5], 'steps': [32, 8, 2, 1], 'quantum': 1, 'halfWin': 30, 'yMax': 250}),
  ('05d-traffic-statistics', 'qa/charts/05d-traffic-statistics-0.png', 440.4, 300, BAR_CFG, {'indices': [0,1,2,3,4,5], 'steps': [32, 8, 2, 1], 'quantum': 1, 'halfWin': 30, 'yMax': 250}),
]
out = {}
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(device_scale_factor=1)
    pg.goto('about:blank'); pg.add_script_tag(path=os.path.join(ROOT, 'clone/assets/chart.umd.min.js'))
    for name, img, w, h, cfg, fit in JOBS:
        r = pg.evaluate(HARNESS, {'img': b64(img), 'w': w, 'h': h, 'cfgSrc': cfg, 'fit': fit})
        for k in ('diffPng', 'renderPng'):
            open(os.path.join(ROOT, 'qa/charts/%s-%s.png' % (name, k)), 'wb').write(base64.b64decode(r.pop(k)))
        out[name] = r
        print(name, json.dumps(r))
    b.close()
json.dump(out, open(os.path.join(ROOT, 'qa/charts/fit.json'), 'w'), indent=1)
