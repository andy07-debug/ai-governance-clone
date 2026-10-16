import os, re, difflib, json
from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
URL='file://'+ROOT+'/clone/index.html'
VIEWS=['05-traffic','05a-traffic-projects','05b-traffic-project-usage','05c-traffic-model-config','05d-traffic-statistics','05e-traffic-applications','05f-traffic-errorlogs']
OUT=os.path.dirname(os.path.abspath(__file__))
def cap_html(v):
    p=open(f'{ROOT}/capture/{v}/page.html',encoding='utf-8').read()
    p=re.sub(r'<link[^>]*>','',p)
    p=re.sub(r'<div id="claude-agent-glow-border".*?</div></div>','',p,flags=re.S)
    p=re.sub(r'<div id="claude-phantom-cursor".*?</svg></div>','',p,flags=re.S)
    css=open(f'{ROOT}/capture/{v}/styles.css',encoding='utf-8').read()
    css=re.sub(r'url\([^)]*\)','none',css)
    return p.replace('</head>','<style>'+css+'</style></head>',1)
with sync_playwright() as pw:
    b=pw.chromium.launch(); 
    for v in VIEWS:
        pg=b.new_page(viewport={'width':1920,'height':936})
        pg.route('**/*', lambda r: r.abort() if not r.request.url.startswith(('file:','data:','about:')) else r.continue_())
        errs=[]
        pg.on('console', lambda m: errs.append(m.type+': '+m.text) if m.type in('error','warning') else None)
        pg.on('pageerror', lambda e: errs.append('pageerror: '+str(e)))
        pg.goto(URL+'#'+v); pg.wait_for_timeout(600)
        ct=pg.evaluate("document.getElementById('root').innerText")
        pg2=b.new_page(viewport={'width':1920,'height':936})
        pg2.route('**/*', lambda r: r.abort())
        pg2.set_content(cap_html(v), wait_until='domcontentloaded'); pg2.wait_for_timeout(300)
        rt=pg2.evaluate("document.getElementById('root').innerText")
        a=[l.strip() for l in rt.split('\n') if l.strip()]; c=[l.strip() for l in ct.split('\n') if l.strip()]
        d=[x for x in difflib.unified_diff(a,c,'capture','clone',n=0,lineterm='') ]
        print('=====',v,'cap lines',len(a),'clone lines',len(c),'errors',errs[:5])
        print('\n'.join(d[:40]))
        pg.close(); pg2.close()
    b.close()
