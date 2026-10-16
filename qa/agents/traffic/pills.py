from playwright.sync_api import sync_playwright
URL='file:///Users/kumaraniket/Desktop/AI Governance Clone/clone/index.html'
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    pg.goto(URL+'#05d-traffic-statistics'); pg.wait_for_timeout(300)
    print(pg.evaluate("""()=>{const b=[...document.querySelectorAll('button')].find(x=>x.innerText.trim().replace(/\\s+/g,' ')=='1 hour'); const p=b.parentElement; return [p.tagName,p.className,[...p.children].map(c=>c.tagName+' | '+c.className)]}"""))
    # model card markup
    print(pg.evaluate("""()=>{const e=[...document.querySelectorAll('[data-panel]')].pop().querySelector('.h-full.overflow-y-auto'); const cards=[...e.querySelectorAll('div')].filter(d=>/cursor-pointer/.test(d.className)); return cards.slice(0,3).map(c=>c.className)}"""))
    # accordion markup
    pg.goto(URL+'#05c-traffic-model-config'); pg.wait_for_timeout(300)
    print(pg.evaluate("""()=>{const a=document.querySelector('a[href^="#pr_id"]'); const tab=a.closest('.p-accordion-tab'); return [a.outerHTML.slice(0,300), tab&&tab.className, [...(tab?tab.children:[])].map(c=>c.className+' '+c.id), document.querySelectorAll('.p-accordion-tab').length, [...document.querySelectorAll('[id^=pr_id]')].map(e=>e.id+':'+e.tagName).slice(0,5)]}"""))
    b.close()
