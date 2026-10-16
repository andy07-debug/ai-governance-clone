from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
OUT='/Users/kumaraniket/Desktop/AI Governance Clone/qa/agents/analytics+firewall+events'
JS="""()=>{const r=[];document.querySelectorAll('*').forEach(e=>{const s=getComputedStyle(e);
 const sy=(s.overflowY=='auto'||s.overflowY=='scroll')&&e.scrollHeight>e.clientHeight+1;
 const sx=(s.overflowX=='auto'||s.overflowX=='scroll')&&e.scrollWidth>e.clientWidth+1;
 const hid=(e.scrollHeight>e.clientHeight+1&&s.overflowY=='hidden')||(e.scrollWidth>e.clientWidth+1&&s.overflowX=='hidden');
 if(sy||sx){const b=e.getBoundingClientRect();r.push({tag:e.tagName,cls:(e.className.baseVal??e.className).slice(0,90),sy,sx,sh:e.scrollHeight,ch:e.clientHeight,sw:e.scrollWidth,cw:e.clientWidth,x:Math.round(b.x),y:Math.round(b.y)})}});
 return r}"""
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    for v in ['01-llm-analytics','02-firewall','03-live-events']:
        for kind,url in [('clone','file://'+ROOT+'/clone/index.html#'+v),('base','file://'+ROOT+'/qa/base/'+v+'.html')]:
            pg.goto(url); pg.wait_for_timeout(700)
            print(v,kind)
            for x in pg.evaluate(JS): print('  ',x)
            print('  doc',pg.evaluate("[document.documentElement.scrollWidth,document.documentElement.scrollHeight]"))
    b.close()
