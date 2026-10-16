from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
URL='file://'+ROOT+'/clone/index.html'
OUT=ROOT+'/qa/agents/skeptic-shell/'
with sync_playwright() as pw:
    b=pw.chromium.launch()
    def fresh(v):
        p=b.new_page(viewport={'width':1920,'height':936}); p.set_default_timeout(4000); p.goto(URL+'#'+v); p.wait_for_timeout(500); return p
    p=fresh('00-home')
    w0=p.evaluate("document.querySelector('[data-panel]').getBoundingClientRect().width")
    hd=p.locator('[data-resize-handle]').first.bounding_box(); print('F8 handle', hd)
    p.mouse.move(hd['x']+hd['width']/2, 500); p.mouse.down(); p.mouse.move(hd['x']-164,500,steps=10); p.mouse.up()
    print('F8 width', w0, p.evaluate("document.querySelector('[data-panel]').getBoundingClientRect().width"))
    p.locator('[title="Expand to right"], button:has-text("Expand to right")').count()
    print('F8 expand btns', p.evaluate("[...document.querySelectorAll('[title]')].map(e=>e.title).filter(t=>/Expand|Chat|New/i.test(t))"))
    p=fresh('07c-shell-projects')
    q="(()=>{const c=document.querySelector('.p-checkbox');return [c.className,c.querySelector('.p-checkbox-box').className,c.querySelector('input').checked,c.querySelector('.p-checkbox-box').innerHTML.length]})()"
    print('F9 before', p.evaluate(q))
    p.locator('.p-checkbox').first.click(); p.wait_for_timeout(200)
    print('F9 after', p.evaluate('location.hash'), p.evaluate(q))
    p.screenshot(path=OUT+'f9.png', clip={'x':1000,'y':140,'width':300,'height':70})
    # F2 alternate escape routes from 07c
    p=fresh('00-home'); p.locator('[data-testid="headerProjectsButton"]').click(); p.wait_for_timeout(200)
    print('07c hash', p.evaluate('location.hash'))
    p.locator('.h-20 .p-dropdown').click(); p.wait_for_timeout(200); p.keyboard.press('Escape'); p.wait_for_timeout(200)
    print('dropdown+esc', p.evaluate('location.hash'))
    p.locator('.h-20 img, .h-20 a').first.click(); p.wait_for_timeout(200); print('logo', p.evaluate('location.hash'))
    b.close()
