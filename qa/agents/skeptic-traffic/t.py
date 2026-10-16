from playwright.sync_api import sync_playwright
import pathlib, json
url = pathlib.Path("/Users/kumaraniket/Desktop/AI Governance Clone/clone/index.html").as_uri()
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width':1920,'height':936})
    pg.goto(url+"#05c-traffic-model-config"); pg.wait_for_timeout(500)
    hl = pg.locator('a.p-accordion-header-link')
    print('headers', hl.count())
    exp = lambda: pg.evaluate("[...document.querySelectorAll('a.p-accordion-header-link')].map(a=>a.getAttribute('aria-expanded')).join(',')")
    c0 = lambda: pg.evaluate("(()=>{const e=document.getElementById('pr_id_185_content_0');return e?e.offsetHeight:null})()")
    print('before', exp(), c0(), pg.evaluate('history.length'))
    hl.nth(1).click(); pg.wait_for_timeout(200)
    print('after sonnet', pg.evaluate('location.hash'), exp(), c0(), pg.evaluate('history.length'))
    hl.nth(0).click(); pg.wait_for_timeout(200)
    print('after haiku', pg.evaluate('location.hash'), exp(), c0())
    print('visible title', pg.evaluate("document.querySelector('main').innerText.slice(0,200)"))
    pg.reload(); pg.wait_for_timeout(500)
    print('reload', pg.evaluate('location.hash'), pg.evaluate("document.querySelector('main')?document.querySelector('main').innerText.slice(0,100):document.body.innerText.slice(0,100)"))
    # buttons inside header
    pg.goto(url+"#05c-traffic-model-config"); pg.wait_for_timeout(300)
    btns = pg.evaluate("[...document.querySelectorAll('a.p-accordion-header-link')][1].querySelectorAll('button').length")
    print('btns in header1', btns)
    if btns:
        pg.locator('a.p-accordion-header-link').nth(1).locator('button').first.click(); pg.wait_for_timeout(200)
        print('after inner btn', pg.evaluate('location.hash'))
    # 05d
    for v in ['05d-traffic-statistics','05b-traffic-project-usage']:
        pg.goto(url+"#"+v); pg.wait_for_timeout(400)
        mores = pg.get_by_role('button', name='more', exact=True)
        print(v,'more count', mores.count())
        if mores.count():
            m = mores.first
            m.scroll_into_view_if_needed()
            info = pg.evaluate("""()=>{const b=[...document.querySelectorAll('button')].find(b=>b.textContent.trim()==='more');
              let p=b.parentElement; for(let i=0;i<4&&p;i++){const c=p.querySelector('.line-clamp-2'); if(c) return [c.className,c.textContent.length,c.offsetHeight,c.scrollHeight]; p=p.parentElement} return null}""")
            print(' before', info)
            m.click(); pg.wait_for_timeout(200)
            info = pg.evaluate("""()=>{const b=[...document.querySelectorAll('button')].find(b=>b.textContent.trim()==='more');
              let p=b.parentElement; for(let i=0;i<4&&p;i++){const c=p.querySelector('.line-clamp-2'); if(c) return [c.className,c.textContent.length,c.offsetHeight,c.scrollHeight]; p=p.parentElement} return null}""")
            print(' after', info)
        # pills
        sel = lambda: pg.evaluate("""()=>[...document.querySelectorAll('button')].filter(b=>['5 min','1 hour','7 days','30 days','Custom'].includes(b.textContent.trim())).map(b=>b.textContent.trim()+':'+b.className).join('\\n')""")
        print(' pills before\n', sel())
        bt = pg.get_by_role('button', name='1 hour', exact=True)
        if bt.count():
            bt.first.click(); pg.wait_for_timeout(200)
            print(' pills after\n', sel())
        img = pg.evaluate("[...document.querySelectorAll('img')].filter(i=>i.src.startsWith('data:image/png')).map(i=>[i.naturalWidth,i.naturalHeight,i.width,i.height])")
        print(' chart imgs', img, 'canvas', pg.evaluate("document.querySelectorAll('canvas').length"))
    b.close()
