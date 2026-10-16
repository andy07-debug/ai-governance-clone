import os
from playwright.sync_api import sync_playwright
URL='file://'+os.path.abspath('../../../clone/index.html')
VIEWS=['00-home','01-llm-analytics','02-firewall','03-live-events','04-policies','04b-policies-changelogs','05-traffic','05a-traffic-projects','05b-traffic-project-usage','05c-traffic-model-config','05d-traffic-statistics','05e-traffic-applications','05f-traffic-errorlogs','06-rbac-access','06b-rbac-usergroups','06c-rbac-config-modules','06d-rbac-config-permissions','06e-rbac-config-roles','06f-rbac-config-mapping','07c-shell-projects']
JS="""() => ({
 exp:[...document.querySelectorAll('button[aria-expanded]')].map(b=>({t:(b.textContent||'').replace(/\\s+/g,' ').trim().slice(0,40), sec:!!b.closest('section'), side:!!b.closest('#sidebar'), v:b.getAttribute('aria-expanded')})),
 more:[...document.querySelectorAll('button')].filter(b=>/^(more|less)$/i.test(b.textContent.trim())).length,
 clamp:document.querySelectorAll('.line-clamp-2').length,
 cb:document.querySelectorAll('.p-checkbox').length,
 acc:document.querySelectorAll('a.p-accordion-header-link').length,
 tabs:[...document.querySelectorAll('[role=tab], .p-tabview-nav li, .p-tabmenuitem')].map(x=>x.textContent.trim().slice(0,20)),
})"""
with sync_playwright() as pw:
    br=pw.chromium.launch(); pg=br.new_page(viewport={'width':1920,'height':936})
    for v in VIEWS:
        pg.goto(URL+'#'+v); pg.reload(); pg.wait_for_timeout(200)
        r=pg.evaluate(JS)
        print(v, r)
