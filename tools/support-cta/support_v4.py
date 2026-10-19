#!/usr/bin/env python3
"""Add the quiet Support entry to a v4 page (home / articles / about). Idempotent (marker si-support-v1).
usage: support_v4.py IN OUT KIND(home|articles|about) [--preview]"""
import sys
src, dst, kind = sys.argv[1], sys.argv[2], sys.argv[3]
prev = "--preview" in sys.argv
s = open(src, encoding="utf-8").read()
if "si-support-v1" in s: sys.exit("already patched")
srcid = {"home": "explore-home", "articles": "explore-articles", "about": "explore-about"}[kind]
if prev: srcid = f"explore-preview:{kind}"
asset = "/preview/support/assets/si-support.js" if prev else "/assets/si-support.js"
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f"anchor x{n}: {old[:80]!r}")
    s = s.replace(old, new)
# menu entry (every v4 page has the same menu sheet)
rep('<li><a href="/about/#tip"><small>Optional tips</small>Support the work</a></li>',
    f'<li><a href="/about/#tip" data-si-support="{srcid}"><small>Email list · tips</small>Support Explore</a></li>')
# footer: the existing "Support" link opens the sheet; one quiet line under the footer links
rep('<a href="/about/#tip">Support</a>', f'<a href="/about/#tip" data-si-support="{srcid}">Support</a>')
if kind in ("articles", "about"):
    rep('        <span>© Superintelligent Silicon</span>', f'        <span>© Superintelligent Silicon<span class="si-sup-line"> · <button type="button" data-si-support="{srcid}" data-si-focus="email">New books by email</button></span></span>')
tag = f'  <script src="{asset}" defer></script><!-- si-support-v1 -->\n'
rep('  <script src="/assets/si-theme.js"></script>\n', '  <script src="/assets/si-theme.js"></script>\n' + tag)
if prev:
    s = s.replace('<head>', '<head>\n  <meta name="robots" content="noindex, nofollow" />', 1)
    for b in ("well-be-right-back", "napkins-are-the-backbone"):
        s = s.replace(f'href="/articles/{b}/"', f'href="/preview/support/articles/{b}/"')
    s = s.replace('href="/articles/"', 'href="/preview/support/articles/"').replace('href="/about/"', 'href="/preview/support/about/"').replace('<a href="/">Home</a>', '<a href="/preview/support/">Home</a>')
open(dst, "w", encoding="utf-8").write(s); print("ok", dst)
