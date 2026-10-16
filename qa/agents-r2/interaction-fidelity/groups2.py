import os
from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
URL='file://'+ROOT+'/clone/index.html'
VIEWS=['00-home','01-llm-analytics','02-firewall','03-live-events','04-policies','04b-policies-changelogs','04c-policies-newpolicy-modal','05-traffic','05a-traffic-projects','05b-traffic-project-usage','05c-traffic-model-config','05d-traffic-statistics','05e-traffic-applications','05f-traffic-errorlogs','06-rbac-access','06b-rbac-usergroups','06c-rbac-config-modules','06d-rbac-config-permissions','06e-rbac-config-roles','06f-rbac-config-mapping','07c-shell-projects']
JS = """() => { const seen=new Set(), out=[]; document.querySelectorAll('button').forEach(b=>{ const p=b.parentElement; if(!p||seen.has(p))return; seen.add(p);
 const s=[...p.children].filter(e=>e.tagName==='BUTTON'); if(s.length<2) return;
 out.push({n:s.length, side:!!b.closest('#sidebar'), hdr:!!b.closest('.h-20'), t:s.map(x=>((x.textContent||'').replace(/\\s+/g,' ').trim().slice(0,22)||x.getAttribute('title')||x.getAttribute('aria-label')||'[icon]'))}); }); return out; }"""
with sync_playwright() as pw:
    br=pw.chromium.launch(); pg=br.new_page(viewport={'width':1920,'height':936})
    for v in VIEWS:
        pg.goto('about:blank'); pg.goto(URL+'#'+v); pg.wait_for_timeout(250)
        for g in pg.evaluate(JS):
            if g['side'] or g['hdr']: continue
            print(v, g['n'], g['t'])
