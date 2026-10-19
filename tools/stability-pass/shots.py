import sys
from playwright.sync_api import sync_playwright
base, tag = sys.argv[1], sys.argv[2]
paths = sys.argv[3].split(",") if len(sys.argv)>3 else ["articles/well-be-right-back/"]
VPS = [(375,667),(390,664),(390,844),(430,932),(844,390)]
OUT="/workspace/explore-articles/stability-pass/shots/"
CHK = """()=>{const out=[];document.querySelectorAll('button,a,[role=button]').forEach(b=>{const cs=getComputedStyle(b);if(cs.visibility=='hidden'||cs.display=='none'||!b.offsetParent&&cs.position!='fixed')return;let p=b,hid=false;while(p){const c=getComputedStyle(p);if(c.visibility=='hidden'||c.opacity=='0'||c.display=='none'){hid=true;break}p=p.parentElement}if(hid)return;const r=b.getBoundingClientRect();if(r.width<1||r.height<1)return;const off=r.left<0||r.top<0||r.right>innerWidth+0.5||r.bottom>innerHeight+0.5;out.push({id:b.id||b.className.toString().slice(0,24)||b.textContent.trim().slice(0,20),x:Math.round(r.left),y:Math.round(r.top),w:Math.round(r.width),h:Math.round(r.height),off})});return {ih:innerHeight,sh:document.documentElement.scrollHeight,list:out}}"""
import json
res={}
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--use-angle=swiftshader","--enable-unsafe-swiftshader","--ignore-gpu-blocklist"])
    for p in paths:
        for vw,vh in VPS:
            c = br.new_context(viewport={"width":vw,"height":vh}, device_scale_factor=3 if vw<500 else 2, is_mobile=True, has_touch=True, color_scheme="dark")
            pg = c.new_page(); pg.goto(base+p, wait_until="load"); pg.wait_for_timeout(2500)
            name=p.strip('/').split('/')[-1]
            pg.screenshot(path=f"{OUT}{tag}-{name}-cover-{vw}x{vh}.png")
            res[f"{name}-{vw}x{vh}"]=pg.evaluate(CHK)
            c.close()
    br.close()
for k,v in res.items():
    offs=[b for b in v['list'] if b['off'] or b['h']<40]
    print(k, 'ih',v['ih'],'sh',v['sh'], 'offscreen/small:', [(b['id'],b['y'],b['h'],b['off']) for b in offs])
