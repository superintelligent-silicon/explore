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


# =====================================================================================
# ---------- 8. INTRO v2: the 3D gallery gets a real light theme (paper studio) ----------
# =====================================================================================
# 8a. sky shader: a light "studio paper" branch (soft gradient + vignette, paper ground, thin gold horizon)
rep("uniform float uGlow; uniform float uStar;", "uniform float uGlow; uniform float uStar; uniform float uLight;")
rep("  vec2 vq = fc/uRes - 0.5; col *= 1.0 - dot(vq, vq)*0.5*uVig;",
"""  if (uLight > 0.5) {
    vec2 sq = fc/uRes;
    vec3 lc = mix(vec3(0.949, 0.933, 0.894), vec3(0.976, 0.965, 0.937), smoothstep(0.0, 1.0, sq.y));
    vec2 hl = uv - vec2(0.22, 0.16); lc += vec3(0.010, 0.008, 0.004)*exp(-dot(hl, hl)*2.4);
    vec3 gnd = vec3(0.929, 0.910, 0.867) - vec3(0.018, 0.018, 0.016)*smoothstep(0.0, uPR*0.5, -dn);
    lc = mix(gnd, lc, outside);
    lc = mix(lc, vec3(0.71, 0.53, 0.17), exp(-abs(d)/(1.1*uDpr))*0.5*intro*(0.45 + 0.55*sunW));
    lc = mix(lc, vec3(0.88, 0.76, 0.50), exp(-dp/(36.0*uDpr))*outside*0.10*intro*(0.3 + sunW));
    lc += vec3(0.035, 0.026, 0.0)*exp(-fd/(90.0*uDpr))*intro;
    vec2 lq = sq - 0.5; lc *= 1.0 - dot(lq, lq)*0.16;
    lc += (hash(fc + fract(uTime)*17.0) - 0.5)/255.0;
    gl_FragColor = vec4(lc, 1.0); return;
  }
  vec2 vq = fc/uRes - 0.5; col *= 1.0 - dot(vq, vq)*0.5*uVig;""")
rep("uStar: { value: 1 }", "uStar: { value: .45 }, uLight: { value: 0 }")

