"""Fullscreen + live-chart geometry probe for 01 / 05b / 05d, and overlays over 07c."""
import os, json
from playwright.sync_api import sync_playwright
ROOT = '/Users/kumaraniket/Desktop/AI Governance Clone'
OUT = os.path.join(ROOT, 'qa/agents-r2/visual-regression/probe')
os.makedirs(OUT, exist_ok=True)
URL = 'file://' + ROOT + '/clone/index.html'
GEO = '''() => [...document.querySelectorAll('canvas[data-chart]')].map(c => {const r=c.getBoundingClientRect(), p=c.parentElement.getBoundingClientRect();
 return {chart:c.dataset.chart, w:Math.round(r.width), h:Math.round(r.height), bw:c.width, bh:c.height, pw:Math.round(p.width), ph:Math.round(p.height), live: !!c.__chart, style:c.getAttribute('style'), pstyle:c.parentElement.getAttribute('style'), pcls:c.parentElement.className}})'''
res = {}
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1920, 'height': 936}); pg.set_default_timeout(3000)
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
    for v in ['01-llm-analytics', '05b-traffic-project-usage', '05d-traffic-statistics']:
        pg.goto('about:blank'); pg.goto(URL + '#' + v); pg.wait_for_timeout(1500)
        r = {'deep': pg.evaluate(GEO)}; pg.screenshot(path=f'{OUT}/{v}-0deep.png')
        pg.locator('[title="Toggle Fullscreen"]').first.click(); pg.wait_for_timeout(1500)
        r['fs'] = pg.evaluate(GEO); pg.screenshot(path=f'{OUT}/{v}-1fs.png')
        pg.locator('[title="Toggle Fullscreen"]').first.click(); pg.wait_for_timeout(1500)
        r['fsoff'] = pg.evaluate(GEO); pg.screenshot(path=f'{OUT}/{v}-2fsoff.png')
        # fs on, go home, come back via __show (fullscreen persists), off
        pg.locator('[title="Toggle Fullscreen"]').first.click(); pg.wait_for_timeout(800)
        pg.evaluate('()=>window.__show("00-home")'); pg.wait_for_timeout(500)
        pg.evaluate('v=>window.__show(v)', v); pg.wait_for_timeout(1500)
        r['fs-renav'] = pg.evaluate(GEO); pg.screenshot(path=f'{OUT}/{v}-3fsrenav.png')
        pg.locator('.maximizeChatButton').first.click(); pg.wait_for_timeout(1500)
        r['bubble-off'] = pg.evaluate(GEO); pg.screenshot(path=f'{OUT}/{v}-4bubbleoff.png')
        res[v] = r
    pg.goto('about:blank'); pg.goto(URL + '#07c-shell-projects'); pg.wait_for_timeout(1000)
    pg.locator('.h-20 .p-dropdown').first.click(); pg.wait_for_timeout(900); pg.screenshot(path=f'{OUT}/07c-dd.png')
    pg.keyboard.press('Escape'); pg.wait_for_timeout(700)
    pg.locator('[title="Open sidebar"]').first.click(); pg.wait_for_timeout(900); pg.screenshot(path=f'{OUT}/07c-drawer.png')
    for live in ['07a-shell-mode-dropdown', '07b-shell-hamburger']:
        pg.goto('about:blank'); pg.goto(URL + '#' + live); pg.wait_for_timeout(1000); pg.screenshot(path=f'{OUT}/{live}-deep.png')
    b.close()
print(json.dumps(res, indent=1)); print('errors', errs[:8])
