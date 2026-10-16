import hashlib, json
from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
ENUM="""()=>{const panels=[...document.querySelectorAll('[data-panel]')];const rp=panels[panels.length-1];
const els=[...rp.querySelectorAll('button, a, [role=button], select, input, textarea, .cursor-pointer, summary, label')];
return els.map((e,i)=>{const r=e.getBoundingClientRect();return {i, tag:e.tagName, text:(e.innerText||e.value||e.placeholder||e.getAttribute('title')||e.getAttribute('aria-label')||'').replace(/\\s+/g,' ').trim().slice(0,50), cls:(e.className.baseVal??e.className).slice(0,70), w:r.width, h:r.height}})}"""
SIG="""()=>{const m=document.getElementById('mount');let h=0;const s=m.innerHTML;for(let i=0;i<s.length;i++){h=(h*31+s.charCodeAt(i))|0};return [location.hash,h]}"""
out=[]
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: errs.append(m.text) if m.type=='error' else None)
    for v in ['01-llm-analytics','02-firewall','03-live-events']:
        pg.goto('file://'+ROOT+'/clone/index.html#'+v); pg.wait_for_timeout(500)
        items=pg.evaluate(ENUM)
        print('==',v,len(items))
        for it in items:
            pg.goto('file://'+ROOT+'/clone/index.html#'+v); pg.reload(); pg.wait_for_timeout(250)
            errs.clear()
            before=pg.evaluate(SIG)
            h=pg.evaluate_handle(f"()=>{{const panels=[...document.querySelectorAll('[data-panel]')];const rp=panels[panels.length-1];return [...rp.querySelectorAll('button, a, [role=button], select, input, textarea, .cursor-pointer, summary, label')][{it['i']}]}}")
            el=h.as_element()
            res='?'
            try:
                if it['w']==0 or it['h']==0: res='hidden'
                else:
                    el.scroll_into_view_if_needed(timeout=1000)
                    if it['tag'] in ('INPUT','TEXTAREA'):
                        el.click(timeout=1500); pg.keyboard.type('abc'); res='typed val='+repr(el.evaluate('e=>e.value'))
                    elif it['tag']=='SELECT':
                        opts=el.evaluate('e=>[...e.options].map(o=>o.value)')
                        if len(opts)>1: el.select_option(opts[1]); res='select ok opts=%d now=%r'%(len(opts), el.evaluate('e=>e.options[e.selectedIndex].text'))
                        else: res='select opts=%d'%len(opts)
                    else:
                        el.click(timeout=1500)
                    pg.wait_for_timeout(200)
                    after=pg.evaluate(SIG)
                    if after[0]!=before[0]: res+=' NAV->'+after[0]
                    elif after[1]!=before[1]: res+=' DOMCHANGE'
                    else: res+=' nochange'
            except Exception as ex:
                res='ERR '+str(ex).splitlines()[0][:120]
            if errs: res+=' JSERR '+str(errs)
            print(f"  [{it['i']}] {it['tag']} '{it['text']}' ({it['cls'][:40]}) -> {res}")
    b.close()
