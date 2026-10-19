import sys, json
from playwright.sync_api import sync_playwright
BASE, TAG = sys.argv[1], sys.argv[2]
def lt(cdp, pg):
    ev = {}
    cdp.on("LayerTree.layerTreeDidChange", lambda e: ev.__setitem__("l", e.get("layers") or []))
    cdp.send("LayerTree.enable"); pg.wait_for_timeout(1500)
    L = ev.get("l", []); cdp.send("LayerTree.disable")
    d = [l for l in L if l.get("drawsContent")]
    area = sum(l["width"]*l["height"] for l in d)
    return {"layers": len(L), "drawing": len(d), "MB@dpr3": round(area*9*4/1048576, 1), "biggest": sorted([(l["width"],l["height"]) for l in d], key=lambda x:-x[0]*x[1])[:6]}
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--use-angle=swiftshader","--enable-unsafe-swiftshader","--ignore-gpu-blocklist"])
    c = br.new_context(viewport={"width":390,"height":844}, device_scale_factor=3, is_mobile=True, has_touch=True, color_scheme="dark")
    pg = c.new_page(); cdp = c.new_cdp_session(pg)
    pg.goto(BASE+"articles/well-be-right-back/", wait_until="load"); pg.wait_for_timeout(3000)
    r = {"cover": lt(cdp, pg)}
    pg.click("#openbook"); pg.wait_for_timeout(2500); r["book"] = lt(cdp, pg)
    pg.evaluate("Ledger.open(0)"); pg.wait_for_timeout(1500); r["ledger"] = lt(cdp, pg)
    pg.evaluate("Ledger.go(12)"); pg.wait_for_timeout(1500); r["ledger12"] = lt(cdp, pg)
    pg.evaluate("Ledger.close()"); pg.wait_for_timeout(800); pg.evaluate("Annex.open(5)"); pg.wait_for_timeout(1500); r["annex5"] = lt(cdp, pg)
    print(json.dumps(r, indent=1))
