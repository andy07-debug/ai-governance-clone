from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
VIEWS='04-policies 04b-policies-changelogs 04c-policies-newpolicy-modal 06-rbac-access 06b-rbac-usergroups 06c-rbac-config-modules 06d-rbac-config-permissions 06e-rbac-config-roles 06f-rbac-config-mapping'.split()
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    fails=[]; pg.on('requestfailed', lambda r: fails.append(r.url[:150])); errs=[]
    pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: errs.append(m.text) if m.type=='error' else None)
    for v in VIEWS:
        pg.goto('file://'+ROOT+'/clone/index.html#'+v); pg.wait_for_timeout(400)
        # broken imgs
        bad=pg.evaluate("[...document.images].filter(i=>!i.complete||i.naturalWidth==0).map(i=>i.src.slice(0,120))")
        print(v,'badimgs',bad)
    print('failed reqs',sorted(set(fails))); print('errs',set(errs))
