from playwright.sync_api import sync_playwright
import difflib
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936})
    pg.goto('file://'+ROOT+'/clone/index.html#04-policies'); pg.wait_for_timeout(300)
    a=pg.evaluate("document.getElementById('mount').innerHTML")
    pg.click('button[title="Toggle Fullscreen"], [aria-label="Toggle Fullscreen"]'); pg.wait_for_timeout(300)
    c=pg.evaluate("document.getElementById('mount').innerHTML")
    sm=difflib.SequenceMatcher(None,a,c,autojunk=False)
    for op in sm.get_opcodes():
        if op[0]!='equal': print(op[0], repr(a[op[1]-80:op[2]+40]), '=>', repr(c[op[3]-80:op[4]+40]))
    pg.screenshot(path='fs.png')
