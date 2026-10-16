import os
from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
URL='file://'+ROOT+'/clone/index.html'
OUT=os.path.dirname(os.path.abspath(__file__))
VIEWS=['05a-traffic-projects','05b-traffic-project-usage','05c-traffic-model-config','05d-traffic-statistics','05e-traffic-applications']
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    for v in VIEWS:
        pg.goto(URL+'#'+v); pg.wait_for_timeout(400)
        # wheel over the right panel in several spots
        for (x,y) in [(1140,600),(1640,600),(1640,880),(1140,880)]:
            pg.mouse.move(x,y)
            for _ in range(15): pg.mouse.wheel(0,400); pg.wait_for_timeout(30)
        pg.wait_for_timeout(300)
        st=pg.evaluate("""[...document.querySelectorAll('#root *')].filter(e=>{const s=getComputedStyle(e);return /(auto|scroll)/.test(s.overflowY)&&e.scrollHeight>e.clientHeight+2}).map(e=>[e.className.toString().slice(0,50),e.scrollTop,e.scrollHeight-e.clientHeight])""")
        print(v, st)
        pg.screenshot(path=f'{OUT}/{v}-wheel.png')
    b.close()
