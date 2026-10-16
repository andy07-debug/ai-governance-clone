import json, random
from playwright.sync_api import sync_playwright
URL='file:///Users/kumaraniket/Desktop/AI Governance Clone/clone/index.html'
GROUPS={'01-llm-analytics':['Requests','Today','Top assistants','By User'],'02-firewall':['Blocked','7d'],
 '05b-traffic-project-usage':['1 hour'],'05d-traffic-statistics':['1 hour']}
GET="""(n)=>{const b=[...document.querySelectorAll('[data-panel]:last-of-type button')].find(b=>b.textContent.trim()===n); const s=[...b.parentElement.children];
 return s.map(x=>{const cs=getComputedStyle(x);return {t:x.textContent.trim(),c:x.className.split(/\\s+/).filter(Boolean).sort().join(' '),bg:cs.backgroundColor,col:cs.color,pad:cs.paddingLeft+'/'+cs.paddingRight,disp:cs.display,w:Math.round(x.getBoundingClientRect().width)}})}"""
random.seed(3)
with sync_playwright() as pw:
    br=pw.chromium.launch(); pg=br.new_page(viewport={'width':1920,'height':936})
    for v,anchors in GROUPS.items():
        for anc in anchors:
            pg.goto('about:blank'); pg.goto(URL+'#'+v); pg.wait_for_timeout(300)
            orig=pg.evaluate(GET,anc); names=[o['t'] for o in orig]
            sel0=[o['t'] for o in orig if o['bg'] not in ('rgba(0, 0, 0, 0)',)]
            seq=[n for n in names[::-1]]+random.sample(names,len(names))+[o['t'] for o in orig if o['c']!=orig[1]['c'] and 0] 
            # end on the originally selected pill
            act0=[o['t'] for o in orig if 'bg-[#5928ED]' in o['c'] or 'bg-gray-200' in o['c'] or 'bg-white' in o['c'].split()]
            seq.append(act0[0])
            bad=[]
            for n in seq:
                pg.locator('[data-panel]:last-of-type button',has_text=n).filter(has_text=n).locator('visible=true').first if False else None
                pg.evaluate("(n)=>{const b=[...document.querySelectorAll('[data-panel]:last-of-type button')].find(b=>b.textContent.trim()===n);}",n)
                h=pg.locator('[data-panel]:last-of-type button').filter(has_text=n)
                # find the one in the right group
                idx=pg.evaluate("([a,n])=>{const bs=[...document.querySelectorAll('[data-panel]:last-of-type button')];const b=bs.find(b=>b.textContent.trim()===a);const t=[...b.parentElement.children].find(x=>x.textContent.trim()===n);return bs.indexOf(t)}",[anc,n])
                pg.locator('[data-panel]:last-of-type button').nth(idx).click()
                pg.wait_for_timeout(750)
                st=pg.evaluate(GET,anc)
                selected=[s['t'] for s in st if s['bg']!=orig[[o['t'] for o in orig].index(s['t'])]['bg'] or False]
                hi=[s['t'] for s in st if s['bg']==[o for o in orig if o['t']==act0[0]][0]['bg']]
                if hi!=[n]: bad.append(('after click',n,'highlighted',hi))
                for s,o in zip(st,orig):
                    if s['pad']!=o['pad'] or s['disp']!=o['disp']: bad.append(('layout',n,s['t'],o['pad'],o['disp'],'->',s['pad'],s['disp']))
            fin=pg.evaluate(GET,anc)
            diff=[(o['t'],o['c'],f['c']) for o,f in zip(orig,fin) if o['c']!=f['c']]
            print(v,anc,'seq',len(seq),'bad',len(bad)); 
            for b in bad[:8]: print('   ',b)
            for d in diff: print('   CLASSDIFF',d)
    br.close()
