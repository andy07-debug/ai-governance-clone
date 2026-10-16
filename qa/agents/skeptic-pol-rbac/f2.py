from playwright.sync_api import sync_playwright
import pathlib
U = pathlib.Path('/Users/kumaraniket/Desktop/AI Governance Clone/clone/index.html').as_uri()
with sync_playwright() as pw:
    b = pw.chromium.launch(); p = b.new_page(viewport={'width':1920,'height':936})
    for v in ['06d-rbac-config-permissions','06e-rbac-config-roles']:
        p.goto(U+'#'+v); p.wait_for_timeout(300)
        print(v, p.evaluate("""[...document.querySelectorAll('button')].filter(b=>['Access Management','RBAC Configuration','User Groups','Configuration','Modules','Permissions','Roles','Mapping'].includes(b.textContent.trim())&&b.offsetParent).map(b=>b.textContent.trim()+' sel='+b.getAttribute('aria-selected')+' '+(b.className.match(/(bg-\\S+|text-appsec-\\S+|border-appsec-\\S+|border-transparent)/g)||[]).join(','))"""))
    b.close()
