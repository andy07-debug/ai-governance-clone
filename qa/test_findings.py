"""Regression checks for the 18 defects confirmed by the adversarial QA workflow."""
import os, sys
from playwright.sync_api import sync_playwright
URL = 'file://' + os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'clone', 'index.html')
fails = 0
def check(n, desc, ok, extra=''):
    global fails
    fails += not ok
    print('PASS' if ok else 'FAIL', '#%d' % n, desc, extra)

with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1920, 'height': 936}); pg.set_default_timeout(4000)
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    H = lambda: pg.evaluate('window.__cloneState()')
    def fresh(v='00-home'):
        pg.goto('about:blank'); pg.goto(URL + '#' + v); pg.wait_for_timeout(250)

    # 0 cost-pill refresh is inert
    fresh(); pg.locator('.h-20 button.bg-violet-50').first.click(); pg.wait_for_timeout(150)
    check(0, 'cost-pill refresh does not open drawer', H() == '00-home' and pg.locator('.p-sidebar').count() == 0, H())
    # 1 Projects -> dropdown -> AI Governance -> landing
    fresh(); pg.locator('[data-testid="headerProjectsButton"]').click(); pg.locator('.h-20 .p-dropdown').click()
    pg.locator('.p-dropdown-panel li', has_text='AI Governance').first.click(); pg.wait_for_timeout(150)
    check(1, 'AI Governance from Projects goes to landing', H() == '00-home' and pg.get_by_text('Welcome to AI Governance').count() == 1, H())
    # 2 overlay from Projects keeps Projects underneath
    fresh(); pg.locator('[data-testid="headerProjectsButton"]').click(); pg.locator('.h-20 .p-dropdown').click(); pg.wait_for_timeout(150)
    under = pg.get_by_text('Welcome to AI Governance').count() == 0 and pg.get_by_text('Shared with me').count() >= 1
    pg.keyboard.press('Escape'); pg.locator('[title="Open sidebar"]').click(); pg.wait_for_timeout(150)
    under2 = pg.get_by_text('Shared with me').count() >= 1 and pg.locator('.p-sidebar').count() == 1
    pg.locator('[title="Click to close sidebar"]').click(); pg.wait_for_timeout(150)
    check(2, 'overlays layer over Projects', under and under2 and H() == '07c-shell-projects', H())
    # 3 chat draft survives navigation
    fresh(); pg.get_by_placeholder('How can I help?').fill('draft text')
    pg.get_by_text('Live Events', exact=True).click(); pg.locator('main button[title="Back to home"]').click()
    pg.locator('.h-20 .p-dropdown').click(); pg.keyboard.press('Escape')
    check(3, 'chat draft persists across views + overlays', pg.get_by_placeholder('How can I help?').input_value() == 'draft text')
    # 4 fullscreen with dropdown open closes dropdown first
    fresh(); pg.locator('.h-20 .p-dropdown').click(); pg.wait_for_timeout(100)
    pg.locator('[title="Toggle Fullscreen"]').click(); pg.wait_for_timeout(150)
    check(4, 'fullscreen click with dropdown open', pg.locator('.p-dropdown-panel').count() == 0, 'panels=%d' % pg.locator('.p-dropdown-panel').count())
    # 5 browser back/forward
    fresh(); pg.get_by_text('Policies', exact=True).click(); pg.get_by_text('Change Logs').first.click(); pg.wait_for_timeout(100)
    pg.go_back(); pg.wait_for_timeout(200); h1 = H(); pg.go_back(); pg.wait_for_timeout(200); h2 = H(); pg.go_forward(); pg.wait_for_timeout(200); h3 = H()
    ok5 = (h1, h2, h3) == ('04-policies', '00-home', '04-policies') and pg.get_by_text('New Policy').count() >= 1
    check(5, 'browser back/forward', ok5, (h1, h2, h3))
    # 6 mode search filters
    fresh(); pg.locator('.h-20 .p-dropdown').click(); pg.get_by_placeholder('Search mode...').fill('agent genie'); pg.wait_for_timeout(100)
    vis = pg.evaluate("[...document.querySelectorAll('.p-dropdown-panel li')].filter(l=>l.offsetParent).map(l=>l.textContent.trim().slice(0,30))")
    check(6, 'mode search filters list', len(vis) >= 1 and all('Agent Genie' in x for x in vis), vis)
    # 7 checkbox
    fresh('07c-shell-projects'); pg.locator('#subProjectCheck').click(force=True); pg.wait_for_timeout(100)
    check(7, 'Show Sub Projects checkbox shows tick', pg.locator('.p-checkbox.p-highlight .p-checkbox-icon').count() == 1)
    # 8 metric Requests toggles
    fresh('01-llm-analytics'); pg.get_by_text('Requests', exact=True).first.click(); pg.wait_for_timeout(800)
    c = pg.evaluate("[...document.querySelectorAll('button')].filter(b=>['Cost','Requests'].includes(b.textContent.trim())).slice(0,2).map(b=>getComputedStyle(b).backgroundColor)")
    check(8, 'METRIC Requests becomes selected', c[0] in ('rgba(0, 0, 0, 0)', 'rgb(255, 255, 255)') and c[1] not in ('rgba(0, 0, 0, 0)', 'rgb(255, 255, 255)'), c)
    # 9 chart stretches in fullscreen
    fresh('01-llm-analytics'); pg.locator('[title="Toggle Fullscreen"]').click(); pg.wait_for_timeout(200)
    pg.wait_for_timeout(600)
    w = pg.evaluate("Math.round(document.querySelector('canvas[data-chart]').getBoundingClientRect().width)")
    check(9, 'cost chart fills width in fullscreen', w > 1500, w)
    # 10 collapse chevrons
    fresh('01-llm-analytics'); btn = pg.locator('section > button[aria-expanded]').first
    btn.click(); pg.wait_for_timeout(100)
    hidden = pg.evaluate("(()=>{const s=document.querySelector('section > button[aria-expanded]').closest('section');return [...s.children].filter(c=>!c.matches('button')).every(c=>c.style.display==='none')})()")
    btn.click(); pg.wait_for_timeout(100)
    shown = pg.evaluate("(()=>{const s=document.querySelector('section > button[aria-expanded]').closest('section');return [...s.children].every(c=>c.style.display!=='none')})()")
    lb = pg.locator('[aria-label="Toggle leaderboard"]').first; lb.click(); pg.wait_for_timeout(100)
    lbh = pg.evaluate("document.querySelector('[aria-label=\"Toggle leaderboard\"]').getAttribute('aria-expanded')")
    check(10, 'section collapse/expand + leaderboard', hidden and shown and lbh == 'false', (hidden, shown, lbh))
    # 11 fullscreen keeps pill state + scroll
    fresh('01-llm-analytics'); pg.get_by_text('30 days', exact=True).first.click()
    pg.evaluate("document.querySelector('main .overflow-y-auto, main [class*=overflow-y-auto]') && 0")
    sc = pg.evaluate("(()=>{const el=[...document.querySelectorAll('[data-panel]:last-of-type *')].find(e=>e.scrollHeight>e.clientHeight+50&&getComputedStyle(e).overflowY!='visible');el.scrollTop=400;return el.scrollTop})()")
    pg.locator('[title="Toggle Fullscreen"]').click(); pg.wait_for_timeout(150); pg.locator('[title="Toggle Fullscreen"]').click(); pg.wait_for_timeout(150)
    st = pg.evaluate("(()=>{const b=[...document.querySelectorAll('button')].find(b=>b.textContent.trim()==='30 days');const el=[...document.querySelectorAll('[data-panel]:last-of-type *')].find(e=>e.scrollTop>0);return [getComputedStyle(b).color, el?el.scrollTop:0]})()")
    check(11, 'fullscreen toggle keeps pill + scroll', st[0] == 'rgb(255, 255, 255)' and st[1] == sc, (st, sc))
    # 12 empty header space does not open modal
    fresh('04-policies'); pg.get_by_text('Smart AI Prompt Policies', exact=True).last.click(); pg.wait_for_timeout(100)
    pg.mouse.click(1300, 330); pg.wait_for_timeout(100)
    check(12, 'clicking non-button areas keeps Policies', H() == '04-policies', H())
    # 13 active RBAC tab keeps sub-tab
    fresh('06e-rbac-config-roles'); pg.get_by_text('RBAC Configuration', exact=True).click(); pg.get_by_text('Configuration', exact=True).click(); pg.wait_for_timeout(100)
    check(13, 'clicking active RBAC tabs keeps Roles', H() == '06e-rbac-config-roles', H())
    # 14/15 accordion
    fresh('05c-traffic-model-config'); pg.locator('a.p-accordion-header-link').nth(1).click(); pg.wait_for_timeout(100)
    h14 = H()
    pg.locator('a.p-accordion-header-link').first.click(force=True); pg.wait_for_timeout(100)
    closed = pg.evaluate("(()=>{const c=document.getElementById(document.querySelector('a.p-accordion-header-link').getAttribute('aria-controls'));return getComputedStyle(c.closest('.p-toggleable-content')||c).display})()")
    pg.locator('a.p-accordion-header-link').first.click(force=True); pg.wait_for_timeout(100)
    reopened = pg.evaluate("(()=>{const c=document.getElementById(document.querySelector('a.p-accordion-header-link').getAttribute('aria-controls'));return getComputedStyle(c.closest('.p-toggleable-content')||c).display})()")
    check(14, 'accordion links do not rewrite hash', h14 == '05c-traffic-model-config', h14)
    check(15, 'open accordion tab collapses/expands', closed == 'none' and reopened != 'none', (closed, reopened))
    # 16 more buttons
    fresh('05d-traffic-statistics'); m = pg.get_by_role('button', name='more', exact=True).first
    m.click(); pg.wait_for_timeout(100)
    check(16, 'error log "more" expands', pg.get_by_role('button', name='less', exact=True).count() == 1)
    # 17 time-range pills toggle
    fresh('05d-traffic-statistics'); pg.get_by_text('hours', exact=False).first.click(); pg.wait_for_timeout(800)
    bg = pg.evaluate("[...document.querySelectorAll('button')].filter(b=>/^(5 min|1 hour|4 hours)$/.test(b.textContent.replace(/\\s+/g,' ').trim())).map(b=>b.textContent.replace(/\\s+/g,' ').trim()+':'+getComputedStyle(b).backgroundColor)")
    check(17, 'time-range pills move selection', any('4 hours' in x and 'rgba(0, 0, 0, 0)' not in x for x in bg) and any('5 min' in x and 'rgba(0, 0, 0, 0)' in x for x in bg), bg)
    # ---------- round 2 ----------
    HASH = lambda: pg.evaluate('location.hash.slice(1)')
    # r2-0: pick AI Governance from dropdown, Back returns to the previous page with no overlay
    fresh(); pg.get_by_text('Live Events', exact=True).click(); pg.locator('.h-20 .p-dropdown').click()
    pg.locator('.p-dropdown-panel li', has_text='AI Governance').first.click(); pg.wait_for_timeout(150)
    pg.go_back(); pg.wait_for_timeout(250)
    check(18, 'Back after mode pick -> previous page, no overlay', H() == '03-live-events' and pg.locator('[data-overlay]').count() == 0, H())
    # r2-1/2/5: overlays never enter history; Back/Forward/reload keep the page
    fresh(); pg.get_by_text('Live Events', exact=True).click(); pg.locator('.h-20 .p-dropdown').click(); pg.wait_for_timeout(100)
    h_open = HASH()
    pg.reload(); pg.wait_for_timeout(400)
    after_reload = H()
    pg.go_back(); pg.wait_for_timeout(250); b1 = H(); pg.go_forward(); pg.wait_for_timeout(250); f1 = H()
    check(19, 'overlay keeps page hash; reload/back/forward stay on pages', h_open == '03-live-events' and after_reload == '03-live-events' and (b1, f1) == ('00-home', '03-live-events') and pg.locator('[data-overlay]').count() == 0, (h_open, after_reload, b1, f1))
    fresh(); pg.get_by_text('Policies', exact=True).click(); pg.locator('[title="Open sidebar"]').click(); pg.wait_for_timeout(100)
    h_drawer = HASH(); pg.go_back(); pg.wait_for_timeout(250)
    check(20, 'drawer is not a history entry', h_drawer == '04-policies' and H() == '00-home' and pg.locator('.p-sidebar').count() == 0, (h_drawer, H()))
    # r2-3: closing New Policy modal does not leave a modal entry behind
    fresh(); pg.get_by_text('Policies', exact=True).click(); pg.get_by_text('New Policy').first.click(); pg.keyboard.press('Escape'); pg.wait_for_timeout(100)
    pg.go_back(); pg.wait_for_timeout(250)
    check(21, 'Back after closing modal goes to home, not the modal', H() == '00-home', H())
    # r2-4: unknown / empty hash resync
    fresh('03-live-events'); pg.evaluate("location.hash='#nope'"); pg.wait_for_timeout(200); u = HASH()
    pg.evaluate("location.hash=''"); pg.wait_for_timeout(200)
    check(22, 'unknown hash resyncs, empty hash -> home', u == '03-live-events' and H() == '00-home', (u, H()))
    # deep link to overlay still works and resolves to the page hash
    fresh('07a-shell-mode-dropdown')
    check(23, 'deep link #07a opens dropdown over home', pg.locator('.p-dropdown-panel').count() == 1 and HASH() == '00-home', HASH())
    # r2-6: Select Mode -> no highlighted item
    fresh('07c-shell-projects'); pg.locator('.h-20 .p-dropdown').click(); pg.wait_for_timeout(100)
    hl = pg.evaluate("[...document.querySelectorAll('.p-dropdown-panel li.p-highlight')].length")
    fresh(); pg.locator('.h-20 .p-dropdown').click(); pg.wait_for_timeout(100)
    hl2 = pg.evaluate("[...document.querySelectorAll('.p-dropdown-panel li.p-highlight')].map(l=>l.getAttribute('aria-label'))")
    check(24, 'highlighted mode follows trigger label', hl == 0 and hl2 == ['AI Governance'], (hl, hl2))
    # r2-7: pill layout tokens never move (Custom keeps px-3 + flex; others keep block)
    fresh('05d-traffic-statistics')
    for label in ['1 hour', '7 days', '5 min', '30 days']:
        pg.locator('button', has_text=label).first.click(); pg.wait_for_timeout(80)
    pg.wait_for_timeout(700)
    lay = pg.evaluate("[...document.querySelectorAll('button')].filter(b=>/^(5 min|1 hour|30 days|Custom)$/.test(b.textContent.replace(/\\s+/g,' ').trim())).map(b=>[b.textContent.replace(/\\s+/g,' ').trim(), getComputedStyle(b).display, getComputedStyle(b).paddingLeft, getComputedStyle(b).backgroundColor])")
    sel = [x for x in lay if x[3] not in ('rgba(0, 0, 0, 0)',)]
    custom = [x for x in lay if x[0] == 'Custom']
    check(25, 'pill toggle keeps layout; exactly one selected', len(sel) == 1 and sel[0][0] == '30 days' and custom and custom[0][1] == 'flex' and all(x[1] == 'block' for x in lay if x[0] != 'Custom'), lay)
    # r2-8: collapsed accordion chevron points down
    fresh('05c-traffic-model-config'); pg.locator('a.p-accordion-header-link').first.click(force=True); pg.wait_for_timeout(900)
    tf = pg.evaluate("getComputedStyle(document.querySelector('a.p-accordion-header-link svg')).transform")
    check(26, 'collapsed chevron un-rotated (points down)', tf in ('none', 'matrix(1, 0, 0, 1, 0, 0)'), tf)
    # r2-9: no-match search shows 'No results found'; clearing restores
    fresh(); pg.locator('.h-20 .p-dropdown').click(); pg.get_by_placeholder('Search mode...').fill('zzzz'); pg.wait_for_timeout(80)
    em = pg.locator('.p-dropdown-empty-message').count(); pg.get_by_placeholder('Search mode...').fill(''); pg.wait_for_timeout(80)
    vis = pg.evaluate("[...document.querySelectorAll('.p-dropdown-panel li.p-dropdown-item')].filter(l=>l.style.display!=='none').length")
    check(27, 'empty search message + restore', em == 1 and pg.locator('.p-dropdown-empty-message').count() == 0 and vis > 5, (em, vis))
    # ---------- round 3 ----------
    fresh(); pg.get_by_text('Policies', exact=True).click(); pg.get_by_text('New Policy').first.click(); pg.wait_for_timeout(100)
    h_modal = HASH(); pg.reload(); pg.wait_for_timeout(400); after = (H(), pg.locator('.animate-slideUp').count())
    pg.get_by_text('New Policy').first.click(); pg.go_back(); pg.wait_for_timeout(250); pg.go_forward(); pg.wait_for_timeout(250)
    fwd = (H(), pg.locator('.animate-slideUp').count())
    check(28, 'modal never in URL; reload/forward never reopen it', h_modal == '04-policies' and after == ('04-policies', 0) and fwd == ('04-policies', 0), (h_modal, after, fwd))
    for v, total in [('05b-traffic-project-usage', 926), ('05d-traffic-statistics', 928)]:
        fresh(v); pg.wait_for_timeout(1300)
        s = pg.evaluate("document.querySelector('canvas[data-chart]').__chart.data.datasets[0].data.reduce((a,b)=>a+b,0)")
        check(29, 'bars sum to TOTAL REQUESTS card on ' + v[:3], s == total, (s, total))
    print('page errors:', errs)
    b.close()
print('FAILURES', fails); sys.exit(1 if fails or errs else 0)
