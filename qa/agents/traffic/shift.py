import re
from playwright.sync_api import sync_playwright
from capscroll import cap_html
URL='file:///Users/kumaraniket/Desktop/AI Governance Clone/clone/index.html'
JS="""()=>[document.scrollingElement.scrollTop, ...[...document.querySelectorAll('body *')].filter(e=>e.scrollTop>0).map(e=>e.tagName+'.'+e.className.toString().slice(0,60)+'='+e.scrollTop+'/'+(e.scrollHeight-e.clientHeight)+' oy='+getComputedStyle(e).overflowY)]"""
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    pg.goto(URL+'#05a-traffic-projects'); pg.wait_for_timeout(300)
    pg.mouse.move(1140,600)
    for _ in range(15): pg.mouse.wheel(0,400); pg.wait_for_timeout(30)
    pg.wait_for_timeout(300); print('clone', pg.evaluate(JS))
    pg2=b.new_page(viewport={'width':1920,'height':936}); pg2.route('**/*',lambda r:r.abort())
    pg2.set_content(cap_html('05a-traffic-projects')); pg2.wait_for_timeout(300)
    pg2.mouse.move(1140,600)
    for _ in range(15): pg2.mouse.wheel(0,400); pg2.wait_for_timeout(30)
    pg2.wait_for_timeout(300); print('capture', pg2.evaluate(JS))
    b.close()
