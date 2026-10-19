#!/usr/bin/env python3
"""Add the quiet support CTAs to a canvas book (WBRB / Napkins / Final Merge engine). Idempotent (marker si-support-v1).
usage: support_book.py IN.html OUT.html SLUG [--preview]
  --preview: sources become explore-preview:SLUG, assets load from /preview/support/assets/, relative fonts/ js/ point at the live
             book folder, the 'All articles' link points at /preview/support/articles/, and the page is noindex."""
import re, sys
src, dst, slug = sys.argv[1], sys.argv[2], sys.argv[3]
prev = "--preview" in sys.argv
s = open(src, encoding="utf-8").read()
MARK = "/* si-support-v1 */"
if MARK in s:
    sys.exit("already patched")
def rep(old, new, count=1, opt=False):
    global s
    n = s.count(old)
    if n != count:
        if opt and n == 0: print("  skip (optional):", old[:60]); return
        sys.exit(f"anchor x{n} (want {count}): {old[:90]!r}")
    s = s.replace(old, new)
book_src = f"explore-preview:{slug}" if prev else f"explore-book:{slug}"
tldr_src = f"explore-preview:{slug}-tldr" if prev else f"explore-tldr:{slug}"
asset = "/preview/support/assets/si-support.js" if prev else "/assets/si-support.js"

# 1) The End page: a plain card in the book's own chip/rule style under the two finale chips
rep('{ t: "finale", id: "end",', '{ t: "finale", id: "end", support: true,')
rep('const textBlock = FS * 1.2 + subL.length * M.lh + FS * 1.2 + chipsH;',
    '''const sup0 = b.support ? supportCard(cw, FS) : null, base0 = FS * 1.2 + subL.length * M.lh + FS * 1.2 + chipsH; /* si-support-v1 */
      /* the card shares The End page when the scene can stay legible; on short phone pages it gets the next page to itself */
      const supIn = !!sup0 && avail - base0 - sup0.gap - sup0.h - FS * 0.5 >= Math.min(sw * 230 / 300, FS * 10), sup = supIn ? sup0 : null, supNext = sup0 && !supIn ? sup0 : null;
      const textBlock = base0 + (sup ? sup.gap + sup.h : 0);''')
# own page after The End when it does not fit
m = re.search(r'\n        anims: \[\{ kind: (?:b\.scene \|\| )?"finale"[^\n]*\}\] \}\);\n', s)
if not m: sys.exit("finale anims anchor")
s = s[:m.end()] + '      if (supNext) { const oy = Math.round((avail - supNext.h) * 0.42); boxes.push({ breakBefore: true, breakAfter: true, h: avail, before: 0, after: 0, links: supNext.links(oy), draw: (c, x, y) => supNext.draw(c, x, y + oy) }); }\n' + s[m.end():]
rep('links: cps.map((ch, i) => ({ dx: ch.dx, dy: ch.dy, w: ch.w, h: chH, target: b.links[i].target })),',
    'links: cps.map((ch, i) => ({ dx: ch.dx, dy: ch.dy, w: ch.w, h: chH, target: b.links[i].target })).concat(sup ? sup.links(Math.round(chipY + chipsH + sup.gap)) : []),')
rep('          drawCentered(c, subL, x + cw / 2, y + top + shh + FS * 1.2, M.lh, FS, C.ink2);',
    '          drawCentered(c, subL, x + cw / 2, y + top + shh + FS * 1.2, M.lh, FS, C.ink2);\n          if (sup) sup.draw(c, x, y + Math.round(chipY + chipsH + sup.gap));')
