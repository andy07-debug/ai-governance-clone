import os,sys
from playwright.sync_api import sync_playwright
URL='file://'+os.path.abspath('qa/agents-r2/skeptic-r2b/patched.html')
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    for v in ['05d-traffic-statistics','05b-traffic-project-usage','01-llm-analytics','02-firewall']:
        pg.goto('about:blank'); pg.goto(URL+'#'+v); pg.wait_for_timeout(500)
        cust=pg.locator('main button',has_text='Custom')
        if cust.count()==0: print(v,'no custom'); continue
        par=cust.first.locator('xpath=..')
        btns=par.locator('xpath=./button')
        n=btns.count(); seq=[n-1,1,0,3,n-1,2]
        for i in seq:
            btns.nth(i).click(); pg.wait_for_timeout(750)
            r=par.evaluate('p=>[...p.children].filter(e=>e.tagName=="BUTTON").map(b=>[b.textContent.trim(),getComputedStyle(b).paddingLeft,getComputedStyle(b).display,getComputedStyle(b).backgroundColor])')
            sel=[x[0] for x in r if x[3]!='rgba(0, 0, 0, 0)']
            bad=[x for x in r if (x[0]=='Custom')!=(x[1]=='12px' and x[2]=='flex')]
            print(v,'click',r[i][0],'selected',sel,'layoutbad',bad)
    pg.goto('about:blank'); pg.goto(URL+'#05c-traffic-model-config'); pg.wait_for_timeout(500)
    h=pg.locator('.p-accordion-header-link').first; bb=h.bounding_box()
    for k in range(2):
        pg.mouse.click(bb['x']+bb['width']*0.6,bb['y']+bb['height']/2); pg.wait_for_timeout(750)
        print('acc',pg.evaluate("[document.querySelector('.p-accordion-header-link').getAttribute('aria-expanded'),getComputedStyle(document.querySelector('.p-accordion-toggle-icon')).transform]"))
    print('errs',errs)
