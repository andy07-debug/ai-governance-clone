import re, os
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
OUT='/Users/kumaraniket/Desktop/AI Governance Clone/qa/agents/analytics+firewall+events'
v='08-fullscreen-live-events'
p=open(f'{ROOT}/capture/{v}/page.html',encoding='utf-8').read()
ha=re.search(r'<html([^>]*)>',p).group(1)
body=re.search(r'(<body[^>]*>.*</body>)',p,re.S).group(1)
body=re.sub(r'<div id="claude-agent-glow-border".*?</div></div>','',body,flags=re.S)
body=re.sub(r'<div id="claude-phantom-cursor".*?</svg></div>','',body,flags=re.S)
css=open(f'{ROOT}/capture/{v}/styles.css',encoding='utf-8').read()
css=re.sub(r'url\("?(?:https://ai-governance-ui-prod-[^/"]+)?/([0-9a-f]{20}\.(?:woff2|woff|ttf))"?\)', r'url("../../../clone/assets/\1")', css)
open(f'{OUT}/b08.css','w').write(css)
open(f'{OUT}/b08.html','w').write('<!doctype html><html%s><head><meta charset="utf-8"><link rel="stylesheet" href="b08.css"></head>%s</html>'%(ha,body))
ANIM='*,*::before,*::after{animation-duration:0s!important;animation-delay:0s!important;transition:none!important;caret-color:transparent!important}'
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    pg.goto('file://'+OUT+'/b08.html'); pg.add_style_tag(content=ANIM); pg.wait_for_timeout(600); pg.screenshot(path=OUT+'/b08.png')
    a=pg.evaluate("document.querySelector('#root').innerText")
    pg.goto('file://'+ROOT+'/clone/index.html#03-live-events'); pg.reload(); pg.add_style_tag(content=ANIM); pg.wait_for_timeout(400)
    pg.click('[title="Toggle Fullscreen"]'); pg.mouse.move(1900,900); pg.wait_for_timeout(500); pg.screenshot(path=OUT+'/c08.png')
    c=pg.evaluate("document.querySelector('#root').innerText")
    b.close()
x=np.asarray(Image.open(OUT+'/b08.png').convert('RGB')).astype(int); y=np.asarray(Image.open(OUT+'/c08.png').convert('RGB')).astype(int)
d=np.abs(x-y).sum(2)>30; ys,xs=np.nonzero(d); print('diff%',round(100*d.mean(),3), (xs.min(),ys.min(),xs.max(),ys.max()) if len(xs) else None)
Image.fromarray((d*255).astype('uint8')).save(OUT+'/d08.png')
import difflib
print('\n'.join(difflib.unified_diff([l for l in a.splitlines() if l.strip()],[l for l in c.splitlines() if l.strip()],lineterm='',n=0)))
