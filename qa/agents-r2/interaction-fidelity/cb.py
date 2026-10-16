from playwright.sync_api import sync_playwright
URL='file:///Users/kumaraniket/Desktop/AI Governance Clone/clone/index.html'
ST="()=>{const c=document.querySelector('.p-checkbox');const i=c.querySelector('input');const b=c.querySelector('.p-checkbox-box');return [i.checked,c.classList.contains('p-highlight'),!!b.querySelector('svg'),getComputedStyle(b).backgroundColor,location.hash]}"
with sync_playwright() as pw:
    br=pw.chromium.launch(); pg=br.new_page(viewport={'width':1920,'height':936})
    pg.goto(URL+'#07c-shell-projects'); pg.wait_for_timeout(300)
    print(pg.evaluate("()=>document.querySelector('.p-checkbox').parentElement.outerHTML.replace(/<svg[\\s\\S]*?<\\/svg>/g,'<svg/>').slice(0,1500)"))
    bb=pg.locator('.p-checkbox-box').bounding_box(); print(bb)
    for k in range(5):
        pg.mouse.click(bb['x']+bb['width']/2, bb['y']+bb['height']/2); pg.wait_for_timeout(750); print('box click',k,pg.evaluate(ST))
    lab=pg.locator('label[for="subProjectCheck"]')
    print('label count',lab.count())
    for k in range(4):
        if lab.count(): lab.first.click(); pg.wait_for_timeout(750); print('label click',k,pg.evaluate(ST))
    pg.screenshot(path='cb.png', clip={'x':bb['x']-300,'y':bb['y']-40,'width':700,'height':100})
    br.close()
