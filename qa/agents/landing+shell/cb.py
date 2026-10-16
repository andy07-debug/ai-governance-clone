from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
URL='file://'+ROOT+'/clone/index.html'
OUT=ROOT+'/qa/agents/landing+shell/'
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    pg.goto(URL+'#07c-shell-projects'); pg.wait_for_timeout(800)
    st=lambda: pg.evaluate("(()=>{const i=document.querySelector('.p-checkbox-input');const c=i.closest('.p-checkbox');return {checked:i.checked, cls:c.className, box:c.querySelector('.p-checkbox-box').className, opacity:getComputedStyle(i).opacity}})()")
    print('before',st())
    pg.mouse.click(1109,173); pg.wait_for_timeout(200); print('after click box',st())
    pg.screenshot(path=OUT+'cb.png', clip={'x':880,'y':150,'width':420,'height':50})
    b.close()
