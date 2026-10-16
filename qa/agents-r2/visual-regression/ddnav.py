from playwright.sync_api import sync_playwright
import numpy as np
from PIL import Image
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'; HERE=ROOT+'/qa/agents-r2/visual-regression'
URL=f'file://{ROOT}/clone/index.html'
AO='*,*::before,*::after{animation-duration:0s!important;animation-delay:0s!important;transition:none!important;caret-color:transparent!important}'
def load(pg,v): pg.goto('about:blank'); pg.goto(URL+'#'+v); pg.add_style_tag(content=AO); pg.wait_for_timeout(1400)
def shot(pg,n):
    pg.evaluate('document.activeElement&&document.activeElement.blur()'); pg.mouse.move(0,935); pg.wait_for_timeout(200); p=f'{HERE}/probe/{n}.png'; pg.screenshot(path=p); return p
def diff(a,b):
    A=np.asarray(Image.open(a).convert('RGB')).astype(int); B=np.asarray(Image.open(b).convert('RGB')).astype(int); d=np.abs(A-B).sum(2)>30
    return round(100*d.mean(),3), ((int(np.where(d.any(0))[0][0]),int(np.where(d.any(1))[0][0]),int(np.where(d.any(0))[0][-1]),int(np.where(d.any(1))[0][-1])) if d.any() else None)
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936}); pg.set_default_timeout(3000)
    base={}
    for v in ['03-live-events','06-rbac-access','00-home','05a-traffic-projects']:
        load(pg,v); base[v]=shot(pg,'ddnav-deep-'+v)
    cases=[('00-home','Live Events card', lambda: pg.get_by_text('Live Events',exact=True).click(), '03-live-events'),
           ('00-home','RBAC btn', lambda: pg.get_by_text('RBAC',exact=True).click(), '06-rbac-access'),
           ('03-live-events','breadcrumb home', lambda: pg.click('main button[title="Back to home"], main span.p-1.text-indigo-600'), '00-home'),
           ('05b-traffic-project-usage','crumb Projects', lambda: pg.locator('main .p-breadcrumb').get_by_text('Projects',exact=True).click(), '05a-traffic-projects')]
    for start,name,act,exp in cases:
        load(pg,start); pg.click('.h-20 .p-dropdown'); pg.wait_for_timeout(700)
        try: act()
        except Exception as e: print(start,name,'ERR',str(e)[:100]); continue
        pg.wait_for_timeout(1400)
        h=pg.evaluate('location.hash'); ov=pg.evaluate("document.querySelectorAll('[data-overlay]').length")
        print(start,'dd open ->',name,h,'overlays',ov, diff(base[exp], shot(pg,'ddnav-'+name.replace(' ','_'))))
    # dd open then fullscreen toggle
    load(pg,'03-live-events'); pg.click('[title="Toggle Fullscreen"]'); pg.wait_for_timeout(1200); fsbase=shot(pg,'ddnav-fsbase')
    load(pg,'03-live-events'); pg.click('.h-20 .p-dropdown'); pg.wait_for_timeout(700); pg.click('[title="Toggle Fullscreen"]'); pg.wait_for_timeout(1200)
    print('dd open -> fullscreen', pg.evaluate('location.hash'), diff(fsbase, shot(pg,'ddnav-fs')))
    b.close()
