import sys, json
from playwright.sync_api import sync_playwright
BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8841/"
import os as _o
OUT = _o.environ.get("SI_OUT", "/workspace/explore-support-cta/shots/")
ONLY = sys.argv[2] if len(sys.argv) > 2 else ""
import os
PFX = os.environ.get("SI_PREFIX", "preview/support/")
SHOTS_TAG = os.environ.get("SI_TAG", "")
res = {}
PAGES = {("well-be-right-back", 390): (58, 59), ("napkins-are-the-backbone", 390): (62, 63), ("well-be-right-back", 1440): (40, 40), ("napkins-are-the-backbone", 1440): (43, 43)}
TAPS = {(390, "napkins-are-the-backbone"): (195, 315, 139, 359), (390, "well-be-right-back"): (195, 315, 139, 359)}
def ctx(br, w, h, scheme):
    mob = w < 700
    c = br.new_context(viewport={"width": w, "height": h}, device_scale_factor=2 if mob else 1, is_mobile=mob, has_touch=mob, color_scheme=scheme)
    c.add_init_script("try{localStorage.setItem('wb-peek','1');localStorage.removeItem('si-theme')}catch(e){}")
    c.grant_permissions(["clipboard-read", "clipboard-write"])
    c.route("**/api/subscribe", lambda r: r.fulfill(status=200, content_type="application/json", body='{"ok":true,"confirm":true}'))
    return c
def watch(pg, key):
    errs = []
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: errs.append(str(e)))
    res[key] = {"errors": errs}
    return res[key]
