#!/usr/bin/env python3
"""Render a v2 screen exactly like a demo frame and optionally build a side-by-side comparison.

usage: python3 v2/tools/shot.py <screen-id>[+<overlay-id>] [--ref demo/frames/f_000013.jpg]
                                [--scroll 600] [--js "document.querySelector('[data-tab=x:y]').click()"]
                                [--out v2/shots/name.png] [--crop x0,y0,x1,y1]
Viewport 1512x863 CSS px at device scale 2 => 3024x1726 PNG, same as the demo frames.
--scroll scrolls #screen (the right panel) by N CSS px; --crop crops BOTH images (frame px) for close-ups.
Writes <out> and, with --ref, <out>-cmp.png (left: replica, right: demo). Prints page errors.
"""
import argparse, os
from playwright.sync_api import sync_playwright
from PIL import Image

V2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(V2)
ap = argparse.ArgumentParser()
ap.add_argument('target')
ap.add_argument('--ref')
ap.add_argument('--scroll', type=int, default=0)
ap.add_argument('--js', action='append', default=[])
ap.add_argument('--out')
ap.add_argument('--crop')
ap.add_argument('--wait', type=int, default=900)
ap.add_argument('--html', help='index.html to render (default clone/index.html; builders use v2/out/<label>/index.html)')
a = ap.parse_args()
out = a.out or os.path.join(V2, 'shots', a.target.replace('+', '__') + ('-s%d' % a.scroll if a.scroll else '') + '.png')
os.makedirs(os.path.dirname(out), exist_ok=True)
errs = []
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={'width': 1512, 'height': 863}, device_scale_factor=2)
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: errs.append('console.' + m.type + ': ' + m.text) if m.type in ('error', 'warning') else None)
    pg.goto('file://' + os.path.abspath(a.html or os.path.join(ROOT, 'clone', 'index.html')) + '#' + a.target)
    pg.wait_for_timeout(300)
    for js in a.js:
        pg.evaluate(js)
        pg.wait_for_timeout(250)
    if a.scroll:
        pg.evaluate('(y)=>{const s=document.getElementById("screen"); s.scrollTop=y;}', a.scroll)
    pg.wait_for_timeout(a.wait)
    pg.screenshot(path=out)
    b.close()
img = Image.open(out).convert('RGB')
if a.crop:
    box = tuple(int(v) for v in a.crop.split(','))
    img = img.crop(box); img.save(out)
print('wrote', out, img.size)
if a.ref:
    ref = Image.open(os.path.join(ROOT, a.ref) if not os.path.isabs(a.ref) else a.ref).convert('RGB')
    if a.crop:
        ref = ref.crop(box)
    ref = ref.resize(img.size)
    cmp = Image.new('RGB', (img.width * 2 + 20, img.height), 'red')
    cmp.paste(img, (0, 0)); cmp.paste(ref, (img.width + 20, 0))
    if cmp.width > 3200:
        cmp = cmp.resize((cmp.width // 2, cmp.height // 2))
    p = out[:-4] + '-cmp.png'; cmp.save(p); print('wrote', p, '(left = replica, right = demo)')
print('page errors:', errs if errs else 'none')
