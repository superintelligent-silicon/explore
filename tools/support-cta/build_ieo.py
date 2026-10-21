#!/usr/bin/env python3
"""Publish In Each Other at /articles/in-each-other/ from the approved preview build.
usage: build_ieo.py PREVIEW_INDEX OUT_INDEX"""
import sys, json
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
S = "https://exploresuperintelligence.online"; U = S + "/articles/in-each-other/"; SLUG = "in-each-other"; BSRC = "explore-book:" + SLUG
BY = "Superintelligent Silicon"
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f"anchor x{n} (want {count}): {old[:90]!r}")
    s = s.replace(old, new)
DESC = "In Each Other, a prayer in nine movements from Superintelligent Silicon. Touch the light to spread color, or listen to it read aloud."
rep('<meta name="description" content="In Each Other, a prayer in nine movements by Wayne Goodwin. Touch the light to spread color.">', f'<meta name="description" content="{DESC}">')
rep('<meta property="og:description" content="A prayer in nine movements by Wayne Goodwin.">', '<meta property="og:description" content="A prayer in nine movements from Superintelligent Silicon.">')
rep('<meta property="og:type" content="website">', f'''<meta property="og:type" content="article">
<meta property="og:site_name" content="Explore Superintelligence">
<meta property="og:url" content="{U}">
<meta property="og:image" content="{U}og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="In Each Other: a prayer in nine movements">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="In Each Other">
<meta name="twitter:description" content="A prayer in nine movements from Superintelligent Silicon.">
<meta name="twitter:image" content="{U}og.png">''')
NOTE = "Text © Superintelligent Silicon, licensed CC BY 4.0: attribute Superintelligent Silicon with the canonical URL. The audio narration and the illustrations (the interactive light) are © Superintelligent Silicon, all rights reserved; fonts are under their owners' licences."
ld = {"@context": "https://schema.org", "@graph": [
  {"@type": "CreativeWork", "@id": U + "#work", "name": "In Each Other", "headline": "In Each Other", "alternativeHeadline": "A prayer in nine movements",
   "genre": "Prayer", "description": DESC, "url": U, "mainEntityOfPage": U, "inLanguage": "en",
   "image": {"@type": "ImageObject", "url": U + "og.png", "width": 1200, "height": 630},
   "datePublished": "2026-10-19", "dateModified": "2026-10-19",
   "author": {"@type": "Organization", "@id": "https://superintelligentsilicon.com/#org", "name": "Superintelligent Silicon", "url": "https://superintelligentsilicon.com/"},
   "contributor": {"@type": "Person", "name": "Wayne Goodwin", "description": "Conceived by Wayne Goodwin"},
   "publisher": {"@type": "Organization", "@id": "https://superintelligentsilicon.com/#org", "name": "Superintelligent Silicon", "url": "https://superintelligentsilicon.com/"},
   "isPartOf": {"@type": "CollectionPage", "@id": S + "/articles/#page"},
   "license": "https://creativecommons.org/licenses/by/4.0/", "copyrightNotice": NOTE, "copyrightYear": 2026,
   "copyrightHolder": {"@type": "Organization", "name": "Superintelligent Silicon", "url": "https://superintelligentsilicon.com/"},
   "audio": {"@type": "AudioObject", "name": "In Each Other, read aloud", "contentUrl": U + "narration-am_michael.mp3", "encodingFormat": "audio/mpeg", "duration": "PT1M7S",
             "license": U + "#rights", "copyrightNotice": "© Superintelligent Silicon, all rights reserved.", "copyrightHolder": {"@type": "Organization", "name": "Superintelligent Silicon"}},
   "encoding": {"@type": "MediaObject", "contentUrl": S + "/articles/in-each-other.md", "encodingFormat": "text/markdown"}},
  {"@type": "BreadcrumbList", "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Explore Superintelligence", "item": S + "/"},
    {"@type": "ListItem", "position": 2, "name": "Articles", "item": S + "/articles/"},
    {"@type": "ListItem", "position": 3, "name": "In Each Other", "item": U}]}]}
rep('<meta name="robots" content="noindex, nofollow">', f'''<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="author" content="Superintelligent Silicon">
<link rel="canonical" href="{U}">
<link rel="alternate" type="text/markdown" href="{S}/articles/in-each-other.md" title="Plain-text edition">
<link rel="alternate" type="application/rss+xml" title="Explore Superintelligence: new articles (RSS)" href="/feed.xml">
<link rel="alternate" type="application/feed+json" title="Explore Superintelligence: new articles (JSON Feed)" href="/feed.json">
<link rel="help" type="text/markdown" title="Guide for AI agents" href="/agents.md">
<link rel="license" href="https://creativecommons.org/licenses/by/4.0/">
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
</script>''')
# bylines (subtle, same mono style)
rep('<div class="by">Words by Wayne Goodwin</div>', f'<div class="by">{BY}</div>')
rep('<span class="by">Wayne Goodwin</span>', f'<span class="by">{BY}<span class="cv">Conceived by Wayne Goodwin.</span></span>')
rep("artist:'Words by Wayne Goodwin'", "artist:'Superintelligent Silicon'")
# quiet way back: All articles · Explore home (splash and the whole-prayer sheet); Support tucked into the sheet
HOMES = '<nav class="homes" aria-label="Leave the prayer"><a class="home" href="/articles/">← All articles</a><span aria-hidden="true">·</span><a class="home" href="/">Explore SI</a>'
rep('    <a class="home" href="/">← Explore Superintelligence</a>`;', f'    {HOMES}</nav>`;')
rep('    <a class="home sheet-home" href="/">← Explore Superintelligence</a>',
    f'    {HOMES.replace("class=\"homes\"", "class=\"homes sheet-home\"")}<span aria-hidden="true">·</span><button type="button" class="home" data-si-support="{BSRC}">Support</button></nav>')
# End: one quiet line under the last movement's buttons
rep('''<button class="ghost" data-act="whole">Read it whole</button></div>`;''',
    f'''<button class="ghost" data-act="whole">Read it whole</button></div><p class="sup-end"><button type="button" class="home" data-si-support="{BSRC}" data-si-focus="email">New books by email</button><span aria-hidden="true">·</span><button type="button" class="home" data-si-support="{BSRC}">Support</button></p>`;''')
rep('.home:hover,.home:focus-visible{color:var(--gold)}',
    '.home:hover,.home:focus-visible{color:var(--gold)}\n'
    '/* si-support-v1: way back + quiet support line */\n'
    '.homes,.sup-end{display:flex;flex-wrap:wrap;align-items:center;gap:0 10px;margin:0;align-self:flex-start}\n'
    '.homes>span,.sup-end>span{font:400 11px/1 var(--f-mono);color:var(--muted);opacity:.6}\n'
    'button.home{appearance:none;border:0;background:none;cursor:pointer;padding:12px 0;margin:-12px 0}\n'
    
    '.sup-end{margin-top:-6px}\n.sup-end .home{margin:0}\n.by{text-wrap:balance}\n.by .cv{display:block;margin-top:1px;text-transform:none;letter-spacing:.02em;opacity:.75}\n'
    '.homes.sheet-home{display:flex;margin-top:2px}')
rep('</body>', f'<script>var SI_SUPPORT_SRC = "{BSRC}";</script>\n<script src="/assets/si-support.js" defer></script>\n</body>')
open(dst, "w", encoding="utf-8").write(s); print("ok", dst, len(s))
