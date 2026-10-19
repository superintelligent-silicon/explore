import sys, json, re
from playwright.sync_api import sync_playwright
INIT = re.search(r'INIT = r"""(.*?)"""', open("/workspace/explore-articles/stability-pass/mem.py").read(), re.S).group(1)
BASE, TAG = sys.argv[1], sys.argv[2]
def w(pg):
    pg.evaluate("window.__work()"); pg.wait_for_timeout(2000); a = pg.evaluate("window.__work()"); return {"glDraws/s": a[0]/2, "canvas2dOps/s": a[1]/2}
out = {}
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--use-angle=swiftshader","--enable-unsafe-swiftshader","--ignore-gpu-blocklist"])
    c = br.new_context(viewport={"width":390,"height":844}, device_scale_factor=3, is_mobile=True, has_touch=True, color_scheme="dark")
    c.add_init_script(INIT); c.add_init_script("try{localStorage.setItem('wb-peek','1')}catch(e){}")
    pg = c.new_page(); pg.goto(BASE+"articles/well-be-right-back/", wait_until="load"); pg.wait_for_timeout(3500)
    out["cover"] = w(pg)
    pg.click("#openbook"); pg.wait_for_timeout(2500); out["book (idle page)"] = w(pg)
    pg.evaluate("Ledger.open(5)"); pg.wait_for_timeout(1500); out["Ad Ledger open, page 6"] = w(pg)
    pg.evaluate("Ledger.close()"); pg.wait_for_timeout(1200); out["back in book after Ledger"] = w(pg)
    pg.evaluate("Annex.open(5)"); pg.wait_for_timeout(1500); out["Long Pitch open, page 6"] = w(pg)
    pg.evaluate("Annex.close()"); pg.wait_for_timeout(1200); out["back in book after both"] = w(pg)
    br.close()
for k,v in out.items(): print(f"{TAG:7s} {k:28s} {v}")
json.dump(out, open(f"work-{TAG}.json","w"), indent=1)
