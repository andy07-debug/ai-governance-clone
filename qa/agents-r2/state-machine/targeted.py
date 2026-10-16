import sys, json
from playwright.sync_api import sync_playwright
BASE='file:///Users/kumaraniket/Desktop/AI%20Governance%20Clone/clone/index.html'
ST='''()=>{const m=document.getElementById('mount');const q=s=>m.querySelectorAll(s).length;
const ps=m.querySelectorAll('[data-panel]');const r=ps[ps.length-1];
const crumb=r?[...r.querySelectorAll('h1,h2')].slice(0,2).map(e=>e.textContent.trim().slice(0,40)).join('|'):'';
const ovs=[...m.querySelectorAll('[data-overlay]')].map(n=>n.className.includes('p-dropdown-panel')?'07a':'07b');
const tr=m.querySelector('.h-20 .p-dropdown-trigger');
return {hash:location.hash.slice(1), ovs, aria:tr&&tr.getAttribute('aria-expanded'), fs:document.querySelectorAll('.maximizeChatButton').length, fsbox:q('.fixed.inset-0.z-20'), modal:q('.animate-slideUp'), crumb, hl:history.length}}'''
def S(pg, tag):
    pg.wait_for_timeout(750); s=pg.evaluate(ST); print('  %-40s %s'%(tag, json.dumps(s))); return s
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936}); pg.set_default_timeout(3000)
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    def fresh(h='',q='a'):
        pg.goto(BASE+'?'+q+('#'+h if h else '')); pg.wait_for_timeout(300)
    print('A: Live Events -> dropdown -> pick AI Governance -> Back')
    fresh('', 'A'); S(pg,'start')
    pg.get_by_text('Live Events',exact=True).click(); S(pg,'live events')
    pg.locator('.h-20 .p-dropdown').click(); S(pg,'dropdown open')
    pg.locator('.p-dropdown-panel').get_by_text('AI Governance',exact=True).click(); S(pg,'picked AI Governance')
    pg.go_back(); S(pg,'Back')
    pg.go_back(); S(pg,'Back again')
    print('A2: home -> dropdown -> pick AI Governance -> Back')
    fresh('', 'A2'); S(pg,'start')
    pg.locator('.h-20 .p-dropdown').click(); S(pg,'dropdown open')
    pg.locator('.p-dropdown-panel').get_by_text('AI Governance',exact=True).click(); S(pg,'picked AI Governance')
    pg.go_back(); S(pg,'Back')
    print('B: home -> Live Events -> dropdown open -> Back -> Forward')
    fresh('', 'B'); pg.get_by_text('Live Events',exact=True).click()
    pg.locator('.h-20 .p-dropdown').click(); S(pg,'dropdown open on 03')
    pg.go_back(); S(pg,'Back')
    pg.go_forward(); S(pg,'Forward')
    pg.keyboard.press('Escape'); S(pg,'Escape')
    pg.go_back(); S(pg,'Back')
    pg.go_forward(); S(pg,'Forward')
    print('B2: same with hamburger drawer')
    fresh('', 'B2'); pg.get_by_text('Policies',exact=True).click()
    pg.locator('[title="Open sidebar"]').click(); S(pg,'drawer open on 04')
    pg.go_back(); S(pg,'Back'); pg.go_forward(); S(pg,'Forward')
    pg.locator('[title="Click to close sidebar"]').click(); S(pg,'drawer X')
    print('C: reload while dropdown open on 03')
    fresh('', 'C'); pg.get_by_text('Live Events',exact=True).click(); pg.locator('.h-20 .p-dropdown').click(); S(pg,'open')
    pg.reload(); pg.wait_for_timeout(300); S(pg,'reloaded')
    pg.keyboard.press('Escape'); S(pg,'Escape')
    print('D: drawer geometry')
    fresh('07b-shell-hamburger','D'); S(pg,'deeplink 07b')
    print('  ', pg.evaluate('''()=>{const s=document.querySelector('[data-overlay] .p-sidebar');const r=s.getBoundingClientRect();const mk=document.querySelector('[data-overlay]').getBoundingClientRect();return [r.x,r.y,r.width,r.height,mk.width,mk.height, document.elementFromPoint(1800,500).className.slice(0,80)]}'''))
    pg.mouse.click(1800,500); S(pg,'click 1800,500')
    print('E: fullscreen on 03 -> Back -> Forward; fullscreen -> dropdown via history')
    fresh('', 'E'); pg.get_by_text('Live Events',exact=True).click(); pg.locator('[title="Toggle Fullscreen"]').click(); S(pg,'fs on 03')
    pg.go_back(); S(pg,'Back (home)'); pg.go_forward(); S(pg,'Forward')
    pg.locator('.maximizeChatButton').click(); S(pg,'bubble exits')
    print('E2: dropdown open on 03 -> Back -> fullscreen on home -> Forward (overlay entry)')
    fresh('', 'E2'); pg.get_by_text('Live Events',exact=True).click(); pg.locator('.h-20 .p-dropdown').click(); pg.go_back(); S(pg,'Back')
    pg.locator('[title="Toggle Fullscreen"]').click(); S(pg,'fs on')
    pg.go_forward(); S(pg,'Forward -> overlay entry in fullscreen')
    print('  visible panel?', pg.evaluate('''()=>{const p=document.querySelector('[data-overlay]');if(!p)return null;const r=p.getBoundingClientRect();const e=document.elementFromPoint(r.x+r.width/2,r.y+20);return [r.x,r.y,r.width,r.height,getComputedStyle(p).zIndex,!!(e&&e.closest('[data-overlay]'))]}'''))
    pg.keyboard.press('Escape'); S(pg,'Escape')
    print('F: 04c modal escape then back')
    fresh('04-policies','F'); pg.get_by_text('New Policy',exact=False).first.click(); S(pg,'modal')
    pg.keyboard.press('Escape'); S(pg,'Escape'); pg.go_back(); S(pg,'Back')
    print('G: dropdown -> hamburger')
    fresh('03-live-events','G'); pg.locator('.h-20 .p-dropdown').click(); pg.locator('[title="Open sidebar"]').click(); S(pg,'hamburger while dd open')
    pg.keyboard.press('Escape'); S(pg,'Escape')
    print('H: dropdown open + fullscreen toggle click')
    fresh('03-live-events','H'); pg.locator('.h-20 .p-dropdown').click(); pg.locator('[title="Toggle Fullscreen"]').click(); S(pg,'fs click while dd')
    print('errors', errs)
    b.close()
