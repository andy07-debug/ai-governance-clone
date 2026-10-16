from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
URL='file://'+ROOT+'/clone/index.html'
OUT=ROOT+'/qa/agents/landing+shell/'
h=lambda p:p.evaluate('location.hash.slice(1)')
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
    # A: home -> Projects -> mode dropdown -> AI Governance
    pg.goto(URL+'#00-home'); pg.wait_for_timeout(300)
    pg.locator('[data-testid="headerProjectsButton"]').click(); pg.wait_for_timeout(150); print('A1',h(pg))
    pg.locator('.h-20 .p-dropdown').click(); pg.wait_for_timeout(150); print('A2',h(pg))
    pg.screenshot(path=OUT+'A2-dropdown-from-projects.png')
    pg.locator('.p-dropdown-panel li', has_text='AI Governance').first.click(); pg.wait_for_timeout(150); print('A3 after picking AI Governance:',h(pg))
    pg.screenshot(path=OUT+'A3-after-pick.png')
    # B: 07c -> hamburger -> background
    pg.goto(URL+'#00-home'); pg.reload(); pg.wait_for_timeout(300)
    pg.locator('[data-testid="headerProjectsButton"]').click(); pg.wait_for_timeout(150)
    pg.mouse.click(1880,40); pg.wait_for_timeout(150); print('B1',h(pg)); pg.screenshot(path=OUT+'B1-drawer-from-projects.png')
    # C: cost pill refresh
    pg.goto(URL+'#00-home'); pg.reload(); pg.wait_for_timeout(300)
    print(pg.evaluate("""()=>{const e=document.elementFromPoint(1821,40).closest('button');return e.outerHTML.slice(0,400)}"""))
    pg.mouse.click(1821,40); pg.wait_for_timeout(150); print('C refresh-in-cost-pill ->',h(pg))
    # D: 07a fullscreen click
    pg.goto(URL+'#07a-shell-mode-dropdown'); pg.reload(); pg.wait_for_timeout(300)
    print('D target',pg.evaluate("""()=>{const e=document.elementFromPoint(1874,110);return e.tagName+' '+(e.className.baseVal??e.className)+' panel?'+!!e.closest('.p-dropdown-panel')}"""))
    pg.mouse.click(1874,110); pg.wait_for_timeout(200); print('D after', h(pg)); pg.screenshot(path=OUT+'D-07a-click-fullscreen.png')
    # E: textarea typing on home
    pg.goto(URL+'#00-home'); pg.reload(); pg.wait_for_timeout(300)
    pg.locator('textarea').click(); pg.keyboard.type('hello world'); print('E textarea', pg.locator('textarea').input_value(), h(pg))
    pg.keyboard.press('Enter'); pg.wait_for_timeout(150); print('E after Enter', repr(pg.locator('textarea').input_value()), h(pg))
    # F: dropdown search typing + list scroll
    pg.goto(URL+'#07a-shell-mode-dropdown'); pg.reload(); pg.wait_for_timeout(300)
    pg.get_by_placeholder('Search mode...').click(); pg.keyboard.type('admin'); print('F search', pg.get_by_placeholder('Search mode...').input_value(), h(pg))
    print('F visible items', pg.evaluate("[...document.querySelectorAll('.p-dropdown-item')].length"))
    info=pg.evaluate("""()=>{const w=document.querySelector('.p-dropdown-items-wrapper')||document.querySelector('.p-dropdown-panel ul').parentElement;return {cls:w.className,sh:w.scrollHeight,ch:w.clientHeight,ov:getComputedStyle(w).overflowY,mh:getComputedStyle(w).maxHeight}}""")
    print('F wrapper',info)
    pg.mouse.move(841,500); pg.mouse.wheel(0,3000); pg.wait_for_timeout(300)
    print('F scrollTop',pg.evaluate("(document.querySelector('.p-dropdown-items-wrapper')||document.querySelector('.p-dropdown-panel ul').parentElement).scrollTop"))
    pg.screenshot(path=OUT+'F-dropdown-scrolled.png')
    # G: resize handle drag
    pg.goto(URL+'#00-home'); pg.reload(); pg.wait_for_timeout(300)
    print('G handle', pg.evaluate("""()=>{const e=document.elementFromPoint(864,500);return e.tagName+' '+e.className+' '+[...e.attributes].map(a=>a.name+'='+a.value.slice(0,40)).join(' ')}"""))
    w0=pg.evaluate("document.querySelectorAll('[data-panel]')[0].getBoundingClientRect().width")
    pg.mouse.move(864,500); pg.mouse.down(); pg.mouse.move(700,500,steps=10); pg.mouse.up(); pg.wait_for_timeout(200)
    w1=pg.evaluate("document.querySelectorAll('[data-panel]')[0].getBoundingClientRect().width")
    print('G left panel width',w0,'->',w1)
    # H: escape on 07b, drawer clicks
    print('errors',errs)
    b.close()
