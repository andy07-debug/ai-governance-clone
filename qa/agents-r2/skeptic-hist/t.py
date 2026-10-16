from playwright.sync_api import sync_playwright
import pathlib
base = pathlib.Path("/Users/kumaraniket/Desktop/AI Governance Clone/clone/index.html").as_uri()
out = pathlib.Path(__file__).parent
def st(p):
    return p.evaluate("""()=>({hash:location.hash,len:history.length,
      ov:!!document.querySelector('[data-overlay]'),
      label:(document.querySelector('.h-20 .p-dropdown .p-dropdown-label')||{}).textContent,
      hl:[...document.querySelectorAll('[data-overlay] li')].filter(l=>l.classList.contains('p-highlight')||l.getAttribute('aria-selected')==='true').map(l=>l.textContent.trim().slice(0,30)),
      body:document.body.innerText.slice(0,120).replace(/\\s+/g,' ')})""")
with sync_playwright() as pw:
    b = pw.chromium.launch(); p = b.new_page(viewport={'width':1920,'height':936})
    p.goto(base+"#00-home"); p.wait_for_timeout(800)
    print('home', st(p))
    btn = p.locator("#sidebar button:has-text('Projects'), button:has-text('Projects')").first
    btn.click(); p.wait_for_timeout(800); print('after projects', st(p))
    p.locator('.h-20 .p-dropdown').first.click(); p.wait_for_timeout(900); print('dd open', st(p))
    p.screenshot(path=str(out/'07c-dd.png'))
    p.go_back(); p.wait_for_timeout(800); print('back', st(p))
    p.go_forward(); p.wait_for_timeout(800); print('fwd', st(p))
    p.keyboard.press('Escape'); p.wait_for_timeout(500); print('esc', st(p))
    # deep-link variant
    p2 = b.new_page(viewport={'width':1920,'height':936})
    p2.goto(base+"#07c-shell-projects"); p2.wait_for_timeout(800); print('deep', st(p2))
    p2.locator('.h-20 .p-dropdown').first.click(); p2.wait_for_timeout(900); print('deep dd', st(p2))
    p2.go_back(); p2.wait_for_timeout(800); print('deep back', p2.url)
    # reload variant
    p3 = b.new_page(viewport={'width':1920,'height':936})
    p3.goto(base+"#07c-shell-projects"); p3.wait_for_timeout(800)
    p3.locator('[title*="sidebar" i], .h-20 button').first.click(); p3.wait_for_timeout(900); print('drawer', st(p3))
    p3.reload(); p3.wait_for_timeout(900); print('reload', st(p3))
    # 07a deep for comparison
    p4 = b.new_page(viewport={'width':1920,'height':936})
    p4.goto(base+"#07a-shell-mode-dropdown"); p4.wait_for_timeout(900); print('07a deep', st(p4))
    b.close()
