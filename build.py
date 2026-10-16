#!/usr/bin/env python3
"""Build a static, clickable replica of appmod.ai AI Governance mode from DOM captures.

capture/<view>/{page.html,styles.css}  ->  clone/index.html + clone/assets/app.css
"""
import json, os, re, urllib.request, hashlib

ROOT = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(ROOT, 'capture')
OUT = os.path.join(ROOT, 'clone')
ASSETS = os.path.join(OUT, 'assets')
os.makedirs(ASSETS, exist_ok=True)

ALL_CAPTURES = sorted(d for d in os.listdir(CAP) if os.path.isfile(os.path.join(CAP, d, 'page.html')))
VIEWS = [d for d in ALL_CAPTURES if not d.startswith('08-')]  # 08-* are state captures used for overlays
FULLSCREEN = '08-fullscreen-live-events'
CHART_VIEWS = {  # view -> (chart id in charts.js, attributes the live <canvas> carried)
    '01-llm-analytics': ('llm-cost-trend', 'aria-label="LLM cost trend chart"'),
    '05b-traffic-project-usage': ('requests-05b', 'role="img" data-pc-section="canvas"'),
    '05d-traffic-statistics': ('requests-05d', 'role="img" data-pc-section="canvas"'),
}
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Safari/537.36'


# ---------- CSS ----------
def split_rules(css):
    """Split a stylesheet into top-level rules (handles nesting, strings, comments)."""
    rules, depth, start, i, n = [], 0, 0, 0, len(css)
    while i < n:
        c = css[i]
        if c == '\\':  # escaped char in a selector, e.g. .font-\[\'Inter\'\]
            i += 2
            continue
        if c == '/' and css.startswith('/*', i):
            j = css.find('*/', i + 2)
            j = n if j < 0 else j + 2
            if depth == 0:  # drop top-level comments (sheet headers)
                css = css[:i] + ' ' * (j - i) + css[j:]
            i = j
            continue
        if c in '"\'':
            j = i + 1
            while j < n and css[j] != c:
                j += 2 if css[j] == '\\' else 1
            i = j + 1
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                rules.append(css[start:i + 1].strip()); start = i + 1
        elif c == ';' and depth == 0:  # @import / @charset statements
            rules.append(css[start:i + 1].strip()); start = i + 1
        i += 1
    return [r for r in rules if r]


def merge_css():
    """Ordered union of every view's rules: a rule first seen in a later view is placed
    right after the rule that preceded it in that view, so cascade order is preserved."""
    base = split_rules(open(os.path.join(CAP, VIEWS[0], 'styles.css'), encoding='utf-8').read())
    seen = set(base)
    after = {}  # anchor rule (None = very top) -> rules inserted after it
    for v in VIEWS[1:]:
        anchor = None
        for r in split_rules(open(os.path.join(CAP, v, 'styles.css'), encoding='utf-8').read()):
            if r not in seen:
                seen.add(r)
                after.setdefault(anchor, []).append(r)
            anchor = r
    out = []
    def emit(r):
        out.append(r)
        for x in after.get(r, []):
            emit(x)
    for x in after.get(None, []):
        emit(x)
    for r in base:
        emit(r)
    return out


def fetch(url, binary=False):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    data = urllib.request.urlopen(req, timeout=60).read()
    return data if binary else data.decode('utf-8')


def localize_google(url):
    css = fetch(url)
    def dl(m):
        u = m.group(1)
        name = 'gf-' + hashlib.md5(u.encode()).hexdigest()[:12] + os.path.splitext(u.split('?')[0])[1]
        p = os.path.join(ASSETS, name)
        if not os.path.exists(p):
            open(p, 'wb').write(fetch(u, binary=True))
        return 'url(%s)' % name
    return re.sub(r'url\(([^)]+)\)', dl, css)


