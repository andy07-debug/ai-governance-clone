from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
URL='file://'+ROOT+'/clone/index.html'
OUT=ROOT+'/qa/agents/landing+shell/'
h=lambda p:p.evaluate('location.hash.slice(1)')
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    errs=[]; pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: errs.append(m.text) if m.type=='error' else None)
    pg.goto(URL+'#00-home'); pg.wait_for_timeout(300)
    pg.locator('[title="Toggle Fullscreen"]').click(); pg.wait_for_timeout(1500); pg.screenshot(path=OUT+'fs-home.png')
    print('cards visible', pg.evaluate("[...document.querySelectorAll('main h3, h3')].map(e=>e.textContent+':'+getComputedStyle(e.closest('button')||e).opacity)"))
    # navigate into a card while fullscreen
    pg.get_by_text('Policies', exact=True).first.click(); pg.wait_for_timeout(800); print('fs card ->',h(pg)); pg.screenshot(path=OUT+'fs-policies.png')
    pg.locator('main button[title="Back to home"], main span.p-1.text-indigo-600').first.click(); pg.wait_for_timeout(500); print('fs home ->',h(pg))
    # close messages
    pg.locator('[aria-label="Close messages"]').click(); pg.wait_for_timeout(200)
    print('bubble msgs left', pg.evaluate("document.body.innerText.includes(\"I'm here\")"))
    pg.locator('.maximizeChatButton').click(); pg.wait_for_timeout(500); print('after chat btn ->',h(pg), 'panels', pg.evaluate("document.querySelectorAll('[data-panel]').length"))
    pg.screenshot(path=OUT+'fs-exit.png')
    # toggle on/off repeatedly
    pg.locator('[title="Toggle Fullscreen"]').click(); pg.wait_for_timeout(300); pg.locator('[title="Toggle Fullscreen"]').click(); pg.wait_for_timeout(800); pg.screenshot(path=OUT+'fs-toggle-off.png')
    print('errors',errs)
    b.close()
