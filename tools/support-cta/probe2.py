from playwright.sync_api import sync_playwright
import sys
b, lo, hi = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--use-angle=swiftshader","--enable-unsafe-swiftshader","--ignore-gpu-blocklist"])
    c = br.new_context(viewport={"width":390,"height":664}, device_scale_factor=1, is_mobile=True, has_touch=True)
    c.add_init_script("try{localStorage.setItem('wb-peek','1')}catch(e){}")
    for n in range(lo, hi+1):
        pg=c.new_page()
        pg.goto(f"http://127.0.0.1:8841/preview/support/articles/{b}/#p{n}"); pg.wait_for_timeout(2500)
        pg.screenshot(path=f"/tmp/pr-{b}-{n:03d}.png")
        pg.close() if False else None
        print(n, pg.evaluate("document.querySelector('.count') && document.querySelector('.count').textContent"))
