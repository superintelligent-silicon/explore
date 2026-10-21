#!/usr/bin/env python3
"""Record the si-nav transition (slow forward, slow back, fast) as video. usage: nav_video.py OUTDIR"""
import sys, os, time, glob, shutil
from playwright.sync_api import sync_playwright
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
EB = "https://exploresuperintelligence.online/preview/nav/"
HELD = []; HOLD = {"on": False}
def router(r):
    if r.request.resource_type == "document" and HOLD["on"]: HELD.append(r); return
    r.continue_()
def release():
    HOLD["on"] = False
    while HELD: HELD.pop(0).continue_()
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
    for (w, h, th) in [(390, 664, "light"), (1440, 900, "dark")]:
        vd = f"{OUT}/raw-{w}-{th}"; shutil.rmtree(vd, ignore_errors=True)
        c = b.new_context(viewport={"width": w, "height": h}, color_scheme=th, record_video_dir=vd, record_video_size={"width": w, "height": h},
                          **({"is_mobile": True, "has_touch": True} if w < 500 else {}))
        c.add_init_script("try{localStorage.setItem('si-theme','%s');localStorage.setItem('ieo-theme','%s')}catch(e){}" % (th, th))
        pg = c.new_page(); pg.route("**/*", router)
        pg.goto(EB + "articles/", wait_until="load"); pg.wait_for_timeout(1500)
        HOLD["on"] = True; pg.click('a[href="/preview/nav/articles/in-each-other/"]', no_wait_after=True)
        pg.wait_for_timeout(1600); release(); pg.wait_for_url(EB + "articles/in-each-other/"); pg.wait_for_timeout(2000)
        HOLD["on"] = True; pg.evaluate("history.back()"); pg.wait_for_timeout(1300); release(); pg.wait_for_timeout(1800)
        pg.click('a[href="/preview/nav/articles/defrost-mode/"]'); pg.wait_for_timeout(1800)   # fast: no overlay
        c.close()
        src = glob.glob(vd + "/*.webm")[0]; dst = f"{OUT}/nav-{w}-{th}.webm"; shutil.move(src, dst); shutil.rmtree(vd, ignore_errors=True); print(dst)
    b.close()
