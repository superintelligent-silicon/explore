#!/usr/bin/env python3
"""Immortal Tombstones variant of support_book.py (same canvas page engine, different finale layout and no Chapters sheet).
Adds: End-page card (own page on short phones), Support link in the text-version bar, TL;DR email line, sheet script.
usage: support_book_it.py IN OUT"""
import re, sys, os
src, dst = sys.argv[1], sys.argv[2]; slug = "immortal-tombstones"
s = open(src, encoding="utf-8").read()
if "/* si-support-v1 */" in s: sys.exit("already patched")
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f"anchor x{n} (want {count}): {old[:90]!r}")
    s = s.replace(old, new)
B = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "support_book.py"), encoding="utf-8").read()
HELPER = re.search(r"HELPER = r'''(.*?)'''", B, re.S).group(1).lstrip("\n")
SHIM = ('/* si-support-v1 shims: this book names its balanced wrap balancedWrap and has no drawCentered */\n'
        'const balanced = balancedWrap;\n'
        'function drawCentered(c, lines, cx, y, lh, size, color) { lines.forEach((ln, i) => { const l = ln[ln.length - 1], lw = l ? l.x + mw(l.w, l.f) : 0; drawLine(c, ln, cx - lw / 2, y + i * lh, lh, size, color); }); }\n')
book_src, tldr_src = f"explore-book:{slug}", f"explore-tldr:{slug}"
# 1) End page
rep('{t:"finale", id:"end",', '{t:"finale", id:"end", support:true,')
rep('      const textBlock = FS * 1.25 + subLines.length * M.lh + FS * 1.1 + chipsH;',
    '''      const sup0 = b.support ? supportCard(cw, FS) : null, base0 = FS * 1.25 + subLines.length * M.lh + FS * 1.1 + chipsH; /* si-support-v1 */
      /* the card shares The End page when the scene can stay legible; on short phone pages it gets the next page to itself */
      const supIn = !!sup0 && avail - base0 - sup0.gap - sup0.h - FS * 0.5 >= Math.min(sw * 230 / 300, FS * 10), sup = supIn ? sup0 : null, supNext = sup0 && !supIn ? sup0 : null;
      const textBlock = base0 + (sup ? sup.gap + sup.h : 0);''')
m = re.search(r'\n        anims: \[\{ kind: "finale"[^\n]*\}\] \}\);\n', s)
if not m: sys.exit("finale anims anchor")
s = s[:m.end()] + '      if (supNext) { const oy = Math.round((avail - supNext.h) * 0.42); boxes.push({ breakBefore: true, breakAfter: true, h: avail, before: 0, after: 0, links: supNext.links(oy), draw: (c, x, y) => supNext.draw(c, x, y + oy) }); }\n' + s[m.end():]
rep('        links: chips.map((ch, i) => ({ dx: ch.dx, dy: ch.dy, w: ch.w, h: chH, target: b.links[i].target })),',
    '        links: chips.map((ch, i) => ({ dx: ch.dx, dy: ch.dy, w: ch.w, h: chH, target: b.links[i].target })).concat(sup ? sup.links(Math.round(chipY + chipsH + sup.gap)) : []),')
rep('          subLines.forEach((ln, i) => { const l = ln[ln.length - 1], lw = l.x + mw(l.w, l.f); drawLine(c, ln, x + cw / 2 - lw / 2, yy + i * M.lh, M.lh, FS, C.ink2); });',
    '          subLines.forEach((ln, i) => { const l = ln[ln.length - 1], lw = l.x + mw(l.w, l.f); drawLine(c, ln, x + cw / 2 - lw / 2, yy + i * M.lh, M.lh, FS, C.ink2); });\n          if (sup) sup.draw(c, x, y + Math.round(chipY + chipsH + sup.gap));')
rep('function roundRect(c, x, y, w, h, r) {', SHIM + HELPER + 'function roundRect(c, x, y, w, h, r) {')
# 2) taps
rep('      if (hit && /^https?:/.test(hit.target)) { openURL(hit.target); return; }',
    '      if (hit && /^(support|tip):/.test(hit.target)) { const [k, v] = hit.target.split(":"); if (k === "tip") { const u = window.SISupport && SISupport.tip(v); if (u) window.open(u, "_blank", "noopener"); } else if (window.SISupport) SISupport.open({ source: SI_SUPPORT_SRC, focus: v === "email" ? "email" : "" }); return; }\n'
    '      if (hit && /^https?:/.test(hit.target)) { openURL(hit.target); return; }')
# 3) end of the text version: one quiet line (the text bar has no room on phones)
rep('</ol>\n</div>\n</article>', '</ol>\n'
    f'<p class="meta it-sup" style="margin-top:2em">Enjoyed this one? <a href="/about/#tip" data-si-support="{book_src}" data-si-focus="email">Get the next book by email</a> · <a href="/about/#tip" data-si-support="{book_src}">Support Explore</a></p>\n</div>\n</article>')
# 4) TL;DR line
rep('''".tl-fol{margin:auto 0 0;''', '''".tl-sup{margin:auto 0 0;padding-top:.5em;text-align:center}.tl-sup+.tl-fol{margin-top:0}"+
  ".tl-sup button{appearance:none;border:0;background:none;padding:0 .6em;min-height:44px;font:500 .74em/1 var(--sans);color:var(--ink);text-decoration:underline;text-decoration-color:var(--rule);text-underline-offset:.3em;cursor:pointer}"+
  ".tl-fol{margin:auto 0 0;''')
rep("""'</ul><p class="tl-fol">'+CFG.fol+'</p></div></div>';""",
    """'</ul><p class="tl-sup"><button type="button" class="tl-sup-b">Get the next book by email</button></p><p class="tl-fol">'+CFG.fol+'</p></div></div>';""")
rep('  ov.addEventListener("click",function(e){ e.stopPropagation(); close(); });',
    f'  ov.querySelector(".tl-sup-b").addEventListener("click",function(e){{ e.stopPropagation(); if(window.SISupport) SISupport.open({{source:"{tldr_src}",focus:"email"}}); }});\n'
    '  ov.addEventListener("click",function(e){ e.stopPropagation(); close(); });')
rep("</body>", f'<script>var SI_SUPPORT_SRC = "{book_src}";</script>\n<script src="/assets/si-support.js" defer></script>\n</body>')
open(dst, "w", encoding="utf-8").write(s); print("ok", dst, len(s))
