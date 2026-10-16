import os, json
from playwright.sync_api import sync_playwright
URL='file://'+os.path.abspath('clone/index.html')
OUT=os.path.abspath('qa/agents-r2/skeptic-r2b')
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    def fresh(v): pg.goto('about:blank'); pg.goto(URL+'#'+v); pg.wait_for_timeout(400)
    # F1
    for v in ['05d-traffic-statistics','05b-traffic-project-usage']:
        fresh(v)
        grp=pg.locator('main button',has_text='Custom').first
        par=grp.locator('xpath=..')
        def dump():
            return par.evaluate('''p=>[...p.children].filter(e=>e.tagName=="BUTTON").map(b=>{const c=getComputedStyle(b);return [b.textContent.trim(),Math.round(b.getBoundingClientRect().width),Math.round(b.getBoundingClientRect().height),c.paddingLeft,c.display,c.backgroundColor,b.className]})''')
        print(v,'INIT'); [print(' ',r[:6]) for r in dump()]
        grp.click(); pg.wait_for_timeout(750)
        par.locator('button',has_text='1 hour').click(); pg.wait_for_timeout(750)
        print(v,'AFTER Custom,1 hour'); [print(' ',r) for r in dump()]
        if v.startswith('05d'): par.screenshot(path=OUT+'/f1_'+v+'.png')
    # F2
    fresh('05c-traffic-model-config')
    heads=pg.locator('.p-accordion-header-link')
    def acc():
        return pg.evaluate('''()=>[...document.querySelectorAll('.p-accordion-header-link')].slice(0,3).map(h=>{const s=h.querySelector('svg');return [h.textContent.trim().slice(0,25),h.getAttribute('aria-expanded'),s&&getComputedStyle(s).transform,s&&s.getAttribute('class'),s&&s.querySelector('path').getAttribute('d').slice(0,12),s&&s.style.transform]})''')
    print('ACC init',acc())
    h0=heads.first; bb=h0.bounding_box(); print('bb',bb)
    pg.mouse.click(bb['x']+bb['width']*0.6,bb['y']+bb['height']/2); pg.wait_for_timeout(750)
    print('ACC after1',acc())
    pg.locator('.p-accordion').first.screenshot(path=OUT+'/f2_collapsed.png')
    pg.mouse.click(bb['x']+bb['width']*0.6,bb['y']+bb['height']/2); pg.wait_for_timeout(750)
    print('ACC after2',acc())
    # F3/F4
    fresh('00-home')
    pg.locator('.h-20 .p-dropdown').click(); pg.wait_for_timeout(400)
    inp=pg.locator('.p-dropdown-panel input')
    for q in ['focus','code','mode','zzzz','']:
        inp.fill(q); pg.wait_for_timeout(300)
        vis=pg.evaluate('''()=>[...document.querySelectorAll('.p-dropdown-panel li')].filter(l=>l.style.display!="none").map(l=>l.getAttribute('aria-label')||l.textContent.trim().slice(0,30))''')
        em=pg.locator('.p-dropdown-empty-message').count()
        print('Q',repr(q),len(vis),vis[:5],'empty',em, round(pg.locator('.p-dropdown-panel').bounding_box()['height']))
    labels=pg.evaluate('''()=>[...document.querySelectorAll('.p-dropdown-panel li')].map(l=>[l.getAttribute('aria-label'),l.querySelector('.p-dropdown-item-label, span, div').outerHTML.slice(0,200)])''')
    print(labels[:2])
    # F5
    fresh('05d-traffic-statistics')
    cards=pg.locator('main div.cursor-pointer.rounded-lg.p-3')
    print('cards',cards.count())
    print([cards.nth(i).get_attribute('class') for i in range(2)])
    c2=cards.filter(has_text='gemini-embedding-001').first
    c2.scroll_into_view_if_needed(); c2.click(); pg.wait_for_timeout(750)
    print('after',[cards.nth(i).get_attribute('class') for i in range(cards.count()) if 'indigo-400' in cards.nth(i).get_attribute('class')], c2.get_attribute('class'))
    print('errs',errs)
