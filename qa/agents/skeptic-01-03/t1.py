from playwright.sync_api import sync_playwright
import json
URL='file:///Users/kumaraniket/Desktop/AI%20Governance%20Clone/clone/index.html#01-llm-analytics'
ACT="""() => [...document.querySelectorAll('button')].filter(b=>/bg-\\[#5928ED\\]|bg-white shadow/.test(b.className)).map(b=>b.textContent.trim()).filter(t=>t.length<40)"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(URL); pg.wait_for_timeout(800)
    print('initial active', pg.evaluate(ACT))
    req=pg.locator('button',has_text='Requests').first
    print('Requests cls before', req.get_attribute('class'))
    print('sibling count', req.evaluate("b=>[...b.parentElement.children].map(e=>e.tagName+':'+e.textContent.trim())"))
    req.click(); pg.wait_for_timeout(200)
    print('Requests cls after', req.get_attribute('class'))
    print('active after Requests', pg.evaluate(ACT))
    pg.locator('button',has_text='30 days').first.click(); pg.wait_for_timeout(200)
    print('active after 30 days', pg.evaluate(ACT))
    # 2-button groups across views
    for v in ['01-llm-analytics','02-firewall','03-live-events']:
        pg.goto(URL.split('#')[0]+'#'+v); pg.wait_for_timeout(500)
        g=pg.evaluate("""()=>{const out=[];const seen=new Set();for(const b of document.querySelectorAll('button')){const p=b.parentElement;if(!p||seen.has(p))continue;seen.add(p);const s=[...p.children].filter(e=>e.tagName==='BUTTON');if(s.length===2&&s[0].className!==s[1].className)out.push(s.map(x=>x.textContent.trim().slice(0,30)));}return out}""")
        print(v,'2-btn groups w/ differing classes',g)
    print('errors',errs)
    b.close()