# 8b. per-theme lighting rig: environment, lights, exposure, clear colour; glow layer composited as ink on paper
rep("  scene.add(new G.AmbientLight(0x404060, .35));",
"""  const ambL = new G.AmbientLight(0x404060, .35); scene.add(ambL);
  /* v4: two lighting rigs. Dark keeps the original studio (minus the blue key); light is a bright, soft paper studio. */
  const envDark = scene.environment;
  const envLight = (() => {
    const s2 = new G.Scene(), dg = new G.SphereGeometry(20, 32, 16), p2 = dg.attributes.position, c2 = new Float32Array(p2.count * 3);
    for (let i = 0; i < p2.count; i++) {
      const y = p2.getY(i) / 20, z = p2.getZ(i) / 20, up = clamp((y + .25) / 1.25, 0, 1), front = clamp(z, 0, 1);
      c2[i * 3] = .30 + .30 * up + .10 * front; c2[i * 3 + 1] = .29 + .29 * up + .095 * front; c2[i * 3 + 2] = .27 + .27 * up + .09 * front;
    }
    dg.setAttribute('color', new G.BufferAttribute(c2, 3));
    s2.add(new G.Mesh(dg, new G.MeshBasicMaterial({ vertexColors: true, side: G.BackSide })));
    const pnl = (w, h, c, pp) => { const m = new G.Mesh(new G.PlaneGeometry(w, h), new G.MeshBasicMaterial({ color: c, side: G.DoubleSide })); m.position.copy(pp); m.lookAt(0, 0, 0); s2.add(m); };
    pnl(7, 4, new G.Color(1.9, 1.86, 1.78), V(-4, 6, 4));
    pnl(8, 4, new G.Color(1.0, .97, .93), V(2, 1, 9));
    pnl(3, 7, new G.Color(.9, .78, .58), V(7, 1, -2));
    pnl(9, 2.4, new G.Color(.18, .17, .16), V(3, -6, 2));
    return pm.fromScene(s2, .04).texture;
  })();
  const RIG = {
    dark: { exp: 1.15, env: envDark, sun: 2.4, key: 1.5, rim: 1.1, amb: .35, ambC: 0x404040, keyC: 0xf0ece4, clear: 0x141416 },
    light: { exp: .78, env: envLight, sun: 1.0, key: 1.6, rim: .4, amb: .32, ambC: 0xfff4e6, keyC: 0xffffff, clear: 0xf6f3ec }
  };
  let LIGHT = false;
  const themeRig = () => {
    LIGHT = document.documentElement.getAttribute('data-theme') === 'light';
    const r = LIGHT ? RIG.light : RIG.dark;
    renderer.toneMappingExposure = r.exp; scene.environment = r.env;
    sunL.intensity = r.sun; keyL.intensity = r.key; keyL.color.setHex(r.keyC); rimL.intensity = r.rim; ambL.intensity = r.amb; ambL.color.setHex(r.ambC);
    renderer.setClearColor(r.clear, 1); U.uLight.value = LIGHT ? 1 : 0;
  };
  themeRig(); themeFns.push(themeRig);
  /* light theme: glows are additive light and vanish on paper, so they render into their own layer
     (solids write depth only, so occlusion is kept) and that layer is laid onto the paper as warm ink */
  const GL2 = renderer.capabilities.isWebGL2;
  const glowRT = new G.WebGLRenderTarget(2, 2, { type: GL2 ? G.HalfFloatType : G.UnsignedByteType, samples: GL2 ? 4 : 0, depthBuffer: true });
  const compM = new G.ShaderMaterial({ uniforms: { tG: { value: glowRT.texture }, uK: { value: 1.8 } }, transparent: true, depthTest: false, depthWrite: false,
    vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }',
    fragmentShader: 'uniform sampler2D tG; uniform float uK; varying vec2 vUv;\\n' +
      'void main(){ vec3 c = max(texture2D(tG, vUv).rgb, vec3(0.0)); float L = max(max(c.r, c.g), c.b); if (L < 0.003) discard;\\n' +
      '  vec3 hue = c/L; float s = max(hue.r, max(hue.g, hue.b)) - min(hue.r, min(hue.g, hue.b));\\n' +
      '  vec3 ink = mix(vec3(0.14, 0.125, 0.105), pow(hue, vec3(1.5))*0.52, 0.5 + 0.3*s);\\n' +
      '  gl_FragColor = vec4(ink, (1.0 - exp(-L*uK))*0.92); }' });
  const compS = new G.Scene(), compC = new G.Camera(), compQ = new G.Mesh(new G.PlaneGeometry(2, 2), compM); compQ.frustumCulled = false; compS.add(compQ);
  const _v2 = new G.Vector2(), _cc = new G.Color();
  const sizeGlowRT = () => { renderer.getDrawingBufferSize(_v2); glowRT.setSize(Math.max(2, _v2.x), Math.max(2, _v2.y)); };
  function renderLight() {
    const mats = []; objs.forEach(o => { if (o.built && o.root.visible) o.mats.forEach(m => mats.push(m)); });
    mats.forEach(m => { m.userData.v0 = m.visible; });
    /* pass 1: paper backdrop and lit solids */
    mats.forEach(m => { if (m.userData.v4a) m.visible = false; });
    renderer.render(scene, camera);
    /* pass 2: glow layer; solids depth-only */
    mats.forEach(m => { m.visible = m.userData.v0; if (!m.userData.v4a) m.colorWrite = false; });
    sky.visible = false; renderer.getClearColor(_cc); const ca = renderer.getClearAlpha();
    renderer.setRenderTarget(glowRT); renderer.setClearColor(0x000000, 0); renderer.clear(); renderer.render(scene, camera);
    renderer.setRenderTarget(null); renderer.setClearColor(_cc, ca); sky.visible = true;
    mats.forEach(m => { m.colorWrite = true; m.visible = m.userData.v0; });
    /* pass 3: ink onto paper */
    const ac = renderer.autoClear; renderer.autoClear = false; renderer.render(compS, compC); renderer.autoClear = ac;
  }""")
rep("    root.visible = false; scene.add(root);", "    root.visible = false; scene.add(root);\n    o.mats.forEach(m => { m.userData.v4a = m.blending === G.AdditiveBlending; });")
rep("    renderer.setPixelRatio(pr); renderer.setSize(W, H, false);", "    renderer.setPixelRatio(pr); renderer.setSize(W, H, false); sizeGlowRT();")
rep("    renderer.render(scene, camera);\n    if (running) raf = requestAnimationFrame(frame);", "    if (LIGHT) renderLight(); else renderer.render(scene, camera);\n    if (running) raf = requestAnimationFrame(frame);")

