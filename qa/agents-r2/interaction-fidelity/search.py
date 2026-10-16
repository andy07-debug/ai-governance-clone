from playwright.sync_api import sync_playwright
URL='file:///Users/kumaraniket/Desktop/AI Governance Clone/clone/index.html'
VISJ="()=>[...document.querySelectorAll('.p-dropdown-panel li')].filter(l=>l.getClientRects().length).map(l=>l.innerText.replace(/\\s+/g,' ').trim().slice(0,40))"
with sync_playwright() as pw:
    br=pw.chromium.launch(); pg=br.new_page(viewport={'width':1920,'height':936})
    pg.goto(URL+'#00-home'); pg.wait_for_timeout(300)
    pg.locator('.h-20 .p-dropdown').click(); pg.wait_for_timeout(300)
    allv=pg.evaluate(VISJ); print('all',len(allv),allv)
    print(pg.evaluate("()=>document.querySelector('.p-dropdown-panel').outerHTML.replace(/<svg[\\s\\S]*?<\\/svg>/g,'<svg/>').slice(0,2500)"))
    s=pg.get_by_placeholder('Search mode...')
    for q in ['gov','GOVERNANCE','zzzz','','  agent ','code','modern']:
        s.fill(q); pg.wait_for_timeout(200)
        vis=pg.evaluate(VISJ)
        empty=pg.evaluate("()=>{const p=document.querySelector('.p-dropdown-panel');return [...p.querySelectorAll('*')].filter(e=>e.getClientRects().length&&/no (results|available|options)/i.test(e.textContent)&&e.children.length==0).map(e=>e.textContent)}")
        print(repr(q),len(vis),vis[:5],'empty-msg:',empty, 'panelH', pg.evaluate("Math.round(document.querySelector('.p-dropdown-panel').getBoundingClientRect().height)"))
    pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
    pg.locator('.h-20 .p-dropdown').click(); pg.wait_for_timeout(300)
    print('reopen search value:',repr(pg.get_by_placeholder('Search mode...').input_value()), len(pg.evaluate(VISJ)))
    pg.get_by_placeholder('Search mode...').fill('zzz'); pg.keyboard.press('Escape'); pg.locator('.h-20 .p-dropdown').click(); pg.wait_for_timeout(300)
    print('reopen after zzz:',repr(pg.get_by_placeholder('Search mode...').input_value()), len(pg.evaluate(VISJ)))
    br.close()
