"""Real-click in-app navigation flows; compare arrived render to the deep-link render."""
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from playwright.sync_api import sync_playwright
import numpy as np
from PIL import Image
ROOT = '/Users/kumaraniket/Desktop/AI Governance Clone'
OUT = os.path.join(ROOT, 'qa/agents-r2/visual-regression/shots')
URL = 'file://' + ROOT + '/clone/index.html'
ANIM_OFF = '*,*::before,*::after{animation-duration:0s!important;animation-delay:0s!important;transition:none!important;caret-color:transparent!important}'

def load(pg, v):
    pg.goto('about:blank'); pg.goto(URL + '#' + v); pg.add_style_tag(content=ANIM_OFF); pg.wait_for_timeout(1400)
def shot(pg, name):
    p = os.path.join(OUT, name + '.png')
    pg.evaluate('document.activeElement && document.activeElement.blur && document.activeElement.blur()')
    pg.mouse.move(0, 935); pg.wait_for_timeout(200)
    pg.screenshot(path=p); return p
def diff(a, b, name):
    A = np.asarray(Image.open(a).convert('RGB')).astype(int); B = np.asarray(Image.open(b).convert('RGB')).astype(int)
    d = np.abs(A - B).sum(2) > 30
    if not d.any(): return (0.0, None)
    ys, xs = np.where(d)
    Image.fromarray((np.stack([d]*3, 2) * 255).astype(np.uint8)).save(os.path.join(OUT, 'diff-' + name + '.png'))
    return (round(100 * float(d.mean()), 3), (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())))

def ct(text, scope='body', exact=True, nth=0):
    return lambda pg: pg.locator(scope).get_by_text(text, exact=exact).nth(nth).click()
def cs(sel, nth=0):
    return lambda pg: pg.locator(sel).nth(nth).click()
HOME = cs('main button[title="Back to home"], main span.p-1.text-indigo-600')

