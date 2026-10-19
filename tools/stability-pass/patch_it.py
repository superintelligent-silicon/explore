#!/usr/bin/env python3
"""Stability + way-back pass for Immortal Tombstones. Idempotent. usage: patch_it.py index.html"""
import sys
P = sys.argv[1]; s = open(P, encoding="utf-8").read()
MARK = "/* si-stability-v1 */"
if MARK in s: print("already patched"); sys.exit(0)
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: sys.exit(f"expected {n}, found {c}: {old[:80]!r}")
    s = s.replace(old, new)
# page canvases and textures at 2x, not 3x: a 3x page is ~10 MB of GPU memory each on an iPhone, and six were cached
rep('dpr = Math.min(window.devicePixelRatio || 1, 3);', 'dpr = Math.min(window.devicePixelRatio || 1, 2); ' + MARK)
rep('if (texCache.size > 6) {', 'if (texCache.size > 4) {')
# the full-page canvas is only needed for the upload; free its backing store right away
rep('gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, cv);', 'gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, cv); cv.width = cv.height = 0;')
# phones drop WebGL contexts under memory pressure: rebuild instead of going blank
rep('if (gl) { try { initGL(); } catch (err) { console.error(err); } }',
    'if (gl) { try { initGL(); } catch (err) { console.error(err); } }\n'
    'cvs.addEventListener("webglcontextlost", e => { e.preventDefault(); texCache.clear(); }, false);\n'
    'cvs.addEventListener("webglcontextrestored", () => { try { initGL(); } catch (err) { console.error(err); } texCache.clear(); draw(); prefetch(); }, false);')
rep("var dpr=Math.min(window.devicePixelRatio||1,3)", "var dpr=Math.min(window.devicePixelRatio||1,2)")
# a way back: a small shelf icon beside "Text" in the toolbar (cover, contents and every page), and links in the text version
ICON = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 4.5v15M8.5 4.5v15M13 6l4.6 13.3M3 19.5h18"/></svg>'
rep('<button id="readbtn" class="textbtn" aria-label="Read as plain text" title="Read as plain text">Text</button>',
    '<span class="it-right"><button id="readbtn" class="textbtn" aria-label="Read as plain text" title="Read as plain text">Text</button>'
    f'<a class="it-home" href="/articles/" aria-label="All articles on Explore Superintelligence" title="All articles">{ICON}</a></span>')
rep('<div class="closebar"><button type="button">Back to the book</button></div>',
    '<div class="closebar"><nav class="cb-out" aria-label="Leave the book"><a href="/articles/">All articles</a><span aria-hidden="true">·</span><a href="/">Explore home</a></nav><button type="button">Back to the book</button></div>')
CSS = """<style id="si-stability">
.bar .it-right { position: absolute; right: max(16px, calc((100% - var(--pw, 100%)) / 2)); top: 50%; transform: translateY(-50%); display: flex; align-items: center; gap: 2px; }
.bar .it-right .textbtn { position: static; transform: none; }
.bar .it-home { position: relative; width: 30px; height: 30px; display: grid; place-items: center; border-radius: 50%; color: var(--ink-2); transition: background .2s, color .2s; }
.bar .it-home::after { content: ""; position: absolute; inset: -7px -10px -7px 0; }
.bar .it-home:hover { background: color-mix(in srgb, var(--ink) 7%, transparent); color: var(--ink); }
.bar .it-home:focus-visible { outline: 2px solid var(--ink-2); outline-offset: 2px; }
.bar .textbtn { position: static; }
.reader .closebar { align-items: center; gap: 12px; }
.reader .cb-out { margin-right: auto; display: flex; align-items: center; gap: 2px; font: 500 13px/1 var(--sans); }
.reader .cb-out a { color: var(--ink-2); text-decoration: none; padding: 0 8px; min-height: 40px; display: inline-flex; align-items: center; }
.reader .cb-out a:first-child { padding-left: 0; }
.reader .cb-out span { color: var(--ink-2); opacity: .6; }
</style>
"""
rep('</body>', CSS + '</body>')
open(P, "w", encoding="utf-8").write(s); print("patched", P)
