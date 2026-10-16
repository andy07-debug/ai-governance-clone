from playwright.sync_api import sync_playwright
import pathlib
URL = pathlib.Path('/Users/kumaraniket/Desktop/AI Governance Clone/qa/agents-r3/skeptic-hist/index.html').as_uri()
def st(p, tag):
    print(tag, p.evaluate("[location.hash, window.__cloneState(), document.querySelectorAll('.animate-slideUp').length, document.querySelectorAll('.p-dropdown-panel').length, history.length]"))
with sync_playwright() as pw:
    b = pw.chromium.launch(headless=True)
    p = b.new_page(viewport={'width':1920,'height':936})
    p.goto(URL); p.wait_for_timeout(1500)
    p.locator('h3', has_text='Policies').first.click(); p.wait_for_timeout(1000)
    st(p,'R1 policies')
    p.locator('button', has_text='New Policy').first.click(); p.wait_for_timeout(1000)
    st(p,'R1 modal open')
    p.reload(); p.wait_for_timeout(1500)
    st(p,'R1 after reload')
    p.go_back(); p.wait_for_timeout(1000); st(p,'R1 back')
    p.go_forward(); p.wait_for_timeout(1000); st(p,'R1 forward')
    # R2
    p.goto(URL); p.wait_for_timeout(1500)
    p.locator('h3', has_text='Policies').first.click(); p.wait_for_timeout(900)
    p.locator('button', has_text='Change Logs').first.click(); p.wait_for_timeout(900)
    p.locator('button', has_text='Policies Deck').first.click(); p.wait_for_timeout(900)
    p.locator('button', has_text='New Policy').first.click(); p.wait_for_timeout(900)
    st(p,'R2 modal')
    p.go_back(); p.wait_for_timeout(1000); st(p,'R2 back')
    p.go_forward(); p.wait_for_timeout(1000); st(p,'R2 fwd')
    # R3
    for h in ['#nope', '#07a-shell-mode-dropdown']:
        p2 = b.new_page(viewport={'width':1920,'height':936})
        p2.goto(URL); p2.wait_for_timeout(1500)
        p2.locator('h3', has_text='Live Events').first.click(); p2.wait_for_timeout(1000)
        st(p2,'R3 '+h+' page')
        p2.evaluate(f"location.hash='{h}'"); p2.wait_for_timeout(1000)
        st(p2,'R3 '+h+' after type')
        if h=='#nope':
            p2.evaluate("document.querySelector('.h-20 .p-dropdown').click()"); p2.wait_for_timeout(1000)
            st(p2,'R3 dd open')
        p2.go_back(); p2.wait_for_timeout(1000); st(p2,'R3 '+h+' back1')
        p2.go_back(); p2.wait_for_timeout(1000); st(p2,'R3 '+h+' back2')
        p2.close()
    b.close()
