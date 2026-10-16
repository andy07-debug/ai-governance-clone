import os
from playwright.sync_api import sync_playwright
URL='file://'+os.path.abspath('clone/index.html'); OUT=os.path.abspath('qa/agents-r2/skeptic-r2b')
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    pg.goto(URL+'#05c-traffic-model-config'); pg.wait_for_timeout(500)
    h=pg.locator('.p-accordion-header-link').first; bb=h.bounding_box()
    pg.screenshot(path=OUT+'/f2_open.png',clip={'x':bb['x'],'y':bb['y'],'width':bb['width'],'height':bb['height']*2+20})
    pg.mouse.click(bb['x']+bb['width']*0.6,bb['y']+bb['height']/2); pg.wait_for_timeout(750)
    bb=h.bounding_box()
    pg.screenshot(path=OUT+'/f2_closed.png',clip={'x':bb['x'],'y':bb['y'],'width':bb['width'],'height':bb['height']*2+20})
    # css rule rotating svg
    print(pg.evaluate('''()=>{const out=[];for(const ss of document.styleSheets){try{for(const r of ss.cssRules){if(r.cssText&&/accordion/.test(r.cssText)&&/rotate|transform/.test(r.cssText))out.push(r.cssText.slice(0,200))}}catch(e){}}return out}'''))
