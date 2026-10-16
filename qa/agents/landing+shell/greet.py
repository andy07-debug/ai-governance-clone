from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
URL='file://'+ROOT+'/clone/index.html'
OUT=ROOT+'/qa/agents/landing+shell/'
JS="""()=>{const w=[...document.querySelectorAll('span,p,div')].filter(e=>/Hey Kumar/.test(e.textContent)).sort((a,b)=>a.textContent.length-b.textContent.length)[0];
const r=w.getBoundingClientRect(); const top=document.elementFromPoint(r.left+5,r.top+r.height/2);
let sc=w; while(sc&&sc.scrollHeight<=sc.clientHeight+1) sc=sc.parentElement;
return {rect:[r.left,r.top,r.width,r.height].map(Math.round), top: top&&(top.tagName+'.'+String(top.className).slice(0,50)), vis:getComputedStyle(w).visibility, sc: sc&&(sc.tagName+'.'+String(sc.className).slice(0,60)+' st='+sc.scrollTop+' sh='+sc.scrollHeight+' ch='+sc.clientHeight)}}"""
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    pg.goto(URL+'#07a-shell-mode-dropdown'); pg.wait_for_timeout(300)
    print('fresh 07a', pg.evaluate(JS))
    pg.get_by_placeholder('Search mode...').click(); pg.wait_for_timeout(200)
    print('after focus search', pg.evaluate(JS)); pg.screenshot(path=OUT+'greet-focus.png')
    pg.goto(URL+'#00-home'); pg.reload(); pg.wait_for_timeout(300)
    print('home', pg.evaluate(JS))
    pg.locator('textarea').click(); pg.wait_for_timeout(200); print('home after textarea focus', pg.evaluate(JS))
    b.close()
