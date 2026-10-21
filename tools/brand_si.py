#!/usr/bin/env python3
"""'Explore' -> 'Explore Superintelligence' (room) / 'Explore SI' (compact). usage: brand_si.py ROOT [--org ORGDIR]
Every replacement is explicit and counted; prose that uses 'explore' as a verb is never touched. Prints a change log."""
import sys, os, re
ROOT = sys.argv[1]
FULL, SHORT = "Explore Superintelligence", "Explore SI"
MENU = [  # the shared v4 menu sheet + header (compact UI)
    ('Everything on <em>Explore</em></h2>', 'Everything on <em>Explore SI</em></h2>'),
    ('<small>About Explore</small>', '<small>About Explore SI</small>'),
]
SUP = [('<small>Email list · tips</small>Support Explore</a>', '<small>Email list · tips</small>Support Explore SI</a>')]
P = {
 "assets/si-v4.css": [("@media (max-width:899px){.brand span{display:none}}",
                       "@media (max-width:899px){.brand span{display:none}.brand:has(> span) b::after{content:\"\\00a0SI\"}}")],
 "assets/si-support.js": [("'<p class=\"sis-k\">Support Explore</p>'", "'<p class=\"sis-k\">Support Explore SI</p>'"),
                          ("'<p class=\"sis-lede\">Explore is free to read,", "'<p class=\"sis-lede\">Explore Superintelligence is free to read,")],
 "assets/home/si-sound.js": [("'<p class=\"wm\">Explore</p>", "'<p class=\"wm\">Explore Superintelligence</p>"),
                             (".wm{font-family:var(--serif,Georgia,serif);font-size:30px;letter-spacing:-.01em;margin:14px 0 4px}", ".wm{font-family:var(--serif,Georgia,serif);font-size:30px;letter-spacing:-.01em;margin:14px 0 4px;text-wrap:balance}")],
 "tools/support-cta/build_ieo.py": [('<a class="home" href="/">Explore home</a>', '<a class="home" href="/">Explore SI</a>')],
 "404.html": MENU,
 "index.html": MENU + SUP + [
    ('"name": "Get new Explore books"', '"name": "Get new Explore Superintelligence books"'),
    ('<p class="label">Superintelligent Silicon · <span class="accent">Explore</span></p>', '<p class="label">Superintelligent Silicon · <span class="accent">Explore SI</span></p>'),
    ('aria-haspopup="dialog">How Explore works</a>', 'aria-haspopup="dialog">How Explore SI works</a>'),
    ('<h2 id="more-h">Also on Explore</h2>', '<h2 id="more-h">Also on Explore SI</h2>'),
    ('<p class="one">Why Explore exists,', '<p class="one">Why Explore Superintelligence exists,'),
    ('<p class="label accent">About Explore</p>', '<p class="label accent">About Explore SI</p>'),
    ('aria-label="About Explore"', 'aria-label="About Explore Superintelligence"'),
    ('<p>Explore is the research side.', '<p>Explore Superintelligence is the research side.'),
    ('<p>Explore is the public research home', '<p>Explore Superintelligence is the public research home')],
 "about/index.html": MENU + SUP + [
    ('content="Research on Explore;', 'content="Research on Explore Superintelligence;', 2),
    ('<p class="label">About · <span class="accent">Explore</span></p>', '<p class="label">About · <span class="accent">Explore SI</span></p>'),
    ('aria-label="About Explore"', 'aria-label="About Explore Superintelligence"'),
    ('<li><strong>Explore</strong><span>', '<li><strong>Explore SI</strong><span>'),
    ('help bring Explore to life', 'help bring Explore Superintelligence to life'),
    ('<p class="note">Explore is brought to you', '<p class="note">Explore Superintelligence is brought to you'),
    ('If Explore’s research has been useful', 'If Explore Superintelligence’s research has been useful')],
 "articles/index.html": MENU + SUP + [('<p class="label">Explore · <span class="accent">Articles</span></p>', '<p class="label">Explore SI · <span class="accent">Articles</span></p>')],
 "research/index.html": MENU + [('<h2 id="elsewhere">Elsewhere on Explore</h2>', '<h2 id="elsewhere">Elsewhere on Explore SI</h2>')],
 "shipping/index.html": MENU + [('shared across the Explore home,', 'shared across the Explore Superintelligence home,'),
                                ('— how Explore relates to Grok Ai Apps', '— how Explore Superintelligence relates to Grok Ai Apps')],
 "sios/index.html": MENU + [('Also on Explore: <a href="/threshold/">', 'Also on Explore SI: <a href="/threshold/">')],
 "sios/shell/index.html": [('<a class="menu-link" href="https://exploresuperintelligence.online/">Explore</a>', '<a class="menu-link" href="https://exploresuperintelligence.online/">Explore SI</a>'),
                           ('· <a href="https://exploresuperintelligence.online/">Explore</a>', '· <a href="https://exploresuperintelligence.online/">Explore Superintelligence</a>')],
 "threshold/index.html": [('<a href="/">← Explore</a>', '<a href="/">← Explore SI</a>')],
 "have-you-seen/index.html": [('<a href="/">← Explore</a>', '<a href="/">← Explore SI</a>')],
 "articles/final-merge/index.html": [('<a href="/">Explore</a><span aria-hidden="true">/</span>', '<a href="/">Explore SI</a><span aria-hidden="true">/</span>'), ('<a href="/">Explore home</a>', '<a href="/">Explore SI</a>')],
 "articles/napkins-are-the-backbone/index.html": [('<a href="/">Explore</a><span aria-hidden="true">/</span>', '<a href="/">Explore SI</a><span aria-hidden="true">/</span>'), ('<a href="/">Explore home</a>', '<a href="/">Explore SI</a>')],
 "articles/well-be-right-back/index.html": [('<a href="/">Explore</a><span aria-hidden="true">/</span>', '<a href="/">Explore SI</a><span aria-hidden="true">/</span>'), ('<a href="/">Explore home</a>', '<a href="/">Explore SI</a>')],
 "articles/immortal-tombstones/index.html": [('<a href="/">Explore home</a>', '<a href="/">Explore SI</a>'), ('>Support Explore</a></p>', '>Support Explore SI</a></p>')],
 "articles/in-each-other/index.html": [('<a class="home" href="/">Explore home</a>', '<a class="home" href="/">Explore SI</a>', 2)],
 "articles/defrost-mode/index.html": [('</svg>Support Explore: new guides by email, tips</a>', '</svg>Support Explore SI: new guides by email, tips</a>')],
 "research/word-swap/index.html": [("<li class=\"toc-h\">Explore</li>", "<li class=\"toc-h\">Explore SI</li>"),
                                   ("<b>·</b>Support Explore<em>", "<b>·</b>Support Explore SI<em>"),
                                   ("keep Explore’s research going", "keep Explore Superintelligence’s research going", 2),
                                   ("you can support Explore’s research.", "you can support Explore Superintelligence’s research.", 2),
                                   ("helps support Explore’s research.", "helps support Explore Superintelligence’s research.", 2)],
 "research/word-swap.md": [("Explore research is supported via", "Explore Superintelligence research is supported via")],
 "agents.md": [("join the Explore email list", "join the Explore Superintelligence email list")],
 "llms.txt": [("and support Explore, the subscribe API", "and support Explore Superintelligence, the subscribe API"),
              ("beautifully designed long reads from Explore,", "beautifully designed long reads from Explore Superintelligence,"),
              ("): Explore is the research side;", "): Explore Superintelligence is the research side;"),
              ("The organization behind Explore.", "The organization behind Explore Superintelligence.")],
 "tools/support-cta/build_agents.py": [("join the Explore email list", "join the Explore Superintelligence email list"),
              ("and support Explore, the subscribe API", "and support Explore Superintelligence, the subscribe API")],
}
ORG = {
 "home.html": [('<a href="https://exploresuperintelligence.online/">Explore</a>\n            <a href="https://exploresuperintelligence.online/articles/">Articles</a>\n            <a href="https://exploresuperintelligence.online/threshold/">Threshold field guide</a>',
                '<a href="https://exploresuperintelligence.online/">Explore SI</a>\n            <a href="https://exploresuperintelligence.online/articles/">Articles</a>\n            <a href="https://exploresuperintelligence.online/threshold/">Threshold field guide</a>'),
               ('<nav aria-label="Superintelligent Silicon">\n              <a href="https://exploresuperintelligence.online/">Explore</a>',
                '<nav aria-label="Superintelligent Silicon">\n              <a href="https://exploresuperintelligence.online/">Explore Superintelligence</a>')],
 "contact.html": MENU + [('Write Superintelligent Silicon / the Explore team.', 'Write Superintelligent Silicon / the Explore SI team.'),
               ('<small>Public research</small>Explore</a>', '<small>Public research</small>Explore Superintelligence</a>')],
}
def apply(path, reps, log):
    s = open(path, encoding="utf-8").read()
    for r in reps:
        a, b = r[0], r[1]; n = r[2] if len(r) > 2 else 1
        c = s.count(a)
        if c != n: sys.exit(f"{path}: anchor x{c} (want {n}): {a[:80]!r}")
        s = s.replace(a, b); log.append((path, a, b, n))
    open(path, "w", encoding="utf-8").write(s)
