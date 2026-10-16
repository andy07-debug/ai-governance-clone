from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
URL='file://'+ROOT+'/clone/index.html'
JS="""()=>[...document.querySelectorAll('*')].filter(e=>{const c=getComputedStyle(e);return /(auto|scroll)/.test(c.overflowY+c.overflowX)&&(e.scrollHeight>e.clientHeight+2||e.scrollWidth>e.clientWidth+2)}).map(e=>e.tagName+'.'+String(e.className).slice(0,50)+' sh='+e.scrollHeight+' ch='+e.clientHeight+' sw='+e.scrollWidth+' cw='+e.clientWidth)"""
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    for v in ['00-home','07a-shell-mode-dropdown','07b-shell-hamburger','07c-shell-projects']:
        pg.goto(URL+'#'+v); pg.reload(); pg.wait_for_timeout(1500); c=pg.evaluate(JS)
        pg.goto('file://'+ROOT+'/qa/base/'+v+'.html'); pg.wait_for_timeout(1500); bs=pg.evaluate(JS)
        print('==',v); print(' clone',c); print(' base ',bs)
        print(' docscroll clone?')
    b.close()
