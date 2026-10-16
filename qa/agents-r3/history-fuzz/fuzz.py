import sys, random, json
from playwright.sync_api import sync_playwright
BASE='file:///Users/kumaraniket/Desktop/AI%20Governance%20Clone/clone/index.html'
PAGES=['00-home','01-llm-analytics','02-firewall','03-live-events','04-policies','04b-policies-changelogs','05-traffic','05a-traffic-projects','05b-traffic-project-usage','05c-traffic-model-config','05d-traffic-statistics','05e-traffic-applications','05f-traffic-errorlogs','06-rbac-access','06b-rbac-usergroups','06c-rbac-config-modules','06d-rbac-config-permissions','06e-rbac-config-roles','06f-rbac-config-mapping','07c-shell-projects']
MODAL='04c-policies-newpolicy-modal'
OVS=['07a-shell-mode-dropdown','07b-shell-hamburger']
CHARTS={'01-llm-analytics':1,'05b-traffic-project-usage':1,'05d-traffic-statistics':1}
STATE='''()=>{const m=document.getElementById('mount');const q=s=>document.querySelectorAll(s).length;
const ovs=[...document.querySelectorAll('[data-overlay]')].map(n=>n.className.includes('p-dropdown-panel')?'07a-shell-mode-dropdown':(n.className.includes('p-sidebar-mask')?'07b-shell-hamburger':'?'));
const cvs=[...document.querySelectorAll('canvas')];
const k=document.getElementById('fs-minimize').content.firstElementChild;
const inst=window.Chart?Object.values(window.Chart.instances).length:-1;
return {hash:location.hash.slice(1), st:window.__cloneState(), hdr:q('.h-20'), side:q('#sidebar'), panels:q('[data-panel]'),
 ovs, ddp:q('.p-dropdown-panel'), masks:q('.p-sidebar-mask'), modal:q('.animate-slideUp'),
 fsbox:q('.fixed.inset-0.z-20'), bubble:q('.maximizeChatButton'), handle:q('[data-resize-handle]'),
 minimize: k? q('svg[class="'+k.getAttribute('class')+'"]'):-1, tf:q('[title="Toggle Fullscreen"]'),
 canv:cvs.length, chartCanv:q('canvas[data-chart]'), bound:cvs.filter(c=>c.__chart).length, inst,
 restore:q('[data-overlay-restore]'), hl:history.length}}'''

# actions: (name, js returning a selector-ish point, or python func)
CLICK_JS='''(sel)=>{const [css,txt,nth]=sel; let els=[...document.querySelectorAll(css)];
 if(txt!==null) els=els.filter(e=>e.textContent.replace(/\\s+/g,' ').trim()===txt);
 els=els.filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0});
 if(!els.length) return null; const e=els[Math.min(nth,els.length-1)]; const r=e.getBoundingClientRect();
 return [r.x+r.width/2, r.y+r.height/2]}'''
