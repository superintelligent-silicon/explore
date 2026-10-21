#!/usr/bin/env python3
"""Build private /preview/nav/ copies with /assets/si-nav.js wired in. usage: nav_preview.py REPO ORGDIR OUTDIR
Explore copies -> OUTDIR/explore/preview/nav/..., org copies -> OUTDIR/org/preview/nav/...
Links between the copied pages (and across the two sites) are pointed at their preview twins so navigation stays inside the preview."""
import re, sys, os
repo, orgdir, out = sys.argv[1:4]
E = "https://exploresuperintelligence.online"; O = "https://superintelligentsilicon.com"
P = "/preview/nav"
EX = {"/": "index.html"}
for f in ["articles/index.html", "about/index.html", "research/index.html", "shipping/index.html", "sios/index.html", "sios/shell/index.html",
          "threshold/index.html", "have-you-seen/index.html", "research/word-swap/index.html",
          "articles/in-each-other/index.html", "articles/defrost-mode/index.html", "articles/final-merge/index.html",
          "articles/immortal-tombstones/index.html", "articles/napkins-are-the-backbone/index.html", "articles/well-be-right-back/index.html"]:
    EX["/" + f[:-len("index.html")]] = f
ORG = {"/": "home.html", "/contact/": "contact.html"}
SLUGS = ["in-each-other", "defrost-mode", "final-merge"]

def link_map(site):
    m = {}
    for p in EX:
        m[E + p] = (E + P + p) if site == "org" else (P + p)
        if site == "explore": m[p] = P + p
    m[E] = m[E + "/"]
    for p in ORG:
        m[O + p] = (O + P + p) if site == "explore" else (P + p)
        if site == "org": m[p] = P + p
    return m

def patch(s, site, livedir, slug=None):
    m = link_map(site)
    def a_tag(t):
        tag = t.group(0)
        return re.sub(r'\bhref="([^"]*)"', lambda h: 'href="%s"' % m.get(h.group(1), h.group(1)), tag)
    s = re.sub(r'<a\b[^>]*>', a_tag, s)
    # relative asset URLs -> live folder (books keep their own copied assets, so only for non-book pages)
    if livedir:
        s = re.sub(r'''(\s(?:href|src)=")(?!/|https?:|#|data:|mailto:|tel:|\$|')([A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*)"''', lambda x: x.group(1) + livedir + x.group(2) + '"', s)
    if slug:
        s = s.replace(f"explore-book:{slug}", f"explore-preview:{slug}").replace(f"explore-tldr:{slug}", f"explore-preview:{slug}-tldr")
    s = s.replace('"explore-home"', '"explore-preview:nav-home"') if site == "explore" else s
    s, n = re.subn(r'<meta name="robots" content="[^"]*"\s*/?>', '<meta name="robots" content="noindex, nofollow">', s)
    mc = re.search(r'<meta charset[^>]*>', s, re.I)
    inc = '\n<script src="%s/assets/si-nav.js"></script>' % P
    if not n: inc = '\n<meta name="robots" content="noindex, nofollow">' + inc
    s = s[:mc.end()] + inc + s[mc.end():]
    # preview copies of the shared assets that carry the brand changes
    s = re.sub(r'"/assets/(si-v4\.css|si-support\.js|home/si-sound\.js)"', lambda x: '"%s/assets/%s"' % (P, x.group(1)), s)
    return s

for p, f in EX.items():
    s = open(os.path.join(repo, f), encoding="utf-8").read()
    slug = p.rstrip("/").rsplit("/", 1)[-1] if p.startswith(("/articles/", "/research/")) and p.count("/") == 3 else None
    # every page but home is served from a server-side copy of its live folder, so relative assets resolve; home points them at /
    s = patch(s, "explore", "/" if p == "/" else None, slug)
    dst = os.path.join(out, "explore", P.strip("/"), p.strip("/"), "index.html")
    os.makedirs(os.path.dirname(dst), exist_ok=True); open(dst, "w", encoding="utf-8").write(s); print("wrote", dst)
for p, f in ORG.items():
    s = open(os.path.join(orgdir, f), encoding="utf-8").read()
    s = patch(s, "org", p)
    dst = os.path.join(out, "org", P.strip("/"), p.strip("/"), "index.html")
    os.makedirs(os.path.dirname(dst), exist_ok=True); open(dst, "w", encoding="utf-8").write(s); print("wrote", dst)
for site in ("explore", "org"):
    a = os.path.join(out, site, P.strip("/"), "assets"); os.makedirs(os.path.join(a, "home"), exist_ok=True)
    for f in ("si-nav.js", "si-v4.css", "si-support.js", "home/si-sound.js"):
        open(os.path.join(a, f), "w", encoding="utf-8").write(open(os.path.join(repo, "assets", f), encoding="utf-8").read())
# plain-text agent files with the brand wording, for review
for f in ("agents.md", "llms.txt"):
    open(os.path.join(out, "explore", P.strip("/"), f), "w", encoding="utf-8").write(open(os.path.join(repo, f), encoding="utf-8").read())
