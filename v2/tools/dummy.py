"""Dummy-data pass for the built replica (runs at the end of build_v2.build_html).

1. Text: real people, emails, apps, projects, clusters, IPs and IDs -> the made-up set the trailer uses
   (same mapping as the trailer's capture/anonymize.js). Only visible text, a few text attributes, chart
   labels and inline scripts are touched; element ids and data-go/data-open targets keep their names so
   links (and the trailer's capture scripts) still work.
2. Charts: the trend lines get sharp spikes (values printed next to the dashboard sparklines are kept).
Set REAL_DATA=1 to build without this pass."""
import html, json, re

PEOPLE = {
    'manogna.dasari': 'priya.raman', 'siddartha.yadav': 'daniel.okafor', 'siddhartha.yadav': 'daniel.okafor',
    'aadhithya.sendhilmanian': 'maya.chen', 'abhijeeth.sadineni': 'ryan.cole', 'arpit.jain': 'lena.fischer',
    'ashish.singh': 'arjun.mehta', 'atharva.bhole': 'leo.martins', 'hardik.sharma': 'noah.kim', 'krishna.mishra': 'sara.lopez',
    'lokesh.choraria': 'ben.walsh', 'neeraj.saini': 'ivy.tan', 'nitish.rao': 'omar.haddad', 'pavan.penumajji': 'kate.morris',
    'raj.rana': 'tom.becker', 'rakshit.chopade': 'ana.silva', 'sambhav.garg': 'chris.allen', 'shivendra.singh': 'ravi.nair',
    'soham.jain': 'zoe.adams', 'varadha.omkareshwar': 'hana.sato', 'chihnita.boppella': 'ella.park', 'rishabh.srivastava': 'max.weber',
}
R = [
    (r'Manogna Shree Dasari', 'Priya Raman'), (r'(?i)manogna\.d\w*', 'priya.r'), (r'(?i)\bmanogna\b', 'priya'),
    (r'Siddartha Yadav Gundelly', 'Daniel Okafor'), (r'Siddh?artha Yadav', 'Daniel Okafor'), (r'Udit Dave', 'Sam Patel'),
    (r'Srikrishna Nutala\w*', 'Nina Brooks'), (r'(?i)\baadhithya\b', 'maya'), (r'\bat Techolution\b', 'at Northwind'),
    (r'(?i)userstoryagentwidget', 'storybot-widget'), (r'(?i)userstoryagentappmod', 'storybot-core'), (r'(?i)userstoryagentqafin', 'storybot-qa'),
    (r'(?i)userstoryagen', 'storybot-'), (r'(?i)promptmodecrtest', 'prompt-lab'), (r'(?i)listfederateddev', 'search-federated'),
    (r'(?i)hireappdirectdm', 'hiring-assistant'), (r'(?i)devcaseassistant', 'case-assistant'),
    (r'(?i)g?gc[il]lmprgenie', 'supportgenie'), (r'(?i)g?gc[il]lmprge', 'supportgen'), (r'GGCLLMAg', 'SupportAg'), (r'(?i)ggcllm', 'support'),
    (r'proposal-auto-ai-internal', 'ops-platform-prod'), (r'proposal-autoai-gke', 'core-gke'), (r'client-cw-prod', 'web-prod'),
    (r'10\.20\.9\.4\b', '10.8.14.21'), (r'10\.20\.3\.69\b', '10.8.6.44'), (r'10\.20\.7\.53\b', '10.8.2.93'), (r'49\.37\.171\.9\b', '203.0.113.24'),
    (r'69cb8b9e9fe228e2051ab655', '6f3a1c09b2d84e7a51c0e9d4'),
    (r'(?i)@techolution\.com', '@northwind.io'), (r'(?i)@techolution\.c\b', '@northwind.io'), (r'(?i)@techolu\w*', '@northwind'),
    (r'\bTecholution\b', 'Northwind'),
]
R = [(re.compile(a), b) for a, b in R]


def _case(orig, rep):
    """Title-case stays title-case (Pavan.Penumajji -> Kate.Morris)."""
    if orig[:1].isupper() and rep[:1].islower():
        return re.sub(r'(^|\.)([a-z])', lambda m: m.group(1) + m.group(2).upper(), rep)
    return rep


def fix(s):
    for k, v in PEOPLE.items():
        s = re.sub(re.escape(k), lambda m, v=v: _case(m.group(0), v), s, flags=re.I)
    for rx, v in R:
        s = rx.sub(lambda m, v=v: (v[0].upper() + v[1:]) if m.group(0)[:1].isupper() and v[:1].islower() and not m.group(0).isupper() else v, s)
    return s


# ---------------------------------------------------------------- charts: spikes
def _pts(xy):
    return [{'x': x, 'y': y} for x, y in xy]


def _spark(c, xy):
    d = c['data']['datasets'][0]
    d['data'] = _pts(xy)
    d['pointRadius'] = [0] * (len(xy) - 1) + [4]
    d['tension'] = 0.12
    d['cubicInterpolationMode'] = 'default'


