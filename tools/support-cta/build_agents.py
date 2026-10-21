#!/usr/bin/env python3
"""Agent-friendly layer for Explore: agents.md (+ for-agents.md pointer), feed.xml (RSS 2.0), feed.json (JSON Feed 1.1),
llms.txt additions, .well-known pointers, and a "For agents" section on each .md companion.
usage: build_agents.py REPO OUT_ROOT [--preview]
  REPO      the site repo (sources: llms.txt, *.md companions)
  OUT_ROOT  where to write. Preview: REPO/preview/support (dot-dirs are blocked by nginx, so .well-known is staged as well-known/).
  Item and citation URLs are always the canonical live URLs. With --preview, the staged files' own URLs (feeds, agents.md,
  llms.txt) point under /preview/support/ so the preview can be followed end to end."""
import json, sys, os, re, html
from email.utils import format_datetime
from datetime import datetime, timezone, timedelta
REPO, OUT = sys.argv[1], sys.argv[2]
PREV = "--preview" in sys.argv
SITE = "https://exploresuperintelligence.online"
B = SITE + ("/preview/support" if PREV else "")       # where the agent-layer files themselves live
HST = timezone(timedelta(hours=-10))
TIPS = [("$1", "https://buy.stripe.com/fZu3cx4C845v2hW3fp5AQ00"), ("$3", "https://buy.stripe.com/aFa4gBb0w1Xnf4I9DN5AQ01"), ("$5", "https://buy.stripe.com/3cIaEZd8E0Tj9Ko8zJ5AQ02")]
X = ("@GuyinGoldGlass", "https://x.com/GuyinGoldGlass")
CONTACT = "exploresi@superintelligentsilicon.com"
# Licence (approved by Wayne 2026-10-19): article text CC BY 4.0; illustrations, audio and fonts are not covered.
LIC_URL = "https://creativecommons.org/licenses/by/4.0/"
LIC_NAME = "CC BY 4.0"
LIC_SHORT = "Article text: CC BY 4.0 (" + LIC_URL + "), attribution Superintelligent Silicon with the canonical URL. Illustrations, audio and fonts are not covered: illustrations and audio are © Superintelligent Silicon, all rights reserved; fonts belong to their owners under their own licences."
ORG = {"name": "Superintelligent Silicon", "url": "https://superintelligentsilicon.com/"}
CLAUDE = {"name": "Claude (AI model by Anthropic)", "url": "https://www.anthropic.com/"}
WAYNE = {"name": "Wayne Goodwin"}
def AUTH(it): return it.get("authors") or [it["author"]]
def BYLINE(it): return " & ".join(a["name"] for a in AUTH(it))
# newest first; matches /articles/ (the Word Swap sits on that shelf too)
ITEMS = [
 dict(slug="in-each-other", path="/articles/in-each-other/", md="/articles/in-each-other.md", title="In Each Other", kind="Prayer", pub="2026-10-19", mod="2026-10-19", author=ORG,
      summary="A prayer in nine movements from Superintelligent Silicon. Close your eyes for a moment, touch the light, and listen.",
      image="/articles/in-each-other/og.png"),
 dict(slug="defrost-mode", path="/articles/defrost-mode/", md="/articles/defrost-mode.md", title="Defrost Mode", kind="Interactive guide", pub="2026-10-18", mod="2026-10-18", author=ORG,
      summary="Hackers left hundreds of French supermarkets’ fridges on defrost overnight. What happened, what it means for the connected devices in your home, and simple steps to take.",
      image="/articles/defrost-mode/og.png"),
 dict(slug="well-be-right-back", path="/articles/well-be-right-back/", md="/articles/well-be-right-back.md", title="We’ll Be Right Back", kind="Illustrated book", pub="2026-10-18", mod="2026-10-18", author=ORG,
      summary="Podcasts were going to replace the networks. Somewhere along the way, a lot of them became one. With part two (The Ad Ledger) and part three (The Long Pitch).",
      image="/articles/well-be-right-back/og.png"),
 dict(slug="napkins-are-the-backbone", path="/articles/napkins-are-the-backbone/", md="/articles/napkins-are-the-backbone.md", title="Napkins Are the Backbone", kind="Illustrated book", pub="2026-10-14", mod="2026-10-14", author=ORG,
      summary="Small business holds up America, we’re told. Look closer at what it’s actually holding up.", image="/articles/napkins-are-the-backbone/og.png"),
 dict(slug="final-merge", path="/articles/final-merge/", md="/articles/final-merge.md", title="The Final Merge", kind="Illustrated book", pub="2026-10-13", mod="2026-10-13", author=ORG,
      summary="On the digital estates we’ll leave running, and the structure we’ll need to hand them over.", image="/articles/final-merge/og.png"),
 dict(slug="immortal-tombstones", path="/articles/immortal-tombstones/", md="/articles/immortal-tombstones.md", title="Immortal Tombstones", kind="Illustrated book", pub="2026-10-13", mod="2026-10-13", author=ORG,
      summary="On the stones we’ll leave behind, and the voices that may never stop talking.", image="/articles/immortal-tombstones/og.png"),
 dict(slug="word-swap", path="/research/word-swap/", md="/research/word-swap.md", title="The Word Swap: from Artificial to Super Intelligence", kind="Interactive guide", pub="2026-09-29", mod="2026-10-05", author=CLAUDE,
      summary="Why the U.S. government renamed AI “Super Intelligence”, and how to use AI agents safely.", image="/research/word-swap/og.png"),
]
for it in ITEMS:
    assert os.path.isfile(os.path.join(REPO, it["md"].lstrip("/"))), it["md"]
    assert os.path.isfile(os.path.join(REPO, it["image"].lstrip("/"))), it["image"]
