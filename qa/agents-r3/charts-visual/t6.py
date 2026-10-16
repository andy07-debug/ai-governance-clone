from playwright.sync_api import sync_playwright
ROOT='/Users/kumaraniket/Desktop/AI Governance Clone'; URL='file://'+ROOT+'/clone/index.html'
errs=[]
S="()=>({st:__cloneState(), n:Object.keys(Chart.instances).length, cv:document.querySelectorAll('canvas[data-chart]').length, ok:[...document.querySelectorAll('canvas[data-chart]')].map(c=>!!Chart.getChart(c)&&c.width>0)})"
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':936}); pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: m.type=='error' and errs.append(m.text))
    pg.goto(URL+'#01-llm-analytics'); pg.wait_for_timeout(100)
    for v in ['00-home','01-llm-analytics','05d-traffic-statistics','05b-traffic-project-usage','01-llm-analytics','05b-traffic-project-usage']*3:
        pg.evaluate("v=>location.hash='#'+v", v); pg.wait_for_timeout(40)
    pg.wait_for_timeout(1300); print('rapid', pg.evaluate(S))
    for i in range(6): pg.go_back(); pg.wait_for_timeout(30)
    pg.wait_for_timeout(1300); print('back spam', pg.evaluate(S))
    pg.goto(URL+'#01-llm-analytics'); pg.wait_for_timeout(1300)
    pg.locator('.h-20 .p-dropdown').first.click(); pg.wait_for_timeout(900); print('07a over 01', pg.evaluate(S))
    pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    pg.locator('[title="Open sidebar"]').first.click(); pg.wait_for_timeout(900); print('07b over 01', pg.evaluate(S))
    pg.locator('[title="Click to close sidebar"]').first.click(); pg.wait_for_timeout(900); print('closed', pg.evaluate(S))
    # collapse/expand Cost trend section
    pg.get_by_text('Cost trend', exact=True).click(); pg.wait_for_timeout(900); print('collapsed', pg.evaluate(S))
    pg.set_viewport_size({'width':1280,'height':936}); pg.wait_for_timeout(300)
    pg.get_by_text('Cost trend', exact=True).click(); pg.wait_for_timeout(1300)
    print('expanded after resize', pg.evaluate("()=>{const c=document.querySelector('canvas[data-chart]');const r=c.getBoundingClientRect();return [r.width,r.height,c.width,c.height,c.parentElement.clientWidth]}"))
    pg.screenshot(path='collapse-resize.png')
    print('ERRS',errs); b.close()
