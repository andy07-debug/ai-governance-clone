from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
VIEWS='04-policies 04b-policies-changelogs 04c-policies-newpolicy-modal 06-rbac-access 06b-rbac-usergroups 06c-rbac-config-modules 06d-rbac-config-permissions 06e-rbac-config-roles 06f-rbac-config-mapping'.split()
JS="""()=>{const out=[];const seen=new Set();document.querySelectorAll('#mount button').forEach(btn=>{const p=btn.parentElement;if(seen.has(p))return;seen.add(p);
const sibs=[...p.children].filter(e=>e.tagName==='BUTTON');if(sibs.length<2)return;const c={};sibs.forEach(s=>c[s.className]=(c[s.className]||0)+1);
const k=Object.keys(c);if(k.length!==2)return;const a=k.filter(x=>c[x]===1);if(a.length!==1)return;
out.push(sibs.map(s=>(s.className===a[0]?'*':'')+(s.innerText||s.title||s.getAttribute('aria-label')||'[icon]').replace(/\\s+/g,' ').slice(0,30)))});return out}"""
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    for v in VIEWS:
        pg.goto('file://'+ROOT+'/clone/index.html#'+v); pg.wait_for_timeout(300)
        print(v, pg.evaluate(JS))
