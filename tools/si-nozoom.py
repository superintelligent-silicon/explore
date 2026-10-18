#!/usr/bin/env python3
"""App-like SI pages: stop accidental page zoom (pinch / double-tap / iOS focus zoom). Idempotent."""
import re, sys
VP = 'width=device-width, initial-scale=1, maximum-scale=1, viewport-fit=cover'
CSS = ('html,body{touch-action:manipulation}'
       ':where(a,button,input,select,textarea,label,summary){touch-action:manipulation}'
       '@supports (-webkit-touch-callout:none){input,textarea,select{font-size:16px!important}}')
JS = ('(function(){var p=function(e){e.preventDefault();};'
      '["gesturestart","gesturechange","gestureend"].forEach(function(t){document.addEventListener(t,p,{passive:false});});'
      'document.addEventListener("touchmove",function(e){if(e.touches&&e.touches.length>1)e.preventDefault();},{passive:false});'
      'if(window.matchMedia&&matchMedia("(pointer: coarse)").matches)document.addEventListener("dblclick",function(e){if(!(e.target.closest&&e.target.closest("input,textarea,[contenteditable]")))e.preventDefault();},{passive:false});})();')
SNIP = f'<!-- si-nozoom: app-like page, no accidental zoom -->\n<style id="si-nozoom">{CSS}</style>\n<script>{JS}</script>\n'
def patch(path, mode):
    s = open(path).read(); o = s
    s, n = re.subn(r'<meta name="viewport" content="[^"]*"', f'<meta name="viewport" content="{VP}"', s, count=1)
    if n != 1: sys.exit(f"no viewport meta: {path}")
    if mode == "inline":
        if 'id="si-nozoom"' not in s:
            m = re.search(r'<meta name="viewport"[^>]*>\n?', s); i = m.end(); s = s[:i] + ('' if s[i-1] == '\n' else '\n') + SNIP + s[i:]
    elif mode == "attr":   # page loads /assets/si-ui.js + si-v4.css, which carry the behaviour for html[data-nozoom]
        if 'data-nozoom' not in s:
            s, n = re.subn(r'<html\b([^>]*)>', lambda m: f'<html{m.group(1)} data-nozoom>', s, count=1); assert n == 1
    if s != o: open(path, 'w').write(s)
    print(("patched " if s != o else "unchanged ") + mode, path)
if __name__ == "__main__":
    mode = sys.argv[1]
    for p in sys.argv[2:]: patch(p, mode)
