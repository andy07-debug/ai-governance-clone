"""Click through every navigation path of the replica and assert the resulting screen."""
import os, sys
from playwright.sync_api import sync_playwright
URL = 'file:///Users/kumaraniket/Desktop/AI Governance Clone/qa/agents-r2/skeptic-r2/patched.html'
R = '[data-panel]:last-of-type'  # right panel
cur = lambda pg: pg.evaluate('location.hash.slice(1)')
fails = 0
def step(pg, desc, action, expect):
    global fails
    try:
        action(pg); pg.wait_for_timeout(120)
        got = cur(pg)
        ok = got == expect
    except Exception as e:
        got, ok = 'ERR ' + str(e)[:120], False
    fails += not ok
    print(('PASS' if ok else 'FAIL'), desc, '->', got, '' if ok else '(expected %s)' % expect)

def click_text(text, scope='body', exact=True, nth=0):
    def f(pg):
        loc = pg.locator(scope).get_by_text(text, exact=exact).nth(nth)
        loc.click()
    return f
def click_sel(sel, nth=0):
    return lambda pg: pg.locator(sel).nth(nth).click()
def go(v):
    return lambda pg: (pg.goto(URL + '#' + v), pg.wait_for_timeout(200))

with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1920, 'height': 936}); pg.set_default_timeout(4000)
    pg.goto(URL); pg.wait_for_timeout(300)
    step(pg, 'start', lambda p: None, '00-home')
    for title, v in [('LLM Studio Analytics', '01-llm-analytics'), ('Firewall Overview', '02-firewall'), ('Live Events', '03-live-events'), ('Policies', '04-policies'), ('Traffic Analysis', '05-traffic')]:
        step(pg, 'home card ' + title, click_text(title), v)
        step(pg, '  breadcrumb home from ' + v, click_sel('main button[title="Back to home"], main span.p-1.text-indigo-600'), '00-home')
    step(pg, 'System Health (soon) stays', lambda p: p.get_by_text('System Health', exact=True).click(force=True), '00-home')
    step(pg, 'RBAC button', click_text('RBAC'), '06-rbac-access')
    step(pg, 'RBAC Configuration tab', click_text('RBAC Configuration'), '06b-rbac-usergroups')
    step(pg, 'Configuration subtab', click_text('Configuration'), '06c-rbac-config-modules')
    step(pg, 'Permissions', click_text('Permissions'), '06d-rbac-config-permissions')
    step(pg, 'Roles', click_text('Roles'), '06e-rbac-config-roles')
    step(pg, 'Mapping', click_text('Mapping'), '06f-rbac-config-mapping')
    step(pg, 'Modules', click_text('Modules'), '06c-rbac-config-modules')
    step(pg, 'User Groups', click_text('User Groups'), '06b-rbac-usergroups')
    step(pg, 'Access Management', click_text('Access Management'), '06-rbac-access')
    step(pg, 'breadcrumb home from RBAC', click_sel('main button[title="Back to home"], main span.p-1.text-indigo-600'), '00-home')
    # policies
    go('04-policies')(pg)
    step(pg, 'Change Logs', click_text('Change Logs', exact=False), '04b-policies-changelogs')
    step(pg, 'Policies Deck', click_text('Policies Deck', exact=False), '04-policies')
    step(pg, 'New Policy', click_text('New Policy', exact=False), '04c-policies-newpolicy-modal')
    step(pg, 'type in Policy Name stays', lambda p: p.get_by_placeholder('e.g., Financial Audit Intercept').fill('Test'), '04c-policies-newpolicy-modal')
    step(pg, 'Deploy Policy is inert', click_text('Deploy Policy'), '04c-policies-newpolicy-modal')
    step(pg, 'Cancel', click_text('Cancel'), '04-policies')
    step(pg, 'New Policy again', click_text('New Policy', exact=False), '04c-policies-newpolicy-modal')
    step(pg, 'modal X', click_sel('.animate-slideUp .border-b button'), '04-policies')
    step(pg, 'New Policy + Escape', lambda p: (click_text('New Policy', exact=False)(p), p.keyboard.press('Escape')), '04-policies')
    # traffic
    go('05-traffic')(pg)
    for t, v in [('Projects', '05a-traffic-projects'), ('Statistics', '05d-traffic-statistics'), ('Applications', '05e-traffic-applications'), ('Error logs', '05f-traffic-errorlogs')]:
        step(pg, 'hub ' + t, click_text(t, scope='main'), v)
        step(pg, '  inner home', click_sel('main .p-breadcrumb-home'), '05-traffic')
    step(pg, 'hub Projects', click_text('Projects', scope='main'), '05a-traffic-projects')
    step(pg, 'View Usage (3rd card)', click_text('View Usage', nth=2), '05b-traffic-project-usage')
    step(pg, 'crumb Projects', click_text('Projects', scope='main .p-breadcrumb'), '05a-traffic-projects')
    step(pg, 'Model Configuration', click_text('Model Configuration'), '05c-traffic-model-config')
    step(pg, 'crumb Projects', click_text('Projects', scope='main .p-breadcrumb'), '05a-traffic-projects')
    step(pg, 'outer home from traffic', click_sel('main button[title="Back to home"], main span.p-1.text-indigo-600'), '00-home')
    # shell
    step(pg, 'mode dropdown', click_sel('.h-20 .p-dropdown'), '07a-shell-mode-dropdown')
    step(pg, 'dropdown search typing stays', lambda p: p.get_by_placeholder('Search mode...').fill('ai'), '07a-shell-mode-dropdown')
    step(pg, 'dropdown pick AI Governance', click_text('AI Governance', scope='.p-dropdown-panel'), '00-home')
    step(pg, 'dropdown + Escape', lambda p: (click_sel('.h-20 .p-dropdown')(p), p.keyboard.press('Escape')), '00-home')
    step(pg, 'hamburger', click_sel('[title="Open sidebar"]'), '07b-shell-hamburger')
    step(pg, 'drawer close', click_sel('[title="Click to close sidebar"]'), '00-home')
    step(pg, 'Projects (left)', click_sel('[data-testid="headerProjectsButton"]'), '07c-shell-projects')
    # fullscreen
    go('03-live-events')(pg)
    step(pg, 'fullscreen on', click_sel('[title="Toggle Fullscreen"]'), '03-live-events')
    fs_on = pg.locator('.fixed.inset-0.z-20').count() == 1 and pg.locator('.maximizeChatButton').count() == 1
    step(pg, 'fullscreen persists across nav', click_sel('main button[title="Back to home"]'), '00-home')
    fs_kept = pg.locator('.fixed.inset-0.z-20').count() == 1
    step(pg, 'chat button exits fullscreen', click_sel('.maximizeChatButton'), '00-home')
    fs_off = pg.locator('.fixed.inset-0.z-20').count() == 0 and pg.locator('[data-resize-handle]').count() == 1
    print(('PASS' if fs_on and fs_kept and fs_off else 'FAIL'), 'fullscreen layer on/kept/off', fs_on, fs_kept, fs_off); fails += not (fs_on and fs_kept and fs_off)
    # pill toggle on LLM analytics
    go('01-llm-analytics')(pg)
    def pill(p):
        p.get_by_text('Requests', exact=True).first.click()
    step(pg, 'metric pill toggle stays', pill, '01-llm-analytics')
    cls = pg.evaluate("""()=>{const bs=[...document.querySelectorAll('button')].filter(b=>['Cost','Requests'].includes(b.textContent.trim()));return bs.map(b=>b.textContent.trim()+':'+b.className.slice(0,60))}""")
    print('   pill classes after click:', cls)
    b.close()
print('FAILURES', fails); sys.exit(1 if fails else 0)
