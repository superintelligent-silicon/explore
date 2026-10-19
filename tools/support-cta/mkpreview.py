#!/usr/bin/env python3
"""Make a private preview copy of a patched live page. usage: mkpreview.py LIVE.html OUT.html LIVEDIR SLUG
LIVEDIR is the page's live folder (e.g. /articles/final-merge/): relative asset URLs are pointed there, the page becomes noindex,
and support sources become explore-preview:SLUG."""
import re, sys
src, dst, livedir, slug = sys.argv[1:5]
s = open(src, encoding="utf-8").read()
s = re.sub(r'''(\s(?:href|src)=")(?!/|https?:|#|data:|mailto:|\$|')([A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*)"''', lambda m: m.group(1) + livedir + m.group(2) + '"', s)
s = re.sub(r'''(url\((["']?))(?!/|https?:|#|data:)([A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*)''', lambda m: m.group(1) + livedir + m.group(3), s)
s = s.replace(f"explore-book:{slug}", f"explore-preview:{slug}").replace(f"explore-tldr:{slug}", f"explore-preview:{slug}-tldr")
s, n = re.subn(r'<meta name="robots" content="[^"]*"\s*/?>', '<meta name="robots" content="noindex, nofollow">', s)
if not n:
    m = re.search(r'<meta charset[^>]*>', s); s = s[:m.end()] + '\n<meta name="robots" content="noindex, nofollow">' + s[m.end():]
open(dst, "w", encoding="utf-8").write(s); print("preview", dst, "robots metas replaced:", n)
