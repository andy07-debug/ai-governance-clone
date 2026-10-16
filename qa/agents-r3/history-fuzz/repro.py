from playwright.sync_api import sync_playwright
BASE='file:///Users/kumaraniket/Desktop/AI%20Governance%20Clone/clone/index.html'
with sync_playwright() as pw:
    b=pw.chromium.launch()
    def fresh(h=''):
        pg=b.new_page(viewport={'width':1920,'height':936}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto(BASE+('#'+h if h else '')); pg.wait_for_timeout(400); return pg
    S=lambda pg:(pg.evaluate('location.hash'), pg.evaluate('__cloneState()'), pg.locator('.animate-slideUp').count(), pg.evaluate('history.length'))
    # R1
    pg=fresh(); pg.click('h3:text-is("Policies")'); pg.wait_for_timeout(300); print('R1 policies',S(pg))
    pg.get_by_role('button',name='New Policy').first.click(); pg.wait_for_timeout(900); print('R1 modal open',S(pg))
    pg.reload(); pg.wait_for_timeout(500); print('R1 after reload',S(pg))
    pg.keyboard.press('Escape'); pg.wait_for_timeout(900); print('R1 esc',S(pg))
    pg.get_by_role('button',name='New Policy').first.click(); pg.wait_for_timeout(900)
    pg.go_back(); pg.wait_for_timeout(500); print('R1 back',S(pg))
    pg.go_forward(); pg.wait_for_timeout(900); print('R1 forward',S(pg))
    pg.close()
    # R2 changelogs path
    pg=fresh('04-policies'); pg.get_by_role('button',name='Change Logs').first.click(); pg.wait_for_timeout(300)
    pg.get_by_role('button',name='Policies Deck').first.click(); pg.wait_for_timeout(300)
    pg.get_by_role('button',name='New Policy').first.click(); pg.wait_for_timeout(300)
    pg.go_back(); pg.wait_for_timeout(500); print('R2 back',S(pg)); pg.go_forward(); pg.wait_for_timeout(900); print('R2 fwd',S(pg)); pg.close()
    # R3 typed unknown/overlay hash -> duplicate entry, dead Back
    for typed in ['nope','07a-shell-mode-dropdown']:
        pg=fresh(); pg.click('h3:text-is("Live Events")'); pg.wait_for_timeout(300)
        h0=pg.evaluate('history.length')
        pg.evaluate('h=>location.hash=h',typed); pg.wait_for_timeout(400)
        print('R3',typed,'after typed',S(pg),'len before',h0)
        if typed=='nope': pg.locator('.h-20 .p-dropdown').click(); pg.wait_for_timeout(300)
        pg.go_back(); pg.wait_for_timeout(500); print('R3',typed,'after 1st Back',S(pg),'dd panels',pg.locator('.p-dropdown-panel').count())
        pg.go_back(); pg.wait_for_timeout(500); print('R3',typed,'after 2nd Back',S(pg),'dd panels',pg.locator('.p-dropdown-panel').count())
        pg.close()
    # R4 fullscreen then reach 07c
    pg=fresh('03-live-events'); pg.click('[title="Toggle Fullscreen"]'); pg.wait_for_timeout(900)
    pg.evaluate('location.hash="#07c-shell-projects"'); pg.wait_for_timeout(1000)
    print('R4', S(pg), 'bubble',pg.locator('.maximizeChatButton').count(),'box',pg.locator('.fixed.inset-0.z-20').count(),'tf',pg.locator('[title="Toggle Fullscreen"]').count(),
      pg.evaluate("[...document.querySelectorAll('[data-panel]')].map(p=>p.getAttribute('data-panel-size')+':'+Math.round(p.getBoundingClientRect().width))"))
    pg.screenshot(path='r4-07c-fs.png')
    pg.click('.maximizeChatButton'); pg.wait_for_timeout(900)
    print('R4 after bubble', pg.evaluate("[...document.querySelectorAll('[data-panel]')].map(p=>p.getAttribute('data-panel-size')+':'+Math.round(p.getBoundingClientRect().width))"))
    b.close()
