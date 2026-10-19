"""Memory/GPU-pressure profile in headless Chrome, iPhone-ish (390x844, DPR3, touch).
usage: mem.py BASE TAG scenario[,scenario]"""
import sys, json, time
from playwright.sync_api import sync_playwright
BASE, TAG = sys.argv[1], sys.argv[2]
SCEN = sys.argv[3].split(",")
PASSES = int(sys.argv[4]) if len(sys.argv) > 4 else 3
INIT = r"""
(()=>{const C=[];window.__cv=C;let gl=0;window.__gl=()=>gl;
const ce=Document.prototype.createElement;Document.prototype.createElement=function(t,...a){const e=ce.call(this,t,...a);if(String(t).toLowerCase()==='canvas')C.push(new WeakRef(e));return e};
const gc=HTMLCanvasElement.prototype.getContext;HTMLCanvasElement.prototype.getContext=function(k,...a){const x=gc.call(this,k,...a);if(x&&/webgl/.test(k)&&!this.__g){this.__g=1;gl++;}return x};
const raf=window.requestAnimationFrame;let n=0;window.__raf=()=>{const v=n;n=0;return v};window.requestAnimationFrame=function(f){n++;return raf.call(window,f)};
let dc=0,c2=0;[window.WebGLRenderingContext,window.WebGL2RenderingContext].filter(Boolean).forEach(P=>['drawElements','drawArrays'].forEach(m=>{const o=P.prototype[m];P.prototype[m]=function(...a){dc++;return o.apply(this,a)}}));
['clearRect','fillRect','drawImage','arc'].forEach(m=>{const o=CanvasRenderingContext2D.prototype[m];CanvasRenderingContext2D.prototype[m]=function(...a){c2++;return o.apply(this,a)}});
window.__work=()=>{const v=[dc,c2];dc=0;c2=0;return v};
window.__stats=()=>{let px=0,live=0,big=0;for(const r of C){const c=r.deref();if(!c)continue;live++;const p=c.width*c.height;px+=p;if(p>1e6)big++;}
 document.querySelectorAll('canvas').forEach(c=>{if(!C.some(r=>r.deref()===c)){live++;px+=c.width*c.height;}});
 const g=document.getElementById('gl');return {glCanvas:g?g.width+'x'+g.height:null,canvases:live,canvasMB:+(px*4/1048576).toFixed(1),bigCanvases:big,webgl:gl,dom:document.getElementsByTagName('*').length}};
})();"""
def metrics(pg, cdp):
    cdp.send("HeapProfiler.collectGarbage"); pg.wait_for_timeout(300)
    m = {x["name"]: x["value"] for x in cdp.send("Performance.getMetrics")["metrics"]}
    st = pg.evaluate("window.__stats()")
    pg.evaluate("window.__work()"); pg.wait_for_timeout(1000); w = pg.evaluate("window.__work()")
    return {"heapMB": round(m["JSHeapUsedSize"]/1048576, 1), "nodes": int(m["Nodes"]), "listeners": int(m["JSEventListeners"]), "glDrawsPerSec": w[0], "canvas2dOpsPerSec": w[1], **st}
def layers(cdp, store):
    pass
out = {}
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--use-angle=swiftshader","--enable-unsafe-swiftshader","--ignore-gpu-blocklist","--enable-precise-memory-info","--js-flags=--expose-gc"])
    for sc in SCEN:
        c = br.new_context(viewport={"width":390,"height":844}, device_scale_factor=3, is_mobile=True, has_touch=True, color_scheme="dark")
        c.add_init_script(INIT); c.add_init_script("try{localStorage.setItem('wb-peek','1')}catch(e){}")
        pg = c.new_page(); errs = []
        pg.on("console", lambda m: errs.append(m.text[:200]) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errs.append("pageerror:" + str(e)[:200]))
        cdp = c.new_cdp_session(pg); cdp.send("Performance.enable")
        rows = []
        if sc.startswith("wbrb"):
            pg.goto(BASE + "articles/well-be-right-back/", wait_until="load"); pg.wait_for_timeout(3500)
            rows.append(("cover", metrics(pg, cdp)))
            if sc == "wbrb-book":
                pg.click("#openbook"); pg.wait_for_timeout(2500)
                rows.append(("book-open", metrics(pg, cdp)))
                N = int(pg.evaluate("document.getElementById('count').textContent.split(' of ')[1]"))
                span = min(N-1, 60)
                for p in range(PASSES):
                    for i in range(span): pg.evaluate("document.getElementById('next').click()"); pg.wait_for_timeout(950)
                    for i in range(span): pg.evaluate("document.getElementById('prev').click()"); pg.wait_for_timeout(950)
                    rows.append((f"pass{p+1}", metrics(pg, cdp)))
            else:
                mag = "Ledger" if sc == "wbrb-ledger" else "Annex"
                pg.click("#lglaunch" if mag == "Ledger" else "#anlaunch"); pg.wait_for_timeout(1500)
                rows.append((mag+"-open", metrics(pg, cdp)))
                n = pg.evaluate(f"document.querySelectorAll('#{'ledger' if mag=='Ledger' else 'annex'} .lg-slot').length")
                for p in range(PASSES):
                    for d in (1, -1):
                        for i in range(n-1):
                            # real touch-ish swipe: scroll the deck by one page width
                            pg.evaluate(f"(()=>{{const d=document.querySelector('#{'ledger' if mag=='Ledger' else 'annex'} .lg-deck');d.scrollBy({{left:{d}*d.clientWidth,behavior:'smooth'}})}})()")
                            pg.wait_for_timeout(420)
                    rows.append((f"pass{p+1}", metrics(pg, cdp)))
                pg.evaluate(f"window.{mag}.close()"); pg.wait_for_timeout(1200)
                rows.append(("closed", metrics(pg, cdp)))
        else:
            pg.goto(BASE + sc + "/", wait_until="load"); pg.wait_for_timeout(3500)
            rows.append(("load", metrics(pg, cdp)))
            # generic: try open button, then next button
            opened = pg.evaluate("""(()=>{const b=document.querySelector('#openbook,#open,.open,[data-open],button.book');if(b){b.click();return b.id||b.className}return null})()""")
            pg.wait_for_timeout(2500)
            rows.append(("opened:"+str(opened), metrics(pg, cdp)))
            nx = pg.evaluate("""(()=>{const b=document.querySelector('#next,.next,[aria-label="Next page"],[aria-label=Next]');return b?(b.id?'#'+b.id:null):null})()""")
            for p in range(PASSES):
                for d in ("next", "prev"):
                    for i in range(40):
                        if nx: pg.evaluate(f"""(()=>{{const b=document.querySelector('#{d}')||document.querySelector('[aria-label^="{'Next' if d=='next' else 'Previous'}"]');if(b)b.click()}})()""")
                        else: pg.keyboard.press("ArrowRight" if d=="next" else "ArrowLeft")
                        pg.wait_for_timeout(700)
                rows.append((f"pass{p+1}", metrics(pg, cdp)))
        out[sc] = {"rows": rows, "errors": errs[:10]}
        print(sc, json.dumps(out[sc]), flush=True)
        c.close()
    br.close()
json.dump(out, open(f"/workspace/explore-articles/stability-pass/mem-{TAG}-{'_'.join(SCEN).replace('/','-')}.json","w"), indent=1)