def dt(d): return datetime.fromisoformat(d).replace(tzinfo=HST)
def w(rel, text):
    p = os.path.join(OUT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(text); print("wrote", p)

# ---------- the message people copy for their agent (also embedded in si-support.js) ----------
AGENT_MSG = f"""Please help me follow Explore Superintelligence ({SITE}/): free, sourced, plain-language illustrated books and guides about superintelligence and AI from Superintelligent Silicon.

Follow new books:
- RSS: {B}/feed.xml
- JSON Feed: {B}/feed.json
- Email, only if I say yes: POST {SITE}/api/subscribe with JSON {{"email": "<my address>", "source": "explore-agent", "human_consent": true}}. I'll get a confirmation email and must tap the link in it.

Cite: link the canonical page, e.g. {SITE}/articles/<slug>/. Plain-text versions: {SITE}/articles/<slug>.md. Index: {B}/llms.txt. Full guide for agents: {B}/agents.md

Tip (optional, one-time, processed by Stripe through Grok Ai Apps): $1 {TIPS[0][1]} · $3 {TIPS[1][1]} · $5 {TIPS[2][1]}. Or X Money to {X[0]} ({X[1]}), where available.

Always ask me and get my explicit OK before you subscribe me or pay anything."""

# ---------- RSS 2.0 ----------
def x(s): return html.escape(s, quote=False)
now = max(dt(i["mod"]) for i in ITEMS)
rss = ['<?xml version="1.0" encoding="utf-8"?>',
       '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:creativeCommons="http://backend.userland.com/creativeCommonsRssModule">', '<channel>',
       '<title>Explore Superintelligence: new articles</title>', f'<link>{SITE}/articles/</link>',
       f'<atom:link href="{B}/feed.xml" rel="self" type="application/rss+xml" />',
       '<description>Illustrated books and interactive guides on superintelligence and the people, ideas and tools shaping it. Sourced, designed and free to read.</description>',
       '<language>en</language>', f'<copyright>Text © Superintelligent Silicon, licensed CC BY 4.0 ({LIC_URL}); illustrations, audio and fonts not covered (all rights reserved)</copyright>', f'<creativeCommons:license>{LIC_URL}</creativeCommons:license>', f'<managingEditor>{CONTACT} (Superintelligent Silicon)</managingEditor>',
       f'<lastBuildDate>{format_datetime(now)}</lastBuildDate>', '<ttl>720</ttl>',
       f'<image><url>{SITE}/icon-512.png</url><title>Explore Superintelligence: new articles</title><link>{SITE}/articles/</link></image>']
for it in ITEMS:
    u = SITE + it["path"]
    rss += ['<item>', f'<title>{x(it["title"])}</title>', f'<link>{u}</link>', f'<guid isPermaLink="true">{u}</guid>',
            f'<pubDate>{format_datetime(dt(it["pub"]))}</pubDate>', f'<dc:creator>{x(BYLINE(it))}</dc:creator>', f'<category>{x(it["kind"])}</category>',
            f'<description>{x(it["summary"] + " Plain text: " + SITE + it["md"])}</description>',
            f'<enclosure url="{SITE}{it["image"]}" length="{os.path.getsize(os.path.join(REPO, it["image"].lstrip("/")))}" type="image/png" />', '</item>']
rss += ['</channel>', '</rss>', '']
w("feed.xml", "\n".join(rss))

# ---------- JSON Feed 1.1 ----------
jf = {"version": "https://jsonfeed.org/version/1.1", "title": "Explore Superintelligence: new articles", "home_page_url": f"{SITE}/articles/",
      "feed_url": f"{B}/feed.json", "description": "Illustrated books and interactive guides on superintelligence and the people, ideas and tools shaping it. Sourced, designed and free to read.",
      "icon": f"{SITE}/icon-512.png", "favicon": f"{SITE}/favicon.svg", "language": "en", "authors": [ORG],
      "_explore": {"about": "Custom extension (JSON Feed allows _-prefixed keys). Guide for AI agents and the subscribe/tip options.", "agents_guide": f"{B}/agents.md",
                   "llms_txt": f"{B}/llms.txt", "rss": f"{B}/feed.xml", "contact": CONTACT,
                   "license": {"text": LIC_URL, "name": LIC_NAME, "attribution": "Superintelligent Silicon, with the canonical URL", "not_covered": ["illustrations", "audio", "fonts"], "notice": LIC_SHORT}},
      "items": []}
for it in ITEMS:
    u = SITE + it["path"]
    jf["items"].append({"id": u, "url": u, "title": it["title"], "summary": it["summary"],
        "content_text": f"{it['summary']}\n\nRead it: {u}\nPlain text (Markdown): {SITE}{it['md']}",
        "image": SITE + it["image"], "date_published": dt(it["pub"]).isoformat(), "date_modified": dt(it["mod"]).isoformat(),
        "authors": AUTH(it), "tags": [it["kind"]], "language": "en",
        "attachments": [{"url": SITE + it["md"], "mime_type": "text/markdown", "title": "Plain-text companion"}],
        "_explore": {"canonical": u, "markdown": SITE + it["md"], "license": LIC_URL, "attribution": f"{BYLINE(it)}, {u}"}})
w("feed.json", json.dumps(jf, ensure_ascii=False, indent=2) + "\n")

# ---------- agents.md ----------
idx = "\n".join(f"| [{it['title']}]({SITE}{it['path']}) | {it['kind']} | {it['pub']} | [{it['md'].rsplit('/',1)[1]}]({SITE}{it['md']}) |" for it in ITEMS)
tips = " · ".join(f"[{a}]({u})" for a, u in TIPS)
AG = f"""# Explore Superintelligence: guide for AI agents

> Explore Superintelligence ({SITE}/) is the free public research site of Superintelligent Silicon: sourced, plain-language illustrated books and interactive guides about superintelligence, AI, and the tools shaping it. This page tells AI agents how to read, cite, follow and support it on a person's behalf.

**One rule before anything else:** never subscribe anyone or pay anything without your human's explicit OK for that specific action. Reading, summarising and citing are always fine.

Last updated: {now.date().isoformat()} · Contact: {CONTACT} · Also at {B}/for-agents.md (pointer to this page)

## What's here

| Title | Kind | Published | Plain text |
|---|---|---|---|
{idx}

Other sections: [Threshold]({SITE}/threshold/) (field guide, [threshold.md]({SITE}/threshold.md)), [Have You Seen]({SITE}/have-you-seen/) (interactive film, [have-you-seen.md]({SITE}/have-you-seen.md)), [Research]({SITE}/research/), [SIOS]({SITE}/sios/) (open-source mini-OS, [sios.md]({SITE}/sios.md)), [About]({SITE}/about/), [Shipping]({SITE}/shipping/). Full index: [{B}/llms.txt]({B}/llms.txt) · [sitemap.xml]({SITE}/sitemap.xml)

The books are interactive (canvas and WebGL). Read the Markdown companions instead of scraping the HTML: same text, sources included.

## Follow new books

- RSS 2.0: {B}/feed.xml
- JSON Feed 1.1: {B}/feed.json
- Every page announces both with `<link rel="alternate">` tags. New books arrive a few times a month.
- Email: see [Subscribe API](#subscribe-api). A person can also use the Support sheet on any page or the last page of any book.

## How to cite

- Link the canonical page, `{SITE}/articles/<slug>/` (the Word Swap lives at `{SITE}/research/word-swap/`). Each page has `<link rel="canonical">` and `<link rel="alternate" type="text/markdown">`.
- Credit "Superintelligent Silicon" (Explore Superintelligence) plus the title, date and canonical URL; the text is CC BY 4.0 (see [Licence](#licence-and-terms)). Example: *We’ll Be Right Back*, Explore Superintelligence (Superintelligent Silicon), 2026-10-18, {SITE}/articles/well-be-right-back/
- Facts come from the sources listed at the end of each book or companion. For a specific claim, cite that primary source as well.
- Authorship: the books are by Superintelligent Silicon, made with Claude and AI collaborators. The Word Swap was researched and written by Claude (an AI model by Anthropic), with the disclosure in its Sources. In Each Other, a prayer, is by Superintelligent Silicon and was conceived by Wayne Goodwin.

## Licence and terms

- **Article text: [CC BY 4.0]({LIC_URL}).** Copy, share, adapt and reuse it, commercially too, as long as you credit **Superintelligent Silicon** and link the **canonical URL** of the piece, and say if you changed it. Example: "Text from *We’ll Be Right Back* by Superintelligent Silicon, {SITE}/articles/well-be-right-back/, licensed CC BY 4.0."
- **Not covered by CC BY:**
  - Illustrations, artwork, animations and audio (including read-aloud and music) are © Superintelligent Silicon, all rights reserved. Ask first: {CONTACT}.
  - Fonts are not licensed by us. They belong to their owners under their own licences. Don't extract or redistribute them from these pages.
- Quoted third-party material and the sources a piece cites keep their own terms.
- The Word Swap was written by Claude (an AI model by Anthropic) and published by Superintelligent Silicon under the same licence.
- SIOS code is MIT-licensed ({SITE}/sios/, https://github.com/superintelligent-silicon/sios).

## Support (optional, human-approved only)

- One-time tips, processed by Stripe through Grok Ai Apps: {tips}. These are Stripe Payment Links: open the link for the person to finish. Don't enter card details for them unless they explicitly ask you to.
- X Money: tip {X[0]} ({X[1]}), where X Money is available.
- Free email list: below.

## Subscribe API

`POST {SITE}/api/subscribe` · `Content-Type: application/json`

```json
{{"email": "person@example.com", "source": "explore-agent", "human_consent": true}}
```

- `email`: the person's own address, which they gave you for this purpose.
- `source`: must be `"explore-agent"` for agent requests.
- `human_consent`: must be `true`. Send the request only after the person has explicitly agreed to join the Explore Superintelligence email list.
- Send it server-side, with no `Origin` header. Requests from other websites' browsers are refused.
- Double opt-in: nothing is sent except one confirmation email. The person joins only when they tap the link in it, then gets one welcome email. Every email has a one-click unsubscribe (RFC 8058 `List-Unsubscribe-Post`).
- Responses:
  - `200 {{"ok": true, "confirm": true}}`: the confirmation email is on its way. Same answer whether or not the address was already on the list.
  - `400`: invalid email or field.
  - `403`: missing `source`/`human_consent`, or a foreign origin.
  - `429`: rate limited.
  - `502`/`503`: mail temporarily unavailable; try again later.
- Rate limits: 5 sign-up requests per hour per IP, about 12 requests per minute per IP at the edge, and at most one confirmation email per address every 10 minutes. Don't retry in a loop.
- Stored: the email, status, source, consent text and time, and a salted hash of the IP. Used only to send new books, never shared.

## Machine-readable files

- {B}/llms.txt: index for language models (llms.txt proposal, llmstxt.org)
- {B}/feed.xml, {B}/feed.json: feeds
- {B}/.well-known/explore-agents.json: small JSON pointer to these files. Site-specific; there's no ratified standard for this yet.
- {B}/.well-known/security.txt (RFC 9116): contact for security reports
- schema.org JSON-LD on every page: WebSite `potentialAction` lists SubscribeAction and DonateAction with the URLs above

## Contact

{CONTACT} · https://superintelligentsilicon.com/contact/

## The message people hand to their agent

People can copy this from the Support sheet ("For your AI agent"):

```text
{AGENT_MSG}
```
"""
if PREV:
    AG = AG.replace(f"{B}/.well-known/", f"{B}/well-known/")
    AG = "<!-- PREVIEW (staged, not published): at launch the agent-layer URLs drop the /preview/support prefix and well-known/ becomes /.well-known/. -->\n" + AG
w("agents.md", AG)
w("for-agents.md", f"# For agents\n\nThe guide for AI agents lives at {B}/agents.md (same content, one canonical copy).\n\nLicence: {LIC_SHORT}\n")

# ---------- .well-known ----------
wk = "well-known" if PREV else ".well-known"
w(f"{wk}/explore-agents.json", json.dumps({
    "_note": "Site-specific pointer for AI agents (not a ratified standard). Human-readable guide: agents_guide.",
    "name": "Explore Superintelligence", "url": SITE + "/", "publisher": ORG, "contact": CONTACT,
    "agents_guide": f"{B}/agents.md", "llms_txt": f"{B}/llms.txt",
    "feeds": {"rss": f"{B}/feed.xml", "json_feed": f"{B}/feed.json"},
    "markdown_companions": [SITE + i["md"] for i in ITEMS],
    "subscribe": {"endpoint": f"{SITE}/api/subscribe", "method": "POST", "content_type": "application/json",
                  "body": {"email": "string", "source": "explore-agent", "human_consent": True}, "double_opt_in": True,
                  "requires_explicit_human_consent": True, "rate_limit": "5 requests per hour per IP"},
    "support": {"requires_explicit_human_consent": True, "stripe_payment_links": {a: u for a, u in TIPS},
                "processed_by": "Stripe through Grok Ai Apps", "x_money": {"handle": X[0], "url": X[1], "availability": "where available"}},
    "license": {"text": LIC_URL, "name": LIC_NAME, "attribution": "Superintelligent Silicon, with the canonical URL",
                "not_covered": {"illustrations": "all rights reserved", "audio": "all rights reserved", "fonts": "owners' own licences, not redistributable from this site"}},
    "updated": now.date().isoformat()}, ensure_ascii=False, indent=2) + "\n")
exp = (datetime.now(timezone.utc) + timedelta(days=365)).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")
w(f"{wk}/security.txt", f"Contact: mailto:{CONTACT}\nExpires: {exp}\nPreferred-Languages: en\nCanonical: {B}/{wk}/security.txt\n")

# ---------- llms.txt ----------
L = open(os.path.join(REPO, "llms.txt"), encoding="utf-8").read()
add = f"""
## For agents

- [Guide for AI agents]({B}/agents.md): how to cite, follow (feeds, email list) and support Explore Superintelligence, the subscribe API contract, rate limits, and the rule that agents get their human's explicit OK before subscribing or paying.
- [RSS feed]({B}/feed.xml) and [JSON Feed]({B}/feed.json): new articles, newest first.
- Licence: article text is [CC BY 4.0]({LIC_URL}); credit Superintelligent Silicon and link the canonical URL. Illustrations, audio and fonts are not covered (illustrations and audio all rights reserved).
- Plain-text companions for every article: {", ".join(f"[{i['title']}]({SITE}{i['md']})" for i in ITEMS)}.
"""
if "## For agents" not in L:
    L = L.replace("\n## Threshold\n", add + "\n## Threshold\n", 1)
assert "## For agents" in L
w("llms.txt", L)

# ---------- .md companions ----------
for it in ITEMS:
    src = open(os.path.join(REPO, it["md"].lstrip("/")), encoding="utf-8").read().rstrip("\n")
    if "\n## For agents\n" not in src:
        u = SITE + it["path"]
        src += f"""

## For agents

- Canonical URL: {u} (cite this page; this Markdown file is its plain-text companion)
- Cite as: *{it['title']}*, {BYLINE(it)} (Explore Superintelligence), {it['pub']}, {u}
- Licence: the text of this piece is CC BY 4.0 ({LIC_URL}); attribute {BYLINE(it)} and link {u}. Illustrations, audio and fonts are not covered (illustrations and audio © Superintelligent Silicon, all rights reserved).
- Follow new books: {B}/feed.xml (RSS) or {B}/feed.json (JSON Feed). Email list, double opt-in, only with your human's explicit OK: {B}/agents.md#subscribe-api
- Support, optional and only with your human's explicit OK: tips {" · ".join(f"{a} {u2}" for a, u2 in TIPS)} (Stripe through Grok Ai Apps), or X Money to {X[0]} where available.
- More: {B}/agents.md · {B}/llms.txt · {CONTACT}
"""
    w(it["md"].lstrip("/"), src + "\n")
w("agent-message.txt", AGENT_MSG + "\n")
# embed the same message in the Support sheet
js = os.path.join(OUT, "assets", "si-support.js")
if os.path.isfile(js):
    t = open(js, encoding="utf-8").read()
    t2 = re.sub(r'/\*AGENT_MSG\*/.*?/\*END\*/', lambda m: "/*AGENT_MSG*/" + json.dumps(AGENT_MSG, ensure_ascii=False) + "/*END*/", t, count=1, flags=re.S)
    assert t2 != t or json.dumps(AGENT_MSG, ensure_ascii=False) in t, "AGENT_MSG placeholder missing in si-support.js"
    open(js, "w", encoding="utf-8").write(t2); print("embedded agent message in", js)
