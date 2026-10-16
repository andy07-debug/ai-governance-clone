from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
U='file://'+ROOT+'/clone/index.html#'
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936}); pg.set_default_timeout(3000)
    errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
    h=lambda: pg.evaluate('location.hash.slice(1)')
    def load(v): pg.goto(U+v); pg.reload(); pg.wait_for_timeout(250)
    for v in ['04-policies','04b-policies-changelogs']:
        load(v); pg.evaluate("document.querySelector('.min-h-0.flex-1.overflow-y-auto').scrollTop=9999"); pg.wait_for_timeout(100); pg.screenshot(path=v+'-bottom.png')
    # blank clicks again with current router
    for xy in [(1100,300),(1600,190),(1060,170)]:
        load('04-policies'); pg.mouse.click(*xy); pg.wait_for_timeout(100); print('blank',xy,h())
    # stat card click
    load('04-policies'); pg.mouse.click(1100,370); pg.wait_for_timeout(100); print('statcard',h())
    # modal inputs
    load('04c-policies-newpolicy-modal')
    pg.get_by_placeholder('e.g., Financial Audit Intercept').fill('My policy')
    pg.locator('main select').select_option(index=2); print('select val', pg.locator('main select').input_value())
    pg.locator('textarea').nth(0).fill('desc'); pg.locator('textarea').nth(1).fill('rule')
    print('vals', pg.evaluate("[...document.querySelectorAll('#mount input, #mount textarea')].map(e=>e.value).filter(Boolean)"), h())
    pg.keyboard.press('Escape'); pg.wait_for_timeout(100); print('esc focused textarea ->',h())
    # reopen: fields cleared?
    pg.get_by_text('New Policy',exact=False).first.click(); pg.wait_for_timeout(100); print('reopen vals',pg.evaluate("[...document.querySelectorAll('#mount input, #mount textarea')].map(e=>e.value).filter(Boolean)"))
    # escape on select open? press Tab focus trap
    for i in range(12): pg.keyboard.press('Tab')
    print('focus after 12 tabs', pg.evaluate("(()=>{const e=document.activeElement;return e.tagName+' '+(e.innerText||e.placeholder||e.title||'').slice(0,30)+' inModal='+!!e.closest('.animate-slideUp')})()"))
    # RBAC active tab clicks
    for v,txt in [('06d-rbac-config-permissions','RBAC Configuration'),('06e-rbac-config-roles','Configuration'),('06f-rbac-config-mapping','RBAC Configuration'),('06c-rbac-config-modules','Configuration')]:
        load(v); pg.get_by_text(txt,exact=True).click(); pg.wait_for_timeout(100); print('active-tab click',v,txt,'->',h())
    # fullscreen + modal
    load('04-policies'); pg.click('[title="Toggle Fullscreen"]'); pg.wait_for_timeout(200)
    pg.get_by_text('New Policy',exact=False).first.click(); pg.wait_for_timeout(200); pg.screenshot(path='fs-modal.png'); print('fs modal',h())
    pg.keyboard.press('Escape'); pg.wait_for_timeout(200); pg.get_by_text('Change Logs',exact=False).first.click(); pg.wait_for_timeout(200); pg.screenshot(path='fs-changelogs.png')
    # RBAC fullscreen
    load('06e-rbac-config-roles'); pg.click('[title="Toggle Fullscreen"]'); pg.wait_for_timeout(200); pg.screenshot(path='fs-roles.png')
    pg.get_by_text('Mapping',exact=True).click(); pg.wait_for_timeout(200); pg.screenshot(path='fs-mapping.png')
    print('errs',errs)
