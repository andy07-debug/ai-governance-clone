from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
VIEWS='04-policies 04b-policies-changelogs 04c-policies-newpolicy-modal 06-rbac-access 06b-rbac-usergroups 06c-rbac-config-modules 06d-rbac-config-permissions 06e-rbac-config-roles 06f-rbac-config-mapping'.split()
JS="""()=>[...document.querySelectorAll('*')].filter(e=>{const s=getComputedStyle(e);return /(auto|scroll)/.test(s.overflowY)&&e.scrollHeight>e.clientHeight+2}).map(e=>[e.tagName,String(e.className).slice(0,50),e.scrollHeight,e.clientHeight])"""
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    for v in VIEWS:
        pg.goto('file://'+ROOT+'/clone/index.html#'+v); pg.wait_for_timeout(300); c=pg.evaluate(JS)
        pg.goto('file://'+ROOT+'/qa/base/'+v+'.html'); pg.wait_for_timeout(300); bb=pg.evaluate(JS)
        print('==',v,'\n clone',c,'\n base ',bb)
