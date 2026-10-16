from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
URL='file://'+ROOT+'/clone/index.html'
OUT=ROOT+'/qa/agents/landing+shell/'
h=lambda p:p.evaluate('location.hash.slice(1)')
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    pg.goto(URL+'#00-home'); pg.wait_for_timeout(2500)
    pg.locator('textarea').click(); pg.keyboard.type('Show me firewall stats'); pg.wait_for_timeout(200)
    pg.screenshot(path=OUT+'P0-typed.png')
    pg.locator('.h-20 .p-dropdown').click(); pg.wait_for_timeout(120)
    pg.screenshot(path=OUT+'P1-dropdown-120ms.png')
    print('in 07a textarea value:', repr(pg.locator('textarea').first.input_value()), h(pg))
    pg.keyboard.press('Escape'); pg.wait_for_timeout(120)
    print('after Esc textarea value:', repr(pg.locator('textarea').first.input_value()), h(pg))
    pg.screenshot(path=OUT+'P2-after-esc-120ms.png')
    # card opacity right after toggle
    pg.locator('.h-20 button[title="Open sidebar"]').click(); pg.wait_for_timeout(80)
    print('07b card opacities 80ms:', pg.evaluate("[...document.querySelectorAll('h3')].map(e=>getComputedStyle(e.closest('button')).opacity.slice(0,4))"))
    print('07b greeting opacity:', pg.evaluate("getComputedStyle(document.querySelector('.delayed-messages')).opacity"))
    b.close()
