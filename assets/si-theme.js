/* Explore v4: theme toggle (light/dark, saved in localStorage). Pair with the inline no-flash snippet in <head>. */
(function(){
  "use strict";
  var d=document.documentElement, KEY="si-theme";
  function cur(){ return d.getAttribute("data-theme")==="dark"?"dark":"light"; }
  function label(){ var b=document.getElementById("theme-toggle"); if(b) b.setAttribute("aria-label", cur()==="dark"?"Switch to light theme":"Switch to dark theme"); }
  function apply(t, save){
    d.classList.add("theming"); d.setAttribute("data-theme",t);
    var m=document.querySelectorAll('meta[name="theme-color"]'); for(var i=0;i<m.length;i++){ m[i].setAttribute("content", t==="dark"?"#141416":"#f6f3ec"); m[i].removeAttribute("media"); }
    if(save){ try{ localStorage.setItem(KEY,t); }catch(e){} }
    label(); clearTimeout(apply.t); apply.t=setTimeout(function(){ d.classList.remove("theming"); },450);
  }
  function init(){
    label();
    var b=document.getElementById("theme-toggle");
    if(b) b.addEventListener("click", function(){ apply(cur()==="dark"?"light":"dark", true); });
  }
  if(document.readyState==="loading") document.addEventListener("DOMContentLoaded", init); else init();
  if(window.matchMedia){ var mq=matchMedia("(prefers-color-scheme: dark)"); var h=function(e){ var s=null; try{ s=localStorage.getItem(KEY); }catch(x){} if(!s) apply(e.matches?"dark":"light", false); }; mq.addEventListener?mq.addEventListener("change",h):mq.addListener&&mq.addListener(h); }
  window.SITheme={apply:apply,current:cur};
})();
