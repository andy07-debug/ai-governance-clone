import os, json, hashlib
from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
URL='file://'+ROOT+'/clone/index.html'
VIEWS=['05-traffic','05a-traffic-projects','05b-traffic-project-usage','05c-traffic-model-config','05d-traffic-statistics','05e-traffic-applications','05f-traffic-errorlogs']
SEL='main button, main a, main [role="button"], main .cursor-pointer, main li, main .p-dropdown, main input, main [tabindex]'
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    errs=[]
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: errs.append(m.text) if m.type=='error' else None)
    for v in VIEWS:
        pg.goto(URL+'#'+v); pg.wait_for_timeout(300)
        # which <main> is the right panel? use last data-panel
        n=pg.evaluate(f"""()=>{{const P=[...document.querySelectorAll('[data-panel]')].pop(); const els=[...P.querySelectorAll('button, a, [role="button"], .cursor-pointer, li, .p-dropdown, input, [tabindex]')]; els.forEach((e,i)=>e.setAttribute('data-qa-c',i)); return els.map((e,i)=>{{const r=e.getBoundingClientRect(); return [i,e.tagName,(e.innerText||e.getAttribute('title')||e.getAttribute('aria-label')||e.className.toString()).replace(/\\s+/g,' ').slice(0,50), Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)]}})}}""")
        print('=====',v,len(n))
        for item in n:
            i=item[0]
            pg.goto('about:blank'); pg.goto(URL+'#'+v); pg.wait_for_timeout(150)
            pg.evaluate(f"""()=>{{const P=[...document.querySelectorAll('[data-panel]')].pop(); [...P.querySelectorAll('button, a, [role="button"], .cursor-pointer, li, .p-dropdown, input, [tabindex]')].forEach((e,i)=>e.setAttribute('data-qa-c',i));}}""")
            before=pg.evaluate("document.getElementById('root').innerHTML.replace(/ data-qa-c=\"\\d+\"/g,'')")
            errs.clear()
            loc=pg.locator(f'[data-qa-c="{i}"]')
            try:
                loc.scroll_into_view_if_needed(timeout=1000)
                loc.click(timeout=1500)
                res='clicked'
            except Exception as e:
                try: loc.click(timeout=800, force=True); res='forced'
                except Exception as e2: res='ERR '+str(e2).split('\n')[0][:60]
            pg.wait_for_timeout(150)
            h=pg.evaluate('location.hash.slice(1)')
            after=pg.evaluate("document.getElementById('root').innerHTML.replace(/ data-qa-c=\"\\d+\"/g,'')")
            changed = 'NAV->'+h if h!=v else ('DOMCHANGE' if after!=before else 'inert')
            print(f'  {item[0]:3} {item[1]:6} {item[2]!r:55} @({item[3]},{item[4]} {item[5]}x{item[6]}) {res:8} {changed} {errs[:2] if errs else ""}')
    b.close()
