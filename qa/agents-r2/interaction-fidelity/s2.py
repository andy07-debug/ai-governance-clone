from playwright.sync_api import sync_playwright
URL='file:///Users/kumaraniket/Desktop/AI Governance Clone/clone/index.html'
with sync_playwright() as pw:
    br=pw.chromium.launch(); pg=br.new_page(viewport={'width':1920,'height':936})
    pg.goto(URL+'#00-home'); pg.wait_for_timeout(300)
    pg.locator('.h-20 .p-dropdown').click(); pg.wait_for_timeout(300)
    print(pg.evaluate("""()=>[...document.querySelectorAll('.p-dropdown-panel li')].filter(l=>/code|modern/i.test(l.textContent)).map(l=>[l.getAttribute('aria-label'), (l.textContent.match(/.{0,30}(code|modern).{0,30}/gi)||[])])"""))
    pg.get_by_placeholder('Search mode...').fill('mode'); pg.wait_for_timeout(200)
    print('mode ->', pg.evaluate("[...document.querySelectorAll('.p-dropdown-panel li')].filter(l=>l.getClientRects().length).length"))
    pg.get_by_placeholder('Search mode...').fill('focus'); pg.wait_for_timeout(200)
    print('focus ->', pg.evaluate("[...document.querySelectorAll('.p-dropdown-panel li')].filter(l=>l.getClientRects().length).map(l=>l.getAttribute('aria-label'))"))
    br.close()
