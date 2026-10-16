import os, difflib
from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
URL='file://'+ROOT+'/clone/index.html'
OUT=ROOT+'/qa/agents/landing+shell'
views=['00-home','07a-shell-mode-dropdown','07b-shell-hamburger','07c-shell-projects']
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    errs=[]
    pg.on('console', lambda m: errs.append((m.type, m.text)) if m.type in ('error','warning') else None)
    pg.on('pageerror', lambda e: errs.append(('pageerror', str(e))))
    pg.on('requestfailed', lambda r: errs.append(('reqfail', r.url[:120])))
    for v in views:
        pg.goto(URL+'#'+v); pg.wait_for_timeout(600)
        c=pg.evaluate("document.body.innerText")
        pg2=b.new_page(viewport={'width':1920,'height':936}); pg2.goto('file://'+ROOT+'/qa/base/'+v+'.html'); pg2.wait_for_timeout(400)
        base=pg2.evaluate("document.body.innerText"); pg2.close()
        cl=[l.strip() for l in c.split('\n') if l.strip()]; bl=[l.strip() for l in base.split('\n') if l.strip()]
        d=[x for x in difflib.unified_diff(bl,cl,lineterm='',n=0) if not x.startswith(('---','+++','@@'))]
        print('==',v,'lines clone',len(cl),'base',len(bl),'diff',len(d))
        for x in d[:40]: print('  ',x)
    print('errors',errs)
    b.close()
