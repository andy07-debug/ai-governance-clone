import os, json
from playwright.sync_api import sync_playwright
URL='file:///Users/kumaraniket/Desktop/AI%20Governance%20Clone/clone/index.html'
VIEWS=['00-home','01-llm-analytics','02-firewall','03-live-events','04-policies','04b-policies-changelogs','04c-policies-newpolicy-modal','05-traffic','05a-traffic-projects','05b-traffic-project-usage','05c-traffic-model-config','05d-traffic-statistics','05e-traffic-applications','05f-traffic-errorlogs','06-rbac-access','06b-rbac-usergroups','06c-rbac-config-modules','06d-rbac-config-permissions','06e-rbac-config-roles','06f-rbac-config-mapping','07a-shell-mode-dropdown','07b-shell-hamburger','07c-shell-projects']
JS='''()=>{const m=document.getElementById('mount');const q=s=>m.querySelectorAll(s).length;
return {hash:location.hash, root:q('#root'), panels:q('[data-panel]'), side:q('#sidebar'), hdr:q('.h-20'), tf:q('[title="Toggle Fullscreen"]'), fsbox:q('.fixed.inset-0.z-20'), bubble:q('.maximizeChatButton'), ov:q('[data-overlay]'), handle:q('[data-resize-handle]'), dd:q('.h-20 .p-dropdown'), ham:q('[title="Open sidebar"]')}}'''
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    for v in VIEWS:
        pg.goto(URL+'#'+v); pg.wait_for_timeout(250)
        r=pg.evaluate(JS)
        t=pg.locator('[title="Toggle Fullscreen"]')
        if t.count():
            try:
                t.first.click(timeout=2000); pg.wait_for_timeout(200); r['fs']=pg.evaluate(JS)
            except Exception as e: r['fs']='ERR '+str(e)[:80]
        print(v, r)
    print(errs)
