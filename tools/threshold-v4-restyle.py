#!/usr/bin/env python3
"""Threshold v4 restyle (preview). Reads the Threshold source from the ex3 repo (v4-phase2 branch: includes the corner home mark),
remaps palette/fonts/backgrounds to the Explore v4 system, keeps all markup, content, animation and interaction code."""
import re, subprocess, sys
SRC = subprocess.run(["git","-C","/workspace/ex3","show","v4-phase2:threshold/index.html"],capture_output=True,text=True,check=True).stdout
s = SRC
n0 = len(s)
def rep(old, new, count=1, must=True):
    global s
    c = s.count(old)
    if must and c < 1: sys.exit(f"MISSING: {old[:80]}")
    s = s.replace(old, new) if count == 0 else s.replace(old, new, count)

# ---------- 1. fonts: Geist -> Inter (UI) + Newsreader (display/serif) ----------
rep('https://fonts.googleapis.com/css2?family=Geist:wght@300..800&family=Geist+Mono:wght@400;500&family=Newsreader:ital,opsz,wght@0,6..72,300..600;1,6..72,300..500&display=swap',
    'https://fonts.googleapis.com/css2?family=Inter:wght@400..700&family=Newsreader:ital,opsz,wght@0,6..72,300..600;1,6..72,300..500&display=swap')
rep('--sans:"Geist",-apple-system,BlinkMacSystemFont,"SF Pro Text","Segoe UI",system-ui,sans-serif;',
    '--sans:"Inter","SF Pro Text",-apple-system,BlinkMacSystemFont,"Helvetica Neue",Arial,sans-serif;')
rep('--mono:"Geist Mono",ui-monospace,"SF Mono",Menlo,Consolas,monospace;',
    '--mono:"Inter","SF Pro Text",-apple-system,BlinkMacSystemFont,"Helvetica Neue",Arial,sans-serif;')

# ---------- 2. palette: neon/space colours -> v4 warm paper, deep neutral, gold ----------
# (case-insensitive; applies to CSS '#rrggbb' and JS 0xRRGGBB alike, so 3D materials follow the same muted family)
MAP = {
 # light-theme base + ink
 "F3F3F1":"F6F3EC","E9E9E6":"EFEADF","141418":"1B1916","45444C":"4D4840","77767D":"6B655B","E9E7E2":"EFEADF",
 # light accents / chapter colours
 "0A9A85":"8A6210","0A917D":"8A6210","6646EA":"45607F","5B3FE0":"45607F","B57400":"66682A","A86F00":"7A5A14",
 "CF3F86":"8C4A5C","D9572A":"A24F2A","D2482A":"A24F2A","2F7BEA":"3F6489","4E8F12":"5B6B23",
 "7B61F2":"7A5610","119F8B":"B5862C","C08A22":"8A6210","D45A98":"8C4A5C",
 # dark base + ink
 "131315":"141416","1D1D21":"1C1C1F","26262B":"232327","F2F0EB":"ECEBE7","C2C0BA":"B9B6AF","8E8C86":"97938B",
 "050608":"141416","0E0F13":"1C1C1F","16171B":"1C1C1F","202126":"232327","F4F2ED":"ECEBE7","CBC9C3":"B9B6AF","8F8D87":"97938B",
 # dark accents / chapter colours / iridescence
 "5EE0C8":"D8B160","A994FF":"9FB3CF","B5A2FF":"A9BAD2","C2B2FF":"B4C2D8","FFC864":"E3C27E","FFD892":"F0D9A0",
 "FF9CCB":"D99AAE","FF8FC4":"D99AAE","FF9C6E":"E09A74","FF8E6E":"E09A74","B8F23E":"B5C07A","7FB8FF":"94B4D6","FFB28E":"E3A88A",
 "b9c3ff":"cfc8b8","bfefff":"e6dcc4","9fe9ff":"e3d3a8","bfe3f2":"ded6c4","eaf8ff":"f3eee2",
 # gallery / info-card category colours
 "5ff6ff":"9fb3cf","9dff5c":"b5c07a","ffd23f":"d8b160","ff8a3d":"e09a74","c58bff":"b4a6c9","ff6f9a":"d99aae","e6ecff":"e6e2d6",
 "ff9d5c":"e09a74","c9a8ff":"b4a6c9",
 # recurring 3D glow tints (teal / cyan / mint) -> warm
 "8ff5e4":"e8d3a0","9ff8ea":"e8d3a0","c8fff4":"f3e6c4","9ff8ff":"e8d3a0","7fe9d8":"c9a974","9fd8ff":"cfc6b0","9fd0ff":"cfc6b0","8fb8ff":"c8c0ac",
}
cnt = {}
def sub_hex(m):
    pre, hx = m.group(1), m.group(2)
    k = next((k for k in MAP if k.lower() == hx.lower()), None)
    if not k: return m.group(0)
    cnt[k] = cnt.get(k,0)+1
    v = MAP[k]
    return pre + (v.upper() if hx.isupper() else v.lower() if hx.islower() else v)