CLICKS=[
 ('card LLM', ['h3','LLM Studio Analytics',0]), ('card Firewall',['h3','Firewall Overview',0]), ('card Live',['h3','Live Events',0]),
 ('card Policies',['h3','Policies',0]), ('card Traffic',['h3','Traffic Analysis',0]), ('RBAC btn',['button','RBAC',0]),
 ('outer home',['main button[title="Back to home"], main span.p-1.text-indigo-600',None,0]),
 ('Change Logs',['button','Change Logs',0]), ('Policies Deck',['button','Policies Deck',0]), ('New Policy',['button','New Policy',0]),
 ('modal Cancel',['.animate-slideUp button','Cancel',0]), ('modal X',['.animate-slideUp .border-b button',None,0]), ('Deploy',['button','Deploy Policy',0]),
 ('hub Projects',['main *','Projects',0]), ('hub Statistics',['main *','Statistics',0]), ('hub Applications',['main *','Applications',0]), ('hub Errorlogs',['main *','Error logs',0]),
 ('inner home',['main .p-breadcrumb-home',None,0]), ('crumb Projects',['main .p-breadcrumb a, main .p-breadcrumb span','Projects',0]),
 ('View Usage',['button','View Usage',2]), ('Model Config',['button','Model Configuration',0]),
 ('tab Access',['*','Access Management',0]), ('tab RBACconf',['*','RBAC Configuration',0]), ('tab Config',['*','Configuration',0]),
 ('tab Perm',['*','Permissions',0]), ('tab Roles',['*','Roles',0]), ('tab Mapping',['*','Mapping',0]), ('tab Modules',['*','Modules',0]), ('tab UserGroups',['*','User Groups',0]),
 ('dd trigger',['.h-20 .p-dropdown',None,0]), ('dd pick AIG',['.p-dropdown-panel li[aria-label="AI Governance"]',None,0]), ('dd other mode',['.p-dropdown-panel li.p-dropdown-item',None,3]),
 ('dd search',['.p-dropdown-panel input',None,0]),
 ('hamburger',['[title="Open sidebar"]',None,0]), ('drawer X',['[title="Click to close sidebar"]',None,0]), ('drawer inside',['.p-sidebar',None,0]),
 ('projects btn',['[data-testid="headerProjectsButton"]',None,0]),
 ('fs toggle',['[title="Toggle Fullscreen"]',None,0]), ('fs bubble',['.maximizeChatButton',None,0]),
 ('metric Requests',['button','Requests',0]),
]
IGNORE_MODAL_HASH=1
HASHES=PAGES+OVS+[MODAL,'nope','','07a','00-HOME']

