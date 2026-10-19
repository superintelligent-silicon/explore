"""Support sheet checks for Defrost Mode, The Final Merge, Immortal Tombstones, The Word Swap.
usage: books_check.py BASE OUT [preview|live] [filter]   (preview: /preview/<slug>/ copies; live: the canonical pages)"""
import sys, json, os
from playwright.sync_api import sync_playwright
BASE, OUT, MODE = sys.argv[1], sys.argv[2], sys.argv[3]
ONLY = sys.argv[4] if len(sys.argv) > 4 else ""
os.makedirs(OUT, exist_ok=True)
PATHS = {"final-merge": ("preview/final-merge/", "articles/final-merge/"), "immortal-tombstones": ("preview/immortal-tombstones/", "articles/immortal-tombstones/"),
         "defrost-mode": ("preview/defrost-mode-support/", "articles/defrost-mode/"), "word-swap": ("preview/word-swap/", "research/word-swap/")}
CANVAS = {"final-merge", "immortal-tombstones"}
res = {}
SHEET = """(async()=>{const d=document.querySelector('dialog.sis');if(!d||!d.open)return {open:false};const c=d.querySelector('.sis-card');
 const bg=getComputedStyle(c).backgroundColor;const tips=[...d.querySelectorAll('a.sis-tip')].map(a=>a.href);const lic=d.querySelector('.sis-lic a');
 return {open:true,inner:c.scrollHeight-c.clientHeight,top:Math.round(c.getBoundingClientRect().top),bottom:Math.round(c.getBoundingClientRect().bottom),bg,tips,lic:lic&&lic.getAttribute('href'),focus:document.activeElement&&document.activeElement.id}})()"""
def ctx(br, w, h, scheme):
    mob = w < 700
    c = br.new_context(viewport={"width": w, "height": h}, device_scale_factor=2 if mob else 1, is_mobile=mob, has_touch=mob, color_scheme=scheme)
    c.add_init_script("try{localStorage.setItem('wb-peek','1');localStorage.setItem('fm-peek','1');localStorage.setItem('it-peek','1');localStorage.removeItem('si-theme');localStorage.removeItem('ws-theme')}catch(e){}")
    c.grant_permissions(["clipboard-read", "clipboard-write"])
    c.route("**/api/subscribe", lambda r: r.fulfill(status=200, content_type="application/json", body='{"ok":true,"confirm":true}'))
    return c
def docscroll(pg): return pg.evaluate("[document.documentElement.scrollHeight-innerHeight, document.documentElement.scrollWidth-innerWidth]")
def sheet_round(pg, r, key, shot):
    pg.wait_for_timeout(800); st = pg.evaluate(SHEET); pg.screenshot(path=shot)
    if st.get("open"):
        pg.click(".sis-cp"); pg.wait_for_timeout(400)
        st["copy"] = pg.evaluate("(async()=>[document.querySelector('.sis-cp').textContent,(await navigator.clipboard.readText()).length])()")
        st["docscroll"] = docscroll(pg)
        pg.keyboard.press("Escape"); pg.wait_for_timeout(500); st["closed"] = pg.evaluate("!document.querySelector('dialog.sis').open")
    r[key] = st