s = re.sub(r'(#|0x)([0-9a-fA-F]{6})(?![0-9a-fA-F])', sub_hex, s)
rep("@property --chc{syntax:'<color>';inherits:true;initial-value:#D8B160}", "@property --chc{syntax:'<color>';inherits:true;initial-value:#8A6210}")
rep("rgba(159,248,255,.85)", "rgba(216,177,96,.85)")

# ---------- 3. hero sky shader: calm the nebula/stars/glow; keep every animated term and its timing ----------
rep('uniform vec2 uPar; uniform float uIntro;\nvarying vec2 vUv;', 'uniform vec2 uPar; uniform float uIntro; uniform vec3 uBase; uniform float uVig; uniform float uGlow; uniform float uStar;\nvarying vec2 vUv;')
rep('vec3 col = vec3(0.005, 0.006, 0.010) + neb*dens*1.7;', 'neb = mix(vec3(dot(neb, vec3(0.333))), neb, 0.25);\n  vec3 col = uBase + neb*dens*0.22;')
rep('col *= 1.0 - dust*0.72*(0.3 + band);', 'col *= 1.0 - dust*0.12*(0.3 + band);')
rep('col += vec3(0.55, 0.58, 0.72)*band*0.05*fbm(pu*14.0);', 'col += vec3(0.6, 0.58, 0.54)*band*0.012*fbm(pu*14.0);')
rep('col += stars(px + uPar*2.0*uDpr, 8.0*uDpr, 0.5, 0.5*uDpr, 0.5, 0.0)*(0.55 + band*0.9);', 'col += stars(px + uPar*2.0*uDpr, 8.0*uDpr, 0.5, 0.5*uDpr, 0.5, 0.0)*(0.55 + band*0.9)*0.16*uStar;')
rep('col += stars(px + uPar*5.0*uDpr, 24.0*uDpr, 0.5, 0.75*uDpr, 0.85, 0.0);', 'col += stars(px + uPar*5.0*uDpr, 24.0*uDpr, 0.5, 0.75*uDpr, 0.85, 0.0)*0.26*uStar;')
rep('col += stars(px + uPar*10.0*uDpr, 110.0*uDpr, 0.45, 1.1*uDpr, 1.25, 1.0);', 'col += stars(px + uPar*10.0*uDpr, 110.0*uDpr, 0.45, 1.1*uDpr, 1.25, 0.0)*0.32*uStar;')
rep('vec3 c = mix(vec3(0.62, 0.72, 1.0), vec3(1.0, 0.97, 0.93), smoothstep(0.08, 0.5, h)); return mix(c, vec3(1.0, 0.74, 0.48), smoothstep(0.76, 1.0, h));',
    'vec3 c = mix(vec3(0.86, 0.85, 0.82), vec3(1.0, 0.97, 0.92), smoothstep(0.08, 0.5, h)); return mix(c, vec3(1.0, 0.86, 0.62), smoothstep(0.76, 1.0, h));')
rep('vec3 rimC = mix(mix(vec3(0.38, 0.44, 1.0), vec3(0.30, 0.95, 0.84), smoothstep(0.0, 0.7, lx)), vec3(1.0, 0.62, 0.32), sunW*0.85);',
    'vec3 rimC = mix(mix(vec3(0.58, 0.56, 0.52), vec3(0.74, 0.66, 0.50), smoothstep(0.0, 0.7, lx)), vec3(0.95, 0.74, 0.40), sunW*0.85);')
