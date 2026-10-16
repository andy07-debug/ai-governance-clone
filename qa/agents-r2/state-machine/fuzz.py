import sys, random, json, hashlib, re
from playwright.sync_api import sync_playwright
BASE='file:///Users/kumaraniket/Desktop/AI%20Governance%20Clone/clone/index.html'
PAGES=['00-home','01-llm-analytics','02-firewall','03-live-events','04-policies','04b-policies-changelogs','04c-policies-newpolicy-modal','05-traffic','05a-traffic-projects','05b-traffic-project-usage','05c-traffic-model-config','05d-traffic-statistics','05e-traffic-applications','05f-traffic-errorlogs','06-rbac-access','06b-rbac-usergroups','06c-rbac-config-modules','06d-rbac-config-permissions','06e-rbac-config-roles','06f-rbac-config-mapping','07c-shell-projects']
OVS=['07a-shell-mode-dropdown','07b-shell-hamburger']
SIGJS='''()=>{const ps=document.querySelectorAll('#mount [data-panel]');const r=ps[ps.length-1];if(!r)return null;
const c=r.cloneNode(true);c.querySelectorAll('[data-overlay]').forEach(n=>n.remove());
return c.textContent.replace(/\\b(more|less)\\b/g,'').replace(/\\s+/g,' ').trim()}'''
STATEJS='''()=>{const m=document.getElementById('mount');const q=s=>m.querySelectorAll(s).length;
const dd=m.querySelector('.h-20 .p-dropdown');const tr=dd&&dd.querySelector('.p-dropdown-trigger');
const ovs=[...m.querySelectorAll('[data-overlay]')].map(n=>n.className.includes('p-dropdown-panel')?'07a':(n.className.includes('p-sidebar-mask')?'07b':'?'));
return {hash:location.hash.slice(1), root:q('#root'), panels:q('[data-panel]'), side:document.querySelectorAll('#sidebar').length, hdr:q('.h-20'),
 fsbox:q('.fixed.inset-0.z-20'), bubble:document.querySelectorAll('.maximizeChatButton').length, handle:q('[data-resize-handle]'),
 ovs:ovs, ddPanels:document.querySelectorAll('.p-dropdown-panel').length, masks:document.querySelectorAll('.p-sidebar-mask').length,
 ddOpen: dd? /p-dropdown-open|p-focus|p-inputwrapper-focus/.test(dd.className):null, ddCls: dd?dd.className:null,
 aria: tr?tr.getAttribute('aria-expanded'):null, restore: q('[data-overlay-restore]'),
 tfBtns: q('[title="Toggle Fullscreen"]'), tfSvgs: [...m.querySelectorAll('[title="Toggle Fullscreen"]')].map(b=>b.querySelectorAll('svg').length),
 minimize: (()=>{const t=document.getElementById('fs-minimize');const k=t&&t.content.firstElementChild;if(!k)return -1;const cls=k.getAttribute('class');return cls?m.querySelectorAll('svg[class="'+cls+'"]').length:-2})(),
 histLen: history.length}}'''