def scroll(pg):
    return pg.evaluate("[document.documentElement.scrollHeight - innerHeight, document.documentElement.scrollWidth - innerWidth]")
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
    for (w, h) in [(390, 664), (1440, 900)]:
        for scheme in ["light", "dark"]:
            tag = f"{w}-{scheme}"
            # books: End page, chapters row, TL;DR line, sheet
            for b in ["well-be-right-back", "napkins-are-the-backbone"]:
                if ONLY and ONLY not in b: continue
                c = ctx(br, w, h, scheme); pg = c.new_page(); r = watch(pg, f"{b}-{tag}")
                fin, card = PAGES[(b, w)]
                pg.goto(BASE + PFX + f"articles/{b}/#p{fin}", wait_until="load"); pg.wait_for_timeout(2600)
                pg.screenshot(path=f"{OUT}{b}-end-{tag}.png")
                if card != fin:
                    pg.keyboard.press("ArrowRight"); pg.wait_for_timeout(1800); pg.screenshot(path=f"{OUT}{b}-endcard-{tag}.png")
                r["scroll"] = scroll(pg)
                if (w, b) in TAPS:
                    bx, by, tx, ty = TAPS[(w, b)]
                    with c.expect_page(timeout=4000) as np_:
                        pg.mouse.click(tx, ty)
                    r["tipTap"] = np_.value.url[:40]; np_.value.close()
                    pg.mouse.click(bx, by); pg.wait_for_timeout(800)
                    r["cardTap"] = pg.evaluate("[document.querySelector('dialog.sis')&&document.querySelector('dialog.sis').open, document.activeElement.id]")
                    pg.keyboard.press("Escape"); pg.wait_for_timeout(500)
                pg.evaluate("SISupport.open({source:SI_SUPPORT_SRC,focus:'email'})"); pg.wait_for_timeout(700)
                pg.screenshot(path=f"{OUT}{b}-sheet-{tag}.png")
                pg.click(".sis-cp"); pg.wait_for_timeout(400)
                r["copy"] = pg.evaluate("(async()=>[document.querySelector('.sis-cp').textContent, document.querySelector('.sis-cpst').textContent, (await navigator.clipboard.readText()).length])()")
                pg.screenshot(path=f"{OUT}{b}-sheet-copied-{tag}.png")
                r["sheet"] = pg.evaluate("""(()=>{const c=document.querySelector('.sis-card').getBoundingClientRect();const d=document.querySelector('.sis-card');
                  return {top:Math.round(c.top),bottom:Math.round(c.bottom),h:Math.round(c.height),inner:d.scrollHeight-d.clientHeight,focus:document.activeElement&&document.activeElement.id,
                  small:[...document.querySelectorAll('.sis-card button,.sis-card a,.sis-card input')].filter(e=>{const r=e.getBoundingClientRect();return r.height<44}).map(e=>e.className)}})()""")
                pg.fill("#sis-em", "reader@example.com"); pg.keyboard.press("ArrowLeft"); pg.keyboard.press("ArrowRight")
                pg.click(".sis-btn"); pg.wait_for_timeout(2300)
                r["status"] = pg.inner_text(".sis-st")
                pg.screenshot(path=f"{OUT}{b}-sheet-sent-{tag}.png")
                pg.keyboard.press("Escape"); pg.wait_for_timeout(500)
                r["closed"] = pg.evaluate("!document.querySelector('dialog.sis').open")
                pg.click("#chap"); pg.wait_for_timeout(900); pg.screenshot(path=f"{OUT}{b}-chapters-{tag}.png")
                r["chOut"] = pg.evaluate("[...document.querySelectorAll('.ch-out a,.ch-out button')].map(a=>{const q=a.getBoundingClientRect();return [a.textContent,Math.round(q.height),q.bottom<=innerHeight]})")
                pg.click(".ch-sup"); pg.wait_for_timeout(700); r["chOpens"] = pg.evaluate("document.querySelector('dialog.sis').open"); pg.keyboard.press("Escape"); pg.wait_for_timeout(500)
                pg.keyboard.press("Escape"); pg.wait_for_timeout(400)
                pg.evaluate("document.querySelector('.tl-chip').click()"); pg.wait_for_timeout(1600)
                pg.screenshot(path=f"{OUT}{b}-tldr-{tag}.png")
                r["tldrFits"] = pg.evaluate("(()=>{const i=document.querySelector('.tl-in');const b=document.querySelector('.tl-sup-b').getBoundingClientRect();return [i.scrollHeight<=i.clientHeight+1, Math.round(b.height), b.bottom<=innerHeight]})()")
                pg.click(".tl-sup-b"); pg.wait_for_timeout(700)
                r["tldrSheet"] = pg.evaluate("[document.querySelector('dialog.sis').open, !document.querySelector('.tl-ov').hidden]")
                c.close()
            for (name, path) in [("articles", PFX + "articles/"), ("about", PFX + "about/"), ("home", PFX)]:
                if ONLY and ONLY != name: continue
                c = ctx(br, w, h, scheme); pg = c.new_page(); r = watch(pg, f"{name}-{tag}")
                pg.goto(BASE + path, wait_until="load"); pg.wait_for_timeout(1500)
                r["scroll"] = scroll(pg)
                pg.screenshot(path=f"{OUT}{name}-{tag}.png")
                if name != "home":
                    r["line"] = pg.evaluate("(()=>{const e=document.querySelector('.si-sup-line');if(!e)return null;const q=e.getBoundingClientRect();return [Math.round(q.top),Math.round(q.bottom),innerHeight,getComputedStyle(e).display]})()")
                pg.evaluate("document.querySelector('[data-open=sh-menu]').click()"); pg.wait_for_timeout(700)
                pg.locator("#sh-menu [data-si-support]").scroll_into_view_if_needed(); pg.wait_for_timeout(300)
                pg.screenshot(path=f"{OUT}{name}-menu-{tag}.png")
                pg.click("#sh-menu [data-si-support]"); pg.wait_for_timeout(800)
                r["menuOpens"] = pg.evaluate("[document.querySelector('dialog.sis').open, document.getElementById('sh-menu').open]")
                pg.screenshot(path=f"{OUT}{name}-sheet-{tag}.png")
                pg.click(".sis-cp"); pg.wait_for_timeout(400)
                r["copy"] = pg.evaluate("(async()=>[document.querySelector('.sis-cp').textContent, document.querySelector('.sis-cpst').textContent, (await navigator.clipboard.readText()).length])()")
                pg.screenshot(path=f"{OUT}{name}-sheet-copied-{tag}.png")
                r["sheetScroll"] = pg.evaluate("(()=>{const d=document.querySelector('.sis-card');return d.scrollHeight-d.clientHeight})()")
                c.close()
    br.close()
json.dump(res, open(OUT + "results.json", "w"), indent=1)
for k, v in res.items(): print(k, json.dumps(v)[:600])
