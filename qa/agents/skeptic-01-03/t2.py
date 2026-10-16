from playwright.sync_api import sync_playwright
URL='file:///Users/kumaraniket/Desktop/AI%20Governance%20Clone/clone/index.html#01-llm-analytics'
IMG="""()=>{const i=[...document.querySelectorAll('img')].find(x=>x.src.startsWith('data:image/png'));if(!i)return null;const r=i.getBoundingClientRect(),q=i.parentElement.getBoundingClientRect();return {img:[r.x,r.width,r.height],parent:[q.x,q.width],style:i.getAttribute('style')}}"""
ACT="""() => [...document.querySelectorAll('button')].filter(b=>/bg-\\[#5928ED\\]|bg-white shadow/.test(b.className)).map(b=>b.textContent.trim()).filter(t=>t.length<40)"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    pg.goto(URL); pg.wait_for_timeout(800)
    print('normal',pg.evaluate(IMG))
    pg.locator('button',has_text='30 days').first.click()
    sc=pg.evaluate("()=>{const e=[...document.querySelectorAll('*')].find(x=>x.scrollHeight>x.clientHeight+50&&getComputedStyle(x).overflowY=='auto'&&x.closest('[data-panel]')===[...document.querySelectorAll('[data-panel]')].pop());e.scrollTop=400;return e.scrollTop}")
    print('scrolled',sc)
    pg.locator('[title="Toggle Fullscreen"]').click(); pg.wait_for_timeout(500)
    print('fs',pg.evaluate(IMG))
    print('fs active',pg.evaluate(ACT))
    print('fs scrollY', pg.evaluate("()=>{return [window.scrollY,...[...document.querySelectorAll('*')].filter(x=>x.scrollTop>0).map(x=>x.className.slice(0,40)+':'+x.scrollTop)]}"))
    pg.screenshot(path='fs.png')
    # chevrons
    pg.locator('[title="Toggle Fullscreen"]').click(); pg.wait_for_timeout(300)
    print('exit fs active',pg.evaluate(ACT))
    hdr=pg.locator('button[aria-expanded]')
    print('aria-expanded buttons', hdr.count(), [hdr.nth(i).inner_text()[:30] for i in range(hdr.count())])
    for i in range(hdr.count()):
        h=hdr.nth(i)
        before=h.evaluate("b=>[b.getAttribute('aria-expanded'),b.nextElementSibling&&b.nextElementSibling.getBoundingClientRect().height, b.parentElement.getBoundingClientRect().height]")
        h.scroll_into_view_if_needed(); h.click(); pg.wait_for_timeout(200)
        after=h.evaluate("b=>[b.getAttribute('aria-expanded'),b.nextElementSibling&&b.nextElementSibling.getBoundingClientRect().height, b.parentElement.getBoundingClientRect().height]")
        print(i,before,after)
    # sort headers
    ths=pg.locator('th button')
    print('th buttons',ths.count())
    rows=lambda: pg.evaluate("()=>[...document.querySelectorAll('tbody tr')].slice(0,4).map(r=>r.innerText.replace(/\\s+/g,' ').slice(0,50))")
    r0=rows()
    ths.nth(1).scroll_into_view_if_needed(); ths.nth(1).click(); pg.wait_for_timeout(200)
    print('sort changed', r0!=rows(), ths.nth(1).inner_text())
    b.close()
