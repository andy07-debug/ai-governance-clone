import asyncio, json, pathlib
from playwright.async_api import async_playwright

URL = pathlib.Path('/Users/kumaraniket/Desktop/AI Governance Clone/qa/agents-r2/skeptic-r2/patched.html').as_uri()
OUT = pathlib.Path(__file__).parent

STATE = """() => ({
  hash: location.hash.slice(1),
  ovs: [...document.querySelectorAll('[data-overlay]')].map(n => n.className.slice(0,30)),
  aria: (document.querySelector('.h-20 .p-dropdown-trigger')||{getAttribute:()=>null}).getAttribute('aria-expanded'),
  crumb: (document.body.innerText.match(/Welcome to AI Governance|Real-time Event Stream|Policies Deck/)||[''])[0],
  modal: document.querySelectorAll('.animate-slideUp').length,
  hl: history.length,
  fsBox: document.querySelectorAll('.fixed.inset-0.z-20').length,
  bubble: document.querySelectorAll('.maximizeChatButton').length,
  toggle: document.querySelectorAll('[title="Toggle Fullscreen"]').length,
  side: (document.getElementById('sidebar')||{getAttribute:()=>null}).getAttribute('data-panel-size'),
})"""

async def st(p, label, res):
    await p.wait_for_timeout(700)
    s = await p.evaluate(STATE)
    res.append((label, s)); print(label, json.dumps(s))

async def click_text_h3(p, txt):
    await p.locator('h3', has_text=txt).first.click()

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        res = []
        async def fresh(h='00-home'):
            ctx = await b.new_context(viewport={'width':1920,'height':936})
            p = await ctx.new_page()
            await p.goto(URL + '#' + h); await p.wait_for_timeout(800)
            return p
        # A: dropdown pick AI Governance then Back
        print('--- A')
        p = await fresh()
        await click_text_h3(p, 'Live Events'); await st(p, 'A1 live', res)
        await p.locator('.h-20 .p-dropdown').first.click(); await st(p, 'A2 dd open', res)
        await p.locator('[data-overlay] li', has_text='AI Governance').first.click(); await st(p, 'A3 picked', res)
        await p.go_back(); await st(p, 'A4 back', res)
        await p.go_back(); await st(p, 'A5 back2', res)
        # A2: on home
        print('--- A2')
        p = await fresh()
        await p.locator('.h-20 .p-dropdown').first.click(); await st(p, 'A2-1 open', res)
        await p.locator('[data-overlay] li', has_text='AI Governance').first.click(); await st(p, 'A2-2 picked', res)
        await p.go_back(); await st(p, 'A2-3 back', res)
        # B
        print('--- B')
        p = await fresh()
        await click_text_h3(p, 'Live Events'); await st(p, 'B1', res)
        await p.locator('.h-20 .p-dropdown').first.click(); await st(p, 'B2 open', res)
        await p.go_back(); await st(p, 'B3 back', res)
        await p.go_forward(); await st(p, 'B4 fwd', res)
        await p.keyboard.press('Escape'); await st(p, 'B5 esc', res)
        await p.go_back(); await st(p, 'B6 back', res)
        await p.go_forward(); await st(p, 'B7 fwd', res)
        # B drawer
        print('--- Bdrawer')
        p = await fresh()
        await click_text_h3(p, 'Policies'); await st(p, 'D1', res)
        await p.locator('.h-20 [title="Open sidebar"]').first.click(); await st(p, 'D2 drawer', res)
        await p.go_back(); await st(p, 'D3 back', res)
        await p.go_forward(); await st(p, 'D4 fwd', res)
        # C reload
        print('--- C')
        p = await fresh()
        await click_text_h3(p, 'Live Events')
        await p.locator('.h-20 .p-dropdown').first.click(); await st(p, 'C1 open', res)
        await p.reload(); await p.wait_for_timeout(800); await st(p, 'C2 reload', res)
        await p.keyboard.press('Escape'); await st(p, 'C3 esc', res)
        # F modal
        print('--- F')
        p = await fresh()
        await click_text_h3(p, 'Policies'); await st(p, 'F1', res)
        await p.locator('button', has_text='New Policy').first.click(); await st(p, 'F2 modal', res)
        await p.keyboard.press('Escape'); await st(p, 'F3 esc', res)
        await p.go_back(); await st(p, 'F4 back', res)
        # F cancel
        p = await fresh()
        await click_text_h3(p, 'Policies')
        await p.locator('button', has_text='New Policy').first.click()
        await p.locator('.animate-slideUp button', has_text='Cancel').first.click(); await st(p, 'F5 cancel', res)
        await p.go_back(); await st(p, 'F6 back', res)
        # G 07c fullscreen
        print('--- G')
        p = await fresh()
        await click_text_h3(p, 'Live Events')
        await p.locator('[data-testid="headerProjectsButton"]').first.click(); await st(p, 'G1 07c normal', res)
        await p.screenshot(path=str(OUT/'p07c-normal.png'))
        await p.go_back(); await st(p, 'G2 back', res)
        await p.locator('[title="Toggle Fullscreen"]').first.click(); await st(p, 'G3 fs', res)
        await p.go_forward(); await st(p, 'G4 fwd 07c', res)
        await p.screenshot(path=str(OUT/'p07c-fs.png'))
        # G via click in fs? projects button in fs?
        p = await fresh()
        await click_text_h3(p, 'Live Events')
        await p.locator('[title="Toggle Fullscreen"]').first.click(); await p.wait_for_timeout(700)
        vis = await p.evaluate("""() => { const b=document.querySelector('[data-testid="headerProjectsButton"]'); if(!b) return null; const r=b.getBoundingClientRect(); const e=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2); return {r:[r.x,r.y,r.width,r.height], top: b.contains(e)}; }""")
        print('projects btn in fs', vis)
        # M unknown hash
        print('--- M')
        p = await fresh()
        await click_text_h3(p, 'Live Events')
        await p.evaluate("location.hash='nope'"); await st(p, 'M1', res)
        await p.evaluate("location.hash=''"); await st(p, 'M2', res)
        await p.reload(); await p.wait_for_timeout(800); await st(p, 'M3 reload', res)
        await b.close()

asyncio.run(main())
