from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    fails=[]
    pg.on('requestfailed', lambda r: fails.append(r.url))
    pg.on('pageerror', lambda e: fails.append('PAGEERR '+str(e)))
    for v in ['01-llm-analytics','02-firewall','03-live-events']:
        fails.clear()
        pg.goto('file://'+ROOT+'/clone/index.html#'+v); pg.wait_for_timeout(800)
        print(v, sorted(set(fails)))
        # images
        print(pg.evaluate("""[...document.querySelectorAll('#mount img, #root img')].map(i=>[i.src.slice(0,80), i.complete, i.naturalWidth])"""))
    b.close()
