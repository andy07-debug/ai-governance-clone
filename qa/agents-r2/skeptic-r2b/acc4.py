import os
from playwright.sync_api import sync_playwright
URL='file://'+os.path.abspath('clone/index.html'); OUT=os.path.abspath('qa/agents-r2/skeptic-r2b')
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    pg.goto(URL+'#05c-traffic-model-config'); pg.wait_for_timeout(500)
    h=pg.locator('.p-accordion-header-link').first; bb=h.bounding_box()
    pg.mouse.click(bb['x']+bb['width']*0.6,bb['y']+bb['height']/2); pg.wait_for_timeout(750)
    print(pg.evaluate('''()=>{const s=document.querySelector('.p-accordion-toggle-icon');s.style.transform='rotate(0deg)';}'''))
    pg.wait_for_timeout(500); print(pg.evaluate("getComputedStyle(document.querySelector('.p-accordion-toggle-icon')).transform"))
    pg.wait_for_timeout(300); bb=h.bounding_box()
    pg.screenshot(path=OUT+'/f2_fixed.png',clip={'x':bb['x']+bb['width']-200,'y':bb['y'],'width':200,'height':bb['height']*2+20})
