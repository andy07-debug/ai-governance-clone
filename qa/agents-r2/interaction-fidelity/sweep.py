"""Click every button that has 2..12 button siblings in every view; report sibling class changes."""
import os, json
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
URL = 'file://' + os.path.join(ROOT, 'clone', 'index.html')
VIEWS = ['00-home','01-llm-analytics','02-firewall','03-live-events','04-policies','04b-policies-changelogs',
 '04c-policies-newpolicy-modal','05-traffic','05a-traffic-projects','05b-traffic-project-usage','05c-traffic-model-config',
 '05d-traffic-statistics','05e-traffic-applications','05f-traffic-errorlogs','06-rbac-access','06b-rbac-usergroups',
 '06c-rbac-config-modules','06d-rbac-config-permissions','06e-rbac-config-roles','06f-rbac-config-mapping','07c-shell-projects']
CANDS = """() => { const out=[]; const bs=[...document.querySelectorAll('button')];
 bs.forEach((b,i)=>{ const p=b.parentElement; if(!p) return; const s=[...p.children].filter(e=>e.tagName==='BUTTON');
   if(s.length>=2 && s.length<=12) out.push(i); }); return out; }"""
SNAP = """(i) => { const b=[...document.querySelectorAll('button')][i]; const s=[...b.parentElement.children].filter(e=>e.tagName==='BUTTON');
 return {text:(b.textContent||'').replace(/\\s+/g,' ').trim().slice(0,40), title:b.getAttribute('title'), aria:b.getAttribute('aria-label'),
   sibs:s.map(x=>({t:(x.textContent||'').replace(/\\s+/g,' ').trim().slice(0,30)||x.getAttribute('title')||x.getAttribute('aria-label')||'', c:x.className})),
   inSidebar: !!b.closest('#sidebar')}; }"""
CLICK = """(i) => { const b=[...document.querySelectorAll('button')][i]; b.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true})); }"""
if __name__ != "__main__": raise SystemExit
res = []
with sync_playwright() as pw:
    br = pw.chromium.launch(); pg = br.new_page(viewport={'width':1920,'height':936})
    for v in VIEWS:
        pg.goto(URL + '#' + v); pg.wait_for_timeout(250)
        cands = pg.evaluate(CANDS)
        for i in cands:
            if pg.evaluate('location.hash.slice(1)') != v:
                pg.goto(URL + '#' + v); pg.reload(); pg.wait_for_timeout(250)
            try:
                before = pg.evaluate(SNAP, i)
            except Exception as e:
                pg.goto(URL + '#' + v); pg.reload(); pg.wait_for_timeout(250)
                continue
            pg.evaluate(CLICK, i); pg.wait_for_timeout(30)
            h = pg.evaluate('location.hash.slice(1)')
            if h != v:
                continue
            try:
                after = pg.evaluate(SNAP, i)
            except Exception:
                pg.reload(); pg.wait_for_timeout(250); continue
            changed = [ (a['t'], sorted(set(a['c'].split())-set(b['c'].split())), sorted(set(b['c'].split())-set(a['c'].split())))
                        for a,b in zip(before['sibs'], after['sibs']) if a['c']!=b['c']]
            if changed:
                res.append({'view':v,'idx':i,'clicked':before['text'] or before['title'] or before['aria'],
                            'group':[s['t'] for s in before['sibs']],'changed':changed,'sidebar':before['inSidebar']})
                pg.goto(URL + '#' + v); pg.reload(); pg.wait_for_timeout(250)
    br.close()
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'sweep.json'),'w'), indent=1)
for r in res:
    print(r['view'], '| clicked:', r['clicked'], '| group:', r['group'], '| sidebar' if r['sidebar'] else '')
    for c in r['changed']: print('     ', c)
