from playwright.sync_api import sync_playwright
URL='file:///Users/kumaraniket/Desktop/AI Governance Clone/clone/index.html'
OUT='/Users/kumaraniket/Desktop/AI Governance Clone/qa/agents-r2/visual-regression/probe/'
S='''()=>({hash:location.hash, len:history.length, overlay:!!document.querySelector('[data-overlay]'), projGrid:!!document.querySelector('[data-panel]:last-of-type') && /Shared with me/.test(document.querySelectorAll('[data-panel]')[document.querySelectorAll('[data-panel]').length-1].textContent), home:/System Health/.test(document.body.innerText)})'''
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    for opener,name in [('.h-20 .p-dropdown','dd'),('[title="Open sidebar"]','drawer')]:
        pg.goto('about:blank'); pg.goto(URL+'#00-home'); pg.wait_for_timeout(800)
        pg.click('[data-testid="headerProjectsButton"]'); pg.wait_for_timeout(700); print(name,'on 07c', pg.evaluate(S))
        pg.click(opener); pg.wait_for_timeout(700); print(name,'overlay open', pg.evaluate(S))
        pg.go_back(); pg.wait_for_timeout(900); print(name,'after Back', pg.evaluate(S)); pg.screenshot(path=OUT+f'hist-{name}-back.png')
        pg.go_forward(); pg.wait_for_timeout(900); print(name,'after Forward', pg.evaluate(S)); pg.screenshot(path=OUT+f'hist-{name}-fwd.png')
        pg.keyboard.press('Escape'); pg.wait_for_timeout(700); print(name,'after Esc', pg.evaluate(S))
    b.close()
