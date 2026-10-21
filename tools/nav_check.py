#!/usr/bin/env python3
"""Verify the si-nav preview. usage: nav_check.py OUTDIR [explore_base] [org_base]"""
import sys, json, time, os, re, functools
print = functools.partial(print, flush=True)
from playwright.sync_api import sync_playwright
OUT = sys.argv[1]; EB = sys.argv[2] if len(sys.argv) > 2 else "https://exploresuperintelligence.online/preview/nav/"
OB = sys.argv[3] if len(sys.argv) > 3 else "https://superintelligentsilicon.com/preview/nav/"
os.makedirs(OUT, exist_ok=True)
PAGES = [EB, EB + "articles/", EB + "about/", EB + "research/", EB + "articles/in-each-other/", EB + "articles/defrost-mode/", EB + "articles/final-merge/", OB, OB + "contact/"]
INIT = r"""
(()=>{ if(window.__snInit) return; window.__snInit=1;
 window.addEventListener('pageshow',e=>{ window.__persisted=e.persisted; try{ window.__snlog({u:location.href,ev:'pageshow',p:e.persisted,t:Date.now()}) }catch(x){} });
 window.addEventListener('pagereveal',e=>{ try{ window.__snlog({u:location.href,ev:'reveal',vt:!!e.viewTransition,t:Date.now()}) }catch(x){} });
 const mo=new MutationObserver(()=>{ if(document.documentElement.classList.contains('si-nav-arrive')&&!window.__arr){ window.__arr=1; try{ window.__snlog({u:location.href,ev:'arrive',t:Date.now()}) }catch(x){} }
   const v=document.documentElement.getAttribute('data-si-nav')||'';
   if(v!==window.__lastV){ window.__lastV=v; try{ window.__snlog({u:location.href,ev:'nav',v:v,t:Date.now()}) }catch(x){}
     if(v==='on') setTimeout(()=>{ const o=document.getElementById('si-nav'); if(!o) return; const cs=getComputedStyle(o);
       try{ window.__snlog({u:location.href,ev:'ovstyle',t:Date.now(),on:o.classList.contains('on'),op:+cs.opacity,vis:cs.visibility,th:o.dataset.t,bg:cs.backgroundColor,bar:getComputedStyle(o.querySelector('.sn-bar')).display,mk:+getComputedStyle(o.querySelector('.sn-mk')).opacity}) }catch(x){} },650); } });
 mo.observe(document,{subtree:true,attributes:true,attributeFilter:['data-si-nav','class']});
})();"""
R = {}
CDP = {}
def ctx(b, w, h, th, rm=None, nonav=False, video=None):
    kw = dict(viewport={"width": w, "height": h}, color_scheme=th, device_scale_factor=1)
    if rm: kw["reduced_motion"] = rm
    if video: kw["record_video_dir"] = video; kw["record_video_size"] = {"width": w, "height": h}
    if w < 500: kw.update(is_mobile=True, has_touch=True, device_scale_factor=2)
    c = b.new_context(**kw)
    log = []
    c.expose_binding("__snlog", lambda src, x: log.append(x))
    if nonav: c.add_init_script("try{Object.defineProperty(window,'navigation',{value:undefined,configurable:true})}catch(e){} try{delete Window.prototype.onpagereveal}catch(e){}")
    c.add_init_script(INIT)
    c.add_init_script("try{localStorage.setItem('si-theme','%s');localStorage.setItem('ieo-theme','%s')}catch(e){}" % (th, th))
    return c, log
DELAY = {"ms": 0}   # non-zero = hold document requests until release()
HELD = []
def router(route):
    r = route.request
    if r.resource_type == "document" and re.search(r"github\.com|stripe\.com", r.url):
        return route.abort()
    if r.resource_type == "document" and DELAY["ms"]:
        HELD.append(route); return
    route.continue_()
def release():
    while HELD:
        try: HELD.pop(0).continue_()
        except Exception: pass
