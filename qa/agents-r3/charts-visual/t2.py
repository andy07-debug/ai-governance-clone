import json
from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'; URL='file://'+ROOT+'/clone/index.html'
INFO = open('t1.py').read().split('INFO = r"""')[1].split('"""')[0]
EXTRA = r"""() => { const cv=document.querySelector('canvas[data-chart]'); const r=cv.getBoundingClientRect();
 let a=cv.parentElement, clip=[]; while(a && a!==document.body){ const ar=a.getBoundingClientRect(); const cs=getComputedStyle(a); if(cs.overflow!=='visible' && (r.right>ar.right+0.5||r.left<ar.left-0.5)) clip.push(a.className.slice(0,60)); a=a.parentElement; }
 return {docSW: document.documentElement.scrollWidth, iw: innerWidth, right: r.right, left:r.left, top:r.top, bottom:r.bottom, clip, ratio: cv.width/r.width, ratioH: cv.height/r.height}; }"""
errs=[]
def summ(tag,r,e):
    c=r['charts'][0]
    print(tag, 'inst',r['nInst'], c['id'], 'css %.1fx%.1f buf %dx%d parent %.1fx%.1f chart %sx%s'%(c['cssW'],c['cssH'],c['bw'],c['bh'],c['parentContentW'],c['parentContentH'],c['chartW'],c['chartH']), 'ratio %.3f/%.3f'%(e['ratio'],e['ratioH']), 'docSW',e['docSW'],'iw',e['iw'],'L-R %.0f-%.0f'%(e['left'],e['right']),'clip',e['clip'], 'painted',c['painted'])
with sync_playwright() as pw:
    b=pw.chromium.launch()
    for v in ['01-llm-analytics','05b-traffic-project-usage','05d-traffic-statistics']:
        pg=b.new_page(viewport={'width':1920,'height':936}); pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(URL+'#'+v); pg.wait_for_timeout(1300)
        def chk(tag):
            pg.wait_for_timeout(1300); summ(v[:3]+' '+tag, pg.evaluate(INFO), pg.evaluate(EXTRA))
        chk('init1920')
        for w in (1280,1600,1920):
            pg.set_viewport_size({'width':w,'height':936}); chk('w%d'%w)
        fs=lambda: pg.locator('[title="Toggle Fullscreen"]').first.click()
        fs(); chk('FS on 1920')
        pg.screenshot(path='fs-%s.png'%v[:3])
        for w in (1280,1600,1920):
            pg.set_viewport_size({'width':w,'height':936}); chk('FS w%d'%w)
        fs(); chk('FS off')
        pg.set_viewport_size({'width':1280,'height':936}); fs(); chk('FS on @1280'); fs(); chk('FS off @1280')
        pg.set_viewport_size({'width':1920,'height':936}); chk('back 1920')
        # nav while FS: go home and back via hash
        fs(); pg.wait_for_timeout(300); pg.evaluate("location.hash='#00-home'"); pg.wait_for_timeout(500); pg.evaluate("location.hash='#%s'"%v); chk('FS kept after nav')
        pg.screenshot(path='fsnav-%s.png'%v[:3])
        fs(); chk('FS off after nav')
        pg.close()
    print('ERRS',errs); b.close()
