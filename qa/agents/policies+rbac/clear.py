from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    pg.goto('file://'+ROOT+'/clone/index.html#04-policies'); pg.wait_for_timeout(300)
    pg.get_by_placeholder('Search policies…').fill('abc'); pg.get_by_text('Clear filter search').click(); pg.wait_for_timeout(100)
    print(repr(pg.get_by_placeholder('Search policies…').input_value()))
    # blank click evidence: what element and its textContent
    print(pg.evaluate("(()=>{const e=document.elementFromPoint(1100,300);return [e.className, e.closest('button,a,li,[role=button],.cursor-pointer,.p-dropdown')]})()"))
