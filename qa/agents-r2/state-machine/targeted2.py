import json
from playwright.sync_api import sync_playwright
BASE='file:///Users/kumaraniket/Desktop/AI%20Governance%20Clone/clone/index.html'
ST='''()=>{const m=document.getElementById('mount');const q=s=>m.querySelectorAll(s).length;
const ps=m.querySelectorAll('[data-panel]');const r=ps[ps.length-1];
const crumb=r?[...r.querySelectorAll('h1,h2')].slice(0,2).map(e=>e.textContent.trim().slice(0,30)).join('|'):'';
const ovs=[...m.querySelectorAll('[data-overlay]')].map(n=>n.className.includes('p-dropdown-panel')?'07a':'07b');
const tr=m.querySelector('.h-20 .p-dropdown-trigger');
return {hash:location.hash.slice(1), ovs, aria:tr&&tr.getAttribute('aria-expanded'), ddcls:(m.querySelector('.h-20 .p-dropdown')||{}).className.includes('p-dropdown-open'), fs:document.querySelectorAll('.maximizeChatButton').length, fsbox:q('.fixed.inset-0.z-20'), handle:q('[data-resize-handle]'), modal:q('.animate-slideUp'), crumb, hdr:q('.h-20'), side:document.querySelectorAll('#sidebar').length}}'''
def S(pg, tag):
    pg.wait_for_timeout(750); s=pg.evaluate(ST); print('  %-34s %s'%(tag, json.dumps(s))); return s
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936}); pg.set_default_timeout(3000)
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    def fresh(h,q): pg.goto(BASE+'?'+q+'#'+h); pg.wait_for_timeout(300)
    print('J: fullscreen on 04, New Policy, Escape, Cancel')
    fresh('04-policies','J'); pg.locator('[title="Toggle Fullscreen"]').click(); S(pg,'fs')
    pg.get_by_text('New Policy',exact=False).first.click(); S(pg,'modal in fs')
    pg.keyboard.press('Escape'); S(pg,'Escape')
    print('K: dblclick trigger')
    fresh('03-live-events','K'); pg.locator('.h-20 .p-dropdown').dblclick(); S(pg,'dblclick')
    pg.locator('.h-20 .p-dropdown').click(); S(pg,'click')
    print('L: search typed then Escape in input')
    pg.locator('.p-dropdown-panel input').fill('zz'); S(pg,'typed zz'); pg.keyboard.press('Escape'); S(pg,'Escape')
    pg.locator('.h-20 .p-dropdown').click(); S(pg,'reopen'); print('   visible li', pg.evaluate("[...document.querySelectorAll('.p-dropdown-panel li')].filter(l=>l.style.display!=='none').length"))
    pg.keyboard.press('Escape')
    print('M: set hash to invalid / empty')
    fresh('03-live-events','M'); pg.evaluate("location.hash='nope'"); S(pg,'#nope'); pg.evaluate("location.hash=''"); S(pg,'#(empty)')
    pg.reload(); pg.wait_for_timeout(300); S(pg,'reload')
    print('N: sethash 07b while 07a open')
    fresh('03-live-events','N'); pg.locator('.h-20 .p-dropdown').click(); pg.evaluate("location.hash='07b-shell-hamburger'"); S(pg,'hash->07b')
    pg.evaluate("location.hash='05-traffic'"); S(pg,'hash->05')
    pg.go_back(); S(pg,'back'); pg.go_back(); S(pg,'back')
    print('O: fullscreen then Projects(left) page 07c, back')
    fresh('03-live-events','O'); pg.locator('[title="Toggle Fullscreen"]').click(); pg.evaluate("location.hash='07c-shell-projects'"); S(pg,'hash->07c in fs'); pg.go_back(); S(pg,'back')
    print('P: fullscreen + Escape key / drawer deep link in fs')
    fresh('05c-traffic-model-config','P'); pg.locator('[title="Toggle Fullscreen"]').click(); pg.evaluate("location.hash='07b-shell-hamburger'"); S(pg,'07b in fs')
    pg.mouse.click(300,500); S(pg,'mask click')
    print('Q: 05c accordion then nav away+back')
    fresh('05c-traffic-model-config','Q'); pg.locator('a.p-accordion-header-link').first.click(); S(pg,'acc toggle'); pg.go_back(); pg.go_forward(); S(pg,'back/fwd')
    print('errors', errs)
    b.close()
