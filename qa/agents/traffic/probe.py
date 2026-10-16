import os, difflib
from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
URL='file://'+ROOT+'/clone/index.html'
OUT=os.path.dirname(os.path.abspath(__file__))
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
    # fullscreen diff
    pg.goto(URL+'#05-traffic'); pg.wait_for_timeout(300)
    a=pg.evaluate("document.getElementById('root').innerHTML")
    pg.click('button[title="Toggle Fullscreen"]'); pg.wait_for_timeout(300)
    c=pg.evaluate("document.getElementById('root').innerHTML")
    import re
    sm=difflib.SequenceMatcher(None,a,c,autojunk=False) if len(a)<200000 else None
    i=next(k for k in range(min(len(a),len(c))) if a[k]!=c[k]); print('fullscreen first diff', a[i-200:i+150]); print('-->',c[i-200:i+150])
    pg.screenshot(path=f'{OUT}/fullscreen.png')
    # accordion anchor
    pg.goto(URL+'#05c-traffic-model-config'); pg.wait_for_timeout(300)
    print('len history', pg.evaluate('history.length'))
    pg.get_by_text('claude-3-5-sonnet', exact=True).click(); pg.wait_for_timeout(300)
    print('hash after header click', pg.evaluate('location.hash'), 'history', pg.evaluate('history.length'))
    st=pg.evaluate("[...document.querySelectorAll('#root .overflow-y-auto')].map(e=>e.scrollTop)")
    print('scrollTops', st, 'id exists', pg.evaluate("!!document.getElementById('pr_id_185_content_1')"))
    pg.screenshot(path=f'{OUT}/accordion-click.png')
    pg.get_by_text('claude-3-5-haiku', exact=True).click(); pg.wait_for_timeout(300)
    print('hash after haiku click', pg.evaluate('location.hash'))
    pg.reload(); pg.wait_for_timeout(400)
    print('after reload hash', pg.evaluate('location.hash'), 'h3/crumb text:', pg.evaluate("document.querySelector('main') && document.querySelector('[data-panel]:last-of-type').innerText.slice(0,80)"))
    pg.screenshot(path=f'{OUT}/accordion-reload.png')
    # back button
    pg.goto(URL+'#05c-traffic-model-config'); pg.wait_for_timeout(300)
    pg.get_by_text('Run Model Test').first.click(); pg.wait_for_timeout(200)
    print('run model test hash', pg.evaluate('location.hash'))
    # spinner
    pg.goto(URL+'#05f-traffic-errorlogs'); pg.wait_for_timeout(300)
    info=pg.evaluate("""()=>{const P=[...document.querySelectorAll('[data-panel]')].pop(); return [...P.querySelectorAll('*')].filter(e=>getComputedStyle(e).animationName!='none').map(e=>[e.tagName,e.className.baseVal??e.className,getComputedStyle(e).animationName,getComputedStyle(e).animationDuration,getComputedStyle(e).animationPlayState,getComputedStyle(e).transform])}""")
    print('anims', info)
    t1=pg.evaluate("""()=>{const P=[...document.querySelectorAll('[data-panel]')].pop(); return [...P.querySelectorAll('*')].filter(e=>getComputedStyle(e).animationName!='none').map(e=>getComputedStyle(e).transform)}"""); pg.wait_for_timeout(270)
    t2=pg.evaluate("""()=>{const P=[...document.querySelectorAll('[data-panel]')].pop(); return [...P.querySelectorAll('*')].filter(e=>getComputedStyle(e).animationName!='none').map(e=>getComputedStyle(e).transform)}""")
    print(t1,t2)
    print('errs',errs)
    b.close()