# 8c. hero toggle (top right of the intro) + app toggle, both driving the shared Explore theme
rep('<nav class="si-corner" aria-label="Explore Superintelligence">', f'<button class="th-theme th-theme-hero" id="theme-toggle-hero" type="button" aria-label="Switch to dark theme">{SUN}</button>\n  <nav class="si-corner" aria-label="Explore Superintelligence">')
rep('<script src="/assets/si-theme.js"></script>\n</body>', '''<script src="/assets/si-theme.js"></script>
<script>
/* v4: every Threshold theme button drives the shared Explore theme; Threshold's CSS, canvases and 3D lighting follow html[data-theme] */
(function(){var d=document.documentElement;function lab(){var dk=d.getAttribute("data-theme")==="dark";document.querySelectorAll(".th-theme").forEach(function(b){b.setAttribute("aria-label",dk?"Switch to light theme":"Switch to dark theme");});
var m=document.querySelector('meta[name="theme-color"]');if(m)m.setAttribute("content",dk?"#141416":"#f6f3ec");}
document.querySelectorAll(".th-theme").forEach(function(b){if(b.id==="theme-toggle")return;b.addEventListener("click",function(e){e.stopPropagation();var t=d.getAttribute("data-theme")==="dark"?"light":"dark";if(window.SITheme)SITheme.apply(t,true);else d.setAttribute("data-theme",t);});});
new MutationObserver(lab).observe(d,{attributes:true,attributeFilter:["data-theme"]});lab();})();
</script>
</body>''')

