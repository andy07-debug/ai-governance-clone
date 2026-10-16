import os
from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'
URL='file://'+ROOT+'/clone/index.html'
OUT=ROOT+'/qa/agents/skeptic-shell/'
h=lambda p:p.evaluate('location.hash')
with sync_playwright() as pw:
    b=pw.chromium.launch(); p=b.new_page(viewport={'width':1920,'height':936}); p.set_default_timeout(4000)
    # F1
    p.goto(URL+'#00-home'); p.wait_for_timeout(500)
    info=p.evaluate('''()=>[...document.querySelectorAll('.h-20 button')].map(b=>{const r=b.getBoundingClientRect();return [b.className.slice(0,60),b.title,b.textContent.trim().slice(0,30),Math.round(r.x+r.width/2),Math.round(r.y+r.height/2)]})''')
    for i in info: print('hdrbtn',i)
    btn=p.locator('.h-20 button.bg-violet-50')
    print('F1 violet count',btn.count())
    if btn.count(): btn.first.click(); p.wait_for_timeout(200); print('F1 after refresh click', h(p))
    p.goto(URL+'#07c-shell-projects'); p.wait_for_timeout(300)
    if p.locator('.h-20 button.bg-violet-50').count(): p.locator('.h-20 button.bg-violet-50').first.click(); p.wait_for_timeout(200); print('F1 from 07c', h(p))
    # F2
    p.goto('about:blank'); p.goto(URL+'#00-home'); p.wait_for_timeout(300)
    p.locator('[data-testid="headerProjectsButton"]').click(); p.wait_for_timeout(200); print('F2 at',h(p), 'histlen', p.evaluate('history.length'))
    print('F2 trigger text', p.locator('.h-20 .p-dropdown').inner_text())
    p.locator('.h-20 .p-dropdown').click(); p.wait_for_timeout(200); print('F2 dropdown',h(p))
    print('F3 trigger text in 07a', p.locator('.h-20 .p-dropdown').inner_text(), 'Welcome visible', p.get_by_text('Welcome to AI Governance').count())
    p.screenshot(path=OUT+'f3.png')
    p.locator('.p-dropdown-panel li', has_text='AI Governance').first.click(); p.wait_for_timeout(200); print('F2 after pick AI Gov', h(p))
    # any way home from 07c? try right-panel breadcrumb home
    print('F2 home crumbs in 07c', p.locator('span.p-1.text-indigo-600, button[title="Back to home"]').count())
    # F6
    p.go_back(); p.wait_for_timeout(300); print('F6 after browser back', p.url[:60])
    # F4
    p.goto(URL+'#00-home'); p.wait_for_timeout(2500)
    ta=p.locator('textarea').first; ta.fill('Show me firewall stats')
    p.locator('.h-20 .p-dropdown').click(); p.wait_for_timeout(120)
    p.screenshot(path=OUT+'f4.png')
    print('F4 textarea in 07a', repr(p.locator('textarea').first.input_value()))
    p.keyboard.press('Escape'); p.wait_for_timeout(200)
    print('F4 after esc', h(p), repr(p.locator('textarea').first.input_value()))
    # F5
    p.goto(URL+'#07a-shell-mode-dropdown'); p.wait_for_timeout(400)
    p.locator('[title="Toggle Fullscreen"]').click(); p.wait_for_timeout(200)
    print('F5', h(p), 'panel', p.locator('.p-dropdown-panel').count(), 'visible', p.locator('.p-dropdown-panel').first.is_visible() if p.locator('.p-dropdown-panel').count() else None, 'fixed', p.locator('.fixed.inset-0.z-20').count())
    p.screenshot(path=OUT+'f5.png')
    # F7
    p.goto(URL+'#07a-shell-mode-dropdown'); p.wait_for_timeout(400)
    p.get_by_placeholder('Search mode...').fill('admin'); p.wait_for_timeout(200)
    print('F7', h(p), 'visible items', p.evaluate("[...document.querySelectorAll('.p-dropdown-item')].filter(e=>e.offsetParent).length"))
    # F8
    p.goto(URL+'#00-home'); p.wait_for_timeout(400)
    w0=p.evaluate("document.querySelector('[data-panel]').getBoundingClientRect().width")
    hd=p.locator('[data-resize-handle]').first.bounding_box(); print('F8 handle', hd)
    p.mouse.move(hd['x']+hd['width']/2, 500); p.mouse.down(); p.mouse.move(hd['x']-164,500,steps=10); p.mouse.up()
    print('F8 width', w0, p.evaluate("document.querySelector('[data-panel]').getBoundingClientRect().width"))
    # F9
    p.goto(URL+'#07c-shell-projects'); p.wait_for_timeout(400)
    cb=p.locator('.p-checkbox').first
    print('F9 before', p.evaluate("(()=>{const c=document.querySelector('.p-checkbox');return [c.className,c.querySelector('.p-checkbox-box').className,c.querySelector('input').checked,c.querySelector('.p-checkbox-box').innerHTML.length]})()"))
    cb.click(); p.wait_for_timeout(200)
    print('F9 after', h(p), p.evaluate("(()=>{const c=document.querySelector('.p-checkbox');return [c.className,c.querySelector('.p-checkbox-box').className,c.querySelector('input').checked,c.querySelector('.p-checkbox-box').innerHTML.length]})()"))
    b.close()
