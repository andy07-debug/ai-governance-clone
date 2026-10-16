from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
URL='file://'+ROOT+'/clone/index.html'
OUT=ROOT+'/qa/agents/landing+shell/'
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    pg.goto(URL+'#00-home'); pg.wait_for_timeout(300)
    pg.locator('[title="Toggle Fullscreen"]').click(); pg.wait_for_timeout(400)
    pg.locator('.maximizeChatButton').click(); pg.wait_for_timeout(3000)
    pg.screenshot(path=OUT+'fs-exit-3s.png')
    print('greeting', pg.evaluate("document.body.innerText.includes('Hey Kumar')"))
    b.close()