# 8d. CSS: v4 sheets/cards/buttons in both themes; real light intro
V4INTRO = r'''<style id="v4-intro">
/* ===== Intro v2: gallery chrome on v4 tokens (no blue glass) ===== */
.th-theme-hero{position:absolute;z-index:6;top:calc(4px + env(safe-area-inset-top,0px));right:calc(8px + env(safe-area-inset-right,0px));width:40px;height:40px;display:grid;place-items:center;border:0;border-radius:12px;background:transparent;color:var(--ink2);cursor:pointer;transition:background-color .2s,color .2s}
.th-theme-hero:hover{color:var(--ink);background:color-mix(in srgb,var(--ink) 8%,transparent)}
.th-theme-hero:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
#hero .si-corner{opacity:.85}
/* dark intro tokens (v4 dark) */
#hero{--surface:#1C1C1F;--elev:#232327;--ink:#ECEBE7;--ink2:#B9B6AF;--muted:#97938B;--line:rgba(236,235,231,.10);--line2:rgba(236,235,231,.2);
  --sheet:rgba(28,28,31,.97);--sheet-line:rgba(236,235,231,.10);--chip:rgba(236,235,231,.05);--chip-h:rgba(236,235,231,.09);--chip-line:rgba(236,235,231,.09);--scrim:rgba(0,0,0,.45);--focus:#D8B160}
.obj-cap b{font-family:var(--serif);font-weight:500;font-size:16px;letter-spacing:-.005em;text-shadow:none}
.obj-cap span{text-shadow:none}
.obj-arrow,.obj-more{border-color:var(--line2);background:color-mix(in srgb,var(--surface) 70%,transparent);color:var(--ink);-webkit-backdrop-filter:none;backdrop-filter:none}
.obj-arrow:hover,.obj-more:hover,.obj-meter:hover{background:var(--chip-h)}
.obj-arrow:focus-visible,.obj-more:focus-visible,.obj-meter:focus-visible,.om-item:focus-visible,.oi-link:focus-visible,.oi-btn:focus-visible,.om-x:focus-visible,.qr-act:focus-visible,.qr-btn:focus-visible{outline:2px solid var(--focus);outline-offset:2px}
.obj-count{color:var(--ink2)}.obj-count svg{fill:var(--muted)}
.obj-track{background:var(--line2)}.obj-track b{background:var(--accent)}
.obj-menu,.obj-info{color:var(--ink)}
.om-back{background:var(--scrim);-webkit-backdrop-filter:none;backdrop-filter:none}
.oi-back{background:linear-gradient(180deg,transparent 25%,var(--scrim))}
@media (min-width:900px){.oi-back{background:linear-gradient(90deg,var(--scrim),transparent 62%)}}
.om-card{background:var(--sheet);border-color:var(--sheet-line);-webkit-backdrop-filter:none;backdrop-filter:none;box-shadow:0 -18px 50px -20px rgba(0,0,0,.45)}
@media (min-width:700px){.om-card{border-bottom:1px solid var(--sheet-line)}}
.om-card::before{background:var(--line2)}
.om-head h2{color:var(--ink);font-size:23px}
.om-head p,.oi-lede,.oi-stat i,.oi-link i{color:var(--ink2)}
.om-x,.oi-btn,.qr-act{background:var(--chip);border:1px solid var(--chip-line);color:var(--ink)}
.om-x:hover,.oi-btn:hover,.qr-act:hover{background:var(--chip-h)}
.om-group h3{color:var(--ink2)}
.om-group h3::before{background:var(--g);box-shadow:none}
.om-item{background:var(--chip);border-color:var(--chip-line);color:var(--ink)}
.om-item:hover{background:var(--chip-h)}
.om-n{color:var(--muted)}
.om-item[aria-current="true"]{border-color:var(--accent);background:color-mix(in srgb,var(--accent) 12%,transparent);box-shadow:none}
.om-item[aria-current="true"] .om-n{color:var(--accent)}
.oi-tag{color:var(--accent)!important}
.oi-stat{background:var(--chip);border-color:var(--chip-line)}
.oi-stat b{background:none;-webkit-background-clip:border-box;background-clip:border-box;color:var(--ink);font-family:var(--serif);font-weight:500;letter-spacing:-.02em}
.oi-sec h3{color:var(--muted)}
.oi-sec p,.oi-link b{color:var(--ink)}
.oi-link{background:var(--chip);border-color:var(--chip-line)}
.oi-link:hover{background:var(--chip-h);border-color:var(--line2)}
.oi-k{color:var(--ink2)}.oi-k::before{background:var(--accent);box-shadow:none}
.oi-link svg{stroke:var(--muted)}
.oi-foot{border-top-color:var(--sheet-line)}
.qr-back{background:var(--scrim)}
.qr-card{background:var(--sheet);border-color:var(--sheet-line);box-shadow:0 30px 80px -30px rgba(0,0,0,.5)}
.qr-code{box-shadow:0 0 0 1px var(--line)}
.qr-btn:hover{box-shadow:none}
/* light intro: warm paper studio */
:root[data-theme="light"] #hero{--bg:#F6F3EC;--bg2:#EFEADF;--surface:#FFFDF8;--elev:#FFFDF8;--ink:#1B1916;--ink2:#4D4840;--muted:#6B655B;--line:rgba(27,25,22,.12);--line2:rgba(27,25,22,.22);
  --accent:#8A6210;--i1:#7A5610;--i2:#B5862C;--i3:#8A6210;--i4:#5E430C;color-scheme:light;
  --sheet:rgba(255,253,248,.98);--sheet-line:rgba(27,25,22,.10);--chip:rgba(27,25,22,.035);--chip-h:rgba(27,25,22,.07);--chip-line:rgba(27,25,22,.10);--scrim:rgba(27,25,22,.2);--focus:#8A6210}
:root[data-theme="light"] #space{filter:saturate(.85)}
:root[data-theme="light"] .obj-cap b{color:var(--ink)}:root[data-theme="light"] .obj-cap span{color:var(--ink2)}
:root[data-theme="light"] #wafer{filter:invert(1) hue-rotate(180deg) saturate(.6);mix-blend-mode:multiply}
:root[data-theme="light"] .om-card{box-shadow:0 -18px 50px -24px rgba(27,25,22,.3)}
:root[data-theme="light"] .qr-card{box-shadow:0 30px 80px -30px rgba(27,25,22,.35)}
:root[data-theme="light"] .om-group h3::before{background:color-mix(in srgb,var(--g) 55%,#1B1916)}
:root[data-theme="light"] .btn.glow{box-shadow:0 8px 22px -14px rgba(27,25,22,.5)}
</style>
'''
rep('</head>', V4INTRO + '</head>')

# ---------- 9. no accidental page zoom (app-like, full viewport) ----------
import os as _os, importlib.util as _iu; _sp = _iu.spec_from_file_location("si_nozoom", _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "si-nozoom.py")); _nz = _iu.module_from_spec(_sp); _sp.loader.exec_module(_nz)
s = s.replace('<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">', '<meta name="viewport" content="%s">' % _nz.VP, 1)
assert _nz.VP in s
_i = s.index('<meta name="viewport"'); _i = s.index('>', _i) + 1
s = s[:_i] + '\n' + _nz.SNIP.rstrip('\n') + s[_i:]

# ---------- 7. preview only: noindex; keep canonical pointing at the live Threshold ----------
import os
if not os.environ.get("THR_COMMIT"):
    rep('<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">', '<meta name="robots" content="noindex, nofollow">')

open(sys.argv[1] if len(sys.argv) > 1 else "/workspace/explore-v4-pages/threshold-restyle/index.html","w").write(s)
print("bytes", n0, "->", len(s)); print("hex remaps:", sum(cnt.values()), dict(sorted(cnt.items(), key=lambda kv:-kv[1])[:12]))
