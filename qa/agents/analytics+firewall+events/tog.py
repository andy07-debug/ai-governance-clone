from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
OUT='/Users/kumaraniket/Desktop/AI Governance Clone/qa/agents/analytics+firewall+events'
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    pg.goto('file://'+ROOT+'/clone/index.html#01-llm-analytics'); pg.wait_for_timeout(500)
    print(pg.evaluate("""()=>{const b=[...document.querySelectorAll('button')].find(x=>x.innerText.trim()=='Requests');return [...b.parentElement.children].map(c=>[c.tagName,c.className,c.innerText])}"""))
    pg.get_by_role('button',name='Requests',exact=True).click(); pg.wait_for_timeout(200)
    pg.get_by_role('button',name='30 days',exact=True).click(); pg.wait_for_timeout(200)
    pg.screenshot(path=OUT+'/tog-metric-range.png', clip={'x':866,'y':140,'width':1054,'height':330})
    # fullscreen
    pg.goto('file://'+ROOT+'/clone/index.html#02-firewall'); pg.reload(); pg.wait_for_timeout(400)
    b4=pg.evaluate("document.getElementById('mount').innerHTML")
    pg.get_by_role('button',name='Toggle Fullscreen').click(); pg.wait_for_timeout(300)
    af=pg.evaluate("document.getElementById('mount').innerHTML")
    import difflib
    sm=difflib.SequenceMatcher(None,b4,af,autojunk=False) if len(b4)<300000 else None
    if sm:
        for op in sm.get_opcodes():
            if op[0]!='equal': print(op[0], repr(b4[op[1]-80:op[2]+40]), '=>', repr(af[op[3]-80:op[4]+40])); 
    pg.screenshot(path=OUT+'/fullscreen.png')
    print(pg.evaluate("""()=>{const b=document.querySelector('button[title="Toggle Fullscreen"]')||[...document.querySelectorAll('button')].find(x=>x.getAttribute('aria-label')=='Toggle Fullscreen');return b?[b.outerHTML.slice(0,200),b.parentElement.outerHTML.slice(0,600)]:null}"""))
    # firewall pills after toggles
    pg.goto('file://'+ROOT+'/clone/index.html#02-firewall'); pg.reload(); pg.wait_for_timeout(400)
    pg.get_by_role('button',name='Blocked',exact=True).click(); pg.get_by_role('button',name='30d',exact=True).click(); pg.wait_for_timeout(200)
    pg.screenshot(path=OUT+'/tog-fw.png', clip={'x':866,'y':230,'width':1054,'height':230})
    b.close()
