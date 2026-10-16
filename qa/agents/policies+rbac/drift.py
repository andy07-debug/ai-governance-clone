import os, re, sys, difflib
from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
VIEWS='04-policies 04b-policies-changelogs 04c-policies-newpolicy-modal 06-rbac-access 06b-rbac-usergroups 06c-rbac-config-modules 06d-rbac-config-permissions 06e-rbac-config-roles 06f-rbac-config-mapping'.split()
OUT=os.path.dirname(os.path.abspath(__file__))
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    errs=[]; pg.on('console', lambda m: errs.append((m.type, m.text)) if m.type in ('error','warning') else None); pg.on('pageerror', lambda e: errs.append(('pageerror', str(e))))
    for v in VIEWS:
        pg.goto('file://'+ROOT+'/clone/index.html#'+v); pg.wait_for_timeout(400)
        ct=pg.evaluate("(document.getElementById('root')||document.body).innerText")
        pg.goto('file://'+ROOT+'/qa/base/'+v+'.html'); pg.wait_for_timeout(400)
        bt=pg.evaluate("(document.getElementById('root')||document.body).innerText")
        cl=[l.strip() for l in ct.split('\n') if l.strip()]; bl=[l.strip() for l in bt.split('\n') if l.strip()]
        d=[x for x in difflib.unified_diff(bl,cl,lineterm='',n=0) if not x.startswith(('---','+++','@@'))]
        print('==',v,len(bl),len(cl),'diff lines',len(d)); print('\n'.join(d[:40]))
    print('console', errs)
