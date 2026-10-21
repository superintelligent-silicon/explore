#!/usr/bin/env python3
"""Before (live) / after (preview) shots of the brand spots + wrap/scroll checks. usage: brand_shots.py OUTDIR"""
import sys, os, json
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
E = "https://exploresuperintelligence.online/"; O = "https://superintelligentsilicon.com/"; P = "preview/nav/"
def enter(pg):
    try: pg.get_by_role("button", name="Enter", exact=True).click(timeout=2500); pg.wait_for_timeout(700)
    except Exception: pass
def menu(pg):
    enter(pg)
    try: pg.locator('button:has-text("Menu")').first.click(timeout=2500); pg.wait_for_timeout(700)
    except Exception as e: print("menu?", e)
def support(pg):
    enter(pg); pg.evaluate("window.SISupport && SISupport.open({source:'explore-preview:nav'})"); pg.wait_for_timeout(900)
def ieo_card(pg):
    pg.click("#wholeBtn"); pg.wait_for_timeout(800)
def sios_none(pg): pass
SPOTS = [  # name, site base, path, w, h, action
 ("home-header", E, "", 390, 664, enter), ("home-gate", E, "", 390, 664, None), ("home-desktop", E, "", 1440, 900, enter),
 ("home-menu", E, "", 390, 664, menu), ("support-sheet", E, "", 390, 664, support),
 ("articles", E, "articles/", 390, 664, None), ("articles-desktop", E, "articles/", 1440, 900, None), ("about", E, "about/", 390, 664, None),
 ("research", E, "research/", 1440, 900, None),
 ("ieo-cover", E, "articles/in-each-other/", 390, 664, None), ("ieo-card", E, "articles/in-each-other/", 390, 664, ieo_card),
 ("final-merge-cover", E, "articles/final-merge/", 390, 664, None), ("threshold", E, "threshold/", 390, 664, None),
 ("sios-shell", E, "sios/shell/", 1440, 900, None),
 ("org-contact", O, "contact/", 390, 664, None), ("org-home-desktop", O, "", 1440, 900, None),
]
WRAPJS = r"""()=>{const out=[];const re=/Explore (SI|Superintelligence)/;
 const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;
 while((n=w.nextNode())){ if(!re.test(n.textContent)) continue; const el=n.parentElement; if(!el||!el.offsetParent&&getComputedStyle(el).position!=='fixed') continue;
   const r=document.createRange(); r.selectNodeContents(n); const rects=[...r.getClientRects()].filter(x=>x.width>0);
   if(!rects.length) continue; const tops=new Set(rects.map(x=>Math.round(x.top)));
   const txt=n.textContent.trim(); if(txt.length>60) continue;  // prose sentences may wrap naturally
   out.push({t:txt.slice(0,50),lines:tops.size,top:Math.round(rects[0].top)}); }
 const b=document.querySelector('.brand b'); if(b) out.push({t:'wordmark:'+b.textContent+getComputedStyle(b,'::after').content,lines:1});
 const d=document.scrollingElement; return {labels:out,scroll:[d.scrollWidth-d.clientWidth,d.scrollHeight-d.clientHeight]}}"""
res = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
    for th in ["light", "dark"]:
        for name, base, path, w, h, act in SPOTS:
            imgs = []
            for tag, url in (("before", base + path), ("after", base + P + path)):
                c = b.new_context(viewport={"width": w, "height": h}, color_scheme=th, device_scale_factor=1,
                                  **({"is_mobile": True, "has_touch": True} if w < 500 else {}))
                c.add_init_script("try{localStorage.setItem('si-theme','%s');localStorage.setItem('ieo-theme','%s');localStorage.setItem('fm-peek','1')}catch(e){}" % (th, th))
                pg = c.new_page(); errs = []
                pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: m.type == "error" and errs.append(m.text))
                pg.goto(url, wait_until="load", timeout=60000); pg.wait_for_timeout(1200)
                if act: act(pg)
                f = f"{OUT}/{name}-{w}-{th}-{tag}.png"; pg.screenshot(path=f); imgs.append(f)
                try: info = pg.evaluate(WRAPJS)
                except Exception as e: info = {"err": str(e)[:80]}
                res[f"{name}-{w}-{th}-{tag}"] = dict(info, errors=errs)
                c.close()
            a, bb = Image.open(imgs[0]), Image.open(imgs[1])
            gap = 24; cv = Image.new("RGB", (a.width + bb.width + gap, max(a.height, bb.height) + 30), (120, 120, 120))
            cv.paste(a, (0, 30)); cv.paste(bb, (a.width + gap, 30)); d = ImageDraw.Draw(cv)
            d.text((8, 8), f"BEFORE (live)  {name} {w} {th}", fill=(255, 255, 255)); d.text((a.width + gap + 8, 8), "AFTER (preview)", fill=(255, 255, 255))
            cv.save(f"{OUT}/pair-{name}-{w}-{th}.png")
    b.close()
json.dump(res, open(f"{OUT}/brand.json", "w"), indent=1); print("done")
