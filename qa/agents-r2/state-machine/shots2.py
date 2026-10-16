from playwright.sync_api import sync_playwright
BASE='file:///Users/kumaraniket/Desktop/AI%20Governance%20Clone/clone/index.html'
D='/Users/kumaraniket/Desktop/AI Governance Clone/qa/agents-r2/state-machine/'
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    pg.goto(BASE+'?e2'); pg.wait_for_timeout(500)
    pg.get_by_text('Live Events',exact=True).click(); pg.wait_for_timeout(300)
    pg.locator('.h-20 .p-dropdown').click(); pg.wait_for_timeout(300); pg.go_back(); pg.wait_for_timeout(300)
    pg.locator('[title="Toggle Fullscreen"]').click(); pg.wait_for_timeout(500); pg.go_forward(); pg.wait_for_timeout(800)
    print(pg.evaluate('location.hash')); pg.screenshot(path=D+'dropdown-over-fs.png')
    # 07c reached by click path then fs then forward
    pg.goto(BASE+'?o2#03-live-events'); pg.wait_for_timeout(500)
    pg.locator('[data-testid="headerProjectsButton"]').click(); pg.wait_for_timeout(300); print(pg.evaluate('location.hash'))
    pg.go_back(); pg.wait_for_timeout(300); pg.locator('[title="Toggle Fullscreen"]').click(); pg.wait_for_timeout(500)
    pg.go_forward(); pg.wait_for_timeout(800); print(pg.evaluate('location.hash'), pg.locator('.maximizeChatButton').count(), pg.locator('[title="Toggle Fullscreen"]').count(), pg.evaluate("document.getElementById('sidebar').getAttribute('data-panel-size')"))
    b.close()
