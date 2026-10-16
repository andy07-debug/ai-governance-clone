from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
OUT='/Users/kumaraniket/Desktop/AI Governance Clone/qa/agents/analytics+firewall+events'
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    pg.goto('file://'+ROOT+'/clone/index.html#01-llm-analytics'); pg.reload(); pg.wait_for_timeout(400)
    pg.get_by_role('button',name='Top users',exact=True).click()
    pg.get_by_role('button',name='By Model',exact=True).click()
    pg.evaluate("()=>{const a=document.querySelectorAll('.min-h-0.flex-1.overflow-y-auto');a[a.length-1].scrollTop=1400}")
    pg.wait_for_timeout(300); pg.screenshot(path=OUT+'/tog-tabs.png', clip={'x':866,'y':140,'width':1054,'height':520})
    # clear filter button
    print(pg.evaluate("""()=>{const bs=[...document.querySelectorAll('button')].filter(b=>b.className.includes('inline-flex h-10 items-center justify-ce'));return bs.map(b=>[b.disabled,b.outerHTML.slice(0,250)])}"""))
    # collapse buttons markup
    print(pg.evaluate("""()=>{const b=[...document.querySelectorAll('button')].find(x=>x.getAttribute('aria-label')=='Toggle leaderboard'||x.title=='Toggle leaderboard');return b&&[b.outerHTML.slice(0,300), b.getAttribute('aria-expanded')]}"""))
    print(pg.evaluate("""()=>{const b=[...document.querySelectorAll('button')].find(x=>x.innerText.startsWith('Cost trend'));return b&&[b.outerHTML.slice(0,200), b.getAttribute('aria-expanded')]}"""))
    b.close()