def EV(pg, js):
    for i in range(6):
        try: return pg.evaluate(js)
        except Exception as e:
            if "context was destroyed" not in str(e) and "navigat" not in str(e): raise
            pg.wait_for_timeout(500)
            try: pg.wait_for_load_state("load", timeout=10000)
            except Exception: pass
    return "ERR"
def overlay(pg):
    return EV(pg, """()=>{const o=document.getElementById('si-nav');if(!o)return null;const cs=getComputedStyle(o);
      return {on:o.classList.contains('on'),op:+cs.opacity,vis:cs.visibility,t:o.dataset.t,bg:cs.backgroundColor,bar:getComputedStyle(o.querySelector('.sn-bar')).display}}""")
def scroll(pg):
    return EV(pg, "()=>{const d=document.scrollingElement;return [d.scrollWidth-d.clientWidth,d.scrollHeight-d.clientHeight]}")
def enter_home(pg):
    try: pg.get_by_role("button", name="Enter", exact=True).click(timeout=1500); pg.wait_for_timeout(500)
    except Exception: pass
def shot(c, pg, path):
    import base64
    d = CDP[id(pg)].send("Page.captureScreenshot", {"format": "png"}); open(path, "wb").write(base64.b64decode(d["data"]))
def ovlog(log, t0):
    x = [y for y in log if y.get("ev") == "ovstyle" and y["t"] >= t0]
    return x[-1] if x else None
def evs(log, t0, ev):
    return [y for y in log if y.get("ev") == ev and y["t"] >= t0]
def shown_between(log, t0, t1):
    return [x for x in log if x.get("ev") == "nav" and x.get("v") == "on" and t0 <= x["t"] <= t1]

