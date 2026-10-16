import os, re, sys, difflib
from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
OUT=os.path.dirname(os.path.abspath(__file__))
views=['01-llm-analytics','02-firewall','03-live-events']
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    errs=[]
    pg.on('console', lambda m: errs.append((m.type, m.text)) if m.type in ('error','warning') else None)
    pg.on('pageerror', lambda e: errs.append(('pageerror', str(e))))
    for v in views:
        pg.goto('file://'+ROOT+'/clone/index.html#'+v); pg.wait_for_timeout(600)
        c=pg.evaluate("document.querySelector('#root') ? document.querySelector('#root').innerText : 'NO ROOT'")
        pg.goto('file://'+ROOT+'/qa/base/'+v+'.html'); pg.wait_for_timeout(600)
        a=pg.evaluate("document.querySelector('#root') ? document.querySelector('#root').innerText : 'NO ROOT'")
        cl=[l.strip() for l in c.splitlines() if l.strip()]; al=[l.strip() for l in a.splitlines() if l.strip()]
        d=[l for l in difflib.unified_diff(al,cl,'capture','clone',lineterm='',n=0)]
        print('==',v,len(al),len(cl),'difflines',len(d)); print('\n'.join(d[:80]))
    print('ERRS',errs)
    b.close()
