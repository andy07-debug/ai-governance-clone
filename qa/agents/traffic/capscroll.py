import os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
from scroll import JS, VIEWS
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
def cap_html(v):
    p=open(f'{ROOT}/capture/{v}/page.html',encoding='utf-8').read()
    p=re.sub(r'<link[^>]*>','',p)
    p=re.sub(r'<div id="claude-agent-glow-border".*?</div></div>','',p,flags=re.S)
    p=re.sub(r'<div id="claude-phantom-cursor".*?</svg></div>','',p,flags=re.S)
    css=open(f'{ROOT}/capture/{v}/styles.css',encoding='utf-8').read()
    css=re.sub(r'url\((?!"?data:)[^)]*\)','none',css)
    return p.replace('</head>','<style>'+css+'</style></head>',1)
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    pg.route('**/*', lambda r: r.abort())
    for v in VIEWS:
        pg.set_content(cap_html(v)); pg.wait_for_timeout(300)
        r=pg.evaluate(JS)
        print('=====',v,'doc',r['docScroll'])
        for s in r['out']: print('  ',s)
        pg.screenshot(path=os.path.dirname(os.path.abspath(__file__))+f'/cap-{v}.png')
    b.close()
