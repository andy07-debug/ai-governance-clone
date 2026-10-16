"""Render clone views + raw-capture baselines at 1920x936 and pixel-diff them."""
import os, re, sys, json
from playwright.sync_api import sync_playwright
import numpy as np
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAP, CLONE, QA = [os.path.join(ROOT, d) for d in ('capture', 'clone', 'qa')]
views = sorted(d for d in os.listdir(CAP) if os.path.isfile(os.path.join(CAP, d, 'page.html')) and not d.startswith('08-'))
os.makedirs(os.path.join(QA, 'clone'), exist_ok=True); os.makedirs(os.path.join(QA, 'base'), exist_ok=True)

def baseline_file(v):
    p = open(os.path.join(CAP, v, 'page.html'), encoding='utf-8').read()
    ha = re.search(r'<html([^>]*)>', p).group(1)
    body = re.search(r'(<body[^>]*>.*</body>)', p, re.S).group(1)
    body = re.sub(r'<div id="claude-agent-glow-border".*?</div></div>', '', body, flags=re.S)
    body = re.sub(r'<div id="claude-phantom-cursor".*?</svg></div>', '', body, flags=re.S)
    css = open(os.path.join(CAP, v, 'styles.css'), encoding='utf-8').read()
    css = re.sub(r'url\("?(?:https://ai-governance-ui-prod-[^/"]+)?/([0-9a-f]{20}\.(?:woff2|woff|ttf))"?\)', r'url("../clone/assets/\1")', css)
    open(os.path.join(QA, 'base', v + '.css'), 'w').write(css)
    f = os.path.join(QA, 'base', v + '.html')
    open(f, 'w').write('<!doctype html><html%s><head><meta charset="utf-8"><link rel="stylesheet" href="%s.css"><link rel="stylesheet" href="../clone/assets/app.css" media="not all"></head>%s</html>' % (ha, v, body))
    return f

ANIM_OFF = '*,*::before,*::after{animation-duration:0s!important;animation-delay:0s!important;transition:none!important;caret-color:transparent!important}'
res = {}
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={'width': 1920, 'height': 936})
    for v in views:
        pg.goto('file://' + os.path.join(CLONE, 'index.html') + '#' + v); pg.add_style_tag(content=ANIM_OFF)
        pg.wait_for_timeout(1600); pg.screenshot(path=os.path.join(QA, 'clone', v + '.png'))
        pg.goto('file://' + baseline_file(v)); pg.add_style_tag(content=ANIM_OFF)
        pg.wait_for_timeout(500); pg.screenshot(path=os.path.join(QA, 'base', v + '.png'))
        a = np.asarray(Image.open(os.path.join(QA, 'clone', v + '.png')).convert('RGB')).astype(int)
        c = np.asarray(Image.open(os.path.join(QA, 'base', v + '.png')).convert('RGB')).astype(int)
        d = np.abs(a - c).sum(2) > 30
        res[v] = round(100 * d.mean(), 3)
        print(v, 'diff%', res[v], flush=True)
    b.close()
json.dump(res, open(os.path.join(QA, 'diff.json'), 'w'), indent=1)