HELPER = r'''
/* si-support-v1: End-page card. Canvas-drawn like the rest of the page; taps are routed in the page's own link hit-test. */
function supportCard(cw, FS) {
  const W = Math.min(cw, Math.round(FS * 22)), pad = Math.round(FS * 1.05), inW = W - pad * 2;
  const headF = `400 ${Math.round(FS * 1.3)}px ${SERIF}`, smallF = `400 ${Math.round(FS * 0.8)}px ${SANS}`, linkF = `500 ${Math.round(FS * 0.8)}px ${SANS}`;
  const chipF = `500 ${Math.round(FS * 0.86)}px ${SANS}`, chH = Math.max(44, Math.round(FS * 2.3)), btnLabel = "Send me the next one";
  const copy = balanced("New books arrive a few times a month. Get the next one by email: free, no spam, unsubscribe anytime.", "sub", inW);
  const lhS = Math.round(FS * 1.35), rowH = 44;
  /* tip row: "Or tip $1 · $3 · $5" + "More ways to support"; wraps to two rows on narrow pages */
  const segs = [{ t: "Or tip", f: smallF }, { t: "$1", f: linkF, k: "tip:1" }, { t: "$3", f: linkF, k: "tip:3" }, { t: "$5", f: linkF, k: "tip:5" }];
  const gap = Math.round(FS * 1.15), more = { t: "More ways to support", f: linkF, k: "support:more" };
  const segW = a => a.reduce((n, g, i) => n + mw(g.t, g.f) + (i ? gap : 0), 0);
  const dotW = mw("·", smallF) + gap, oneRow = segW(segs) + dotW + mw(more.t, more.f) <= inW;
  const rows = oneRow ? [segs.concat([{ t: "·", f: smallF, dot: 1 }, more])] : [segs, [more]];
  const headH = Math.round(FS * 1.7), btnW = Math.min(inW, Math.round(mw(btnLabel, chipF) + FS * 2.6));
  const yHead = pad, yCopy = yHead + headH + Math.round(FS * 0.25), yBtn = yCopy + copy.length * lhS + Math.round(FS * 0.55), yTip = yBtn + chH + Math.round(FS * 0.2);
  const h = yTip + rows.length * rowH + Math.round(pad * 0.35), x0 = Math.round((cw - W) / 2);
  const place = (row, ry) => { const tw = row.reduce((n, g, i) => n + mw(g.t, g.f) + (i ? gap : 0), 0); let xx = x0 + (W - tw) / 2;
    return row.map((g, i) => { if (i) xx += gap; const o = { g, x: xx, y: ry, w: mw(g.t, g.f) }; xx += o.w; return o; }); };
  const placed = () => rows.map((r, i) => place(r, yTip + i * rowH));
  return { h, gap: Math.round(FS * 1.1),
    links: oy => [{ dx: x0 + Math.round((W - btnW) / 2), dy: oy + yBtn, w: btnW, h: chH, target: "support:email" }]
      .concat(...placed().map(r => r.filter(o => o.g.k).map(o => { const hw = Math.max(44, Math.round(o.w + gap)); return { dx: Math.round(o.x + o.w / 2 - hw / 2), dy: oy + o.y, w: hw, h: rowH, target: o.g.k }; }))),
    draw: (c, x, oy) => {
      const L = x + x0, T = oy;
      c.strokeStyle = C.rule; c.lineWidth = 1; roundRect(c, L + 0.5, T + 0.5, W - 1, h - 1, Math.round(FS * 0.75)); c.stroke();
      c.textAlign = "center"; c.font = headF; c.fillStyle = C.ink; c.fillText("Enjoyed this one?", L + W / 2, T + yHead + Math.round(FS * 1.2)); c.textAlign = "left";
      drawCentered(c, copy, L + W / 2, T + yCopy, lhS, FS, C.ink2);
      const bx = L + Math.round((W - btnW) / 2), by = T + yBtn;
      c.fillStyle = C.chip; roundRect(c, bx, by, btnW, chH, chH / 2); c.fill();
      c.font = chipF; c.fillStyle = C.chipInk; c.textAlign = "center"; c.fillText(btnLabel, bx + btnW / 2, by + chH / 2 + FS * 0.3); c.textAlign = "left";
      placed().forEach(r => r.forEach(o => { const by2 = T + o.y + rowH / 2 + FS * 0.28; c.font = o.g.f; c.fillStyle = o.g.k ? C.ink : C.ink2; c.fillText(o.g.t, x + o.x, by2);
        if (o.g.k) { c.strokeStyle = C.rule; c.lineWidth = 1; c.beginPath(); c.moveTo(x + o.x, by2 + FS * 0.3 + 0.5); c.lineTo(x + o.x + o.w, by2 + FS * 0.3 + 0.5); c.stroke(); } }));
    } };
}
'''
rep('function roundRect(c, x, y, w, h, r) {', HELPER.lstrip("\n") + 'function roundRect(c, x, y, w, h, r) {')
# 2) tap routing for the new canvas targets
rep('      const hit = (pages[idx].links || []).find(l => p.x >= l.x && p.x <= l.x + l.w && p.y >= l.y && p.y <= l.y + l.h);\n      if (hit) {\n',
    '      const hit = (pages[idx].links || []).find(l => p.x >= l.x && p.x <= l.x + l.w && p.y >= l.y && p.y <= l.y + l.h);\n      if (hit) {\n'
    '        if (/^(support|tip):/.test(hit.target)) { const [k, v] = hit.target.split(":"); if (k === "tip") { const u = window.SISupport && SISupport.tip(v); if (u) window.open(u, "_blank", "noopener"); } else if (window.SISupport) SISupport.open({ source: SI_SUPPORT_SRC, focus: v === "email" ? "email" : "" }); return; }\n')
