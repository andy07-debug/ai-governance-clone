import sys, json, os
from playwright.sync_api import sync_playwright
JS = r'''()=>{const pick=(re)=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){if(n.parentElement.closest('template'))continue;if(re.test(n.textContent)){const r=document.createRange();r.selectNodeContents(n);const b=r.getBoundingClientRect();if(!b.width)continue;const cs=getComputedStyle(n.parentElement);return {x:b.x,w:Math.round(b.width*100)/100,ff:cs.fontFamily}}}};
return {a:pick(/Get Instant Insights/),b:pick(/Select a project from the list/),c:pick(/Welcome to AI Governance/),d:pick(/Monitor, protect, and manage/),e:pick(/^Projects$/),f:pick(/Cost, request, assistant/),
fonts:[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family+' '+f.weight)}}'''
url = sys.argv[1]
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1920, 'height': 992})
    pg.goto(url); pg.wait_for_timeout(1500)
    print(json.dumps(pg.evaluate(JS), indent=0))
    b.close()
