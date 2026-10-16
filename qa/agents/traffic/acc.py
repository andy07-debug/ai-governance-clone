from playwright.sync_api import sync_playwright
URL='file:///Users/kumaraniket/Desktop/AI Governance Clone/clone/index.html'
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    pg.goto(URL+'#05c-traffic-model-config'); pg.wait_for_timeout(300)
    st=lambda: pg.evaluate("[...document.querySelectorAll('.p-accordion-header-link')].map(a=>a.getAttribute('aria-expanded')).join(',')+' | content0 visible='+(document.getElementById('pr_id_185_content_0')?.offsetHeight ?? document.querySelector('.pr_id_185_content_0')?.offsetHeight)")
    print('before', st(), pg.evaluate('location.hash'))
    pg.locator('#pr_id_185_header_0').click(position={'x':300,'y':30}); pg.wait_for_timeout(300)
    print('after haiku header', st(), pg.evaluate('location.hash'))
    pg.locator('#pr_id_185_header_1').click(position={'x':300,'y':30}); pg.wait_for_timeout(300)
    print('after sonnet header', st(), pg.evaluate('location.hash'))
    pg.locator('#pr_id_185_header_1 svg').last.click(); pg.wait_for_timeout(300)
    print('after sonnet chevron', st(), pg.evaluate('location.hash'))
    pg.reload(); pg.wait_for_timeout(400); print('reload ->', pg.evaluate('location.hash'))
    b.close()
