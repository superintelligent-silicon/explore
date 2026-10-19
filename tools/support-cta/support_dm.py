#!/usr/bin/env python3
"""Defrost Mode: quiet Support entry in the Chapters sheet + one chip on the last page. usage: support_dm.py IN OUT"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
if "si-support-v1" in s: sys.exit("already patched")
SRC = "explore-book:defrost-mode"
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f"anchor x{n} (want {count}): {old[:90]!r}")
    s = s.replace(old, new)
# Chapters sheet: a second quiet row under "All articles", same row style
rep('All articles on Explore Superintelligence</a></div>`); }',
    'All articles on Explore Superintelligence</a><a class="menu-out dm-sup" href="/about/#tip" data-dm-sup=""><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3.5" y="6" width="17" height="12" rx="2"/><path d="m4.5 7.5 7.5 6 7.5-6"/></svg>Support Explore: new guides by email, tips</a></div>`); }')
rep('.menu a.menu-out svg{color:var(--frost)}',
    '.menu a.menu-out svg{color:var(--frost)}\n/* si-support-v1 */ .menu a.menu-out.dm-sup{margin-top:0;border-top:0}')
# last page: one more chip in the closing row
rep('<button class="chip" type="button" id="toStart">Back to cover</button>',
    '<button class="chip" type="button" id="toStart">Back to cover</button>\n            <button class="chip" type="button" data-dm-sup="email">Get the next one by email</button>')
# open the shared sheet after closing this guide's own sheet
rep('$("#menuBtn").addEventListener("click",menuSheet);',
    '$("#menuBtn").addEventListener("click",menuSheet);\n'
    '/* si-support-v1: shared Support sheet (/assets/si-support.js) */\n'
    'document.addEventListener("click",e=>{ const t=e.target.closest("[data-dm-sup]"); if(!t) return; e.preventDefault(); e.stopPropagation();\n'
    '  const f=t.getAttribute("data-dm-sup"); if(sheet.classList.contains("on")) closeSheet(); setTimeout(()=>{ if(window.SISupport) SISupport.open({source:SI_SUPPORT_SRC,focus:f}); },0); },true);')
rep('</body>', f'<script>var SI_SUPPORT_SRC = "{SRC}", SI_SUPPORT_THEME = "dark";</script>\n<script src="/assets/si-support.js" defer></script>\n</body>')
open(dst, "w", encoding="utf-8").write(s); print("ok", dst, len(s))
