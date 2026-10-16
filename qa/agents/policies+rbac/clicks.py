from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
VIEWS='04-policies 04b-policies-changelogs 04c-policies-newpolicy-modal 06-rbac-access'.split()
SEL='[data-panel]:last-of-type button, [data-panel]:last-of-type a, [data-panel]:last-of-type [role=button], [data-panel]:last-of-type .cursor-pointer, [data-panel]:last-of-type select, [data-panel]:last-of-type input, [data-panel]:last-of-type textarea, body > div:not(#root) button'
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936}); pg.set_default_timeout(2000)
    errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
    for v in VIEWS:
        pg.goto('file://'+ROOT+'/clone/index.html#'+v); pg.wait_for_timeout(300)
        n=pg.locator(SEL).count()
        print('=====',v,n)
        for i in range(n):
            pg.goto('file://'+ROOT+'/clone/index.html#'+v); pg.reload(); pg.wait_for_timeout(150)
            loc=pg.locator(SEL).nth(i)
            try:
                info=loc.evaluate("e=>{const r=e.getBoundingClientRect();return [e.tagName,(e.innerText||e.placeholder||e.getAttribute('aria-label')||e.title||'').replace(/\\s+/g,' ').slice(0,40),Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)]}")
            except Exception as ex: print(i,'ERR info'); continue
            if info[4]==0: continue
            before=pg.evaluate("document.getElementById('mount').innerHTML")
            try: loc.click(timeout=1500)
            except Exception as ex: print(i,info,'CLICKFAIL',str(ex).split('\n')[0][:100]); continue
            pg.wait_for_timeout(120)
            h=pg.evaluate('location.hash.slice(1)')
            after=pg.evaluate("document.getElementById('mount').innerHTML")
            res='NAV->'+h if h!=v else ('DOMCHANGE' if after!=before else 'none')
            print(i,info,res)
    print('errs',errs)
