from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
URL='file://'+ROOT+'/clone/index.html'
OUT=ROOT+'/qa/agents/landing+shell/'
JS="""()=>[...document.querySelectorAll('[data-panel]')[0].querySelectorAll('*')].map(e=>[e,getComputedStyle(e)]).filter(([e,c])=>c.animationName!=='none').map(([e,c])=>e.tagName+'.'+String(e.className).slice(0,60)+' | '+c.animationName+' '+c.animationDuration+' delay '+c.animationDelay+' iter '+c.animationIterationCount+' op '+c.opacity+' txt='+e.textContent.slice(0,30))"""
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    pg.goto(URL+'#00-home'); pg.wait_for_timeout(50)
    for i,t in enumerate([50,400,1000,2000,4000,8000]):
        if i: pg.wait_for_timeout(t-prev)
        prev=t
        pg.screenshot(path=OUT+f'tl-{t}.png', clip={'x':0,'y':140,'width':864,'height':796})
    for x in pg.evaluate(JS): print(x)
    b.close()
