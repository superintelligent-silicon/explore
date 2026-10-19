#!/usr/bin/env python3
"""Stability + mobile-fit + way-back pass for the illustrated-book engine (We'll Be Right Back, The Final Merge, Napkins Are the Backbone). Idempotent; applied to the built index.html.
usage: patch_wbrb.py path/to/index.html"""
import sys
P = sys.argv[1]
s = open(P, encoding="utf-8").read()
MARK = "/* si-stability-v1 */"
if MARK in s: print("already patched"); sys.exit(0)
import re
HAS_MAG = "const makeMag" in s
def rep(old, new, n=1, opt=False):
    global s
    c = s.count(old)
    if c == 0 and opt: return
    if c != n: sys.exit(f"expected {n}, found {c}: {old[:80]!r}")
    s = s.replace(old, new)

# 1. the room (three.js particles) and the book's living pictures pause while a magazine covers the screen or the tab is hidden
rep('function frame() {\n      requestAnimationFrame(frame);\n      try {',
    'function frame() {\n      requestAnimationFrame(frame);\n      if (document.hidden || window.LedgerOpen) { clockT.getDelta(); return; } ' + MARK + '\n      try {')
rep('if (reduce || !gl || !N || document.hidden || !opened) return;',
    'if (reduce || !gl || !N || document.hidden || !opened || window.LedgerOpen) return;')
# 2. release canvas backing stores as soon as a page leaves the cache (iOS counts them until GC runs)
rep('if (far !== null && far !== i) baseCache.delete(far); }',
    'if (far !== null && far !== i) { const o = baseCache.get(far); baseCache.delete(far); if (o) [o.text, o.under].forEach(z => { if (z) z.width = z.height = 0; }); } }')
rep('function clearTex() { flatCache = null; grainPat = null; baseCache.clear();',
    'function clearTex() { if (flatCache && flatCache.cv) flatCache.cv.width = flatCache.cv.height = 0; flatCache = null; grainPat = null; for (const o of baseCache.values()) [o.text, o.under].forEach(z => { if (z) z.width = z.height = 0; }); baseCache.clear();')
rep('if (!pc) { if (POOL.size > 24) POOL.clear();',
    'if (!pc) { if (POOL.size > 24) { for (const q of POOL.values()) q.cv.width = q.cv.height = 0; POOL.clear(); }')
OPT = not HAS_MAG
# 3. magazines: only the current page and its neighbours are painted; everything else is skipped (no layers, no tiles)
rep('    CFG.spreads.forEach((sp, i) => page(sp, i));\n',
    '    CFG.spreads.forEach((sp, i) => page(sp, i));\n'
    '    slots = [...deck.children];\n', opt=OPT)
rep('let root, deck, count, prevB, nextB, cur = 0, built = false, isOpen = false, from = null;',
    'let root, deck, count, prevB, nextB, cur = 0, built = false, isOpen = false, from = null, slots = [], cullAt = -9;\n'
    '  function cull(at, extra) { if (!slots.length) return; const k = isOpen ? at : -99; if (k === cullAt && extra == null) return; cullAt = extra == null ? k : -9;\n'
    '    slots.forEach((sl, i) => { const near = isOpen && (Math.abs(i - k) <= 1 || (extra != null && Math.abs(i - extra) <= 1)); sl.classList.toggle("lg-far", !near); }); }', opt=OPT)
rep('if (i !== cur) { cur = i; untip(); try { Sound.plip(0.15); } catch (e) {} } ui(); }); });',
    'if (i !== cur) { cur = i; untip(); try { Sound.plip(0.15); } catch (e) {} } cull(Math.round(deck.scrollLeft / deck.clientWidth)); ui(); }); });\n'
    '    deck.addEventListener("scrollend", () => cull(cur));', opt=OPT)
