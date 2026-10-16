import os
from playwright.sync_api import sync_playwright
URL='file://'+os.path.abspath('clone/index.html')
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    pg.goto(URL+'#05c-traffic-model-config'); pg.wait_for_timeout(500)
    print(pg.evaluate('''()=>{const s=document.querySelector('.p-accordion-toggle-icon');return s.outerHTML.slice(0,300)}'''))
    print(pg.evaluate('''()=>{const s=document.querySelectorAll('.p-accordion-toggle-icon')[1];return s.outerHTML.slice(0,300)}'''))
