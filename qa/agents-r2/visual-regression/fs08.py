import os, re
from playwright.sync_api import sync_playwright
import numpy as np
from PIL import Image
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'; HERE=ROOT+'/qa/agents-r2/visual-regression'
v='08-fullscreen-live-events'
p=open(f'{ROOT}/capture/{v}/page.html',encoding='utf-8').read()
ha=re.search(r'<html([^>]*)>',p).group(1); body=re.search(r'(<body[^>]*>.*</body>)',p,re.S).group(1)
body=re.sub(r'<div id="claude-agent-glow-border".*?</div></div>','',body,flags=re.S); body=re.sub(r'<div id="claude-phantom-cursor".*?</svg></div>','',body,flags=re.S)
css=open(f'{ROOT}/capture/{v}/styles.css',encoding='utf-8').read()
css=re.sub(r'url\("?(?:https://ai-governance-ui-prod-[^/"]+)?/([0-9a-f]{20}\.(?:woff2|woff|ttf))"?\)', r'url("../../../../clone/assets/\1")', css)
open(f'{HERE}/base/{v}.css','w').write(css)
open(f'{HERE}/base/{v}.html','w').write('<!doctype html><html%s><head><meta charset="utf-8"><link rel="stylesheet" href="%s.css"></head>%s</html>'%(ha,v,body))
AO='*,*::before,*::after{animation-duration:0s!important;animation-delay:0s!important;transition:none!important;caret-color:transparent!important}'
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    pg.goto(f'file://{HERE}/base/{v}.html'); pg.add_style_tag(content=AO); pg.wait_for_timeout(800); pg.screenshot(path=f'{HERE}/probe/live08.png')
    for start in ['03-live-events','00-home']:
        pg.goto('about:blank'); pg.goto(f'file://{ROOT}/clone/index.html#'+start); pg.add_style_tag(content=AO); pg.wait_for_timeout(1000)
        pg.click('[title="Toggle Fullscreen"]')
        if start=='00-home':
            pg.get_by_text('Live Events',exact=True).click()
        pg.wait_for_timeout(1200); pg.mouse.move(1900,930); pg.wait_for_timeout(200); pg.screenshot(path=f'{HERE}/probe/clonefs03-{start}.png')
        A=np.asarray(Image.open(f'{HERE}/probe/live08.png').convert('RGB')).astype(int); B=np.asarray(Image.open(f'{HERE}/probe/clonefs03-{start}.png').convert('RGB')).astype(int)
        d=np.abs(A-B).sum(2)>30
        print(start, round(100*d.mean(),3), np.where(d.any(0))[0][[0,-1]] if d.any() else None, np.where(d.any(1))[0][[0,-1]] if d.any() else None, pg.evaluate('location.hash'))
        Image.fromarray((np.stack([d]*3,2)*255).astype(np.uint8)).save(f'{HERE}/probe/diff-fs03-{start}.png')
    b.close()
