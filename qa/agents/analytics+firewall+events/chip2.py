from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    pg.goto('file://'+ROOT+'/clone/index.html#01-llm-analytics'); pg.wait_for_timeout(800)
    print(pg.evaluate("""()=>{const e=[...document.querySelectorAll('#root td *')].find(x=>x.childElementCount==0&&x.textContent.trim()=='gemini-3-flash-preview');
    const out=[];let n=e;while(n&&n.tagName!='TABLE'){const s=getComputedStyle(n);out.push([n.tagName,(n.className.baseVal??n.className).slice(0,160),s.color,s.backgroundColor,s.opacity,s.fontFamily.slice(0,60),n.getAttribute('style')]);n=n.parentElement}return out}"""))
    b.close()
