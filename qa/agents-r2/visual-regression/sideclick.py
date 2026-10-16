from playwright.sync_api import sync_playwright
URL='file:///Users/kumaraniket/Desktop/AI Governance Clone/clone/index.html'
SNAP='''()=>[...document.querySelectorAll('#sidebar *, .h-20 *')].map(e=>e.tagName+'|'+(e.getAttribute('class')||'')+'|'+(e.getAttribute('style')||'')+'|'+(e.getAttribute('aria-pressed')||''))'''
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936}); pg.set_default_timeout(2000)
    pg.goto(URL+'#01-llm-analytics'); pg.wait_for_timeout(1000)
    n=pg.locator('#sidebar button').count(); print('sidebar buttons',n)
    for i in range(n):
        pg.goto('about:blank'); pg.goto(URL+'#01-llm-analytics'); pg.wait_for_timeout(700)
        before=pg.evaluate(SNAP); btn=pg.locator('#sidebar button').nth(i)
        desc=pg.evaluate('e=>(e.getAttribute("title")||e.getAttribute("aria-label")||e.textContent.trim().slice(0,30))+" :: "+e.className.slice(0,80)', btn.element_handle())
        try: btn.click(timeout=1500)
        except Exception as e: print(i,desc,'unclickable'); continue
        pg.wait_for_timeout(700)
        after=pg.evaluate(SNAP); h=pg.evaluate('location.hash')
        ch=[(a,b2) for a,b2 in zip(before,after) if a!=b2]
        print(i,desc,h,'changed',len(ch) + abs(len(before)-len(after)))
        for a,b2 in ch[:4]: print('    ',a[:160],'\n  ->',b2[:160])
    b.close()
