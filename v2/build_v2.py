#!/usr/bin/env python3
"""Build the v2 (demo-version) AI Governance replica.

Shell  = v1's exact captured AskMod/AppMod shell (capture/00-home), re-themed to the demo
         (dark Appmod.AI header, narrow empty chat panel, 20/80 split).
Screens = hand-built fragments in v2/screens/<id>.html (right-panel content, below the breadcrumb bar).
Overlays = drawers / modals / popovers in v2/overlays/<id>.html (rendered above the page).

Output: clone/index.html + clone/assets/ (v1's app.css for the shell, Tailwind-compiled screens.css).
"""
import os, re, sys, json, shutil, subprocess, html

V2 = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(V2)
OUT = os.path.join(ROOT, 'clone')
ASSETS = os.path.join(OUT, 'assets')
sys.path.insert(0, ROOT)
import build as v1  # noqa: E402  (v1 capture helpers: view_parts, CSS pipeline)
from bs4 import BeautifulSoup  # noqa: E402

HEADER_BG = '#17112b'
SIDEBAR_PCT = 20


def build_shell():
    """Return (html_attrs, body_attrs, shell_html) with #screen and #overlay-root slots."""
    ha, ba, body = v1.view_parts('00-home')
    s = BeautifulSoup(body, 'lxml')

    # --- header: dark Appmod theme + logo ---
    bar = s.select_one('.w-full.h-20 > div')
    bar['style'] = 'background-color: %s;' % HEADER_BG
    bar['class'] = [c for c in bar['class'] if not c.startswith('border-b')]
    logo_box = bar.select_one('.w-\\[30\\%\\]')
    logo_box.clear()
    logo_box.append(BeautifulSoup(
        '<div class="flex flex-col w-fit"><div class="flex items-center cursor-pointer" data-go="dashboard">'
        '<img src="assets/appmod-logo@2x.png" alt="Appmod.AI — Code Smarter, Build Faster!" '
        'width="200" height="53" style="display:block;width:200px;height:53px;margin:1.5px 0 0 2.5px"></div></div>', 'lxml').body.div)
    burger = bar.select_one('[title="Open sidebar"]')
    if burger is not None:
        burger['style'] = (burger.get('style', '') + ';color:#fff;').lstrip(';')
        for svg in burger.select('svg'):
            svg['stroke'] = '#ffffff'
            for p in svg.select('[stroke]'):
                p['stroke'] = '#ffffff'

    # --- panels: 20 / 80 split like the demo ---
    side = s.select_one('#sidebar')
    side['style'] = 'flex: %d 1 0px; overflow: hidden;' % SIDEBAR_PCT
    side['data-panel-size'] = '%.1f' % SIDEBAR_PCT
    side['class'] = [c for c in side['class'] if c != 'w-[45%]']
    panels = s.select('[data-panel]')
    right = panels[-1]
    right['style'] = 'flex: %d 1 0px; overflow: hidden;' % (100 - SIDEBAR_PCT)
    right['data-panel-size'] = '%.1f' % (100 - SIDEBAR_PCT)

    # --- chat panel: empty conversation (as in the demo) ---
    title_row = side.select_one('.w-full.flex.py-3.px-5')
    if title_row is not None:
        title_row.decompose()
    msgs = side.select_one('.relative.flex.flex-col.flex-1.px-5.pt-5.pb-0.overflow-y-auto')
    bot_tpl = ''
    if msgs is not None:
        # keep the real AskMod bot-message markup as a template for the scripted chat (chat.js)
        bot = msgs.select_one('.delayed-messages > div')
        if bot is not None:
            count = bot.select_one('.text-\\[10px\\] > span')
            if count is not None:
                count.decompose()  # "(50)" counter next to the time: meaning unknown, not reproduced
            bot_tpl = '<template id="chat-bot-tpl">%s</template>' % str(bot)
        msgs.clear()
        msgs.append(BeautifulSoup('<div class="mt-auto flex flex-col"><div id="chat-log" class="flex flex-col"></div>'
                                  '<div id="chat-chips" class="flex flex-col items-start gap-2 pb-3"></div></div>', 'lxml').body.div)
    tools = side.select_one('.w-full.flex.items-end')
    if tools is not None:
        btns = tools.select('.relative.inline-block')
        if btns:
            btns[-1].decompose()  # the demo shows only the first tool button above the input

    # --- right panel: breadcrumb bar + screen slot ---
    main = right.select_one('main')
    crumb = main.select_one('.w-full.flex.items-center.justify-between.px-5.py-3')
    left = crumb.select_one('.flex.items-center.gap-1\\.5')
    home = left.select_one('span.p-1')
    home.name = 'button'
    home['class'] = ['p-1', 'rounded', 'text-slate-400', 'hover:text-indigo-600', 'transition-colors']
    home['title'] = 'Back to home'
    home['data-go'] = 'dashboard'
    title = left.select_one('span.text-base')
    title['id'] = 'crumb-title'
    content = main.select_one('.flex-1.overflow-y-auto')
    content.replace_with(BeautifulSoup('<div id="screen" class="flex-1 overflow-y-auto relative"></div>', 'lxml').body.div)
    root = s.select_one('#root')
    root.append(BeautifulSoup('<div id="overlay-root"></div>', 'lxml').body.div)
    return ha, ba, ''.join(str(c) for c in s.body.contents) + bot_tpl


