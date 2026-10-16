from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
OUT='/Users/kumaraniket/Desktop/AI Governance Clone/qa/agents/analytics+firewall+events'
SC="""()=>{const r=[];document.querySelectorAll('*').forEach(e=>{const s=getComputedStyle(e);if((s.overflowY=='auto'||s.overflowY=='scroll')&&e.scrollHeight>e.clientHeight+1){const b=e.getBoundingClientRect();r.push([e.className.slice(0,60),e.scrollHeight,e.clientHeight,Math.round(b.y),Math.round(b.height)])}});return r}"""
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
    for v in ['01-llm-analytics','02-firewall','03-live-events']:
        pg.goto('file://'+ROOT+'/clone/index.html#'+v); pg.reload(); pg.wait_for_timeout(400)
        pg.click('[title="Toggle Fullscreen"]'); pg.wait_for_timeout(400)
        print(v,'scrollables',pg.evaluate(SC))
        pg.mouse.move(1300,500)
        for i in range(8): pg.mouse.wheel(0,800); pg.wait_for_timeout(120)
        pg.wait_for_timeout(300)
        pg.screenshot(path=f'{OUT}/fs-{v}-bottom.png')
        print(' doc', pg.evaluate("[document.documentElement.scrollHeight, scrollY]"))
    # bubble close
    pg.goto('file://'+ROOT+'/clone/index.html#02-firewall'); pg.reload(); pg.wait_for_timeout(400)
    pg.click('[title="Toggle Fullscreen"]'); pg.wait_for_timeout(300)
    n0=pg.evaluate("document.body.innerText.includes(\"I'm here, your AskMod.ai!\")")
    pg.click('[aria-label="Close messages"]'); pg.wait_for_timeout(300)
    n1=pg.evaluate("document.body.innerText.includes(\"I'm here, your AskMod.ai!\")")
    print('bubble before/after close', n0, n1)
    # breadcrumb home in fullscreen
    pg.click('button[title="Back to home"]'); pg.wait_for_timeout(300)
    print('after home', pg.evaluate("location.hash"), pg.evaluate("!!document.querySelector('.fixed.inset-0.z-20')"))
    pg.screenshot(path=f'{OUT}/fs-home.png')
    # exit fullscreen
    pg.click('[title="Toggle Fullscreen"]'); pg.wait_for_timeout(300)
    print('after exit', pg.evaluate("!!document.querySelector('.fixed.inset-0.z-20')"), pg.evaluate("document.getElementById('sidebar')&&document.getElementById('sidebar').getBoundingClientRect().width"))
    print('errs',errs)
    b.close()
