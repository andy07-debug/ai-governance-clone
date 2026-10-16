import os, sys, json, re, traceback
from playwright.sync_api import sync_playwright
import numpy as np
from PIL import Image
ROOT = '/Users/kumaraniket/Desktop/AI Governance Clone'
OUT = os.path.join(ROOT, 'qa/agents-r2/visual-regression/shots')
os.makedirs(OUT, exist_ok=True)
URL = 'file://' + ROOT + '/clone/index.html'
ANIM_OFF = '*,*::before,*::after{animation-duration:0s!important;animation-delay:0s!important;transition:none!important;caret-color:transparent!important}'
views = re.findall(r'<template id="v-([0-9][^"]*)"', open(ROOT + '/clone/index.html').read())
pages = [v for v in views if v not in ('07a-shell-mode-dropdown', '07b-shell-hamburger')]

def load(pg, v):
    pg.goto('about:blank'); pg.goto(URL + '#' + v); pg.add_style_tag(content=ANIM_OFF); pg.wait_for_timeout(1400)
def shot(pg, name):
    p = os.path.join(OUT, name + '.png')
    pg.evaluate('document.activeElement && document.activeElement.blur && document.activeElement.blur()')
    pg.mouse.move(0, 935)
    pg.wait_for_timeout(150)
    pg.screenshot(path=p); return p
def diff(a, b, name):
    A = np.asarray(Image.open(a).convert('RGB')).astype(int); B = np.asarray(Image.open(b).convert('RGB')).astype(int)
    if A.shape != B.shape: return ('shape', A.shape, B.shape)
    d = np.abs(A - B).sum(2) > 30
    if not d.any(): return (0.0, None)
    ys, xs = np.where(d)
    m = (np.stack([d]*3, 2) * 255).astype(np.uint8)
    Image.fromarray(m).save(os.path.join(OUT, 'diff-' + name + '.png'))
    return (round(100 * d.mean(), 3), (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())))

scen = sys.argv[1:]
res = {}
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1920, 'height': 936}); pg.set_default_timeout(3000)
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    base = {}
    for v in views:
        load(pg, v); base[v] = shot(pg, 'deep-' + v)
    def run(key, fn):
        try: res[key] = fn()
        except Exception as e: res[key] = 'ERR ' + str(e).split('\n')[0][:150]
        print(key, res[key], flush=True)
    for v in pages:
        if 'fromother' in scen:
            for src in ['01-llm-analytics', '05b-traffic-project-usage', '07c-shell-projects', '06f-rbac-config-mapping', '04c-policies-newpolicy-modal']:
                if src == v: continue
                def f(src=src):
                    load(pg, src); pg.evaluate('v=>window.__show(v)', v); pg.wait_for_timeout(1400)
                    return diff(base[v], shot(pg, 'arr-' + v + '-from-' + src), v + '-from-' + src)
                run(v + ' <- ' + src, f)
        if 'fs' in scen:
            def f():
                load(pg, v)
                if not pg.locator('[title="Toggle Fullscreen"]').count(): return 'no toggle'
                pg.locator('[title="Toggle Fullscreen"]').first.click(force=True); pg.wait_for_timeout(1400); shot(pg, 'fs-' + v)
                pg.locator('[title="Toggle Fullscreen"]').first.click(force=True); pg.wait_for_timeout(1400)
                r1 = diff(base[v], shot(pg, 'fsoff-' + v), 'fsoff-' + v)
                pg.locator('[title="Toggle Fullscreen"]').first.click(force=True); pg.wait_for_timeout(500)
                r2 = None
                if pg.locator('.maximizeChatButton').count():
                    pg.locator('.maximizeChatButton').first.click(force=True); pg.wait_for_timeout(1400)
                    r2 = diff(base[v], shot(pg, 'fsoff2-' + v), 'fsoff2-' + v)
                return [r1, r2]
            run(v + ' fs on/off', f)
            def g():
                # fullscreen on, then navigate in-app (via __show) to home and back
                load(pg, v)
                if not pg.locator('[title="Toggle Fullscreen"]').count(): return 'no toggle'
                pg.locator('[title="Toggle Fullscreen"]').first.click(force=True); pg.wait_for_timeout(500)
                other = '00-home' if v != '00-home' else '01-llm-analytics'
                pg.evaluate('v=>window.__show(v)', other); pg.wait_for_timeout(500)
                pg.locator('[title="Toggle Fullscreen"]').first.click(force=True); pg.wait_for_timeout(500)
                pg.evaluate('v=>window.__show(v)', v); pg.wait_for_timeout(1400)
                return diff(base[v], shot(pg, 'fsnav-' + v), 'fsnav-' + v)
            run(v + ' fs->nav->fsoff->nav', g)
        if 'overlay' in scen:
            def f():
                load(pg, v)
                pg.locator('.h-20 .p-dropdown').first.click(force=True); pg.wait_for_timeout(500)
                shot(pg, 'dd-' + v)
                pg.keyboard.press('Escape'); pg.wait_for_timeout(1400)
                r1 = diff(base[v], shot(pg, 'ddx-' + v), 'ddx-' + v)
                pg.locator('[title="Open sidebar"]').first.click(force=True); pg.wait_for_timeout(500)
                shot(pg, 'dr-' + v)
                pg.locator('[title="Click to close sidebar"]').first.click(force=True); pg.wait_for_timeout(1400)
                r2 = diff(base[v], shot(pg, 'drx-' + v), 'drx-' + v)
                return [r1, r2]
            run(v + ' dd/drawer', f)
    b.close()
print('pageerrors', errs[:5])
json.dump(res, open(os.path.join(OUT, '..', 'res2-' + '-'.join(scen) + '.json'), 'w'), indent=1)