def projects_template():
    """The real Projects page (captured from the live app, capture/07c-shell-projects) as a full-panel screen."""
    _, _, body = v1.view_parts('07c-shell-projects')
    s = BeautifulSoup(body, 'lxml')
    right = s.select('[data-panel]')[-1]
    inner = ''.join(str(c) for c in right.contents)
    return '<template id="s-projects" data-title="Projects" data-fullpanel="1">%s</template>' % inner


META = re.compile(r'^\s*<!--(.*?)-->', re.S)


def read_fragments(folder, prefix):
    out = []
    d = os.path.join(V2, folder)
    if not os.path.isdir(d):
        return out
    for f in sorted(os.listdir(d)):
        if not f.endswith('.html'):
            continue
        sid = f[:-5]
        src = open(os.path.join(d, f), encoding='utf-8').read()
        meta = {}
        m = META.match(src)
        if m:
            for part in m.group(1).split('|'):
                if ':' in part:
                    k, v = part.split(':', 1)
                    meta[k.strip()] = v.strip()
        attrs = ''.join(' data-%s="%s"' % (k, html.escape(v, quote=True)) for k, v in meta.items())
        out.append('<template id="%s-%s"%s>%s</template>' % (prefix, sid, attrs, src))
    return out


def copy_assets():
    os.makedirs(ASSETS, exist_ok=True)
    for f in os.listdir(os.path.join(V2, 'assets')):
        shutil.copy2(os.path.join(V2, 'assets', f), os.path.join(ASSETS, f))


def compile_tailwind(dest):
    cfg = os.path.join(V2, 'tailwind.config.js')
    src = os.path.join(V2, 'screens.src.css')
    r = subprocess.run(['npx', 'tailwindcss', '-c', cfg, '-i', src, '-o', dest, '--minify'], cwd=V2, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit('tailwind failed:\n' + r.stderr)


def build_css():
    v1.build_css()  # writes clone/assets/app.css (+ fonts) for the shell
    compile_tailwind(os.path.join(ASSETS, 'screens.css'))
    copy_assets()


def build_html(out_dir=OUT, css_name='screens.css'):
    """out_dir=clone/ for the real build; a private dir (e.g. v2/out/<label>) for parallel builders."""
    ha, ba, shell = build_shell()
    tpls = read_fragments('screens', 's') + read_fragments('overlays', 'o') + [projects_template()]
    js = open(os.path.join(V2, 'router.js'), encoding='utf-8').read() + '\n' + open(os.path.join(V2, 'chat.js'), encoding='utf-8').read()
    rel = os.path.relpath(ASSETS, out_dir).replace(os.sep, '/')
    body = shell + '\n' + '\n'.join(tpls)
    if rel != 'assets':  # private build: point asset references at the shared clone/assets
        body = body.replace('src="assets/', 'src="%s/' % rel).replace('url(assets/', 'url(%s/' % rel).replace("url('assets/", "url('%s/" % rel)
    page = '''<!doctype html>
<html%s>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AppMod | Techolution</title>
<link rel="stylesheet" href="%s/app.css">
<link rel="stylesheet" href="%s/%s">
</head>
<body%s>
<div id="mount" style="display:contents">%s</div>
<script src="%s/chart.umd.min.js"></script>
<script>
%s
</script>
</body>
</html>''' % (ha, rel, rel, css_name, ba, body, rel, js)
    os.makedirs(out_dir, exist_ok=True)
    open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8').write(page)
    print('screens+overlays', len(tpls), '->', os.path.relpath(os.path.join(out_dir, 'index.html'), ROOT), len(page), 'bytes')


if __name__ == '__main__':
    args = sys.argv[1:]
    if '--out' in args:
        # private build for a parallel builder: v2/out/<label>/index.html, CSS compiled into clone/assets/screens-<label>.css
        label = args[args.index('--out') + 1]
        copy_assets()
        compile_tailwind(os.path.join(ASSETS, 'screens-%s.css' % label))
        build_html(os.path.join(V2, 'out', label), 'screens-%s.css' % label)
    else:
        if '--html-only' not in args:
            build_css()
        build_html()
