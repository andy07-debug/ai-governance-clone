import os
from playwright.sync_api import sync_playwright
from sweep import URL, VIEWS
JS = """() => { const seen=new Set(), out=[]; document.querySelectorAll('button').forEach(b=>{ const p=b.parentElement; if(!p||seen.has(p))return; seen.add(p);
 const s=[...p.children].filter(e=>e.tagName==='BUTTON'); if(s.length<2) return;
 out.push({n:s.length, side:!!b.closest('#sidebar'), t:s.map(x=>((x.textContent||'').replace(/\\s+/g,' ').trim().slice(0,22)||x.getAttribute('title')||x.getAttribute('aria-label')||'[icon]')), c:s.map(x=>x.className.length)}); }); return out; }"""
with sync_playwright() as pw:
    br=pw.chromium.launch(); pg=br.new_page(viewport={'width':1920,'height':936})
    for v in VIEWS:
        pg.goto(URL+'#'+v); pg.reload(); pg.wait_for_timeout(200)
        for g in pg.evaluate(JS):
            if g['side']: continue
            print(v, g['n'], g['t'])