def run(seed, nsteps, out, script=None):
    rnd=random.Random(seed); log=[]; viol=[]
    with sync_playwright() as pw:
        b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936}); pg.set_default_timeout(3000)
        errs=[]; pg.on('pageerror',lambda e: errs.append('pageerror '+str(e)))
        pg.on('console',lambda m: errs.append('console '+m.text) if m.type=='error' else None)
        # model of history: list of page hashes + idx; modal/overlay never in history
        M={'ent':[],'i':-1,'page':None,'ov':None,'modal':False,'fs':False}
        def push(h):
            if M['ent'] and M['ent'][M['i']]==h: return
            M['ent']=M['ent'][:M['i']+1]+[h]; M['i']+=1
        def replace(h): M['ent'][M['i']]=h
        P={'pg':pg}
        def gonav(h, fresh=True):
            nonlocal pg
            old=pg; pg=b.new_page(viewport={'width':1920,'height':936}); pg.set_default_timeout(3000)
            pg.on('pageerror',lambda e: errs.append('pageerror '+str(e)))
            pg.on('console',lambda m: errs.append('console '+m.text) if m.type=='error' else None)
            old.close()
            pg.goto(BASE+('#'+h if h else '')); pg.wait_for_timeout(300)
        def resetmodel(h):
            p = h if h in PAGES else ('04-policies' if h==MODAL else '00-home')
            M.update(ent=[p],i=0,page=p,ov=(h if h in OVS else None),modal=(h==MODAL),fs=False)
        start=rnd.choice(HASHES) if script is None else script[0]
        gonav(start); resetmodel(start); log.append(('load',start))
        def check(desc):
            s=pg.evaluate(STATE); bad=[]
            if s['hdr']!=1: bad.append('hdr=%d'%s['hdr'])
            if s['side']!=1: bad.append('sidebar=%d'%s['side'])
            if len(s['ovs'])>1 or s['ddp']>1 or s['masks']>1: bad.append('overlays %s ddp=%d masks=%d'%(s['ovs'],s['ddp'],s['masks']))
            ov=s['ovs'][0] if s['ovs'] else None
            if ov:
                if s['st']!=ov: bad.append('state %s != overlay %s'%(s['st'],ov))
                if s['hash'] not in PAGES: bad.append('hash %s not a page while overlay open'%s['hash'])
            else:
                if s['hash']!=s['st'] and not (s['st']==MODAL and s['hash']=='04-policies'): bad.append('hash %s != state %s'%(s['hash'],s['st']))
            if (s['st']==MODAL or s['hash']==MODAL) and IGNORE_MODAL_HASH==0:
                if s['hash']!='04-policies': bad.append('modal open but hash=%s (contract: URL stays on page)'%s['hash'])
            if s['modal']>1: bad.append('modal x%d'%s['modal'])
            if (s['st']==MODAL) != (s['modal']==1) and not ov: bad.append('modal dom=%d state=%s'%(s['modal'],s['st']))
            if s['bubble']>1 or s['minimize']>1 or s['fsbox']>1: bad.append('dup fs bubble=%d min=%d box=%d'%(s['bubble'],s['minimize'],s['fsbox']))
            fsd=s['bubble']==1
            if fsd!=M['fs']: bad.append('fs model=%s dom bubble=%d'%(M['fs'],s['bubble']))
            if s['tf'] and fsd!=(s['fsbox']==1 and s['minimize']==1 and s['handle']==0): bad.append('fs partial bubble=%d box=%d min=%d handle=%d'%(s['bubble'],s['fsbox'],s['minimize'],s['handle']))
            if not fsd and s['handle']!=1: bad.append('handle=%d'%s['handle'])
            pagev = s['hash'] if ov else s['st']
            exp=CHARTS.get(pagev,0)
            if s['chartCanv']!=exp or s['bound']!=exp or s['inst']!=exp or s['canv']!=exp: bad.append('charts canv=%d dc=%d bound=%d inst=%d exp=%d'%(s['canv'],s['chartCanv'],s['bound'],s['inst'],exp))
            if not ov and s['restore']: bad.append('stale restore attrs %d'%s['restore'])
            # model
            mp = MODAL if M['modal'] else M['page']
            if M['ent'][M['i']]!=s['hash'] and not (M['modal'] and not IGNORE_MODAL_HASH): bad.append('model entry %s != hash %s'%(M['ent'][M['i']],s['hash']))
            mstate = M['ov'] or mp
            if s['st']!=mstate: bad.append('model expects %s got %s'%(mstate,s['st']))
            if errs: bad.append('; '.join(errs)); errs.clear()
            return s,bad
        for k in range(nsteps):
            if script: 
                if k+1>=len(script): break
                act=script[k+1]
            else:
                r=rnd.random()
                if r<0.55:
                    avail=[n for n,sel in CLICKS if pg.evaluate(CLICK_JS,sel) is not None]
                    act=('click',rnd.choice(avail)) if avail else ('esc',)
                elif r<0.62: act=('esc',)
                elif r<0.72: act=('back',) if rnd.random()<.6 else ('fwd',)
                elif r<0.76: act=('burst',rnd.randint(2,5))
                elif r<0.80: act=('reload',)
                elif r<0.93: act=('hash',rnd.choice(HASHES))
                elif r<0.96: act=('deeplink',rnd.choice(HASHES))
                else: act=('outside',)
            desc=' '.join(map(str,act)); skip=False; prehash=pg.evaluate('location.hash.slice(1)'); preI=M['i']
            try:
                a=act[0]
                if a=='click':
                    sel=dict(CLICKS)[act[1]]
                    pt=pg.evaluate(CLICK_JS,sel)
                    if pt is None: skip=True
                    else:
                        # predict model
                        pre=pg.evaluate(STATE)
                        pg.mouse.click(pt[0],pt[1]); pg.wait_for_timeout(250)
                        if act[1]=='dd search': pg.keyboard.type('ai')
                elif a=='esc': pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
                elif a=='back':
                    if M['i']==0: skip=True
                    else: pg.go_back(); pg.wait_for_timeout(250)
                elif a=='fwd': pg.go_forward(); pg.wait_for_timeout(250)
                elif a=='burst':
                    ii=M['i']
                    for j in range(act[1]):
                        if j%3!=2:
                            if ii==0: continue
                            ii-=1; pg.evaluate('history.back()')
                        else:
                            if ii<len(M['ent'])-1: ii+=1
                            pg.evaluate('history.forward()')
                    pg.wait_for_timeout(500)
                elif a=='reload': pg.reload(); pg.wait_for_timeout(350)
                elif a=='hash': pg.evaluate('h=>{location.hash=h}', act[1]); pg.wait_for_timeout(250)
                elif a=='deeplink': gonav(act[1])
                elif a=='outside': pg.mouse.click(1500,880); pg.wait_for_timeout(250)
            except Exception as e:
                desc+=' EXC '+str(e)[:80]
            s=pg.evaluate(STATE)
            # update model from observed truth for click actions (we only model history), then check invariants
            ovd=s['ovs'][0] if s['ovs'] else None
            if a in ('click','esc','outside') and not skip:
                # trust app for which screen was chosen; model the history effect
                newpage = s['hash'] if ovd else s['st']
                if newpage==MODAL:
                    M['modal']=True; M['ov']=ovd
                    if IGNORE_MODAL_HASH and s['hash']==MODAL: replace(MODAL)
                else:
                    if M['modal'] and IGNORE_MODAL_HASH: replace(newpage)
                    elif newpage!=M['page']: push(newpage)
                    M['page']=newpage if newpage in PAGES else M['page']; M['modal']=False; M['ov']=ovd
                if a=='click': M['fs']= s['bubble']==1
                if M['fs'] and not s['tf'] and s['bubble']==0: M['fs']=False
            elif a in ('back','fwd','burst'):
                if skip: pass
                elif a=='back': M['i']=max(0,M['i']-1)
                elif a=='fwd': M['i']=min(len(M['ent'])-1,M['i']+1)
                else:
                    for j in range(act[1]): M['i']=max(0,M['i']-1) if j%3!=2 else min(len(M['ent'])-1,M['i']+1)
                if not skip and M['ent'][M['i']]!=prehash:
                    e=M['ent'][M['i']]; M['ov']=None; M['modal']= e==MODAL; M['page']='04-policies' if e==MODAL else e
            elif a=='reload':
                M['ov']=None; M['fs']=False
                # contract: modal never in URL -> reload shows the page
                M['modal']= IGNORE_MODAL_HASH and prehash==MODAL
            elif a=='hash':
                h=act[1]; curh=prehash
                if h!=curh:
                    tgt = '00-home' if h=='' else (h if h in PAGES else ('04-policies' if h==MODAL else M['page']))
                    M['ent']=M['ent'][:M['i']+1]+[tgt]; M['i']+=1
                    if IGNORE_MODAL_HASH and h==MODAL: tgt=MODAL; M['ent'][M['i']]=MODAL
                    if h=='' or h in PAGES: M.update(page=tgt,ov=None,modal=False)
                    elif h in OVS: M['ov']=h
                    elif h==MODAL: M.update(page='04-policies',modal=True,ov=None)
            elif a=='deeplink':
                resetmodel(act[1])
            if skip: desc+=' [skip]'
            s,bad=check(desc)
            log.append((desc, s['hash'], s['st'], M['fs'], bad, list(M['ent']), M['i']))
            if bad: viol.append((k,desc,bad))
            # resync model to reality after a violation so we don't cascade
            if bad:
                ovd=s['ovs'][0] if s['ovs'] else None
                M['ov']=ovd; M['modal']= (s['st']==MODAL); M['page']= s['hash'] if s['hash'] in PAGES else M['page']
                M['fs']= s['bubble']==1
                if s['hash']: M['ent'][M['i']]=s['hash']
        b.close()
    with open(out,'w') as f:
        for i,l in enumerate(log): f.write('%3d %s\n'%(i,json.dumps(l)))
    return viol

if __name__=='__main__':
    tot=0
    for seed in map(int,sys.argv[1:]):
        v=run(seed,120,'/Users/kumaraniket/Desktop/AI Governance Clone/qa/agents-r3/history-fuzz/log_%d.txt'%seed)
        print('seed',seed,'violations',len(v))
        for x in v: print('  ',x)
