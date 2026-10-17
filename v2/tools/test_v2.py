"""Click every wired control in every v2 screen/overlay; report errors and dangling targets."""
import os, json
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
URL = 'file://' + os.path.join(ROOT, 'clone', 'index.html')
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1512, 'height': 863})
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: errs.append(m.text) if m.type in ('error', 'warning') else None)
    pg.goto(URL); pg.wait_for_timeout(500)
    inv = pg.evaluate("""()=>({screens:[...document.querySelectorAll('template[id^="s-"]')].map(t=>t.id.slice(2)),
      overlays:[...document.querySelectorAll('template[id^="o-"]')].map(t=>t.id.slice(2)),
      gos:[...new Set([...document.querySelectorAll('template')].flatMap(t=>[...t.content.querySelectorAll('[data-go]')].map(e=>e.getAttribute('data-go'))).concat([...document.querySelectorAll('#mount [data-go]')].map(e=>e.getAttribute('data-go'))))],
      opens:[...new Set([...document.querySelectorAll('template')].flatMap(t=>[...t.content.querySelectorAll('[data-open]')].map(e=>e.getAttribute('data-open'))))]})""")
    print('screens', inv['screens']); print('overlays', inv['overlays'])
    print('data-go targets missing:', sorted(set(inv['gos']) - set(inv['screens'])))
    print('data-open targets missing:', sorted(set(inv['opens']) - set(inv['overlays'])))
    unopened = sorted(set(inv['overlays']) - set(inv['opens'])); print('overlays never opened by any control:', unopened)
    results = {}
    for s in inv['screens']:
        pg.goto('about:blank'); pg.goto(URL + '#' + s); pg.wait_for_timeout(700)
        n = {'go': 0, 'open': 0, 'tab': 0, 'toggle': 0, 'fail': []}
        # tabs + toggles: click each, ensure no error
        for kind in ('tab', 'toggle'):
            cnt = pg.locator('#screen [data-%s]' % kind).count()
            for i in range(cnt):
                el = pg.locator('#screen [data-%s]' % kind).nth(i)
                try:
                    if el.is_visible(): el.click(timeout=1500); n[kind] += 1
                except Exception as e: n['fail'].append('%s#%d %s' % (kind, i, str(e)[:60]))
        # overlays: open each, check it rendered, close
        cnt = pg.locator('#screen [data-open]').count()
        for i in range(cnt):
            el = pg.locator('#screen [data-open]').nth(i)
            oid = el.get_attribute('data-open')
            try:
                el.scroll_into_view_if_needed(timeout=1500); el.click(timeout=1500); pg.wait_for_timeout(300)
                ok = pg.evaluate("(id)=>!!document.querySelector('[data-overlay=\"'+id+'\"]')", oid)
                if not ok: n['fail'].append('overlay %s did not render' % oid)
                pg.keyboard.press('Escape'); pg.wait_for_timeout(150); n['open'] += 1
            except Exception as e: n['fail'].append('open %s %s' % (oid, str(e)[:60]))
        # navigation: each data-go reaches its screen
        gos = pg.evaluate("[...document.querySelectorAll('#screen [data-go], #mount [data-go]')].map(e=>e.getAttribute('data-go'))")
        for g in sorted(set(gos)):
            if g not in inv['screens']: continue
            pg.goto('about:blank'); pg.goto(URL + '#' + s); pg.wait_for_timeout(300)
            el = pg.locator('[data-go="%s"]' % g).first
            try:
                el.scroll_into_view_if_needed(timeout=1500); el.click(timeout=1500); pg.wait_for_timeout(250)
                st = pg.evaluate('window.__v2.state().screen')
                if st != g: n['fail'].append('go %s -> %s' % (g, st))
                n['go'] += 1
            except Exception as e: n['fail'].append('go %s %s' % (g, str(e)[:60]))
        results[s] = n
        print(s, {k: v for k, v in n.items() if k != 'fail'}, 'FAILS:' if n['fail'] else '', n['fail'][:6])
    pg.goto('about:blank'); pg.goto(URL + '#policies'); pg.wait_for_timeout(300); pg.go_back() if False else None
    print('page errors/warnings:', [e for e in errs if 'no screen' not in e][:10])
    print('warnings for missing screens (expected for non-essential sections):', sorted(set(e for e in errs if 'no screen' in e)))
    b.close()
