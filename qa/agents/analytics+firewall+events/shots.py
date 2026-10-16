from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
OUT='/Users/kumaraniket/Desktop/AI Governance Clone/qa/agents/analytics+firewall+events'
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    for v,sel in [('01-llm-analytics','.min-h-0.flex-1.overflow-y-auto'),('02-firewall','.flex-1.overflow-y-auto.p-6')]:
        pg.goto('file://'+ROOT+'/clone/index.html#'+v); pg.wait_for_timeout(700)
        el=pg.locator(sel).last
        el.hover()
        i=0
        while True:
            st=pg.evaluate(f"document.querySelectorAll('{sel}')[document.querySelectorAll('{sel}').length-1].scrollTop")
            pg.screenshot(path=f'{OUT}/{v}-s{i}.png'); i+=1
            pg.mouse.wheel(0,700); pg.wait_for_timeout(300)
            st2=pg.evaluate(f"document.querySelectorAll('{sel}')[document.querySelectorAll('{sel}').length-1].scrollTop")
            print(v,i,st,st2)
            if st2==st: break
    b.close()
