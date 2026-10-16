from playwright.sync_api import sync_playwright
import pathlib
U = pathlib.Path('/Users/kumaraniket/Desktop/AI Governance Clone/clone/index.html').as_uri()
def cur(p): return p.evaluate("location.hash")
with sync_playwright() as pw:
    b = pw.chromium.launch(); p = b.new_page(viewport={'width':1920,'height':936})
    errs=[]; p.on('pageerror', lambda e: errs.append(str(e)))
    # F1
    for xy in [(1100,300),(1600,190),(1060,170),(1700,280),(1700,480),(1400,600)]:
        p.goto(U+'#04-policies'); p.wait_for_timeout(300)
        tgt = p.evaluate(f"(()=>{{const e=document.elementFromPoint({xy[0]},{xy[1]});return e.tagName+'.'+e.className.toString().slice(0,60)+' |'+(e.textContent||'').trim().slice(0,40)}})()")
        p.mouse.click(*xy); p.wait_for_timeout(200)
        modal = p.evaluate("!!document.querySelector('.animate-slideUp')")
        print('F1', xy, tgt, '->', cur(p), 'modal', modal)
    # F2
    for v,label in [('06d-rbac-config-permissions','RBAC Configuration'),('06e-rbac-config-roles','RBAC Configuration'),('06f-rbac-config-mapping','RBAC Configuration'),('06e-rbac-config-roles','Configuration'),('06d-rbac-config-permissions','Configuration'),('06b-rbac-usergroups','RBAC Configuration'),('06c-rbac-config-modules','Configuration')]:
        p.goto(U+'#'+v); p.wait_for_timeout(300)
        loc = p.locator('main button:visible, [data-panel] button:visible').filter(has_text=label)
        cands = [i for i in range(loc.count()) if loc.nth(i).inner_text().strip()==label]
        if not cands: print('F2 no button', v, label); continue
        el = loc.nth(cands[-1]); cls = el.get_attribute('class')
        el.click(); p.wait_for_timeout(200)
        print('F2', v, label, 'cls', (cls or '')[:80], '->', cur(p))
    # F3
    p.goto(U+'#04-policies'); p.wait_for_timeout(300)
    inp = p.locator('input[placeholder^="Search policies"]'); inp.fill('abc')
    p.get_by_text('Clear filter search').click(); p.wait_for_timeout(200)
    print('F3 input value after clear:', repr(inp.input_value()), cur(p))
    # F4
    p.goto(U+'#06-rbac-access'); p.wait_for_timeout(300)
    t = p.locator('#SMART_AI_PROMPT_POLICIES'); t.click(); p.wait_for_timeout(200)
    print('F4 tab aria', t.get_attribute('aria-selected'), cur(p))
    print('errors', errs)
    b.close()
