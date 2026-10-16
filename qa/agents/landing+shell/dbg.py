from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
URL='file://'+ROOT+'/clone/index.html'
OUT=ROOT+'/qa/agents/landing+shell/'
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    pg.goto(URL+'#07a-shell-mode-dropdown'); pg.wait_for_timeout(400)
    print(pg.evaluate("location.href"), pg.evaluate("document.querySelectorAll('[data-panel]').length"))
    pg.evaluate("""()=>{window.__log=[];const o=window.__show;window.__show=function(n,p){__log.push(n);return o(n,p)}}""")
    pg.mouse.click(1874,110); pg.wait_for_timeout(300)
    print(pg.evaluate("location.hash"), pg.evaluate("document.querySelectorAll('[data-panel]').length"), pg.evaluate("document.fullscreenElement&&document.fullscreenElement.tagName"))
    print(pg.evaluate("document.body.innerText.slice(0,300)"))
    pg.screenshot(path=OUT+'dbg.png')
    # same from fresh goto without reload difference
    pg2=b.new_page(viewport={'width':1920,'height':936}); pg2.goto(URL+'#00-home'); pg2.wait_for_timeout(300)
    pg2.mouse.click(1874,110); pg2.wait_for_timeout(300); print('home fullscreen click ->',pg2.evaluate("location.hash"), pg2.evaluate("document.querySelectorAll('[data-panel]').length")); pg2.screenshot(path=OUT+'dbg-home-fs.png')
    b.close()