def run(seed, nsteps, log, script=None):
    rnd=random.Random(seed)
    out=[]
    with sync_playwright() as pw:
        b=pw.chromium.launch(); ctx=b.new_context(viewport={'width':1920,'height':936}); pg=ctx.new_page(); pg.set_default_timeout(1200)
        errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
        # signatures
        sigs={}
        for v in PAGES:
            pg.goto(BASE+'?sig'+v+'#'+v); pg.wait_for_timeout(150); sigs[v]=pg.evaluate(SIGJS)
        dup=[v for v in sigs if list(sigs.values()).count(sigs[v])>1]
        if dup: print('dup sigs',dup)
        model={'fs':False}
        n=[0]
        def load(h):
            n[0]+=1; pg.goto(BASE+'?l%d#%s'%(n[0],h) if h else BASE+'?l%d'%n[0]); pg.wait_for_timeout(250); model['fs']=False
        load('')
        steps=[]
        def which_page():
            s=pg.evaluate(SIGJS)
            for v,x in sigs.items():
                if x==s: return v
            return '??'
        def check(desc):
            st=pg.evaluate(STATEJS); pv=which_page(); bad=[]
            if st['root']!=1: bad.append('root=%d'%st['root'])
            if st['hdr']!=1: bad.append('hdr=%d'%st['hdr'])
            if st['side']!=1: bad.append('sidebar=%d'%st['side'])
            if st['panels']!=2: bad.append('panels=%d'%st['panels'])
            if len(st['ovs'])>1 or st['ddPanels']>1 or st['masks']>1: bad.append('overlays=%s dd=%d masks=%d'%(st['ovs'],st['ddPanels'],st['masks']))
            if st['bubble']>1: bad.append('bubble=%d'%st['bubble'])
            if any(x>1 for x in st['tfSvgs']): bad.append('tf svgs %s'%st['tfSvgs'])
            if st['minimize']>1: bad.append('minimize=%d'%st['minimize'])
            fs_dom = st['bubble']==1
            if fs_dom != model['fs']: bad.append('fullscreen model=%s dom bubble=%d'%(model['fs'],st['bubble']))
            if pv!='07c-shell-projects':
                if fs_dom and (st['fsbox']!=1 or st['handle']!=0): bad.append('fs partial fsbox=%d handle=%d'%(st['fsbox'],st['handle']))
                if not fs_dom and (st['fsbox']!=0 or st['handle']!=1): bad.append('nonfs partial fsbox=%d handle=%d'%(st['fsbox'],st['handle']))
            ov = st['ovs'][0] if st['ovs'] else None
            if ov:
                if st['hash'][:3]!=ov: bad.append('overlay %s shown but hash %s'%(ov,st['hash']))
            else:
                if st['hash']!=pv: bad.append('hash %s but page shown %s'%(st['hash'],pv))
            if (ov=='07a') != (st['aria']=='true'): bad.append('dropdown aria=%s ov=%s'%(st['aria'],ov))
            if not ov=='07a' and st['restore']: bad.append('leftover restore attrs')
            if errs: bad.append('pageerror %s'%errs[:2]); errs.clear()
            steps.append(desc)
            line='%3d %-45s hash=%-30s page=%-28s ov=%s fs=%s %s'%(len(steps),desc[:45],st['hash'],pv,ov,fs_dom,'BAD '+'; '.join(bad) if bad else '')
            log.write(line+'\n')
            if bad: out.append((list(steps),bad,st))
            return st,pv,ov
        def click(sel, nth=0, text=None, scope=None):
            loc = pg.locator(scope or 'body').get_by_text(text,exact=True) if text else pg.locator(sel)
            loc=loc.nth(nth)
            try:
                if not loc.count(): return False
                loc.click(timeout=800); return True
            except Exception: return False
        HOME=['LLM Studio Analytics','Firewall Overview','Live Events','Policies','Traffic Analysis']
        def actions(pv, ov, st):
            A=[]
            A.append(('back',lambda: pg.go_back(wait_until='commit')))
            A.append(('forward',lambda: pg.go_forward(wait_until='commit')))
            A.append(('escape',lambda: pg.keyboard.press('Escape')))
            if rnd.random()<0.15: A.append(('reload',lambda: (pg.reload(),model.update(fs=False))))
            if rnd.random()<0.15:
                h=rnd.choice(['07a-shell-mode-dropdown','07b-shell-hamburger','04c-policies-newpolicy-modal',rnd.choice(PAGES)])
                A.append(('deeplink #'+h,lambda h=h: load(h)))
            if rnd.random()<0.1:
                h=rnd.choice(OVS+PAGES)
                A.append(('sethash #'+h,lambda h=h: pg.evaluate('h=>{location.hash=h}',h)))
            A.append(('click trigger',lambda: click('.h-20 .p-dropdown')))
            A.append(('click hamburger',lambda: click('[title="Open sidebar"]')))
            A.append(('click outside (right-panel point)',lambda: pg.mouse.click(1500,700)))
            A.append(('click header logo area',lambda: pg.mouse.click(60,40)))
            A.append(('click fullscreen toggle',lambda: click('[title="Toggle Fullscreen"]')))
            A.append(('click bubble',lambda: click('.maximizeChatButton')))
            A.append(('click Projects(left)',lambda: click('[data-testid="headerProjectsButton"]')))
            A.append(('click outer home crumb',lambda: click('main button[title="Back to home"], main span.p-1.text-indigo-600')))
            if ov=='07a':
                A+= [('pick AI Governance',lambda: click(None,text='AI Governance',scope='.p-dropdown-panel')),
                     ('type search',lambda: pg.locator('.p-dropdown-panel input').fill(rnd.choice(['ai','gov','zz','']))),
                     ('click other mode li',lambda: click('.p-dropdown-panel li',nth=rnd.randint(0,3)))]*2
            if ov=='07b':
                A+= [('drawer X',lambda: click('[title="Click to close sidebar"]')),('mask click',lambda: pg.mouse.click(1800,500)),('click inside drawer',lambda: pg.mouse.click(100,400))]*2
            if pv=='00-home':
                for h in HOME: A.append(('home card '+h,lambda h=h: click(None,text=h)))
                A.append(('RBAC btn',lambda: click(None,text='RBAC')))
            if pv.startswith('04'):
                A+=[('Change Logs',lambda: click(None,text='Change Logs')),('Policies Deck',lambda: click(None,text='Policies Deck')),('New Policy',lambda: click(None,text='New Policy'))]
                # text may include icon/whitespace; also partial
                A+=[('New Policy~',lambda: pg.get_by_text('New Policy',exact=False).first.click(timeout=800)),('Change Logs~',lambda: pg.get_by_text('Change Logs',exact=False).first.click(timeout=800))]
            if pv=='04c-policies-newpolicy-modal':
                A+=[('modal Cancel',lambda: click(None,text='Cancel')),('modal X',lambda: click('.animate-slideUp .border-b button')),('modal backdrop',lambda: pg.mouse.click(1880,900))]*2
            if pv.startswith('05'):
                for t in ['Projects','Statistics','Applications','Error logs']: A.append(('hub '+t,lambda t=t: click(None,text=t,scope='main')))
                A.append(('inner crumb home',lambda: click('main .p-breadcrumb-home')))
                A.append(('crumb Projects',lambda: click(None,text='Projects',scope='main .p-breadcrumb')))
                A.append(('View Usage',lambda: click(None,text='View Usage',nth=rnd.randint(0,2))))
                A.append(('Model Configuration',lambda: click(None,text='Model Configuration',nth=0)))
            if pv.startswith('06'):
                for t in ['Access Management','RBAC Configuration','Configuration','Modules','Permissions','Roles','Mapping','User Groups']: A.append(('tab '+t,lambda t=t: click(None,text=t)))
            return A
        st,pv,ov=check('start')
        for i in range(nsteps):
            A=actions(pv,ov,st)
            name,fn=rnd.choice(A)
            before_fs=model['fs']
            try:
                r=fn()
            except Exception as e:
                r=False; name+=' (ERR %s)'%str(e)[:40]
            # update fs model
            if name=='click fullscreen toggle' and r: model['fs']=not before_fs
            if name=='click bubble' and r: model['fs']=False
            pg.wait_for_timeout(250)
            st,pv,ov=check(name+('' if r is not False else ' [skip]'))
        b.close()
    return out

if __name__=='__main__':
    seeds=[int(x) for x in sys.argv[1:]] or [1]
    allbad=[]
    for s in seeds:
        with open('log_%d.txt'%s,'w') as log:
            bad=run(s,60,log)
        print('seed',s,'violations',len(bad))
        for steps,b_,st in bad[:6]: print('  at step',len(steps),steps[-1],b_)
