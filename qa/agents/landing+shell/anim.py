from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
URL='file://'+ROOT+'/clone/index.html'
JS="""()=>{const w=[...document.querySelectorAll('*')].find(e=>e.children.length<3&&/Hey Kumar/.test(e.textContent)&&e.textContent.length<120);
let e=w, out=[]; while(e&&e!==document.body){const cs=getComputedStyle(e); if(cs.opacity!=='1'||cs.animationName!=='none'||cs.transform!=='none') out.push(e.tagName+'.'+String(e.className).slice(0,40)+' op='+cs.opacity+' anim='+cs.animationName+' '+cs.animationDuration+' '+cs.animationDelay+' tf='+cs.transform); e=e.parentElement}
return out}"""
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    for v in ['00-home','07a-shell-mode-dropdown']:
        pg.goto(URL+'#'+v); pg.reload()
        for t in [100,600,1500,3000]:
            pg.wait_for_timeout(t if t==100 else t-prev); prev=t
            print(v,t,pg.evaluate(JS))
        prev=0
    b.close()
