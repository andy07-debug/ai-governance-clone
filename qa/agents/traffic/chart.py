from playwright.sync_api import sync_playwright
URL='file:///Users/kumaraniket/Desktop/AI Governance Clone/clone/index.html'
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936}, device_scale_factor=1)
    for v in ['05b-traffic-project-usage','05d-traffic-statistics']:
        pg.goto(URL+'#'+v); pg.wait_for_timeout(400)
        print(v, pg.evaluate("""()=>[...document.querySelectorAll('[data-panel]:last-of-type img, [data-panel] img')].filter(i=>i.src.startsWith('data:image/png')).map(i=>{const r=i.getBoundingClientRect();return [i.naturalWidth,i.naturalHeight,Math.round(r.width),Math.round(r.height),Math.round(r.x),Math.round(r.y),i.className, i.parentElement.className.slice(0,80)]})"""))
        print(' canvases', pg.evaluate("document.querySelectorAll('#root canvas').length"))
    b.close()