def apply_org_contact_links(path, log):
    # contact page header/footer links to Explore: header (compact) -> Explore SI, footer -> full name
    s = open(path, encoding="utf-8").read()
    a = '<a href="https://exploresuperintelligence.online/">Explore</a>'
    idx = [m.start() for m in re.finditer(re.escape(a), s)]
    if len(idx) != 2: sys.exit(f"{path}: Explore links x{len(idx)}")
    s = s[:idx[1]] + a.replace(">Explore<", ">Explore Superintelligence<") + s[idx[1] + len(a):]
    s = s.replace(a, a.replace(">Explore<", ">Explore SI<"), 1)
    open(path, "w", encoding="utf-8").write(s); log.append((path, a, "header: Explore SI; footer: Explore Superintelligence", 2))
if __name__ == "__main__":
    log = []
    if "--org" in sys.argv:
        od = sys.argv[sys.argv.index("--org") + 1]
        for f, reps in ORG.items(): apply(os.path.join(od, f), reps, log)
        apply_org_contact_links(os.path.join(od, "contact.html"), log)
    else:
        for f, reps in P.items(): apply(os.path.join(ROOT, f), reps, log)
    for pth, a, b, n in log:
        print(f"- {os.path.relpath(pth, ROOT) if not pth.startswith('/') or ROOT in pth else pth} (x{n}): {re.sub(r'<[^>]+>', '', a)[:70]!r} -> {re.sub(r'<[^>]+>', '', b)[:80]!r}")
