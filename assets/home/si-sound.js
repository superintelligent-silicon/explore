/* Explore — entry splash + Web Audio interaction sounds. No audio files. Progressive: no-JS = no splash. */
(function(){
  "use strict";
  var KEY="si-sound", LS={get:function(){try{return localStorage.getItem(KEY);}catch(e){return null;}},set:function(v){try{localStorage.setItem(KEY,v);}catch(e){}}};
  var reduce=window.matchMedia&&matchMedia("(prefers-reduced-motion: reduce)").matches;
  var AC=window.AudioContext||window.webkitAudioContext;
  var ctx=null, master=null, pad=null, on=false, lastHover=0;

  /* ---------- styles ---------- */
  var css=document.createElement("style");
  css.textContent=
  ".si-splash{position:fixed;inset:0;z-index:9999;display:grid;place-items:center;background:radial-gradient(ellipse at 50% 45%,#141210 0%,#070708 62%);color:#f5f5f7;transition:opacity .7s ease,visibility .7s;font-family:inherit}"+
  ".si-splash.out{opacity:0;visibility:hidden}"+
  ".si-splash .in{display:flex;flex-direction:column;align-items:center;gap:22px;text-align:center}"+
  ".si-mark{width:112px;height:112px;border-radius:50%;border:0;background:none;padding:0;cursor:pointer;position:relative;display:grid;place-items:center;-webkit-tap-highlight-color:transparent}"+
  ".si-mark svg{width:100%;height:100%;overflow:visible}"+
  ".si-mark .halo{position:absolute;inset:-14px;border-radius:50%;border:1px solid rgba(236,196,89,.35);animation:siPulse 2.4s ease-in-out infinite}"+
  ".si-mark[disabled]{cursor:progress}.si-mark[disabled] .core{animation:siBreath 1.2s ease-in-out infinite}"+
  ".si-mark:not([disabled]):hover svg,.si-mark:not([disabled]):focus-visible svg{transform:scale(1.05)}.si-mark svg{transition:transform .4s cubic-bezier(.22,.8,.2,1)}"+
  ".si-mark .core{transform-origin:50% 50%}"+
  ".si-cap{font-size:12px;letter-spacing:.22em;text-transform:uppercase;color:rgba(245,245,247,.62);min-height:1.2em;transition:opacity .4s}"+
  ".si-skip{background:none;border:0;color:rgba(245,245,247,.38);font:inherit;font-size:12.5px;cursor:pointer;padding:6px 10px;text-decoration:underline;text-underline-offset:3px;opacity:0;transition:opacity .5s}"+
  ".si-ready .si-skip{opacity:1}.si-skip:hover{color:rgba(245,245,247,.7)}"+
  "@keyframes siPulse{0%,100%{transform:scale(.96);opacity:.25}50%{transform:scale(1.06);opacity:.8}}"+
  "@keyframes siBreath{0%,100%{opacity:.45}50%{opacity:1}}"+
  ".si-snd{position:fixed;right:14px;bottom:calc(76px + env(safe-area-inset-bottom));z-index:60;width:38px;height:38px;border-radius:50%;border:1px solid rgba(245,245,247,.16);background:rgba(14,14,16,.72);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);color:#ecc459;display:grid;place-items:center;cursor:pointer;transition:opacity .3s,transform .3s}"+
  ".si-snd:hover{transform:scale(1.06)}.si-snd[aria-pressed=false]{color:rgba(245,245,247,.5)}"+
  "@media (min-width:900px){.si-snd{bottom:22px;right:22px}}"+
  "@media (prefers-reduced-motion:reduce){.si-mark .halo,.si-mark[disabled] .core{animation:none}.si-splash{transition:opacity .2s}}";
  document.head.appendChild(css);

  /* ---------- audio engine ---------- */
  function init(){
    if(ctx||!AC) return;
    ctx=new AC(); master=ctx.createGain(); master.gain.value=0;
    var comp=ctx.createDynamicsCompressor(); comp.threshold.value=-22; comp.ratio.value=4;
    var lp=ctx.createBiquadFilter(); lp.type="lowpass"; lp.frequency.value=5200;
    master.connect(lp); lp.connect(comp); comp.connect(ctx.destination);
  }
  function tone(f,t0,dur,vol,type,det){
    var o=ctx.createOscillator(), g=ctx.createGain();
    o.type=type||"sine"; o.frequency.value=f; if(det) o.detune.value=det;
    g.gain.setValueAtTime(0,t0); g.gain.linearRampToValueAtTime(vol,t0+0.012); g.gain.exponentialRampToValueAtTime(0.0001,t0+dur);
    o.connect(g); g.connect(master); o.start(t0); o.stop(t0+dur+0.05);
  }
  function noise(t0,dur,vol,from,to){
    var n=Math.floor(ctx.sampleRate*dur), b=ctx.createBuffer(1,n,ctx.sampleRate), d=b.getChannelData(0);
    for(var i=0;i<n;i++) d[i]=Math.random()*2-1;
    var s=ctx.createBufferSource(); s.buffer=b;
    var f=ctx.createBiquadFilter(); f.type="bandpass"; f.Q.value=0.9;
    f.frequency.setValueAtTime(from,t0); f.frequency.exponentialRampToValueAtTime(to,t0+dur);
    var g=ctx.createGain(); g.gain.setValueAtTime(0,t0); g.gain.linearRampToValueAtTime(vol,t0+dur*0.35); g.gain.exponentialRampToValueAtTime(0.0001,t0+dur);
    s.connect(f); f.connect(g); g.connect(master); s.start(t0);
  }
  var S={
    chime:function(t){ [523.25,659.25,783.99,1046.5].forEach(function(f,i){ tone(f,t+i*0.07,1.8-i*0.2,0.07,"sine"); tone(f*2,t+i*0.07,0.6,0.012,"triangle"); }); },
    tick:function(t){ tone(1760,t,0.06,0.035,"sine"); tone(880,t,0.05,0.02,"triangle"); },
    open:function(t){ noise(t,0.32,0.05,500,2400); tone(587.33,t+0.05,0.35,0.025,"sine"); },
    close:function(t){ noise(t,0.26,0.04,2200,450); tone(440,t+0.03,0.25,0.02,"sine"); },
    hover:function(t){ tone(1318.5,t,0.09,0.012,"sine"); },
    tap:function(t){ tone(659.25,t,0.14,0.035,"sine"); tone(987.77,t+0.02,0.12,0.015,"sine"); }
  };
  function play(name){
    if(!on||!ctx) return;
    if(ctx.state!=="running") ctx.resume();
    S[name](ctx.currentTime+0.005);
  }
  function startPad(){
    if(pad||!ctx) return;
    var g=ctx.createGain(); g.gain.value=0;
    var f=ctx.createBiquadFilter(); f.type="lowpass"; f.frequency.value=700;
    var lfo=ctx.createOscillator(), lg=ctx.createGain(); lfo.frequency.value=0.07; lg.gain.value=220; lfo.connect(lg); lg.connect(f.frequency); lfo.start();
    var os=[130.81,196,261.63,329.63].map(function(fr,i){ var o=ctx.createOscillator(); o.type=i%2?"triangle":"sine"; o.frequency.value=fr; o.detune.value=(i-1.5)*4; o.connect(f); o.start(); return o; });
    f.connect(g); g.connect(master);
    g.gain.linearRampToValueAtTime(0.018,ctx.currentTime+6);
    pad={g:g,os:os.concat([lfo])};
  }
  function stopPad(){
    if(!pad) return; var p=pad; pad=null; var t=ctx.currentTime;
    p.g.gain.cancelScheduledValues(t); p.g.gain.setValueAtTime(p.g.gain.value,t); p.g.gain.linearRampToValueAtTime(0,t+0.8);
    setTimeout(function(){ p.os.forEach(function(o){ try{o.stop();}catch(e){} }); },900);
  }
  function setOn(v,persist){
    on=!!v&&!!AC; if(persist) LS.set(on?"on":"off");
    if(on){ init(); ctx.resume(); var t=ctx.currentTime; master.gain.cancelScheduledValues(t); master.gain.setValueAtTime(master.gain.value,t); master.gain.linearRampToValueAtTime(0.9,t+0.25); startPad(); }
    else if(ctx){ stopPad(); var t2=ctx.currentTime; master.gain.cancelScheduledValues(t2); master.gain.setValueAtTime(master.gain.value,t2); master.gain.linearRampToValueAtTime(0,t2+0.6); }
    if(btn){ btn.setAttribute("aria-pressed",on?"true":"false"); btn.setAttribute("aria-label",on?"Mute sound":"Turn sound on"); btn.innerHTML=on?ICON_ON:ICON_OFF; }
  }

  /* ---------- sound toggle in chrome ---------- */
  var ICON_ON='<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M2 6h2.5L8 3v10L4.5 10H2z" fill="currentColor"/><path d="M10.5 5.5a3.5 3.5 0 010 5M12.2 3.8a6 6 0 010 8.4" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg>';
  var ICON_OFF='<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M2 6h2.5L8 3v10L4.5 10H2z" fill="currentColor"/><path d="M10.5 6l4 4M14.5 6l-4 4" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg>';
  var btn=null;
  function addToggle(){
    if(!AC||btn) return;
    btn=document.createElement("button"); btn.type="button"; btn.className="si-snd"; btn.id="si-sound-toggle";
    btn.addEventListener("click",function(){ var nv=!on; setOn(nv,true); if(nv) play("tap"); });
    document.body.appendChild(btn); setOn(on,false);
  }

  /* ---------- interaction hooks (delegated; no coupling to page code) ---------- */
  document.addEventListener("click",function(e){
    var t=e.target.closest&&e.target.closest("[role=tab],[data-jump],.tabbar a,.tabbar button,.rail-arrow,[data-dir]");
    if(t){ play("tick"); return; }
    if(e.target.closest&&e.target.closest(".card,.btn,.tile")) play("tap");
  },true);
  document.addEventListener("keydown",function(e){ if((e.key==="ArrowLeft"||e.key==="ArrowRight")&&e.target.closest&&e.target.closest("[role=tablist],.rail")) play("tick"); });
  document.addEventListener("pointerover",function(e){
    if(e.pointerType!=="mouse") return;
    var c=e.target.closest&&e.target.closest(".card"); if(!c||c.contains(e.relatedTarget)) return;
    var n=Date.now(); if(n-lastHover<140) return; lastHover=n; play("hover");
  });
  if(window.MutationObserver){
    new MutationObserver(function(ms){ ms.forEach(function(m){ var d=m.target; if(d.tagName==="DIALOG") play(d.open?"open":"close"); }); })
      .observe(document.body,{subtree:true,attributes:true,attributeFilter:["open"]});
  }
  document.addEventListener("visibilitychange",function(){ if(!ctx) return; if(document.hidden) ctx.suspend(); else if(on) ctx.resume(); });

  /* ---------- splash ---------- */
  var pref=LS.get();
  function finish(withSound, persist){
    if(withSound){ init(); setOn(true,persist); play("chime"); } else setOn(false,persist);
    addToggle();
    var sp=document.getElementById("si-splash"); if(!sp) return;
    sp.classList.add("out"); document.documentElement.style.overflow="";
    setTimeout(function(){ sp.remove(); var m=document.getElementById("main")||document.querySelector("main"); if(m&&m.focus) { m.setAttribute("tabindex","-1"); m.focus({preventScroll:true}); } }, reduce?200:750);
  }
  /* Returning visitors who chose: skip splash (audio still needs a gesture -> unlock on first interaction). */
  if(pref){
    on=false; addToggle();
    if(pref==="on"){
      var unlock=function(){ document.removeEventListener("pointerdown",unlock,true); document.removeEventListener("keydown",unlock,true); setOn(true,false); };
      document.addEventListener("pointerdown",unlock,true); document.addEventListener("keydown",unlock,true);
      btn&&(btn.setAttribute("aria-pressed","true"),btn.innerHTML=ICON_ON,btn.setAttribute("aria-label","Mute sound"));
    }
    return;
  }
  var sp=document.createElement("div"); sp.id="si-splash"; sp.className="si-splash"; sp.setAttribute("role","dialog"); sp.setAttribute("aria-modal","true"); sp.setAttribute("aria-label","Welcome to Explore Superintelligence");
  sp.innerHTML='<div class="in"><button class="si-mark" type="button" disabled aria-label="Enter with sound"><span class="halo" aria-hidden="true"></span>'+
    '<svg viewBox="0 0 26 26" aria-hidden="true"><circle cx="13" cy="13" r="11.5" fill="none" stroke="rgba(236,196,89,.45)" stroke-width=".6"/><circle cx="13" cy="13" r="6" fill="none" stroke="#ecc459" stroke-opacity=".85" stroke-width=".7"/><circle class="core" cx="13" cy="13" r="2" fill="#ecc459"/></svg></button>'+
    '<div class="si-cap" aria-live="polite">Loading</div><button class="si-skip" type="button">Enter without sound</button></div>';
  document.body.appendChild(sp); document.documentElement.style.overflow="hidden";
  var mark=sp.querySelector(".si-mark"), cap=sp.querySelector(".si-cap");
  function ready(){ if(!mark.disabled) return; mark.disabled=false; sp.classList.add("si-ready"); cap.textContent=AC?"Tap to enter · with sound":"Tap to enter"; mark.focus({preventScroll:true}); }
  if(document.readyState==="complete") setTimeout(ready, reduce?0:500); else window.addEventListener("load",function(){ setTimeout(ready, reduce?0:350); });
  setTimeout(ready,2500); /* never hold users longer than ~2.5s */
  mark.addEventListener("click",function(){ finish(!!AC,true); });
  sp.querySelector(".si-skip").addEventListener("click",function(){ finish(false,true); });
  sp.addEventListener("keydown",function(e){ if(e.key==="Escape") finish(false,false); });
})();
