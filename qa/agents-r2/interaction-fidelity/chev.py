from playwright.sync_api import sync_playwright
URL='file:///Users/kumaraniket/Desktop/AI Governance Clone/clone/index.html'
VIEWS=['00-home','01-llm-analytics','02-firewall','03-live-events','04-policies','04b-policies-changelogs','05-traffic','05a-traffic-projects','05b-traffic-project-usage','05c-traffic-model-config','05d-traffic-statistics','05e-traffic-applications','05f-traffic-errorlogs','06-rbac-access','06b-rbac-usergroups','06c-rbac-config-modules','06d-rbac-config-permissions','06e-rbac-config-roles','06f-rbac-config-mapping','07c-shell-projects']
LIST="""()=>[...document.querySelectorAll('[data-panel]:last-of-type button[aria-expanded]')].map((b,i)=>({i,t:(b.textContent||'').replace(/\\s+/g,' ').trim().slice(0,50),aria:b.getAttribute('aria-label'),exp:b.getAttribute('aria-expanded'),sec:!!b.closest('section'),
  secKids: b.closest('section')?b.closest('section').children.length:0, ctrl:b.getAttribute('aria-controls')}))"""
VIS="""()=>{const r=document.querySelector('[data-panel]:last-of-type');return [...r.querySelectorAll('h1,h2,h3,h4,table,canvas,img,svg.recharts-surface')].filter(e=>e.getClientRects().length&&getComputedStyle(e).visibility!='hidden').map(e=>e.tagName+':'+(e.textContent||'').trim().slice(0,30))}"""
with sync_playwright() as pw:
    br=pw.chromium.launch(); pg=br.new_page(viewport={'width':1920,'height':936})
    for v in VIEWS:
        pg.goto('about:blank'); pg.goto(URL+'#'+v); pg.wait_for_timeout(300)
        L=pg.evaluate(LIST)
        for b in L:
            pg.goto('about:blank'); pg.goto(URL+'#'+v); pg.wait_for_timeout(300)
            before=pg.evaluate(VIS)
            loc=pg.locator('[data-panel]:last-of-type button[aria-expanded]').nth(b['i'])
            loc.click(); pg.wait_for_timeout(300)
            after=pg.evaluate(VIS); exp=loc.get_attribute('aria-expanded'); h=pg.evaluate('location.hash')
            gone=[x for x in before if x not in after]; new=[x for x in after if x not in before]
            loc.click(); pg.wait_for_timeout(300); after2=pg.evaluate(VIS); exp2=loc.get_attribute('aria-expanded')
            print(v,b, '\n    exp',b['exp'],'->',exp,'->',exp2,h,'| hidden:',gone[:6],len(gone),'| shown:',new[:4],'| restored:',after2==before)
    br.close()