def build_css():
    rules = merge_css()
    imports, body = [], []
    for r in rules:
        if r.startswith('@charset') or re.search(r'claude-(agent|pulse|phantom)', r):  # extension overlay styles
            continue
        if r.startswith('@import'):
            m = re.search(r'url\("?([^")]+)"?\)', r)
            u = m.group(1) if m else ''
            if 'fonts.googleapis.com' in u and u not in imports:
                imports.append(u)
            continue  # theme/colors.css imports resolve to empty sheets on the live site
        body.append(r)
    head = ['/* Google Fonts (localized) */'] + [localize_google(u) for u in imports]
    css = '\n'.join(head) + '\n' + '\n'.join(body)
    # self-hosted font files -> local assets
    css = re.sub(r'url\("?(?:https://ai-governance-ui-prod-[^/"]+)?/([0-9a-f]{20}\.(?:woff2|woff|ttf))"?\)',
                 r'url("\1")', css)
    open(os.path.join(ASSETS, 'app.css'), 'w', encoding='utf-8').write(css)
    print('css rules', len(rules), 'bytes', len(css), 'google imports', len(imports))


# ---------- HTML ----------
def view_parts(v):
    p = open(os.path.join(CAP, v, 'page.html'), encoding='utf-8').read()
    html_attrs = re.search(r'<html([^>]*)>', p).group(1)
    m = re.search(r'<body([^>]*)>(.*)</body>', p, re.S)
    body_attrs, body = m.group(1), m.group(2)
    body = re.sub(r'<style[^>]*>.*?</style>', '', body, flags=re.S)
    # overlays injected by the browser-automation extension during capture (not part of the app)
    body = re.sub(r'<div id="claude-agent-glow-border".*?</div></div>', '', body, flags=re.S)
    body = re.sub(r'<div id="claude-phantom-cursor".*?</svg></div>', '', body, flags=re.S)
    assert 'id="claude-' not in body, v
    body = re.sub(r'\sdata-s[tl]="[^"]*"', '', body)
    # Canvas charts were snapshotted as bitmaps; put the canvas back so charts.js redraws them (sharp at any width).
    if v in CHART_VIEWS:
        chart_id, attrs = CHART_VIEWS[v]
        body, n = re.subn(r'<img src="data:image/png;base64,[^"]+"( style="[^"]*")[^>]*width="\d+"[^>]*>',
                          lambda m: '<canvas %s data-chart="%s"%s></canvas>' % (attrs, chart_id, m.group(1)), body, count=1)
        assert n == 1, v
    return html_attrs, body_attrs, body


def build_html():
    views = {}
    html_attrs = body_attrs = ''
    for v in VIEWS:
        ha, ba, body = view_parts(v)
        if v == '00-home':
            html_attrs, body_attrs = ha, ba
        views[v] = body
    tpl = '\n'.join('<template id="v-%s">%s</template>' % (k, b) for k, b in views.items())
    # fullscreen extras (floating AskMod bubble + chat button, minimize icon) taken from the live fullscreen capture
    fs = view_parts(FULLSCREEN)[2]
    bubble = re.search(r'<span class="">\s*<div class="fixed bottom-\[90px\].*?maximizeChatButton.*?</button></span>', fs, re.S).group(0)
    minimize = re.search(r'<svg[^>]*lucide-minimize.*?</svg>', fs, re.S).group(0)
    tpl += '\n<template id="fs-bubble">%s</template>\n<template id="fs-minimize">%s</template>' % (bubble, minimize)
    router = open(os.path.join(ROOT, 'charts.js'), encoding='utf-8').read() + '\n' + open(os.path.join(ROOT, 'router.js'), encoding='utf-8').read()
    page = f'''<!doctype html>
<html{html_attrs}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AppMod | Techolution</title>
<link rel="stylesheet" href="assets/app.css">
</head>
<body{body_attrs}>
<div id="mount"></div>
{tpl}
<script src="assets/chart.umd.min.js"></script>
<script>
{router}
</script>
</body>
</html>'''
    open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(page)
    print('views', len(views), 'index.html bytes', len(page))


if __name__ == '__main__':
    build_css()
    build_html()
