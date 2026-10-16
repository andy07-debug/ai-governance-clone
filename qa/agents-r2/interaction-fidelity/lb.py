from playwright.sync_api import sync_playwright
URL='file:///Users/kumaraniket/Desktop/AI Governance Clone/clone/index.html'
with sync_playwright() as pw:
    br=pw.chromium.launch(); pg=br.new_page(viewport={'width':1920,'height':936})
    pg.goto(URL+'#01-llm-analytics'); pg.wait_for_timeout(300)
    print(pg.evaluate("""()=>{const b=document.querySelector('[aria-label="Toggle leaderboard"]');const s=b.closest('section');
      return [...s.children].map(c=>({tag:c.tagName,cls:c.className.slice(0,80),hasBtn:c.contains(b),h:Math.round(c.getBoundingClientRect().height),txt:c.innerText.slice(0,200)}))}"""))
    print(pg.evaluate("""()=>{const b=document.querySelector('[aria-label="Toggle leaderboard"]');return b.parentElement.outerHTML.replace(/<svg[\\s\\S]*?<\\/svg>/g,'<svg/>').slice(0,1500)}"""))
    b=pg.locator('[aria-label="Toggle leaderboard"]'); y0=pg.evaluate("document.querySelector('[aria-label=\"Toggle leaderboard\"]').closest('section').getBoundingClientRect().height")
    b.click(); pg.wait_for_timeout(400)
    y1=pg.evaluate("document.querySelector('[aria-label=\"Toggle leaderboard\"]').closest('section').getBoundingClientRect().height")
    print('section h',y0,'->',y1)
    print(pg.evaluate("""()=>{const b=document.querySelector('[aria-label="Toggle leaderboard"]');const s=b.closest('section');
      return [...s.children].map(c=>({hasBtn:c.contains(b),disp:c.style.display,h:Math.round(c.getBoundingClientRect().height),txt:c.innerText.slice(0,300)}))}"""))
    pg.screenshot(path='lb_collapsed.png', full_page=False)
    pg.evaluate("document.querySelector('[aria-label=\"Toggle leaderboard\"]').scrollIntoView({block:'center'})"); pg.screenshot(path='lb_collapsed2.png')
    br.close()
