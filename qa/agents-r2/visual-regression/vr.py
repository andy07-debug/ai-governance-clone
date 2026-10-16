import os, sys, json
from playwright.sync_api import sync_playwright
import numpy as np
from PIL import Image
ROOT = '/Users/kumaraniket/Desktop/AI Governance Clone'
OUT = os.path.join(ROOT, 'qa/agents-r2/visual-regression/shots')
os.makedirs(OUT, exist_ok=True)
URL = 'file://' + ROOT + '/clone/index.html'
ANIM_OFF = '*,*::before,*::after{animation-duration:0s!important;animation-delay:0s!important;transition:none!important;caret-color:transparent!important}'
import re
views = re.findall(r'<template id="v-([0-9][^"]*)"', open(ROOT + '/clone/index.html').read())
views = [v for v in views if v not in ('07a-shell-mode-dropdown', '07b-shell-hamburger')] + ['07a-shell-mode-dropdown', '07b-shell-hamburger']

def load(pg, v):
    pg.goto('about:blank'); pg.goto(URL + '#' + v); pg.add_style_tag(content=ANIM_OFF); pg.wait_for_timeout(800)
def shot(pg, name):
    p = os.path.join(OUT, name + '.png'); pg.evaluate('document.activeElement && document.activeElement.blur && document.activeElement.blur()')
    pg.wait_for_timeout(100)
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

res = {}
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1920, 'height': 936}); pg.set_default_timeout(3000)
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    base = {}
    for v in views:
        load(pg, v); base[v] = shot(pg, 'deep-' + v)
    scen = sys.argv[1:] or ['fromhome', 'fromother', 'back', 'fs', 'overlay']
    for v in views:
        if v.startswith('07a') or v.startswith('07b'): continue
        if 'fromhome' in scen:
            src = '05c-traffic-model-config' if v == '00-home' else '00-home'
            load(pg, src); pg.evaluate('v=>window.__show(v)', v); pg.wait_for_timeout(800)
            res[v + ' <- ' + src] = diff(base[v], shot(pg, 'arr-' + v + '-from-' + src), v + '-from-' + src)
        if 'fromother' in scen:
            for src in ['01-llm-analytics', '05b-traffic-project-usage', '07c-shell-projects', '06f-rbac-config-mapping']:
                if src == v: continue
                load(pg, src); pg.evaluate('v=>window.__show(v)', v); pg.wait_for_timeout(800)
                res[v + ' <- ' + src] = diff(base[v], shot(pg, 'arr-' + v + '-from-' + src), v + '-from-' + src)
        if 'back' in scen:
            other = '00-home' if v != '00-home' else '03-live-events'
            load(pg, v); pg.evaluate('v=>window.__show(v)', other); pg.wait_for_timeout(300); pg.go_back(); pg.wait_for_timeout(800)
            res[v + ' back'] = diff(base[v], shot(pg, 'back-' + v), 'back-' + v)
        if 'fs' in scen:
          try:
            load(pg, v)
            if pg.locator('[title="Toggle Fullscreen"]').count():
                pg.locator('[title="Toggle Fullscreen"]').first.click(); pg.wait_for_timeout(800); shot(pg, 'fs-' + v)
                pg.locator('[title="Toggle Fullscreen"]').first.click(); pg.wait_for_timeout(800)
                res[v + ' fs on/off(toggle)'] = diff(base[v], shot(pg, 'fsoff-' + v), 'fsoff-' + v)
                pg.locator('[title="Toggle Fullscreen"]').first.click(); pg.wait_for_timeout(500)
                if pg.locator('.maximizeChatButton').count():
                    pg.locator('.maximizeChatButton').first.click(); pg.wait_for_timeout(800)
                    res[v + ' fs on/off(bubble)'] = diff(base[v], shot(pg, 'fsoff2-' + v), 'fsoff2-' + v)
            else:
                res[v + ' fs'] = 'no toggle'
        if 'overlay' in scen:
            load(pg, v)
            pg.locator('.h-20 .p-dropdown').first.click(); pg.wait_for_timeout(500)
            pg.keyboard.press('Escape'); pg.wait_for_timeout(800)
            res[v + ' dd open/esc'] = diff(base[v], shot(pg, 'ddx-' + v), 'ddx-' + v)
            pg.locator('[title="Open sidebar"]').first.click(); pg.wait_for_timeout(500)
            pg.locator('[title="Click to close sidebar"]').first.click(); pg.wait_for_timeout(800)
            res[v + ' drawer open/close'] = diff(base[v], shot(pg, 'drx-' + v), 'drx-' + v)
    b.close()
for k, r in res.items(): print(k, r)
print('pageerrors', errs[:5])
json.dump(res, open(os.path.join(OUT, '..', 'res-' + '-'.join(scen) + '.json'), 'w'), indent=1)
