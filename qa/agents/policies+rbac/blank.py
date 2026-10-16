from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
U='file://'+ROOT+'/clone/index.html#'
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    def t(v,x,y):
        pg.goto(U+v); pg.reload(); pg.wait_for_timeout(200)
        el=pg.evaluate(f"(()=>{{const e=document.elementFromPoint({x},{y});return e.tagName+'.'+String(e.className).slice(0,60)}})()")
        pg.mouse.click(x,y); pg.wait_for_timeout(150)
        print(v,(x,y),el,'->',pg.evaluate('location.hash.slice(1)'))
    for xy in [(1100,300),(1400,300),(1600,190),(1700,280),(1700,480),(1400,600),(1400,900),(1060,170)]: t('04-policies',*xy)
    for xy in [(1100,300),(1400,600),(1200,230)]: t('04b-policies-changelogs',*xy)
    for xy in [(300,500),(700,40),(1500,500),(1880,40),(60,110),(1870,110),(900,110),(960,170),(960,730)]: t('04c-policies-newpolicy-modal',*xy)