with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--autoplay-policy=no-user-gesture-required"])
    for (w, h) in [(390, 664), (1440, 900)]:
        for th in ["light", "dark"]:
            k = f"{w}-{th}"; res = R[k] = {}
            c, log = ctx(b, w, h, th); pg = c.new_page(); CDP[id(pg)] = c.new_cdp_session(pg); errs = []
            pg.on("console", lambda m: m.type == "error" and "MutationObserver" not in m.text and errs.append(m.text)); pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.route("**/*", router)
            res["pages"] = {}
            for u in PAGES:
                print("load", k, u); pg.goto(u, wait_until="load", timeout=45000); pg.wait_for_timeout(400)
                res["pages"][u] = {"ov": overlay(pg), "scroll": scroll(pg), "inc": pg.evaluate("!!window.__siNav")}
            DELAY["ms"] = 0
            pg.goto(EB, wait_until="load"); enter_home(pg)
            t0 = int(time.time() * 1000)
            pg.click('a[href="/preview/nav/articles/"] >> visible=true'); pg.wait_for_url(EB + "articles/"); pg.wait_for_load_state("load")
            t1 = int(time.time() * 1000); pg.wait_for_timeout(300)
            print("step", k, 'res["fast"]'); res["fast"] = {"ms": t1 - t0, "shown": len(shown_between(log, t0, t1 + 300)), "after": overlay(pg)}
            DELAY["ms"] = 1
            t0 = int(time.time() * 1000)
            pg.click('a[href="/preview/nav/articles/in-each-other/"]', no_wait_after=True)
            pg.wait_for_timeout(700)
            shot(c, pg, f"{OUT}/slow-mid-{k}.png"); pg.wait_for_timeout(200); mid = ovlog(log, t0); held = len(HELD)
            DELAY["ms"] = 0; release()
            pg.wait_for_url(EB + "articles/in-each-other/"); pg.wait_for_load_state("load"); t1 = int(time.time() * 1000)
            pg.wait_for_timeout(500)
            print("step", k, 'res["slow"]'); res["slow"] = {"held": held, "mid": mid, "shownLog": len(shown_between(log, t0, t1)), "after": overlay(pg), "arrive": len(evs(log, t0, "arrive")), "reveal": evs(log, t0, "reveal")[-1:]}
            pg.screenshot(path=f"{OUT}/arrived-{k}.png")
            DELAY["ms"] = 0
            t0 = int(time.time() * 1000)
            try: pg.click("text=In silence", timeout=3000)
            except Exception: pass
            pg.wait_for_timeout(800)
            for i in range(3):
                pg.keyboard.press("ArrowRight"); pg.wait_for_timeout(450)
            aud = None
            try:
                pg.click('#wholeBtn', timeout=2000); pg.wait_for_timeout(500)
                pg.click('#sheet button:has-text("Listen")', timeout=2000); pg.wait_for_timeout(1500)
                aud = pg.evaluate("(()=>{const b=[...document.querySelectorAll('#sheet button')].map(x=>x.textContent.trim());return b})()")
            except Exception as e:
                aud = "err " + str(e)[:80]
            t1 = int(time.time() * 1000)
            print("step", k, 'res["bookInternal"]'); res["bookInternal"] = {"shown": len(shown_between(log, t0, t1)), "url": pg.url, "audio": aud, "count": pg.evaluate("(document.querySelector('.count')||{}).textContent"), "ov": overlay(pg)}
            def trav(js):
                DELAY["ms"] = 1; t0 = int(time.time() * 1000); pg.evaluate(js); pg.wait_for_timeout(900)
                m = ovlog(log, t0)
                n = len(HELD); DELAY["ms"] = 0; release(); pg.wait_for_load_state("load"); pg.wait_for_timeout(300)
                return m, n
            bm, bn = trav("history.back()")
            print("step", k, 'res["back"] ='); res["back"] = {"midOv": bm, "held": bn, "url": pg.url, "persisted": EV(pg, "window.__persisted"), "ov": overlay(pg), "attr": EV(pg, "document.documentElement.getAttribute('data-si-nav')"), "scroll": scroll(pg)}
            pg.wait_for_timeout(1500); res["back"]["ov2"] = overlay(pg)
            fm, fn_ = trav("history.forward()")
            print("step", k, 'res["fwd"]'); res["fwd"] = {"midOv": fm, "held": fn_, "url": pg.url, "persisted": EV(pg, "window.__persisted"), "ov": overlay(pg)}
            trav("history.back()"); pg.wait_for_timeout(1500)
            res["back2"] = {"url": pg.url, "persisted": EV(pg, "window.__persisted"), "ov": overlay(pg)}
            pg.goto(EB + "about/", wait_until="load"); pg.wait_for_timeout(300); DELAY["ms"] = 1
            ign = {}
            def probe(name, fn):
                DELAY["ms"] = 0
                if not pg.url.endswith("/preview/nav/about/"): pg.goto(EB + "about/", wait_until="load"); pg.wait_for_timeout(300)
                DELAY["ms"] = 1
                t0 = int(time.time() * 1000)
                try: fn()
                except Exception as e: ign[name + "_err"] = str(e)[:80]
                pg.wait_for_timeout(500); ign[name] = len(shown_between(log, t0, int(time.time() * 1000)))
                for r_ in list(HELD):
                    HELD.remove(r_); r_.abort()
            probe("hash", lambda: pg.evaluate("(()=>{const a=document.createElement('a');a.href='#tip';a.textContent='x';document.body.appendChild(a);a.click();a.remove()})()"))
            probe("modifier", lambda: pg.evaluate("(()=>{const a=document.createElement('a');a.href='/preview/nav/articles/';document.body.appendChild(a);a.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true,ctrlKey:true,metaKey:true}));a.remove()})()"))
            probe("newtab", lambda: pg.evaluate("(()=>{const a=document.createElement('a');a.href='/preview/nav/research/';a.target='_blank';document.body.appendChild(a);a.click();a.remove()})()"))
            for pp in c.pages[1:]: pp.close()
            probe("download", lambda: pg.evaluate("(()=>{const a=document.createElement('a');a.href='/llms.txt';a.download='llms.txt';document.body.appendChild(a);a.click();a.remove()})()"))
            probe("prevented", lambda: pg.evaluate("(()=>{const a=document.createElement('a');a.href='/preview/nav/research/';a.addEventListener('click',e=>e.preventDefault());document.body.appendChild(a);a.click();a.remove()})()"))
            probe("external", lambda: pg.evaluate("(()=>{const a=document.createElement('a');a.href='https://github.com/superintelligent-silicon';document.body.appendChild(a);a.click();a.remove()})()"))
            probe("stripe", lambda: pg.evaluate("(()=>{const a=document.createElement('a');a.href='https://buy.stripe.com/test';document.body.appendChild(a);a.click();a.remove()})()"))
            print("step", k, 'res["ignored"]'); res["ignored"] = ign; res["ignoredUrl"] = pg.url; DELAY["ms"] = 0
            DELAY["ms"] = 0; pg.goto(OB, wait_until="load"); pg.wait_for_timeout(400); DELAY["ms"] = 1
            pg.evaluate("(()=>{const a=[...document.querySelectorAll('a[href=\"https://exploresuperintelligence.online/preview/nav/articles/\"]')][0];a.click()})()")
            t0 = int(time.time() * 1000); pg.wait_for_timeout(700); shot(c, pg, f"{OUT}/org-slow-mid-{k}.png"); pg.wait_for_timeout(200); midorg = ovlog(log, t0); DELAY["ms"] = 0; release()
            pg.wait_for_url(EB + "articles/"); pg.wait_for_load_state("load"); pg.wait_for_timeout(500)
            print("step", k, 'res["cross"]'); res["cross"] = {"mid": midorg, "after": overlay(pg), "url": pg.url, "arrive": len(evs(log, t0, "arrive")), "reveal": evs(log, t0, "reveal")[-1:]}
            DELAY["ms"] = 0
            res["errors"] = errs
            c.close()
            json.dump(R, open(f"{OUT}/results.json", "w"), indent=1)
    for th in ["light", "dark"]:
        c, log = ctx(b, 390, 664, th); pg = c.new_page(); errs = []
        pg.on("console", lambda m: m.type == "error" and "MutationObserver" not in m.text and errs.append(m.text)); pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(EB + "articles/", wait_until="load"); pg.wait_for_timeout(300)
        pg.evaluate("window.SINav.start(); window.SINav.show()"); pg.wait_for_timeout(400)
        forced = overlay(pg)
        pg.goto(EB + "about/", wait_until="load"); pg.wait_for_timeout(300)
        pg.go_back(wait_until="load"); pg.wait_for_timeout(800)
        R["bfcache-" + th] = {"forcedBefore": forced, "persisted": EV(pg, "window.__persisted"), "after": overlay(pg), "attr": EV(pg, "document.documentElement.getAttribute('data-si-nav')"), "errors": errs}
        c.close()
    for name, kw in [("reduced", dict(rm="reduce")), ("fallback", dict(nonav=True))]:
        c, log = ctx(b, 390, 664, "light", **kw); pg = c.new_page(); CDP[id(pg)] = c.new_cdp_session(pg); errs = []
        pg.on("console", lambda m: m.type == "error" and "MutationObserver" not in m.text and errs.append(m.text)); pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.route("**/*", router)
        pg.goto(EB + "articles/", wait_until="load"); pg.wait_for_timeout(300)
        DELAY["ms"] = 1
        t0 = int(time.time() * 1000); pg.click('a[href="/preview/nav/articles/defrost-mode/"]', no_wait_after=True); pg.wait_for_timeout(700)
        shot(c, pg, f"{OUT}/{name}-mid.png"); pg.wait_for_timeout(200); mid = ovlog(log, t0); DELAY["ms"] = 0; release()
        pg.wait_for_url(EB + "articles/defrost-mode/"); pg.wait_for_load_state("load")
        arr = pg.evaluate("document.documentElement.className"); pg.wait_for_timeout(600)
        DELAY["ms"] = 0
        R[name] = {"mid": mid, "arriveCls": arr, "after": overlay(pg), "hasNavApi": pg.evaluate("!!window.navigation"), "errors": errs}
        c.close()
    b.close()
json.dump(R, open(f"{OUT}/results.json", "w"), indent=1)
print("done")
