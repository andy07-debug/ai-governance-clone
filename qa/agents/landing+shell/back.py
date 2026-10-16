from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
URL='file://'+ROOT+'/clone/index.html'
OUT=ROOT+'/qa/agents/landing+shell/'
h=lambda p:p.evaluate('location.href.split("/").pop()')
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    pg.goto('about:blank'); pg.goto(URL+'#00-home'); pg.wait_for_timeout(300)
    pg.locator('[data-testid="headerProjectsButton"]').click(); pg.wait_for_timeout(150); print('at',h(pg), 'history.length', pg.evaluate('history.length'))
    pg.go_back(); pg.wait_for_timeout(300); print('after browser Back ->', pg.url)
    # dead-end check
    pg.goto(URL+'#00-home'); pg.wait_for_timeout(300)
    pg.locator('[data-testid="headerProjectsButton"]').click(); pg.wait_for_timeout(150)
    pg.locator('.h-20 .p-dropdown').click(); pg.wait_for_timeout(150)
    pg.keyboard.press('Escape'); pg.wait_for_timeout(150); print('07c->dropdown->Esc', h(pg))
    pg.locator('.h-20 .p-dropdown').click(); pg.wait_for_timeout(150)
    pg.locator('.p-dropdown-panel li', has_text='AI Governance').first.click(); pg.wait_for_timeout(150); print('07c->dropdown->AI Governance', h(pg))
    pg.mouse.click(201,32); pg.wait_for_timeout(150); print('logo', h(pg))
    pg.locator('[data-testid="headerProjectsButton"]').click(); pg.wait_for_timeout(150); print('Projects again', h(pg))
    print('trigger label in 07c:', pg.evaluate("document.querySelector('.h-20 .p-dropdown').innerText"))
    b.close()