rep('vec3 surf = vec3(0.004, 0.005, 0.008) + vec3(0.010, 0.014, 0.022)*fbm(', 'vec3 surf = uBase*0.55 + vec3(0.010, 0.010, 0.010)*fbm(')
rep('surf += vec3(1.0, 0.76, 0.46)*cl*0.4;', 'surf += vec3(1.0, 0.84, 0.6)*cl*0.12;')
rep('col += rimC*(rim*1.15 + exp(-dp/(28.0*uDpr))*outside*0.45 + exp(-dp/(120.0*uDpr))*outside*0.12)*(0.3 + 1.4*(0.3 + sunW))*intro;',
    'col += rimC*(rim*0.75 + exp(-dp/(28.0*uDpr))*outside*0.12 + exp(-dp/(120.0*uDpr))*outside*0.03)*(0.3 + 1.4*(0.3 + sunW))*intro;')
rep('col += vec3(1.0, 0.62, 0.32)*exp(-fd/(70.0*uDpr))*0.45*intro + vec3(1.0, 0.92, 0.8)*exp(-fd/(6.0*uDpr))*1.4*intro;',
    'col += vec3(0.95, 0.74, 0.42)*exp(-fd/(70.0*uDpr))*0.14*intro*uGlow + vec3(1.0, 0.94, 0.84)*exp(-fd/(6.0*uDpr))*0.8*intro*uGlow;')
rep('col += vec3(0.55, 0.7, 1.0)*exp(-abs(sv.y)/(1.1*uDpr))*exp(-abs(sv.x)/(280.0*uDpr))*0.55*intro;',
    'col += vec3(0.9, 0.82, 0.66)*exp(-abs(sv.y)/(1.1*uDpr))*exp(-abs(sv.x)/(280.0*uDpr))*0.16*intro;')
rep('col *= 1.0 - dot(vq, vq)*0.5;', 'col *= 1.0 - dot(vq, vq)*0.5*uVig;')
rep("uPar: { value: new G.Vector2() }, uIntro: { value: 0 } };",
    "uPar: { value: new G.Vector2() }, uIntro: { value: 0 }, uBase: { value: new G.Vector3(0.052, 0.052, 0.057) }, uVig: { value: 1 }, uGlow: { value: 1 }, uStar: { value: 1 } };\n\n"
    "  /* v4: the gallery stays a calm deep-neutral stage in both themes (its 102 objects are lit for a dark backdrop) */")


# ---------- 4. app background: the still night sky is retired (calm paper / neutral instead) ----------
rep("if (!isDark()) { cv.hidden = true; return; }", "if (true) { cv.hidden = true; return; } /* v4: no starfield behind the tour */")

# ---------- 5. v4 theme: no-flash snippet, toggle buttons, si-theme.js ----------
NOFLASH = '''<script>
/* v4 theme before first paint: saved choice (shared with the rest of Explore), else system. */
(function(){var t=null;try{t=localStorage.getItem("si-theme");}catch(e){}
if(t!=="light"&&t!=="dark")t=(window.matchMedia&&matchMedia("(prefers-color-scheme: dark)").matches)?"dark":"light";
var d=document.documentElement;d.setAttribute("data-theme",t);
var m=document.querySelectorAll('meta[name="theme-color"]');for(var i=0;i<m.length;i++){m[i].setAttribute("content",t==="dark"?"#141416":"#f6f3ec");m[i].removeAttribute("media");}})();
</script>
'''
rep('<meta name="theme-color" content="#0b0b10">', '<meta name="theme-color" content="#141416">')
rep('<link rel="preconnect" href="https://fonts.googleapis.com">', NOFLASH + '<link rel="preconnect" href="https://fonts.googleapis.com">')
SUN = '<svg class="sun" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2.5v2M12 19.5v2M2.5 12h2M19.5 12h2M5.3 5.3l1.4 1.4M17.3 17.3l1.4 1.4M5.3 18.7l1.4-1.4M17.3 6.7l1.4-1.4"/></svg><svg class="moon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/></svg>'
# hero: top-right, beside nothing (the corner home mark stays top-left)
# app header: just before the slide controls
rep('    <div class="nav-ctl">', f'    <button class="th-theme iconbtn" id="theme-toggle" type="button" aria-label="Switch to dark theme">{SUN}</button>\n    <div class="nav-ctl">')
THEMEJS = '<script src="/assets/si-theme.js"></script>\n'
rep('</body>', THEMEJS + '</body>')

