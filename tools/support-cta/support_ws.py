#!/usr/bin/env python3
"""The Word Swap: quiet Support row in the Contents sheet + an email line in both existing tip boxes. usage: support_ws.py IN OUT"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
if "si-support-v1" in s: sys.exit("already patched")
SRC = "explore-book:word-swap"
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f"anchor x{n} (want {count}): {old[:90]!r}")
    s = s.replace(old, new)
# Contents sheet: one more row in the list's own style, under its own small heading
rep("""  h+='</ul>';
  openSheet("Contents",h);""",
    """  h+='<li class="toc-h">Explore</li><li><button type="button" data-ws-sup=""><b>·</b>Support Explore<em>email, tips</em></button></li>'; /* si-support-v1 */
  h+='</ul>';
  openSheet("Contents",h);""")
# the existing end-of-part tip boxes: add the email list beside the tips
rep('rel="noopener">$5</a></p>',
    'rel="noopener">$5</a> · <button type="button" class="si-sup-inl" data-ws-sup="email">New research by email</button></p>', count=2)
rep("</body>", f'''<script>var SI_SUPPORT_SRC = "{SRC}";
/* si-support-v1: shared Support sheet; close this guide's own sheet first */
document.addEventListener("click",function(e){{ var t=e.target.closest&&e.target.closest("[data-ws-sup]"); if(!t) return; e.preventDefault(); e.stopPropagation();
  var sh=document.getElementById("sheet"), f=t.getAttribute("data-ws-sup"); if(sh&&sh.classList.contains("on")){{ var x=document.querySelector("#sheet [data-close],#sheetX,#sheet .x"); if(x) x.click(); else {{ sh.classList.remove("on"); }} }}
  setTimeout(function(){{ if(window.SISupport) SISupport.open({{source:SI_SUPPORT_SRC,focus:f}}); }},0); }},true);</script>
<script src="/assets/si-support.js" defer></script>
</body>''')
open(dst, "w", encoding="utf-8").write(s); print("ok", dst, len(s))
