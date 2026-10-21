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
  ".si-splash{position:fixed;inset:0;z-index:9999;display:grid;place-items:center;background:var(--bg,#f6f3ec);color:var(--ink,#1b1916);font-family:var(--ui,inherit);transition:opacity .45s ease,visibility .45s;padding:24px}"+
  ".si-splash.out{opacity:0;visibility:hidden}"+
  ".si-splash .in{display:flex;flex-direction:column;align-items:center;text-align:center;max-width:320px;animation:siIn .6s cubic-bezier(.22,.8,.2,1) both}"+
  ".si-splash .wm{font-family:var(--serif,Georgia,serif);font-size:30px;letter-spacing:-.01em;margin:14px 0 4px;text-wrap:balance}"+
  ".si-splash .sub{font-size:13.5px;color:var(--dim,#6b655b);margin:0 0 26px}"+
  ".si-splash .row{display:flex;gap:10px;flex-wrap:wrap;justify-content:center}"+
  ".si-splash button{height:42px;padding:0 18px;border-radius:999px;font:inherit;font-size:14.5px;font-weight:500;cursor:pointer;border:1px solid var(--line2,rgba(0,0,0,.2));background:transparent;color:inherit;display:inline-flex;align-items:center;gap:8px}"+
  ".si-splash .si-enter{background:var(--ink,#1b1916);color:var(--bg,#f6f3ec);border-color:var(--ink,#1b1916)}"+
  ".si-splash button:hover{opacity:.88}"+
  "@keyframes siIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}"+
  "@media (prefers-reduced-motion:reduce){.si-splash .in{animation:none}.si-splash{transition:opacity .15s}}";
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
    chime:function(t){ [659.25,987.77].forEach(function(f,i){ tone(f,t+i*0.09,0.9,0.04,"sine"); }); },
    tick:function(t){ tone(1760,t,0.06,0.035,"sine"); tone(880,t,0.05,0.02,"triangle"); },
    open:function(t){ noise(t,0.32,0.05,500,2400); tone(587.33,t+0.05,0.35,0.025,"sine"); },
    close:function(t){ noise(t,0.26,0.04,2200,450); tone(440,t+0.03,0.25,0.02,"sine"); },
    hover:function(t){ tone(1318.5,t,0.09,0.012,"sine"); },
    snap:function(t,i){ var sc=[659.25,739.99,830.61,987.77,1108.73,1318.51,1479.98,1661.22]; var f=sc[(i||0)%sc.length]; tone(f,t,0.11,0.026,"sine"); tone(f*1.5,t,0.05,0.008,"triangle"); },
    tabbar:function(t){ tone(392,t,0.16,0.03,"sine"); tone(784,t+0.01,0.08,0.01,"triangle"); },
    bump:function(t){ tone(130.81,t,0.18,0.05,"sine"); noise(t,0.08,0.02,300,160); },
    tap:function(t){ tone(659.25,t,0.14,0.035,"sine"); tone(987.77,t+0.02,0.12,0.015,"sine"); }
  };
  function play(name,arg){
    if(!on||!ctx) return;
    if(ctx.state!=="running") ctx.resume();
    S[name](ctx.currentTime+0.005,arg);
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
    if(on){ init(); ctx.resume(); var t=ctx.currentTime; master.gain.cancelScheduledValues(t); master.gain.setValueAtTime(master.gain.value,t); master.gain.linearRampToValueAtTime(0.6,t+0.25); }
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
    var hw=document.querySelector(".hdr .wrap"), mb=hw&&hw.querySelector(".menu-btn"); if(hw) hw.insertBefore(btn,mb||null); else document.body.appendChild(btn); setOn(on,false);
  }

  /* ---------- interaction hooks (delegated; no coupling to page code) ---------- */
  document.addEventListener("click",function(e){
    var t=e.target.closest&&e.target.closest("[role=tab],[data-jump],.rail-arrow,[data-dir]");
    if(t){ play("tick"); return; }
    if(e.target.closest&&e.target.closest(".tabbar a,.tabbar button")){ play("tabbar"); buzz(6); return; }
    if(e.target.closest&&e.target.closest(".theme-btn")){ play("tick"); return; }
    if(e.target.closest&&e.target.closest(".card,.btn,.tile,.bk,.pd,.btn-p")) play("tap");
  },true);
  function buzz(ms){ if(on&&navigator.vibrate){ try{navigator.vibrate(ms);}catch(e){} } }
  /* Rail: one pitched tick per settled snap; soft bump when pushing past either end */
  (function(){
    var rail=document.getElementById("rail"); if(!rail) return;
    var items=rail.children, last=-1, tmr=0, lastBump=0, sx=0, startIdx=0;
    function idx(){ var st=items[1]?items[1].offsetLeft-items[0].offsetLeft:rail.clientWidth; var max=rail.scrollWidth-rail.clientWidth; var i=Math.round(rail.scrollLeft/st); if(rail.scrollLeft>=max-4) i=items.length-1; return Math.max(0,Math.min(items.length-1,i)); }
    last=idx();
    function settle(){ var i=idx(); if(i!==last){ last=i; play("snap",i); buzz(4); } }
    rail.addEventListener("scroll",function(){ clearTimeout(tmr); tmr=setTimeout(settle,90); },{passive:true});
    function bump(){ var n=Date.now(); if(n-lastBump<700) return; lastBump=n; play("bump"); buzz(10); }
    function atEnd(dir){ var max=rail.scrollWidth-rail.clientWidth; return dir<0?rail.scrollLeft<=2:rail.scrollLeft>=max-2; }
    rail.addEventListener("touchstart",function(e){ sx=e.touches[0].clientX; startIdx=idx(); },{passive:true});
    rail.addEventListener("touchend",function(e){ var dx=e.changedTouches[0].clientX-sx; if(Math.abs(dx)>30){ var dir=dx<0?1:-1; setTimeout(function(){ if(idx()===startIdx&&atEnd(dir)) bump(); },260);} },{passive:true});
    rail.addEventListener("wheel",function(e){ var d=Math.abs(e.deltaX)>Math.abs(e.deltaY)?e.deltaX:0; if(d&&atEnd(d>0?1:-1)) bump(); },{passive:true});
    document.addEventListener("click",function(e){ var b=e.target.closest&&e.target.closest("[data-dir]"); if(b&&b.disabled) bump(); },true);
  })();
  document.addEventListener("keydown",function(e){ if((e.key==="ArrowLeft"||e.key==="ArrowRight")&&e.target.closest&&e.target.closest("[role=tablist]")) play("tick"); });
  document.addEventListener("pointerover",function(e){
    if(e.pointerType!=="mouse") return;
    var c=e.target.closest&&e.target.closest(".card,.bk,.pd"); if(!c||c.contains(e.relatedTarget)) return;
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
    setTimeout(function(){ sp.remove(); var m=document.getElementById("main")||document.querySelector("main"); if(m&&m.focus) { m.setAttribute("tabindex","-1"); m.focus({preventScroll:true}); } }, reduce?150:480);
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
  sp.innerHTML='<div class="in"><svg width="40" height="40" viewBox="0 0 26 26" aria-hidden="true"><circle cx="13" cy="13" r="11.5" fill="none" stroke="currentColor" stroke-opacity=".3"/><circle cx="13" cy="13" r="6" fill="none" stroke="var(--accent-ui,#b5862c)"/><circle cx="13" cy="13" r="2" fill="var(--accent-ui,#b5862c)"/></svg>'+
    '<p class="wm">Explore Superintelligence</p><p class="sub">Superintelligent Silicon · sound is optional</p><div class="row">'+
    '<button class="si-enter" type="button">Enter</button>'+(AC?'<button class="si-mark" type="button" aria-label="Enter with sound"><svg width="15" height="15" viewBox="0 0 16 16" aria-hidden="true"><path d="M2 6h2.5L8 3v10L4.5 10H2z" fill="currentColor"/><path d="M10.5 5.5a3.5 3.5 0 010 5M12.2 3.8a6 6 0 010 8.4" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg>With sound</button>':'')+'</div></div>';
  document.body.appendChild(sp); document.documentElement.style.overflow="hidden";
  var en=sp.querySelector(".si-enter"), mark=sp.querySelector(".si-mark");
  en.focus({preventScroll:true});
  en.addEventListener("click",function(){ finish(false,true); });
  if(mark) mark.addEventListener("click",function(){ finish(true,true); });
  sp.addEventListener("keydown",function(e){ if(e.key==="Escape") finish(false,false); });
})();
