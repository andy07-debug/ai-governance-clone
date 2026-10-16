from playwright.sync_api import sync_playwright
URL='file:///Users/kumaraniket/Desktop/AI Governance Clone/clone/index.html'
SC='''()=>{const o=[];document.querySelectorAll('*').forEach(e=>{if(e.scrollTop>0)o.push([e.tagName+'.'+String(e.className).slice(0,50),e.scrollTop])});return {win:scrollY,els:o,hash:location.hash}}'''
SCROLLALL='''()=>{document.querySelectorAll('*').forEach(e=>{if(e.scrollHeight>e.clientHeight+5){e.scrollTop=99999}});window.scrollTo(0,99999)}'''
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    for start,act in [('05b-traffic-project-usage', lambda: pg.locator('main .p-breadcrumb').get_by_text('Projects',exact=True).click()),
                      ('01-llm-analytics', lambda: pg.click('main button[title="Back to home"], main span.p-1.text-indigo-600')),
                      ('06-rbac-access', lambda: pg.get_by_text('RBAC Configuration',exact=True).click()),
                      ('04-policies', lambda: pg.get_by_text('Change Logs',exact=False).first.click())]:
        pg.goto('about:blank'); pg.goto(URL+'#'+start); pg.wait_for_timeout(1200)
        pg.evaluate(SCROLLALL); pg.wait_for_timeout(300); print(start,'scrolled',pg.evaluate(SC))
        act(); pg.wait_for_timeout(900); print('  after nav',pg.evaluate(SC))
    # fullscreen scroll then exit
    pg.goto('about:blank'); pg.goto(URL+'#05d-traffic-statistics'); pg.wait_for_timeout(1200)
    pg.click('[title="Toggle Fullscreen"]'); pg.wait_for_timeout(900); pg.evaluate(SCROLLALL); pg.wait_for_timeout(300); print('fs scrolled', pg.evaluate(SC))
    pg.click('.maximizeChatButton'); pg.wait_for_timeout(900); print(' fs off', pg.evaluate(SC)); pg.screenshot(path='probe/fs-scroll-off.png')
    b.close()
