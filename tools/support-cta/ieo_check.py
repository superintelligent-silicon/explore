"""In Each Other launch checks. usage: ieo_check.py URL OUTDIR"""
import sys, json, os
from playwright.sync_api import sync_playwright
U, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
HOOK = """(()=>{window.__ramps=[];const P=AudioParam.prototype,o=P.linearRampToValueAtTime;P.linearRampToValueAtTime=function(v,t){window.__ramps.push(+v.toFixed(3));return o.call(this,v,t)};
const A=window.Audio;window.Audio=function(...a){const x=new A(...a);window.__na=x;return x};window.Audio.prototype=A.prototype;})();"""
SHEET = """(()=>{const d=document.querySelector('dialog.sis');if(!d||!d.open)return {open:false};const c=d.querySelector('.sis-card');
 return {open:true,inner:c.scrollHeight-c.clientHeight,top:Math.round(c.getBoundingClientRect().top),bg:getComputedStyle(c).backgroundColor,focus:document.activeElement&&document.activeElement.id}})()"""
def scr(p): return p.evaluate("[document.documentElement.scrollHeight-innerHeight, document.documentElement.scrollWidth-innerWidth]")
res = {}
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--autoplay-policy=no-user-gesture-required"])
    for w, h in [(390, 664), (1440, 900)]:
        for scheme in ["light", "dark"]:
            tag = f"{w}-{scheme}"; m = w < 700
            c = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=2 if m else 1, is_mobile=m, has_touch=m, color_scheme=scheme)
            c.add_init_script(HOOK); c.grant_permissions(["clipboard-read", "clipboard-write"])
            c.route("**/api/subscribe", lambda r: r.fulfill(status=200, content_type="application/json", body='{"ok":true,"confirm":true}'))
            p = c.new_page(); errs = []; mp3 = []
            p.on("pageerror", lambda e: errs.append(str(e))); p.on("console", lambda x: errs.append(x.text) if x.type == "error" else None)
            p.on("response", lambda r: mp3.append([r.status, r.headers.get("content-type")]) if r.url.endswith(".mp3") else None)
            o = res[tag] = {"errors": errs}
            p.goto(U, wait_until="networkidle"); p.wait_for_timeout(1200)
            o["scrollSplash"] = scr(p); p.screenshot(path=f"{OUT}splash-{tag}.png")
            o["splash"] = p.evaluate("[document.querySelector('.verse .by').textContent, [...document.querySelectorAll('.verse .homes a')].map(a=>[a.textContent,a.getAttribute('href'),Math.round(a.getBoundingClientRect().height)])]")
            p.click("[data-act=begin]"); p.wait_for_timeout(1500)
            # the whole prayer sheet: Listen with ducking
            p.click("#wholeBtn"); p.wait_for_timeout(400)
            p.evaluate("__ramps=[]"); p.click("#listenBtn"); p.wait_for_timeout(4000)
            o["listen"] = p.evaluate("[document.getElementById('listenBtn').textContent, !__na.paused, +__na.currentTime.toFixed(2), +__na.duration.toFixed(2), __na.src.split('/').pop()]")
            o["rampsListen"] = p.evaluate("__ramps")
            p.screenshot(path=f"{OUT}whole-listening-{tag}.png")
            o["wholeFoot"] = p.evaluate("[document.querySelector('.card-foot .by').textContent, [...document.querySelectorAll('.sheet-home a,.sheet-home button')].map(a=>[a.textContent,a.getAttribute('href'),Math.round(a.getBoundingClientRect().bottom)<=innerHeight]), (()=>{const c=document.querySelector('#sheet .card');return c.scrollHeight-c.clientHeight})()]")
            p.evaluate("__ramps=[]"); p.click("#listenBtn"); p.wait_for_timeout(900)
            o["pause"] = p.evaluate("[document.getElementById('listenBtn').textContent, __na.paused, __ramps]")
            # tucked-away Support in the whole-prayer sheet
            p.click(".sheet-home [data-si-support]"); p.wait_for_timeout(800); o["sheetFromWhole"] = p.evaluate(SHEET)
            p.screenshot(path=f"{OUT}sheet-{tag}.png")
            p.click(".sis-cp"); p.wait_for_timeout(400)
            o["copy"] = p.evaluate("(async()=>[document.querySelector('.sis-cp').textContent,(await navigator.clipboard.readText()).length])()")
            try:
                with c.expect_page(timeout=5000) as np_: p.click("a.sis-tip >> nth=1")
                o["tip"] = np_.value.url[:45]; np_.value.close()
            except Exception as e: o["tip"] = "FAIL"
            p.keyboard.press("Escape"); p.wait_for_timeout(500); o["sisClosed"] = p.evaluate("!document.querySelector('dialog.sis').open")
            p.evaluate("document.getElementById('closeSheet').click()"); p.wait_for_timeout(600)
            # the last movement
            for _ in range(12):
                if p.evaluate("document.getElementById('count').textContent.trim().startsWith('09')"): break
                p.evaluate("document.getElementById('next').click()"); p.wait_for_timeout(500)
            p.wait_for_timeout(1500)
            o["count"] = p.evaluate("document.getElementById('count').textContent")
            o["scrollEnd"] = scr(p); p.screenshot(path=f"{OUT}end-{tag}.png")
            o["endFit"] = p.evaluate("""(()=>{const v=document.getElementById('verse'),e=v.querySelector('.sup-end');if(!e)return null;const r=e.getBoundingClientRect(),f=document.querySelector('footer').getBoundingClientRect();
              return {supBottom:Math.round(r.bottom),footerTop:Math.round(f.top),inner:v.scrollHeight-v.clientHeight,main:(()=>{const m=document.querySelector('main');return m.scrollHeight-m.clientHeight})(),h:[...e.querySelectorAll('button')].map(b=>Math.round(b.getBoundingClientRect().height))}})()""")
            p.click(".sup-end [data-si-focus=email]"); p.wait_for_timeout(800); o["sheetFromEnd"] = p.evaluate(SHEET)
            p.screenshot(path=f"{OUT}sheet-end-{tag}.png")
            p.keyboard.press("Escape"); p.wait_for_timeout(500)
            o["countAfter"] = p.evaluate("document.getElementById('count').textContent")
            o["mp3"] = mp3; o["finalScroll"] = scr(p)
            c.close()
    # back links navigate
    c = b.new_context(viewport={"width": 390, "height": 664}, is_mobile=True, has_touch=True); p = c.new_page(); nav = []
    for sel in [".verse .homes a[href='/articles/']", ".verse .homes a[href='/']"]:
        p.goto(U, wait_until="networkidle"); p.wait_for_timeout(600); p.click(sel); p.wait_for_load_state("load"); nav.append(p.url)
    res["backLinks"] = nav; c.close(); b.close()
json.dump(res, open(OUT + "results.json", "w"), indent=1)
for k, v in res.items(): print(k, json.dumps(v)[:1400])
