from playwright.sync_api import sync_playwright
URL='file:///Users/kumaraniket/Desktop/AI Governance Clone/clone/index.html'
VIEWS=['01-llm-analytics','02-firewall','03-live-events','04-policies','04b-policies-changelogs','05a-traffic-projects','05b-traffic-project-usage','05c-traffic-model-config','05d-traffic-statistics','05e-traffic-applications','05f-traffic-errorlogs','06-rbac-access','06b-rbac-usergroups','06c-rbac-config-modules','06d-rbac-config-permissions','06e-rbac-config-roles','06f-rbac-config-mapping','07c-shell-projects']
J="""()=>{const R=document.querySelector('[data-panel]:last-of-type');return [...R.querySelectorAll('[role=switch],[role=checkbox],[role=radio],input[type=checkbox],input[type=radio],.p-inputswitch,.p-checkbox,.p-radiobutton,[aria-checked],[aria-pressed],[data-state]')].map(e=>e.tagName+' '+(e.getAttribute('role')||e.type||'')+' aria-checked='+e.getAttribute('aria-checked')+' state='+e.getAttribute('data-state')+' | '+e.className.slice(0,60))}"""
with sync_playwright() as pw:
    br=pw.chromium.launch(); pg=br.new_page(viewport={'width':1920,'height':936})
    for v in VIEWS:
        pg.goto('about:blank'); pg.goto(URL+'#'+v); pg.wait_for_timeout(300)
        r=pg.evaluate(J)
        if r: print(v,len(r)); [print('   ',x) for x in sorted(set(r))[:8]]
    br.close()
