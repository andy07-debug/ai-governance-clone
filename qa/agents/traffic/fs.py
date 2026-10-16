from playwright.sync_api import sync_playwright
URL='file:///Users/kumaraniket/Desktop/AI Governance Clone/clone/index.html'
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(URL+'#05-traffic'); pg.wait_for_timeout(300)
    pg.click('[title="Toggle Fullscreen"]'); pg.wait_for_timeout(200)
    h=lambda: pg.evaluate('location.hash')
    steps=[('tile Projects', lambda: pg.locator('main').get_by_text('Projects',exact=True).first.click()),
           ('View Usage 5th', lambda: pg.get_by_text('View Usage',exact=True).nth(4).click()),
           ('crumb Projects', lambda: pg.locator('main .p-breadcrumb').get_by_text('Projects',exact=True).click()),
           ('Model Configuration 13th', lambda: pg.get_by_text('Model Configuration',exact=True).nth(12).click()),
           ('inner home', lambda: pg.locator('main .p-breadcrumb-home').click()),
           ('tile Error logs', lambda: pg.locator('main').get_by_text('Error logs',exact=True).click()),
           ('inner home', lambda: pg.locator('main .p-breadcrumb-home').click()),
           ('exit fullscreen', lambda: pg.click('[title="Toggle Fullscreen"]')),
          ]
    for n,f in steps:
        try: f(); pg.wait_for_timeout(200); print(n,'->',h())
        except Exception as e: print(n,'ERR',str(e).split('\n')[0][:100])
    pg.goto(URL+'#05a-traffic-projects'); pg.wait_for_timeout(200); pg.click('[title="Toggle Fullscreen"]'); pg.wait_for_timeout(200)
    pg.screenshot(path='fs-05a.png')
    pg.goto(URL+'#05d-traffic-statistics'); pg.wait_for_timeout(200); pg.click('[title="Toggle Fullscreen"]'); pg.wait_for_timeout(200)
    pg.screenshot(path='fs-05d.png')
    print(errs)
    b.close()
