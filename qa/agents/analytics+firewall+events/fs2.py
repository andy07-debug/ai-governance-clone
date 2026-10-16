from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
OUT='/Users/kumaraniket/Desktop/AI Governance Clone/qa/agents/analytics+firewall+events'
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    pg.goto('file://'+ROOT+'/clone/index.html#01-llm-analytics'); pg.reload(); pg.wait_for_timeout(400)
    pg.click('[title="Toggle Fullscreen"]'); pg.wait_for_timeout(400)
    pg.screenshot(path=f'{OUT}/fs-01-top.png')
    print(pg.evaluate("""()=>{const i=[...document.querySelectorAll('img')].find(x=>x.src.startsWith('data:image/png'));const r=i.getBoundingClientRect();const p=i.parentElement.getBoundingClientRect();return [i.className, i.getAttribute('style'), i.naturalWidth,i.naturalHeight, r.width,r.height,p.width,p.height, getComputedStyle(i).objectFit]}"""))
    b.close()
