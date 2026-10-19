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
# phone fit (390x664): the 6-book list and the About header no longer push the page past one screen
FIT = {
 "articles": "@media (max-width:759px) and (max-height:760px){ main>.wrap{gap:14px;padding-top:16px} .ac{grid-template-columns:52px minmax(0,1fr);gap:12px;padding:8px 0} .ac .art{width:52px;height:52px;border-radius:9px} .ac h2{font-size:17.5px} .ac .kind{font-size:10.5px} } @media (max-width:759px) and (max-height:680px){ .ac{padding:6px 0} .page-h1{font-size:30px} }",
 "about": "@media (max-width:759px) and (max-height:760px){ main>.wrap{gap:12px;padding-top:16px;padding-bottom:10px} .page-h1{font-size:34px} .ab-h .label{margin-bottom:6px} .ab-h .intro{margin-top:8px;font-size:14px;line-height:1.45} .tabs{margin-top:0} .blk{padding:12px 14px 4px} .blk li{padding:7px 0;font-size:13.5px;line-height:1.45} .blk .note{font-size:13.5px} } @media (max-width:759px) and (max-height:900px){ main:has(#support-p:not([hidden])) .ab-h .intro{display:none} }",
}
if kind in FIT:
    rep('  </style>\n</head>', f'    /* si-support-v1 phone fit */ {FIT[kind]}\n  </style>\n</head>')
# feed autodiscovery + agent guide pointers (every page)
fp = "/preview/support" if prev else ""
heads = (f'  <link rel="alternate" type="application/rss+xml" title="Explore Superintelligence: new articles (RSS)" href="{fp}/feed.xml" />\n'
         f'  <link rel="alternate" type="application/feed+json" title="Explore Superintelligence: new articles (JSON Feed)" href="{fp}/feed.json" />\n'
         f'  <link rel="help" type="text/markdown" title="Guide for AI agents" href="{fp}/agents.md" />\n')
rep('  <link rel="stylesheet" href="/assets/si-v4.css" />\n', '  <link rel="stylesheet" href="/assets/si-v4.css" />\n' + heads)
tag = f'  <script src="{asset}" defer></script><!-- si-support-v1 -->\n'
rep('  <script src="/assets/si-theme.js"></script>\n', '  <script src="/assets/si-theme.js"></script>\n' + tag)
if kind == "home":
    import json, re
    m = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)', s, re.S)
    d = json.loads(m.group(2)); site = [n for n in d["@graph"] if n.get("@type") == "WebSite"][0]
    S = "https://exploresuperintelligence.online"
    site["potentialAction"] = [
      {"@type": "SubscribeAction", "name": "Get new Explore books", "description": "Follow new articles by feed, or join the free email list (double opt-in; agents need their human's explicit consent).",
       "target": [{"@type": "EntryPoint", "urlTemplate": S + "/feed.xml", "contentType": "application/rss+xml"},
                  {"@type": "EntryPoint", "urlTemplate": S + "/feed.json", "contentType": "application/feed+json"},
                  {"@type": "EntryPoint", "urlTemplate": S + "/api/subscribe", "httpMethod": "POST", "contentType": "application/json", "description": "Body: {email, source: explore-agent, human_consent: true}. See " + S + "/agents.md"}]}] + [
      {"@type": "DonateAction", "name": f"Tip {a}", "description": "Optional one-time tip, processed by Stripe through Grok Ai Apps.", "price": a.strip("$") + ".00", "priceCurrency": "USD",
       "target": {"@type": "EntryPoint", "urlTemplate": u}} for a, u in [("$1", "https://buy.stripe.com/fZu3cx4C845v2hW3fp5AQ00"), ("$3", "https://buy.stripe.com/aFa4gBb0w1Xnf4I9DN5AQ01"), ("$5", "https://buy.stripe.com/3cIaEZd8E0Tj9Ko8zJ5AQ02")]]
    site["license"] = "https://creativecommons.org/licenses/by/4.0/"
    site["copyrightHolder"] = {"@id": "https://superintelligentsilicon.com/#org"}
    site["copyrightNotice"] = "Article text © Superintelligent Silicon, licensed CC BY 4.0: attribute Superintelligent Silicon with the canonical URL. Illustrations, audio and fonts are not covered (illustrations and audio all rights reserved; fonts under their owners' licences)."
    site["subjectOf"] = {"@type": "DigitalDocument", "name": "Guide for AI agents", "url": S + "/agents.md", "encodingFormat": "text/markdown"}
    s = s[:m.start(2)] + "\n" + json.dumps(d, ensure_ascii=False, indent=2) + "\n  " + s[m.end(2):]
if prev:
    s = s.replace('<head>', '<head>\n  <meta name="robots" content="noindex, nofollow" />', 1)
    for b in ("well-be-right-back", "napkins-are-the-backbone"):
        s = s.replace(f'href="/articles/{b}/"', f'href="/preview/support/articles/{b}/"')
    s = s.replace('href="/articles/"', 'href="/preview/support/articles/"').replace('href="/about/"', 'href="/preview/support/about/"').replace('<a href="/">Home</a>', '<a href="/preview/support/">Home</a>')
open(dst, "w", encoding="utf-8").write(s); print("ok", dst)
