from playwright.sync_api import sync_playwright
URL='file:///Users/kumaraniket/Desktop/AI Governance Clone/clone/index.html'
with sync_playwright() as pw:
    br=pw.chromium.launch(); pg=br.new_page(viewport={'width':1920,'height':936})
    for v in ['05b-traffic-project-usage','05d-traffic-statistics']:
        pg.goto('about:blank'); pg.goto(URL+'#'+v); pg.wait_for_timeout(300)
        print(pg.evaluate("""()=>{const b=[...document.querySelectorAll('button')].find(b=>b.textContent.trim()==='more');let p=b.closest('tr')||b.parentElement.parentElement.parentElement;return p.outerHTML.replace(/<svg[\\s\\S]*?<\\/svg>/g,'<svg/>').slice(0,3000)}"""))
        L=pg.evaluate("""()=>{const bs=[...document.querySelectorAll('[data-panel]:last-of-type button')].filter(b=>b.textContent.trim()==='more');
          return bs.map(b=>{const cell=b.closest('td')||b.parentElement; const cl=cell.querySelectorAll('.line-clamp-2'); return {cellClamps:cl.length, prevSibClamp: !!(b.previousElementSibling&&b.previousElementSibling.classList.contains('line-clamp-2'))}})}""")
        print(v, L[:20])
        # click each more: check that the clamp unclamped is in the same cell
        res=[]
        for i in range(len(L)):
            r=pg.evaluate("""(i)=>{const bs=[...document.querySelectorAll('[data-panel]:last-of-type button')].filter(b=>/^(more|less)$/.test(b.textContent.trim()));const b=bs[i];
               const before=[...document.querySelectorAll('.line-clamp-2')]; b.click(); const after=new Set(document.querySelectorAll('.line-clamp-2'));
               const changed=before.filter(e=>!after.has(e)); const cell=b.closest('td')||b.parentElement;
               const ok=changed.length===1&&cell.contains(changed[0]); const t1=b.textContent; b.click(); const t2=b.textContent; b.click(); const t3=b.textContent; b.click();
               return {i, changed:changed.length, sameCell:ok, overflowBefore: changed[0]?null:null, txt:[t1,t2,t3,b.textContent], changedTxt: changed[0]?changed[0].textContent.slice(0,40):null, cellTxt: cell.textContent.slice(0,40)}}""", i)
            res.append(r)
        for r in res:
            if not r['sameCell'] or r['txt']!=['less','more','less','more']: print('  BAD',r)
        print(v,'checked',len(res))
    br.close()