# 3) Chapters sheet: Support row beside All articles / Explore home
rep('<a href="/">Explore home</a></nav>',
    f'<a href="/">Explore home</a><span aria-hidden="true">·</span><button type="button" class="ch-sup" data-si-support="{book_src}">Support</button></nav>')
rep('.ch-out a:hover, .ch-out a:focus-visible { color: var(--room-ink); }',
    '.ch-out a:hover, .ch-out a:focus-visible { color: var(--room-ink); }\n'
    '.ch-out .ch-sup { appearance: none; border: 0; background: none; font: inherit; color: var(--room-ink-2); padding: 0 10px; min-height: 44px; cursor: pointer; }\n'
    '.ch-out .ch-sup:hover, .ch-out .ch-sup:focus-visible { color: var(--room-ink); }')
# 4) TL;DR: one quiet line at the end
rep('''".tl-fol{margin:auto 0 0;''', '''".tl-sup{margin:auto 0 0;padding-top:.5em;text-align:center}.tl-sup+.tl-fol{margin-top:0}"+
  ".tl-sup button{appearance:none;border:0;background:none;padding:0 .6em;min-height:44px;font:500 .74em/1 var(--sans);color:var(--ink);text-decoration:underline;text-decoration-color:var(--rule);text-underline-offset:.3em;cursor:pointer}"+
  ".tl-fol{margin:auto 0 0;''')
rep("""'</ul><p class="tl-fol">'+CFG.fol+'</p></div></div>';""",
    """'</ul><p class="tl-sup"><button type="button" class="tl-sup-b">Get the next book by email</button></p><p class="tl-fol">'+CFG.fol+'</p></div></div>';""")
rep('  ov.addEventListener("click",function(e){ e.stopPropagation(); close(); });',
    f'  ov.querySelector(".tl-sup-b").addEventListener("click",function(e){{ e.stopPropagation(); if(window.SISupport) SISupport.open({{source:"{tldr_src}",focus:"email"}}); }});\n'
    '  ov.addEventListener("click",function(e){ e.stopPropagation(); close(); });')
# 5) load the shared sheet + source constant
tag = f'<script>var SI_SUPPORT_SRC = "{book_src}";</script>\n<script src="{asset}" defer></script>\n'
if "</body>" in s: rep("</body>", tag + "</body>")
else: s += "\n" + tag
if prev:
    s = re.sub(r'(["(])(fonts|js)/', lambda m: f'{m.group(1)}/articles/{slug}/{m.group(2)}/', s)
    s = s.replace('href="/articles/">All articles', 'href="/preview/support/articles/">All articles')
    s = s.replace('<head>', '<head>\n<meta name="robots" content="noindex, nofollow" />', 1)
open(dst, "w", encoding="utf-8").write(s)
print("ok", dst, len(s))