# ---------- 6. v4 overrides (appended last so they win) ----------
V4CSS = r'''<style id="v4-restyle">
/* ===== Threshold on the Explore v4 system: restrained, editorial; animation and interaction untouched ===== */
:root{--accent:#8A6210;--i1:#7A5610;--i2:#B5862C;--i3:#D8B160;--i4:#8A6210;--glass:rgba(255,253,248,.82);--glass-line:rgba(27,25,22,.08);
  --line:rgba(27,25,22,.12);--line2:rgba(27,25,22,.22);--amb:.035;--on-ch:#FFFDF8;--shadow:0 1px 2px rgba(27,25,22,.05),0 8px 24px -12px rgba(27,25,22,.18)}
:root[data-theme="dark"]{--accent:#D8B160;--i1:#B58B3C;--i2:#D8B160;--i3:#F0D9A0;--i4:#C9A14D;--glass:rgba(28,28,31,.82);--glass-line:rgba(236,235,231,.08);
  --line:rgba(236,235,231,.10);--line2:rgba(236,235,231,.2);--amb:.04;--on-ch:#141416;--shadow:0 1px 2px rgba(0,0,0,.3),0 10px 30px -14px rgba(0,0,0,.6)}
body{font-feature-settings:"ss01","cv11"}
/* editorial display type */
.txt h2,.cover h2,.hero-copy h1,.more .closing,.om-head h2,.qr-card h2,.sheet-head h2{font-family:var(--serif);font-weight:440;letter-spacing:-.018em}
.txt h2{line-height:1.06}.cover h2{line-height:1}
.hero-copy h1{font-weight:400;letter-spacing:-.03em;line-height:.95}
.logo{font-family:var(--serif);font-weight:500;font-size:19px;letter-spacing:-.01em}
.appicon{background:var(--ink);box-shadow:none}
/* calmer glows */
.btn.glow{box-shadow:0 8px 24px -14px rgba(0,0,0,.5)}
.btn.glow::before{opacity:.75}
.chart .glowline{opacity:.07}
.om-group h3::before,.oi-k::before{box-shadow:none}
.om-item[aria-current="true"]{box-shadow:none}
.hero-chaps button:hover{box-shadow:none}
.panel{box-shadow:var(--shadow)}
.chap-name::before,.progress button.cur::before,.tip b::before,.caret,.rung.now .bar,.bars5 div:last-child{box-shadow:none}
.tl-knob{box-shadow:0 0 0 5px color-mix(in srgb,var(--ch) 22%,transparent),0 2px 6px rgba(0,0,0,.25)}
.btn.ch{box-shadow:0 8px 20px -14px var(--ch)}.btn.ch:hover{box-shadow:0 10px 24px -14px var(--ch)}
.cell[aria-pressed="true"],.rung[aria-pressed="true"]{box-shadow:0 0 0 1px var(--ch)}
/* hero stage: deep neutral; gallery canvas desaturated toward the gold accent */
#hero{--bg:#141416;--accent:#D8B160;--i1:#B58B3C;--i2:#D8B160;--i3:#F0D9A0;--i4:#C9A14D;--irid:linear-gradient(100deg,var(--i1) 0%,var(--i2) 36%,var(--i3) 66%,var(--i4) 100%)}
#space,#wafer{filter:saturate(.55) sepia(.1)}
.lede{text-shadow:none}
/* theme buttons */
.th-theme .moon{display:none}:root[data-theme="dark"] .th-theme .sun{display:none}:root[data-theme="dark"] .th-theme .moon{display:block}
/*hero toggle removed*/.th-theme-x{position:absolute;z-index:6;top:calc(4px + env(safe-area-inset-top,0px));right:calc(8px + env(safe-area-inset-right,0px));width:40px;height:40px;display:grid;place-items:center;border:0;border-radius:12px;background:transparent;color:var(--ink2);opacity:.8;cursor:pointer;transition:opacity .2s,background-color .2s}
.th-theme-x:hover{opacity:1;background:color-mix(in srgb,var(--ink) 8%,transparent)}
.th-theme.iconbtn svg{fill:none}
</style>
'''
rep('</head>', V4CSS + '</head>')

# ---------- 7. preview only: noindex; keep canonical pointing at the live Threshold ----------
rep('<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">', '<meta name="robots" content="noindex, nofollow">')

open(sys.argv[1] if len(sys.argv) > 1 else "/workspace/explore-v4-pages/threshold-restyle/index.html","w").write(s)
print("bytes", n0, "->", len(s)); print("hex remaps:", sum(cnt.values()), dict(sorted(cnt.items(), key=lambda kv:-kv[1])[:12]))
