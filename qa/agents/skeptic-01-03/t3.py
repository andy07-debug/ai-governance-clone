from playwright.sync_api import sync_playwright
URL='file:///Users/kumaraniket/Desktop/AI%20Governance%20Clone/clone/index.html#01-llm-analytics'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    pg.goto(URL); pg.wait_for_timeout(600)
    u=pg.locator('button',has_text='Top users').first; u.scroll_into_view_if_needed(); u.click()
    print(u.get_attribute('class')[-40:])
    print(pg.locator('text=Applications driving the highest LLM spend.').count(), pg.locator('text=No tagged application groups yet').count())
    m=pg.locator('button',has_text='By Model').first; m.click(); print(m.get_attribute('class')[-50:])
    print(pg.evaluate("()=>[...document.querySelectorAll('thead th')].map(t=>t.innerText.trim()).join('|')"))
    b.close()
