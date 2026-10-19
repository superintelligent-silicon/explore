import sys, json
from playwright.sync_api import sync_playwright
BASE = sys.argv[1]; OUT = sys.argv[2]
PAGES = ["articles/defrost-mode/", "articles/final-merge/", "articles/immortal-tombstones/", "research/", "research/word-swap/", "threshold/", "have-you-seen/", "sios/", "shipping/"]
res = {}
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
    for (w, h) in [(390, 664), (1440, 900)]:
        for sc in ["light", "dark"]:
            for p in PAGES:
                mob = w < 700
                c = br.new_context(viewport={"width": w, "height": h}, device_scale_factor=2 if mob else 1, is_mobile=mob, has_touch=mob, color_scheme=sc)
                pg = c.new_page(); errs = []
                pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None); pg.on("pageerror", lambda e: errs.append(str(e)))
                pg.goto(BASE + p, wait_until="load"); pg.wait_for_timeout(1800)
                feeds = pg.evaluate("[...document.querySelectorAll('link[rel=alternate][href$=\"feed.xml\"],link[rel=alternate][href$=\"feed.json\"]')].length")
                sc_ = pg.evaluate("[document.documentElement.scrollHeight-innerHeight, document.documentElement.scrollWidth-innerWidth]")
                res[f"{p}-{w}-{sc}"] = {"errors": errs, "scroll": sc_, "feeds": feeds}
                c.close()
    br.close()
json.dump(res, open(OUT + "pages.json", "w"), indent=1)
for k, v in res.items(): print(k, v)
