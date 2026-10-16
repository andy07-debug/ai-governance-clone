from playwright.sync_api import sync_playwright
URL='file:///Users/kumaraniket/Desktop/AI Governance Clone/clone/index.html'
VIEWS=['01-llm-analytics','02-firewall','03-live-events','04-policies','04b-policies-changelogs','04c-policies-newpolicy-modal','05-traffic','05a-traffic-projects','05b-traffic-project-usage','05c-traffic-model-config','05d-traffic-statistics','05e-traffic-applications','05f-traffic-errorlogs','06-rbac-access','06b-rbac-usergroups','06c-rbac-config-modules','06f-rbac-config-mapping','07c-shell-projects']
JS="""()=>{const seen=new Set(),out=[];const R=document.querySelector('[data-panel]:last-of-type');
 R.querySelectorAll('.cursor-pointer, [role=tab], [role=radio], li, label').forEach(e=>{if(e.tagName==='BUTTON')return;const p=e.parentElement;if(seen.has(p))return;seen.add(p);
  const s=[...p.children].filter(x=>x.tagName===e.tagName&&x.tagName!=='TR');if(s.length<2||s.length>12)return;
  const cls=s.map(x=>x.className); if(new Set(cls).size<2) return;
  out.push({tag:e.tagName,t:s.map(x=>(x.textContent||'').replace(/\\s+/g,' ').trim().slice(0,18))})});return out}"""
with sync_playwright() as pw:
    br=pw.chromium.launch(); pg=br.new_page(viewport={'width':1920,'height':936})
    for v in VIEWS:
        pg.goto('about:blank'); pg.goto(URL+'#'+v); pg.wait_for_timeout(300)
        for g in pg.evaluate(JS): print(v,g)
    br.close()
