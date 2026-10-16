from playwright.sync_api import sync_playwright
BASE='file:///Users/kumaraniket/Desktop/AI%20Governance%20Clone/clone/index.html'
D='/Users/kumaraniket/Desktop/AI Governance Clone/qa/agents-r2/state-machine/'
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    pg.goto(BASE+'?s1#07c-shell-projects'); pg.wait_for_timeout(800); pg.screenshot(path=D+'07c-normal.png')
    print('07c toggle btns', pg.locator('[title="Toggle Fullscreen"]').count(), 'projects btn', pg.locator('[data-testid="headerProjectsButton"]').count(),
          pg.evaluate("(()=>{const b=document.querySelector('[data-testid=\"headerProjectsButton\"]');if(!b)return null;const r=b.getBoundingClientRect();return [r.x,r.y,r.width,r.height]})()"))
    pg.goto(BASE+'?s2#03-live-events'); pg.wait_for_timeout(500)
    pg.locator('[title="Toggle Fullscreen"]').click(); pg.wait_for_timeout(800)
    print('in fs: projects btn visible/hit?', pg.evaluate("(()=>{const b=document.querySelector('[data-testid=\"headerProjectsButton\"]');if(!b)return null;const r=b.getBoundingClientRect();const e=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return [r.x,r.y,r.width,r.height,!!(e&&b.contains(e))]})()"))
    pg.evaluate("location.hash='07c-shell-projects'"); pg.wait_for_timeout(800); pg.screenshot(path=D+'07c-fs.png')
    pg.go_back(); pg.wait_for_timeout(300)
    pg.locator('.maximizeChatButton').click(); pg.wait_for_timeout(800)
    # E2 shot
    pg.locator('.h-20 .p-dropdown').click(); pg.wait_for_timeout(300); pg.go_back(); pg.wait_for_timeout(300)
    pg.locator('[title="Toggle Fullscreen"]').click(); pg.wait_for_timeout(500); pg.go_forward(); pg.wait_for_timeout(800)
    pg.screenshot(path=D+'dropdown-over-fs.png')
    b.close()
