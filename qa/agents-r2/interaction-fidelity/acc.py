from playwright.sync_api import sync_playwright
URL='file:///Users/kumaraniket/Desktop/AI Governance Clone/clone/index.html'
with sync_playwright() as pw:
    br=pw.chromium.launch(); pg=br.new_page(viewport={'width':1920,'height':936})
    pg.goto(URL+'#05c-traffic-model-config'); pg.wait_for_timeout(300)
    info=pg.evaluate("""()=>[...document.querySelectorAll('a.p-accordion-header-link')].slice(0,3).map(a=>({exp:a.getAttribute('aria-expanded'),ctrl:a.getAttribute('aria-controls'),hasContent:!!document.getElementById(a.getAttribute('aria-controls')),
       svgs:[...a.querySelectorAll('svg')].map(s=>s.getAttribute('class')+' '+(s.querySelector('path')||{getAttribute:()=>''}).getAttribute('d').slice(0,40)), txt:a.textContent.trim().slice(0,40), hdrCls:a.closest('.p-accordion-header').className}))""")
    for i in info: print(i)
    first=pg.locator('a.p-accordion-header-link').first
    tb=first.bounding_box(); print(tb)
    ST="""()=>{const a=document.querySelector('a.p-accordion-header-link');const c=document.getElementById(a.getAttribute('aria-controls'));const w=c.closest('.p-toggleable-content')||c;const s=a.querySelector('svg');
       return [a.getAttribute('aria-expanded'), getComputedStyle(w).display, Math.round(w.getBoundingClientRect().height), s.style.transform, getComputedStyle(a.closest('.p-accordion-header')).backgroundColor, getComputedStyle(a).backgroundColor]}"""
    print('init',pg.evaluate(ST))
    for k in range(4):
        pg.mouse.click(tb['x']+tb['width']*0.5, tb['y']+tb['height']/2); pg.wait_for_timeout(750); print('click',k,pg.evaluate(ST))
    # second tab click
    sec=pg.locator('a.p-accordion-header-link').nth(1); sb=sec.bounding_box()
    b4=pg.evaluate("()=>document.querySelectorAll('a.p-accordion-header-link')[1].outerHTML.length")
    pg.mouse.click(sb['x']+sb['width']*0.4, sb['y']+sb['height']/2); pg.wait_for_timeout(750)
    print('2nd tab click hash',pg.evaluate('location.hash'), pg.evaluate("()=>document.querySelectorAll('a.p-accordion-header-link')[1].getAttribute('aria-expanded')"))
    br.close()
