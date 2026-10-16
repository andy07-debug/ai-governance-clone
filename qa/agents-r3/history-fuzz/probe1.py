from playwright.sync_api import sync_playwright
BASE='file:///Users/kumaraniket/Desktop/AI%20Governance%20Clone/clone/index.html'
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    for v in ['01-llm-analytics','03-live-events','00-home']:
        pg.goto('about:blank'); pg.goto(BASE+'#'+v); pg.wait_for_timeout(400)
        pg.click('[title="Toggle Fullscreen"]'); pg.wait_for_timeout(900)
        r=pg.evaluate('''()=>{const h=document.querySelector('[title="Open sidebar"]');const r=h.getBoundingClientRect();const x=r.x+r.width/2,y=r.y+r.height/2;
          const e=document.elementFromPoint(x,y);return [x,y,e.tagName,e.className.toString().slice(0,80),e.closest('.maximizeChatButton')?'BUBBLE':'',(e.closest('button')||{}).outerHTML?.slice(0,200)]}''')
        print(v,r)
        bb=pg.evaluate("(()=>{const r=document.querySelector('.maximizeChatButton').getBoundingClientRect();return [r.x,r.y,r.width,r.height]})()")
        print('  bubble rect',bb)
    b.close()