def spikes(c):
    ds = c['data']['datasets']
    labels = [d.get('label') for d in ds]
    if 'Total Cost' in labels:  # LLM Studio cost trend: half-day points, spend running away (same as the trailer)
        days = ['07/22', '07/23', '07/24', '07/25', '07/26', '07/27', '07/28']
        c['data']['labels'] = [l for d in days for l in (d, '')][:-1]
        llm = [1100, 2900, 1500, 6100, 1900, 2600, 9400, 2500, 3600, 13200, 3300, 7900, 15600]
        infra = [700, 1200, 900, 2300, 1100, 1300, 3100, 1400, 1700, 4300, 1600, 2900, 5200]
        val = {'LLM Cost': llm, 'Infra Cost': infra, 'Total Cost': [a + b for a, b in zip(llm, infra)]}
        for d in ds:
            d['data'] = val[d['label']]
            d['tension'] = 0.04; d['cubicInterpolationMode'] = 'default'; d['pointRadius'] = 3.5
        y = c['options']['scales'].setdefault('y', {})
        y['max'] = 24000; y.setdefault('ticks', {})['stepSize'] = 4000
        y['ticks'].pop('count', None); y['ticks'].pop('maxTicksLimit', None); y.pop('suggestedMax', None)
        c['options']['scales'].setdefault('x', {}).setdefault('ticks', {})['autoSkip'] = False
        return True
    if 'Critical' in labels and 'Total' in labels:  # Firewall security trend
        val = {'Blocked': [0, 0, 3, 0, 2, 0, 4], 'Total': [3, 1, 12, 2, 9, 1, 15], 'Critical': [2, 0, 10, 1, 7, 0, 12], 'High': [0, 0, 0, 0, 0, 0, 0]}
        for d in ds:
            if d['label'] in val: d['data'] = val[d['label']]
            d['tension'] = 0.15
        y = c['options'].get('scales', {}).get('y')
        if isinstance(y, dict):
            y.pop('max', None); y.pop('suggestedMax', None); y['suggestedMax'] = 16
        return True
    if labels == ['Cost'] and len(ds[0]['data']) == 7:  # a user's cost (drawer)
        ds[0]['data'] = [4.2, 30.5, 3.1, 24.8, 1.6, 33.2, 13.7]
        ds[0]['tension'] = 0.15; ds[0]['cubicInterpolationMode'] = 'default'
        return True
    d0 = ds[0]['data']
    if isinstance(d0, list) and d0 and isinstance(d0[0], dict):  # dashboard sparklines (ends + printed values kept)
        x0, x1 = d0[0]['x'], d0[-1]['x']; ymax = max(p['y'] for p in d0)
        if ymax == 3 and x0 == 247:  # security: critical incidents
            _spark(c, [(247, 0.2), (266, 1.4), (284, 0.3), (302, 2.1), (320, 0.5), (338, 0.4), (356, 2.6), (374, 0.8), (392, 1.2),
                       (410, 2.9), (428, 0.9), (446, 1.5), (464, 0.6), (482, 2.2), (500, 1.1), (518, 2.7), (534, 1.4), (549, 3.0)])
        elif ymax == 472.92:  # finops: spend ($472.92 top / $2.23 bottom are printed beside it)
            _spark(c, [(837, 472.92), (855, 180), (872, 390), (889, 95), (906, 310), (923, 60), (940, 262), (958, 2.23), (975, 140),
                       (992, 35), (1010, 330), (1028, 120), (1046, 420), (1064, 150), (1082, 362), (1100, 210), (1120, 440), (1138, 395.28)])
        elif ymax == 8600:  # system health: requests (8.6K printed)
            _spark(c, [(247, 3), (265, 1400), (280, 200), (298, 2900), (315, 600), (333, 4100), (350, 900), (368, 5200), (385, 1800),
                       (403, 7400), (420, 2600), (438, 8600), (455, 3100), (472, 6900), (490, 2200), (510, 7800), (530, 3900), (549, 7004.68)])
        elif ymax == 1 and x0 == 837:  # change management
            _spark(c, [(837, 0), (862, 0.45), (884, 0), (912, 0.7), (934, 0.05), (960, 0.3), (985, 0), (1010, 1), (1032, 0.15),
                       (1058, 0), (1084, 0.6), (1106, 0.05), (1124, 0.35), (1138, 0.15)])
        else:
            return False
        return True
    return False


def _chart(m):
    try:
        c = json.loads(html.unescape(m.group(1)))
    except ValueError:
        return m.group(0)  # not chart data (e.g. a code comment)
    spikes(c)
    for d in c['data']['datasets']:
        if isinstance(d.get('label'), str): d['label'] = fix(d['label'])
    c['data']['labels'] = [fix(l) if isinstance(l, str) else l for l in c['data'].get('labels', [])]
    return "data-chart='%s'" % html.escape(json.dumps(c, separators=(',', ':')), quote=False).replace("'", '&#39;')


TEXT_ATTRS = re.compile(r'''\b(title|placeholder|value|alt|aria-label)=("[^"]*"|'[^']*')''')


def _tag(t):
    return TEXT_ATTRS.sub(lambda m: '%s=%s' % (m.group(1), fix(m.group(2))), t)


def dummy(page):
    page = re.sub(r"data-chart='([^']*)'", _chart, page)
    out = []
    # scripts: replace inside (chat answers, suggestion regexes); everything else: text between tags + text attributes
    for part in re.split(r'(<script\b[^>]*>.*?</script>)', page, flags=re.S | re.I):
        if part.lower().startswith('<script'):
            out.append(fix(part)); continue
        for seg in re.split(r'(<[^>]+>)', part):
            out.append(_tag(seg) if seg.startswith('<') else fix(seg))
    return ''.join(out)


if __name__ == '__main__':
    import sys
    p = sys.argv[1]
    s = open(p, encoding='utf-8').read()
    open(p, 'w', encoding='utf-8').write(dummy(s))
    print('dummy data ->', p)
