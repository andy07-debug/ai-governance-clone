from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    pg.goto('file://'+ROOT+'/clone/index.html#01-llm-analytics'); pg.wait_for_timeout(800)
    print(pg.evaluate("""()=>{const e=[...document.querySelectorAll('#root *')].find(x=>x.childElementCount==0&&x.textContent.trim()=='gemini-3-flash-preview');
    const out=[];let n=e;while(n&&n.id!='root'){const s=getComputedStyle(n);out.push([n.tagName,(n.className.baseVal??n.className).slice(0,120),s.color,s.backgroundColor,s.opacity,s.fontFamily.slice(0,60),n.getAttribute('style')]);n=n.parentElement}return out.slice(0,4)}"""))
    print(pg.evaluate("""()=>{const i=[...document.querySelectorAll('#root img')].find(x=>x.src.startsWith('data:image/png'));const r=i.getBoundingClientRect();return [i.outerHTML.slice(0,300).replace(/base64,[^"]+/,'...'),r.x,r.y,r.width,r.height, i.parentElement.outerHTML.slice(0,300).replace(/base64,[^"]+/,'...')]}"""))
    # elements with inline opacity / transform (mid animation captures)
    print(pg.evaluate("""()=>[...document.querySelectorAll('#root [style]')].map(e=>e.getAttribute('style')).filter(s=>/opacity|transform/.test(s)).slice(0,30)"""))
    print(pg.evaluate("""()=>[...document.querySelectorAll('#root canvas')].map(c=>[c.width,c.height,c.className])"""))
    b.close()