def tip_click(pg, c, r):
    pg.wait_for_timeout(600)
    try:
        with c.expect_page(timeout=5000) as np_: pg.click("a.sis-tip >> nth=1")
        r["tipOpens"] = np_.value.url[:45]; np_.value.close()
    except Exception as e: r["tipOpens"] = "FAIL " + str(e)[:80]
    pg.keyboard.press("Escape"); pg.wait_for_timeout(400)
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
    for (w, h) in [(390, 664), (1440, 900)]:
        for scheme in ["light", "dark"]:
            tag = f"{w}-{scheme}"
            for slug, (pp, lp) in PATHS.items():
                if ONLY and ONLY not in slug: continue
                path = pp if MODE == "preview" else lp
                c = ctx(br, w, h, scheme); pg = c.new_page(); errs = []
                pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None); pg.on("pageerror", lambda e: errs.append(str(e)))
                r = res[f"{slug}-{tag}"] = {"errors": errs}
                pg.goto(BASE + path, wait_until="networkidle"); pg.wait_for_timeout(2500)
                r["scroll0"] = docscroll(pg); pg.screenshot(path=f"{OUT}{slug}-cover-{tag}.png")
                if slug in CANVAS:
                    fin = pg.evaluate("__RA.pages.findIndex(p=>(p.anims||[]).some(a=>a.kind==='finale'))")
                    pg.goto(BASE + path + f"#p{fin+1}"); pg.reload(wait_until="networkidle"); pg.wait_for_timeout(3000)
                    r["fin"] = [fin, pg.evaluate("__RA.idx"), pg.evaluate("__RA.pages.length")]
                    pg.screenshot(path=f"{OUT}{slug}-end-{tag}.png")
                    # where is the card: on The End page or the next one
                    where = pg.evaluate("[__RA.idx, (__RA.pages[__RA.idx].links||[]).map(l=>l.target)]")
                    if not any(str(t).startswith("support") for t in where[1]):
                        pg.keyboard.press("ArrowRight"); pg.wait_for_timeout(1800); pg.screenshot(path=f"{OUT}{slug}-endcard-{tag}.png")
                    r["cardPage"] = pg.evaluate("[__RA.idx, (__RA.pages[__RA.idx].links||[]).map(l=>l.target)]")
                    r["scrollEnd"] = docscroll(pg)
                    if MODE == "preview" or True:
                        L = pg.evaluate("(()=>{const s=document.getElementById('sheet').getBoundingClientRect();return (__RA.pages[__RA.idx].links||[]).filter(l=>/^(support|tip):/.test(l.target)).map(l=>({t:l.target,x:s.left+l.x+l.w/2,y:s.top+l.y+l.h/2,w:l.w,h:l.h}))})()")
                        r["cardLinks"] = [(l["t"], round(l["w"]), round(l["h"])) for l in L]
                        tip = [l for l in L if l["t"] == "tip:3"]; em = [l for l in L if l["t"] == "support:email"]
                        if tip:
                            try:
                                with c.expect_page(timeout=5000) as np_: pg.mouse.click(tip[0]["x"], tip[0]["y"])
                                r["cardTip"] = np_.value.url[:45]; np_.value.close()
                            except Exception as e: r["cardTip"] = "FAIL"
                            pg.wait_for_timeout(1300)
                        if em:
                            pg.mouse.click(em[0]["x"], em[0]["y"]); sheet_round(pg, r, "sheetCard", f"{OUT}{slug}-sheet-{tag}.png")
                    # tucked-away entry
                    if slug == "final-merge":
                        pg.click("#chap"); pg.wait_for_timeout(900); pg.screenshot(path=f"{OUT}{slug}-chapters-{tag}.png")
                        r["back"] = pg.evaluate("[...document.querySelectorAll('.ch-out a,.ch-out button')].map(a=>[a.textContent,a.getAttribute('href'),Math.round(a.getBoundingClientRect().height)])")
                        pg.click(".ch-sup"); sheet_round(pg, r, "sheetEntry", f"{OUT}{slug}-sheet-entry-{tag}.png")
                        pg.keyboard.press("Escape"); pg.wait_for_timeout(500)
                    else:
                        pg.evaluate("document.getElementById('readbtn').click()"); pg.wait_for_timeout(900); pg.screenshot(path=f"{OUT}{slug}-text-{tag}.png")
                        r["back"] = pg.evaluate("[...document.querySelectorAll('.cb-out a')].map(a=>[a.textContent,a.getAttribute('href'),Math.round(a.getBoundingClientRect().height)])")
                        pg.evaluate("document.querySelector('.it-sup').scrollIntoView({block:'center'})"); pg.wait_for_timeout(500); pg.screenshot(path=f"{OUT}{slug}-text-end-{tag}.png")
                        pg.click(".it-sup [data-si-support]"); sheet_round(pg, r, "sheetEntry", f"{OUT}{slug}-sheet-entry-{tag}.png")
                        r["readerStillOpen"] = pg.evaluate("document.getElementById('reader').classList.contains('on')||getComputedStyle(document.getElementById('reader')).display!=='none'")
                        pg.evaluate("document.querySelector('.closebar button').click()"); pg.wait_for_timeout(700)
                    # TL;DR line
                    pg.evaluate("document.querySelector('.tl-chip').click()"); pg.wait_for_timeout(1600); pg.screenshot(path=f"{OUT}{slug}-tldr-{tag}.png")
                    r["tldrFits"] = pg.evaluate("(()=>{const i=document.querySelector('.tl-in');const b=document.querySelector('.tl-sup-b');if(!b)return null;const q=b.getBoundingClientRect();return [i.scrollHeight<=i.clientHeight+1,Math.round(q.height),q.bottom<=innerHeight]})()")
                    if r["tldrFits"]:
                        pg.click(".tl-sup-b"); sheet_round(pg, r, "sheetTldr", f"{OUT}{slug}-sheet-tldr-{tag}.png")
                    # sheet tip link
                    pg.evaluate("SISupport.open({source:SI_SUPPORT_SRC})"); tip_click(pg, c, r)
                elif slug == "defrost-mode":
                    pg.evaluate("document.getElementById('menuBtn').click()"); pg.wait_for_timeout(800)
                    pg.evaluate("document.querySelector('#shBody .dm-sup').scrollIntoView({block:'nearest'})"); pg.wait_for_timeout(300)
                    pg.screenshot(path=f"{OUT}{slug}-chapters-{tag}.png")
                    r["back"] = pg.evaluate("[...document.querySelectorAll('#shBody a.menu-out')].map(a=>[a.textContent,a.getAttribute('href'),Math.round(a.getBoundingClientRect().height)])")
                    pg.evaluate("document.querySelector('#shBody .dm-sup').click()"); sheet_round(pg, r, "sheetEntry", f"{OUT}{slug}-sheet-entry-{tag}.png")
                    r["ownSheetClosed"] = pg.evaluate("!document.getElementById('sheet').classList.contains('on')")
                    pg.evaluate("document.querySelector('[data-go=buy]')?0:0"); pg.evaluate("document.getElementById('menuBtn').click()"); pg.wait_for_timeout(600)
                    pg.evaluate("document.querySelector('#shBody [data-go=buy]').click()"); pg.wait_for_timeout(1500)
                    r["scrollEnd"] = docscroll(pg)
                    r["endPage"] = pg.evaluate("(()=>{const p=document.querySelector('[data-id=buy]');return [p.scrollHeight-p.clientHeight]})()")
                    pg.screenshot(path=f"{OUT}{slug}-end-{tag}.png")
                    pg.evaluate("document.querySelector('[data-id=buy] .chips').scrollIntoView({block:'nearest'})"); pg.wait_for_timeout(400); pg.screenshot(path=f"{OUT}{slug}-end-chips-{tag}.png")
                    r["endChips"] = pg.evaluate("[...document.querySelectorAll('[data-id=buy] .chips .chip')].map(b=>[b.textContent.trim(),Math.round(b.getBoundingClientRect().height),Math.round(b.getBoundingClientRect().top)])")
                    if pg.query_selector('[data-id=buy] [data-dm-sup]'):
                        pg.click('[data-id=buy] [data-dm-sup]'); sheet_round(pg, r, "sheetCard", f"{OUT}{slug}-sheet-{tag}.png")
                    pg.evaluate("SISupport.open({source:SI_SUPPORT_SRC})") if pg.evaluate("!!window.SISupport") else None
                    if pg.evaluate("!!window.SISupport"): tip_click(pg, c, r)
                else:  # word-swap
                    pg.click("#btnToc"); pg.wait_for_timeout(800)
                    if pg.query_selector("#sheetB [data-ws-sup]"): pg.evaluate("document.querySelector('#sheetB [data-ws-sup]').scrollIntoView({block:'nearest'})")
                    pg.wait_for_timeout(300); pg.screenshot(path=f"{OUT}{slug}-contents-{tag}.png")
                    if pg.query_selector("#sheetB [data-ws-sup]"):
                        pg.click("#sheetB [data-ws-sup]"); sheet_round(pg, r, "sheetEntry", f"{OUT}{slug}-sheet-entry-{tag}.png")
                        r["ownSheetClosed"] = pg.evaluate("!document.getElementById('sheet').classList.contains('on')")
                    else: pg.keyboard.press("Escape"); pg.wait_for_timeout(400)
                    # last chapter
                    pg.evaluate("document.getElementById('btnToc').click()"); pg.wait_for_timeout(600)
                    pg.evaluate("[...document.querySelectorAll('[data-toc]')].pop().click()"); pg.wait_for_timeout(1500)
                    pg.evaluate("document.getElementById('supportTip2').scrollIntoView({block:'center'})"); pg.wait_for_timeout(500)
                    r["scrollEnd"] = docscroll(pg); pg.screenshot(path=f"{OUT}{slug}-end-{tag}.png")
                    r["back"] = pg.evaluate("[...document.querySelectorAll('#p2src p.note a')].slice(0,3).map(a=>[a.textContent,a.getAttribute('href')])")
                    if pg.query_selector("#supportTip2 [data-ws-sup]"):
                        pg.click("#supportTip2 [data-ws-sup]"); sheet_round(pg, r, "sheetCard", f"{OUT}{slug}-sheet-{tag}.png")
                    if pg.evaluate("!!window.SISupport"): pg.evaluate("SISupport.open({source:SI_SUPPORT_SRC})"); tip_click(pg, c, r)
                r["pageBg"] = pg.evaluate("getComputedStyle(document.body).backgroundColor")
                r["finalScroll"] = docscroll(pg)
                c.close()
    br.close()
json.dump(res, open(OUT + "results.json", "w"), indent=1)
for k, v in res.items(): print(k, json.dumps(v)[:900])