rep('function go(i, instant) { i = Math.max(0, Math.min(CFG.spreads.length - 1, i));',
    'function go(i, instant) { i = Math.max(0, Math.min(CFG.spreads.length - 1, i)); cull(cur, i); clearTimeout(go._t); go._t = setTimeout(() => cull(cur), 1200);', opt=OPT)
rep('root.classList.add("on"); requestAnimationFrame(() => {',
    'root.classList.add("on"); cull(typeof at === "number" ? at : cur); requestAnimationFrame(() => {', opt=OPT)
rep('untip(); root.classList.remove("on");',
    'untip(); root.classList.remove("on"); setTimeout(() => { if (!isOpen) cull(-99); }, 600);', opt=OPT)
# 4. magazine covers: their drift loops only draw while the cover is on screen
rep('if (!W || document.hidden) return; if (!colors) colors = cols();',
    'if (document.hidden || !c.closest(".on") || c.closest(".lg-far")) return; if (cv.clientWidth && Math.abs(cv.clientWidth - W) > 1) fit(); if (!W) return; if (!colors) colors = cols();', opt=OPT)
rep("let raf = 0; const tick = now => { raf = requestAnimationFrame(tick); if (document.hidden) return; draw(now); };",
    "let raf = 0; const tick = now => { raf = requestAnimationFrame(tick); if (document.hidden || !c.closest(\".on\") || c.closest(\".lg-far\")) return; if (cv.clientWidth && Math.abs(cv.clientWidth - W) > 1) fit(); draw(now); };", opt=OPT)
# 5. TL;DR overlay: cap its canvases at 2x like the rest of the book
rep("var dpr=Math.min(window.devicePixelRatio||1,3)", "var dpr=Math.min(window.devicePixelRatio||1,2)")
# 6. a way back: magazine top bars get an Articles link next to Contents / Book
rep('const tr = H("div", {}, top); const tocB = H("button", { class: "lg-btn", type: "button" }, tr, "Contents");',
    'const tr = H("div", {}, top); const homeA = H("a", { class: "lg-btn lg-home", href: "/articles/", "aria-label": "All articles on Explore Superintelligence" }, tr, "Articles"); void homeA; const tocB = H("button", { class: "lg-btn", type: "button" }, tr, "Contents");', opt=OPT)
# chapters sheet: a quiet footer that always shows, under the list
rep('    <ul class="ch-list" id="ch-list"></ul>\n  </div>',
    '    <ul class="ch-list" id="ch-list"></ul>\n    <nav class="ch-out" aria-label="Leave the book"><a href="/articles/">All articles</a><span aria-hidden="true">·</span><a href="/">Explore home</a></nav>\n  </div>')
# cover screen: a small breadcrumb, top left, in the cover's own type
m = re.search(r'<div id="intro" aria-label="[^"]*">\n', s); assert m
rep(m.group(0),
    m.group(0) + '  <nav class="intro-nav" aria-label="Explore Superintelligence"><a href="/">Explore</a><span aria-hidden="true">/</span><a href="/articles/">Articles</a></nav>\n')

