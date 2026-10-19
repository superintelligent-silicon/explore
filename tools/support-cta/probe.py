from playwright.sync_api import sync_playwright
import sys
b=sys.argv[1]
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--use-angle=swiftshader","--enable-unsafe-swiftshader","--ignore-gpu-blocklist"])
    c = br.new_context(viewport={"width":390,"height":664}, device_scale_factor=2, is_mobile=True, has_touch=True)
    c.add_init_script("try{localStorage.setItem('wb-peek','1')}catch(e){}")
    pg=c.new_page(); errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(f"http://127.0.0.1:8841/preview/support/articles/{b}/"); pg.wait_for_timeout(2500); pg.click("#openbook"); pg.wait_for_timeout(2000)
    pg.click("#chap"); pg.wait_for_timeout(800)
    print(pg.evaluate("[...document.querySelectorAll('#ch-list button, #ch-list a, #ch-list li')].slice(-6).map(e=>e.tagName+':'+e.textContent.trim().slice(0,40))"))
    print(pg.evaluate("document.querySelector('.count') && document.querySelector('.count').textContent"), errs)
