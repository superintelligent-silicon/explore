/* Explore v4: quick-look sheets (dialog), drag-to-dismiss, focus trap, tabs. Exposes window.SIUI.open(id, tabId). */
  (function(){
    "use strict";
    var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
    var $ = function(s,r){ return (r||document).querySelector(s); }, $$ = function(s,r){ return Array.prototype.slice.call((r||document).querySelectorAll(s)); };

    /* ---------- Sheets ---------- */
    var opener = null, current = null;
    var FOCUSABLE = 'a[href],button:not([disabled]),[tabindex]:not([tabindex="-1"])';
    function lock(on){ document.documentElement.style.overflow = on ? "hidden" : ""; }
    function openSheet(id, tabId, from){
      var d = document.getElementById(id); if (!d || typeof d.showModal !== "function") return false;
      if (current && current !== d) closeSheet(current, true);
      opener = from || document.activeElement; current = d;
      d.classList.remove("closing"); d.style.transform = "";
      if (!d.open) d.showModal();
      lock(true);
      if (tabId) selectTab(document.getElementById(tabId), false);
      var body = $(".sh-body", d); if (body) body.scrollTop = 0;
      var first = tabId ? document.getElementById(tabId) : $(".sh-body a.btn, .sh-body a", d);
      (first || $(".x", d)).focus({preventScroll:true});
      return true;
    }
    function closeSheet(d, instant){
      d = d || current; if (!d || !d.open) return;
      var done = function(){ d.classList.remove("closing"); d.style.transform=""; if (d.open) d.close(); };
      if (instant || reduce){ done(); }
      else { d.classList.add("closing"); setTimeout(done, 230); }
      if (d === current){ current = null; lock(false); if (opener && opener.focus && !instant) opener.focus({preventScroll:true}); }
    }
    $$("dialog.sheet").forEach(function(d){
      d.addEventListener("cancel", function(e){ e.preventDefault(); closeSheet(d); });
      d.addEventListener("click", function(e){
        if (e.target === d){ var r=d.getBoundingClientRect(); if (e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom) closeSheet(d); }
        if (e.target.closest("[data-close]")) closeSheet(d);
      });
      d.addEventListener("close", function(){ if (current === d){ current=null; lock(false); } });
      // focus trap (on top of showModal's inert background)
      d.addEventListener("keydown", function(e){
        if (e.key !== "Tab") return;
        var f = $$(FOCUSABLE, d).filter(function(el){ return el.offsetParent !== null; });
        if (!f.length) return;
        var a=f[0], z=f[f.length-1];
        if (e.shiftKey && document.activeElement === a){ e.preventDefault(); z.focus(); }
        else if (!e.shiftKey && document.activeElement === z){ e.preventDefault(); a.focus(); }
      });
      // drag down to dismiss (phones)
      var g = $(".grab", d); if (!g) return;
      var y0=0, dy=0, dragging=false;
      g.addEventListener("pointerdown", function(e){ dragging=true; y0=e.clientY; dy=0; d.classList.add("dragging"); g.setPointerCapture(e.pointerId); });
      g.addEventListener("pointermove", function(e){ if(!dragging) return; dy=Math.max(0,e.clientY-y0); d.style.transform="translateY("+dy+"px)"; });
      var end=function(){ if(!dragging) return; dragging=false; d.classList.remove("dragging"); if (dy>90) closeSheet(d); else { d.style.transition="transform .3s cubic-bezier(.22,.8,.2,1)"; d.style.transform=""; setTimeout(function(){ d.style.transition=""; },320); } };
      g.addEventListener("pointerup", end); g.addEventListener("pointercancel", end);
    });
    document.addEventListener("click", function(e){
      var t = e.target.closest("[data-open]"); if (!t) return;
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.button === 1) return; // let new-tab clicks through
      if (openSheet(t.getAttribute("data-open"), t.getAttribute("data-tab"), t)) e.preventDefault();
    });

    /* ---------- Tabs (About sheet) ---------- */
    var tabs = $$('[role="tab"]');
    function selectTab(tab, focus){
      if (!tab) return;
      tabs.forEach(function(t){ var on = t === tab; t.setAttribute("aria-selected", on); t.tabIndex = on ? 0 : -1; document.getElementById(t.getAttribute("aria-controls")).hidden = !on; });
      tab.scrollIntoView({block:"nearest", inline:"nearest"});
      if (focus) tab.focus();
      var body = tab.closest("dialog") && $(".sh-body", tab.closest("dialog")); if (body) body.scrollTop = 0;
    }
    tabs.forEach(function(t, i){
      t.addEventListener("click", function(){ selectTab(t, false); });
      t.addEventListener("keydown", function(e){
        var k=e.key, n=null;
        if (k==="ArrowRight") n=tabs[(i+1)%tabs.length]; else if (k==="ArrowLeft") n=tabs[(i-1+tabs.length)%tabs.length]; else if (k==="Home") n=tabs[0]; else if (k==="End") n=tabs[tabs.length-1];
        if (n){ e.preventDefault(); selectTab(n, true); }
      });
    });

    window.SIUI={open:openSheet,close:closeSheet,tab:selectTab};
  })();
