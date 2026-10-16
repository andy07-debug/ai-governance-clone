from playwright.sync_api import sync_playwright
URL='file:///Users/kumaraniket/Desktop/AI Governance Clone/clone/index.html'
VIEWS=['01-llm-analytics','02-firewall','03-live-events','04-policies','04b-policies-changelogs','05b-traffic-project-usage','05c-traffic-model-config','05d-traffic-statistics','05e-traffic-applications','05f-traffic-errorlogs','06-rbac-access','06b-rbac-usergroups','06e-rbac-config-roles']
with sync_playwright() as pw:
    br=pw.chromium.launch(); pg=br.new_page(viewport={'width':1920,'height':936})
    for v in VIEWS:
        pg.goto('about:blank'); pg.goto(URL+'#'+v); pg.wait_for_timeout(300)
        n=pg.evaluate("[...document.querySelectorAll('[data-panel]:last-of-type button, [data-panel]:last-of-type span, [data-panel]:last-of-type a')].filter(b=>/^(more|less|show more|show less|view more|\\+\\d+ more)$/i.test(b.textContent.trim())).map(b=>b.tagName+':'+b.textContent.trim())")
        lc=pg.evaluate("document.querySelectorAll('[data-panel]:last-of-type [class*=line-clamp], [data-panel]:last-of-type .truncate').length")
        print(v,len(n),n[:5],'clamped',lc)
    br.close()
