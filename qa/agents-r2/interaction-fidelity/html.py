import sys
from playwright.sync_api import sync_playwright
URL='file:///Users/kumaraniket/Desktop/AI Governance Clone/clone/index.html'
v, needle = sys.argv[1], sys.argv[2]
with sync_playwright() as pw:
    br=pw.chromium.launch(); pg=br.new_page(viewport={'width':1920,'height':936})
    pg.goto(URL+'#'+v); pg.wait_for_timeout(250)
    print(pg.evaluate("""(n)=>{const b=[...document.querySelectorAll('button')].find(b=>b.textContent.trim()===n); let p=b.parentElement; return p.outerHTML.replace(/<svg[\\s\\S]*?<\\/svg>/g,'<svg/>').slice(0,4000)}""", needle))