FLOWS = [
  # name, start view, [actions], expected view
  ('home>01', '00-home', [ct('LLM Studio Analytics')], '01-llm-analytics'),
  ('home>02', '00-home', [ct('Firewall Overview')], '02-firewall'),
  ('home>03', '00-home', [ct('Live Events')], '03-live-events'),
  ('home>04', '00-home', [ct('Policies')], '04-policies'),
  ('home>05', '00-home', [ct('Traffic Analysis')], '05-traffic'),
  ('home>06', '00-home', [ct('RBAC')], '06-rbac-access'),
  ('01>home', '01-llm-analytics', [HOME], '00-home'),
  ('05d>home', '05d-traffic-statistics', [HOME], '00-home'),
  ('06f>home', '06f-rbac-config-mapping', [HOME], '00-home'),
  ('07c>dd>home', '07c-shell-projects', [cs('.h-20 .p-dropdown'), ct('AI Governance', scope='.p-dropdown-panel')], '00-home'),
  ('05b>dd>home', '05b-traffic-project-usage', [cs('.h-20 .p-dropdown'), ct('AI Governance', scope='.p-dropdown-panel')], '00-home'),
  ('04>04b', '04-policies', [ct('Change Logs', exact=False)], '04b-policies-changelogs'),
  ('04b>04', '04b-policies-changelogs', [ct('Policies Deck', exact=False)], '04-policies'),
  ('04>04c', '04-policies', [ct('New Policy', exact=False)], '04c-policies-newpolicy-modal'),
  ('04c>04', '04c-policies-newpolicy-modal', [ct('Cancel')], '04-policies'),
  ('05>05a', '05-traffic', [ct('Projects', scope='main')], '05a-traffic-projects'),
  ('05>05d', '05-traffic', [ct('Statistics', scope='main')], '05d-traffic-statistics'),
  ('05>05e', '05-traffic', [ct('Applications', scope='main')], '05e-traffic-applications'),
  ('05>05f', '05-traffic', [ct('Error logs', scope='main')], '05f-traffic-errorlogs'),
  ('05a>05b', '05a-traffic-projects', [ct('View Usage', nth=2)], '05b-traffic-project-usage'),
  ('05a>05c', '05a-traffic-projects', [ct('Model Configuration')], '05c-traffic-model-config'),
  ('05b>05a', '05b-traffic-project-usage', [ct('Projects', scope='main .p-breadcrumb')], '05a-traffic-projects'),
  ('05c>05a', '05c-traffic-model-config', [ct('Projects', scope='main .p-breadcrumb')], '05a-traffic-projects'),
  ('05d>05', '05d-traffic-statistics', [cs('main .p-breadcrumb-home')], '05-traffic'),
  ('06>06b', '06-rbac-access', [ct('RBAC Configuration')], '06b-rbac-usergroups'),
  ('06b>06c', '06b-rbac-usergroups', [ct('Configuration')], '06c-rbac-config-modules'),
  ('06c>06d', '06c-rbac-config-modules', [ct('Permissions')], '06d-rbac-config-permissions'),
  ('06d>06e', '06d-rbac-config-permissions', [ct('Roles')], '06e-rbac-config-roles'),
  ('06e>06f', '06e-rbac-config-roles', [ct('Mapping')], '06f-rbac-config-mapping'),
  ('06f>06c', '06f-rbac-config-mapping', [ct('Modules')], '06c-rbac-config-modules'),
  ('06c>06b', '06c-rbac-config-modules', [ct('User Groups')], '06b-rbac-usergroups'),
  ('06b>06', '06b-rbac-usergroups', [ct('Access Management')], '06-rbac-access'),
  ('home>07c', '00-home', [cs('[data-testid="headerProjectsButton"]')], '07c-shell-projects'),
  ('05b>07c', '05b-traffic-project-usage', [cs('[data-testid="headerProjectsButton"]')], '07c-shell-projects'),
  # fullscreen on, navigate in fullscreen, then off
  ('03 fs>home>fsoff', '03-live-events', [cs('[title="Toggle Fullscreen"]'), HOME, cs('[title="Toggle Fullscreen"]')], '00-home'),
  ('05b fs>05a>fsoff', '05b-traffic-project-usage', [cs('[title="Toggle Fullscreen"]'), ct('Projects', scope='main .p-breadcrumb'), cs('[title="Toggle Fullscreen"]')], '05a-traffic-projects'),
  ('01 fs>bubble', '01-llm-analytics', [cs('[title="Toggle Fullscreen"]'), cs('.maximizeChatButton')], '01-llm-analytics'),
  # back/forward with real clicks
  ('home>01>back', '00-home', [ct('LLM Studio Analytics'), lambda pg: pg.go_back()], '00-home'),
  ('home>01>back>fwd', '00-home', [ct('LLM Studio Analytics'), lambda pg: pg.go_back(), lambda pg: pg.go_forward()], '01-llm-analytics'),
  ('05a>05b>back(fs)', '05a-traffic-projects', [ct('View Usage', nth=2), cs('[title="Toggle Fullscreen"]'), lambda pg: pg.go_back()], '05a-traffic-projects'),
  ('07c>dd>back', '07c-shell-projects', [cs('.h-20 .p-dropdown'), lambda pg: pg.go_back()], '07c-shell-projects'),
]

res = {}
only = sys.argv[1:]
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1920, 'height': 936}); pg.set_default_timeout(3000)
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    base = {}
    for name, start, acts, exp in FLOWS:
        if only and name not in only: continue
        try:
            if exp not in base:
                load(pg, exp); base[exp] = shot(pg, 'deep-' + exp)
            load(pg, start)
            for a in acts:
                a(pg); pg.wait_for_timeout(1400)
            got = pg.evaluate('location.hash.slice(1)')
            fn = 'flow-' + name.replace('>', '_').replace(' ', '_').replace('(', '').replace(')', '')
            r = diff(base[exp], shot(pg, fn), fn)
            res[name] = (got, r)
        except Exception as e:
            res[name] = 'ERR ' + str(e).split('\n')[0][:150]
        print(name, res[name], flush=True)
    b.close()
print('pageerrors', errs[:5])
json.dump(res, open(os.path.join(OUT, '..', 'res3.json'), 'w'), indent=1)