CSS = """<style id="si-stability">
/* si-stability-v1: mobile fit, magazine culling, way back */
.app { height: 100%; height: 100dvh; }
.lg-slot.lg-far > .lg-page { visibility: hidden; content-visibility: hidden; box-shadow: none; }
#intro { padding: calc(46px + env(safe-area-inset-top, 0px)) max(16px, env(safe-area-inset-right, 0px)) calc(14px + env(safe-area-inset-bottom, 0px)) max(16px, env(safe-area-inset-left, 0px)); }
#intro .intro-in { transform: translateY(var(--iy, 12vh)) scale(var(--is, 1)); }
#intro.out .intro-in { transform: translateY(var(--iy, 12vh)) scale(calc(var(--is, 1) * 1.04)); }
#intro .book-label, #intro .lg-launch { min-height: 44px; }
#intro .intro-k { text-wrap: balance; }
.intro-nav { position: absolute; z-index: 2; top: calc(2px + env(safe-area-inset-top, 0px)); left: max(8px, env(safe-area-inset-left, 0px)); display: flex; align-items: center; pointer-events: auto; cursor: auto; font: 500 10.5px/1 var(--sans); letter-spacing: .2em; text-transform: uppercase; }
.intro-nav a { color: var(--room-ink-2); text-decoration: none; padding: 16px 8px; min-height: 44px; box-sizing: border-box; display: inline-flex; align-items: center; transition: color .2s; }
.intro-nav a:hover, .intro-nav a:focus-visible { color: var(--room-ink); }
.intro-nav span { color: var(--room-ink-3, rgba(236,235,230,.36)); }
#intro.out .intro-nav { pointer-events: none; }
.ch-body { grid-template-rows: auto 1fr auto; }
.ch-out { display: flex; justify-content: center; align-items: center; gap: 4px; padding: 2px 16px calc(6px + env(safe-area-inset-bottom, 0px)); border-top: 1px solid var(--room-edge); font: 500 12.5px/1 var(--sans); }
.ch-out a { color: var(--room-ink-2); text-decoration: none; padding: 0 10px; min-height: 44px; display: inline-flex; align-items: center; }
.ch-out a:hover, .ch-out a:focus-visible { color: var(--room-ink); }
.ch-out span { color: var(--room-ink-3, rgba(236,235,230,.36)); }
.lg-top a.lg-btn { text-decoration: none; display: inline-flex; align-items: center; }
.lg-top .lg-mast b { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
@media (max-width: 400px) { .lg-top .lg-btn { padding-inline: 7px; min-width: 40px; } #ledger .lg-mast b { font-size: 14px; letter-spacing: .1em; } #annex .lg-mast b { font-size: 16px; letter-spacing: .03em; } }
@media (orientation: landscape) and (max-height: 520px) {
  #intro .intro-in { grid-template-columns: minmax(0, 1fr) auto; column-gap: 36px; max-width: 820px; align-items: center; }
  #intro .intro-in > * { grid-column: 1; }
  #intro .intro-in > .book { grid-column: 2; grid-row: 1 / span 3; }
  #intro .intro-in > .lg-launches { grid-column: 2; grid-row: 4 / span 2; flex-direction: column; align-items: stretch; }
  #intro .intro-t { font-size: min(84px, 15vh); }
}
</style>
<script id="si-stability-js">
/* fit the cover screen to whatever is visible (Safari's bars, the home indicator, landscape) without scrolling */
(function () {
  var intro = document.getElementById("intro"), inn = intro && intro.querySelector(".intro-in"); if (!inn) return;
  var nav = intro.querySelector(".intro-nav");
  if (nav) ["pointerdown", "touchstart", "click"].forEach(function (t) { nav.addEventListener(t, function (e) { e.stopPropagation(); }, { passive: true }); });
  var raf = 0;
  function fit() {
    raf = 0; var cs = getComputedStyle(intro);
    var av = intro.clientHeight - parseFloat(cs.paddingTop) - parseFloat(cs.paddingBottom), aw = intro.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
    var h = inn.offsetHeight, w = inn.offsetWidth; if (!h || !w || av < 50) return;
    var sc = Math.max(0.62, Math.min(1, av / h, aw / w)), free = av - h * sc;
    intro.style.setProperty("--is", sc.toFixed(3));
    intro.style.setProperty("--iy", Math.max(0, Math.min(innerHeight * 0.12, free / 2 - 2)).toFixed(1) + "px");
  }
  function q() { if (!raf) raf = requestAnimationFrame(fit); }
  fit(); addEventListener("resize", q); addEventListener("orientationchange", q); addEventListener("load", q);
  if (window.visualViewport) visualViewport.addEventListener("resize", q);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(q);
  setTimeout(q, 600);
})();
</script>
"""
if '</body>' in s: rep('</body>', CSS + '</body>')
else: s = s.rstrip('\n') + '\n' + CSS
open(P, "w", encoding="utf-8").write(s)
print("patched", P)
