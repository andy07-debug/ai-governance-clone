import os
from playwright.sync_api import sync_playwright
URL='file://'+os.path.abspath('clone/index.html')
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    pg.goto(URL+'#05c-traffic-model-config'); pg.wait_for_timeout(500)
    print(pg.evaluate('''()=>{const s=document.querySelector('.p-accordion-toggle-icon');const out=[];for(const ss of document.styleSheets){let rs;try{rs=ss.cssRules}catch(e){continue}for(const r of rs){if(r.selectorText&&/transform|rotate/.test(r.style.cssText)){try{if(s.matches(r.selectorText))out.push(r.cssText.slice(0,250))}catch(e){}}}}return [s.getAttribute('style'),out]}'''))
