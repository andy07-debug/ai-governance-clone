from playwright.sync_api import sync_playwright
URL='file:///Users/kumaraniket/Desktop/AI Governance Clone/clone/index.html'
SIDE='''()=>{const s=document.getElementById('sidebar');const o=[];s.querySelectorAll('*').forEach(e=>{if(e.scrollHeight>e.clientHeight+5 && getComputedStyle(e).overflowY!='visible')o.push([e.tagName+'.'+String(e.className).slice(0,60),e.scrollTop,e.scrollHeight,e.clientHeight])});const ta=s.querySelector('textarea');return {els:o,draft:ta&&ta.value, same: s===window.__sb}}'''
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    for v in ['00-home','01-llm-analytics','05b-traffic-project-usage','06-rbac-access','07c-shell-projects']:
        pg.goto('about:blank'); pg.goto(URL+'#'+v); pg.wait_for_timeout(800)
        print(v, pg.evaluate(SIDE))
    pg.goto('about:blank'); pg.goto(URL+'#01-llm-analytics'); pg.wait_for_timeout(800)
    pg.evaluate("()=>{window.__sb=document.getElementById('sidebar');document.getElementById('sidebar').querySelectorAll('*').forEach(e=>{if(e.scrollHeight>e.clientHeight+5)e.scrollTop=99999})}")
    pg.locator('#sidebar textarea').first.fill('draft text')
    print('before', pg.evaluate(SIDE))
    pg.click('main button[title="Back to home"], main span.p-1.text-indigo-600'); pg.wait_for_timeout(800)
    print('after', pg.evaluate(SIDE))
    b.close()
