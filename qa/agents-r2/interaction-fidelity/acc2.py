from playwright.sync_api import sync_playwright
URL='file:///Users/kumaraniket/Desktop/AI Governance Clone/clone/index.html'
with sync_playwright() as pw:
    br=pw.chromium.launch(); pg=br.new_page(viewport={'width':1920,'height':936})
    pg.goto(URL+'#05c-traffic-model-config'); pg.wait_for_timeout(300)
    pg.locator('a.p-accordion-header-link').first.click(); pg.wait_for_timeout(800)
    tb=pg.locator('a.p-accordion-header-link').first.bounding_box()
    pg.screenshot(path='acc_collapsed.png', clip={'x':tb['x'],'y':tb['y']-5,'width':tb['width'],'height':240})
    br.close()
