/* Explore v4: navigation progress. Shared by exploresuperintelligence.online and superintelligentsilicon.com.
   - Leaving a page: if the next page hasn't arrived within ~150ms, the page fades to its own background with a thin
     gold progress line and a small breathing SI mark. Fast loads never show it.
   - Arriving: the page fades in (cross-document View Transitions where supported, a short CSS fade otherwise).
   - Never on: new tabs, modifier clicks, downloads/files, external or Stripe links, hash links, same-document
     history (books' page turns), reloads, links or events whose default was prevented.
   - Back/forward cache: the overlay is cleared on pageshow(persisted) and a safety timeout means it can't stick.
   Include early in <head>, without defer: <script src="/assets/si-nav.js"></script>  Opt out a link: data-si-nav="off". */
(function () {
  "use strict";
  var W = window, D = document, d = D.documentElement;
  if (W.__siNav) return; W.__siNav = 1;
  var DELAY = 150, SAFETY = 12000, KEY = "si-nav-t";
  var HOSTS = ["exploresuperintelligence.online", "www.exploresuperintelligence.online",
               "superintelligentsilicon.com", "www.superintelligentsilicon.com"];
  var FILE = /\.(pdf|zip|gz|mp3|m4a|wav|ogg|mp4|webm|mov|png|jpe?g|gif|webp|avif|svg|ico|md|txt|xml|json|csv|vcf|ics|woff2?)$/i;

  var css =
    "@view-transition{navigation:auto}" +
    "::view-transition-old(root),::view-transition-new(root){animation-duration:.24s;animation-timing-function:cubic-bezier(.2,.7,.2,1)}" +
    "#si-nav{position:fixed;inset:0;z-index:2147483600;pointer-events:none;opacity:0;visibility:hidden;contain:strict;" +
      "background:var(--sn-bg);transition:opacity .2s ease,visibility 0s linear .2s;-webkit-tap-highlight-color:transparent}" +
    "#si-nav.on{opacity:1;visibility:visible;transition:opacity .22s ease}" +
    "#si-nav.cut{transition:none!important}" +
    "#si-nav[data-t=light]{--sn-bg:#f6f3ec;--sn-ac:#8a6210;--sn-ln:rgba(27,25,22,.08);--sn-ring:rgba(27,25,22,.22);--sn-cap:#6b655b}" +
    "#si-nav[data-t=dark]{--sn-bg:#141416;--sn-ac:#d8b160;--sn-ln:rgba(236,235,231,.08);--sn-ring:rgba(236,235,231,.22);--sn-cap:#97938b}" +
    "#si-nav .sn-bar{position:absolute;left:0;right:0;top:env(safe-area-inset-top,0px);height:2px;background:var(--sn-ln);overflow:hidden}" +
    "#si-nav .sn-bar i{position:absolute;inset:0;background:var(--sn-ac);transform-origin:0 50%;transform:scaleX(0)}" +
    "#si-nav.on .sn-bar i{animation:sn-prog 9s cubic-bezier(.08,.7,.15,1) forwards}" +
    "@keyframes sn-prog{0%{transform:scaleX(0)}6%{transform:scaleX(.28)}30%{transform:scaleX(.62)}100%{transform:scaleX(.94)}}" +
    "#si-nav .sn-mk{position:absolute;left:50%;top:50%;width:26px;height:26px;margin:-13px 0 0 -13px;opacity:0;transition:opacity .3s ease}" +
    "#si-nav.on .sn-mk,#si-nav.on .sn-cap{opacity:1;transition-delay:.35s}" +
    "#si-nav .sn-cap{position:absolute;left:0;right:0;top:calc(50% + 24px);text-align:center;opacity:0;transition:opacity .3s ease;" +
      "font:600 10.5px/1 Inter,system-ui,-apple-system,'Segoe UI',sans-serif;letter-spacing:.16em;text-transform:uppercase;color:var(--sn-cap)}" +
    "#si-nav .sn-mk circle.r1{stroke:var(--sn-ring)}#si-nav .sn-mk circle.r2{stroke:var(--sn-ac)}" +
    "#si-nav .sn-mk circle.dt{fill:var(--sn-ac);transform-origin:13px 13px;animation:sn-breathe 1.8s ease-in-out infinite}" +
    "@keyframes sn-breathe{0%,100%{opacity:.4;transform:scale(.75)}50%{opacity:1;transform:scale(1)}}" +
    "html.si-nav-arrive body{animation:sn-in .26s ease-out both}" +
    "@keyframes sn-in{from{opacity:0}to{opacity:1}}" +
    "@media (prefers-reduced-motion:reduce){" +
      "#si-nav .sn-bar{display:none}#si-nav .sn-mk circle.dt{animation:none;opacity:.8}" +
      "::view-transition-old(root),::view-transition-new(root){animation-duration:.18s}}";
  var st = D.createElement("style"); st.id = "si-nav-css"; st.textContent = css;
  (D.head || d).appendChild(st);

  var el = null, timer = 0, safety = 0, pending = false, clickEv = null;
  function ensure() {
    if (el && el.isConnected) return el;
    el = D.createElement("div"); el.id = "si-nav"; el.setAttribute("aria-hidden", "true");
    el.innerHTML = '<div class="sn-bar"><i></i></div><svg class="sn-mk" viewBox="0 0 26 26" fill="none">' +
      '<circle class="r1" cx="13" cy="13" r="11.5"/><circle class="r2" cx="13" cy="13" r="6"/><circle class="dt" cx="13" cy="13" r="2"/></svg><span class="sn-cap"></span>';
    el.querySelector(".sn-cap").textContent = /superintelligentsilicon\.com$/.test(location.hostname) ? "Superintelligent Silicon" : "Explore SI";
    (D.body || d).appendChild(el); return el;
  }
  function lum(el2) {
    if (!el2) return null;
    var m = /rgba?\(([\d.]+)[, ]+([\d.]+)[, ]+([\d.]+)(?:[,/ ]+([\d.]+))?/.exec(getComputedStyle(el2).backgroundColor || "");
    if (!m || (m[4] !== undefined && +m[4] < 0.5)) return null;
    return (0.2126 * m[1] + 0.7152 * m[2] + 0.0722 * m[3]) / 255 < 0.5 ? "dark" : "light";
  }
  function theme() {
    var t = d.getAttribute("data-theme");
    if (t === "dark" || t === "light") return t;
    t = W.SI_NAV_THEME || W.SI_SUPPORT_THEME;
    if (t === "dark" || t === "light") return t;
    return lum(D.body) || lum(d) || (W.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  }
  function show() {
    timer = 0;
    if (!pending || (clickEv && clickEv.defaultPrevented)) { reset(); return; }
    var o = ensure(); o.setAttribute("data-t", theme()); void o.offsetWidth;
    o.classList.add("on"); d.setAttribute("aria-busy", "true"); d.setAttribute("data-si-nav", "on");
  }
  function start(ev) {
    clickEv = ev || null;
    if (pending) return; pending = true;
    try { sessionStorage.setItem(KEY, String(Date.now())); } catch (e) {}
    timer = setTimeout(show, DELAY);
    safety = setTimeout(function () { reset(); }, SAFETY);
  }
  function reset(instant) {
    clearTimeout(timer); clearTimeout(safety); timer = safety = 0; pending = false; clickEv = null;
    d.removeAttribute("aria-busy"); d.removeAttribute("data-si-nav");
    if (el) {
      if (instant) { el.classList.add("cut"); el.classList.remove("on"); void el.offsetWidth; el.classList.remove("cut"); }
      else el.classList.remove("on");
    }
  }

  function ok(u, viaClick) {
    if (!u || !/^https?:$/.test(u.protocol)) return false;
    if (u.origin !== location.origin && HOSTS.indexOf(u.hostname) < 0) return false; // external, incl. Stripe
    if (/(^|\.)stripe\.com$/i.test(u.hostname)) return false;
    if (FILE.test(u.pathname)) return false;
    if (u.origin === location.origin && u.pathname === location.pathname && u.search === location.search &&
        (u.hash || viaClick)) return false; // hash links / same page
    return true;
  }

  if (W.navigation && typeof W.navigation.addEventListener === "function") {
    W.navigation.addEventListener("navigate", function (e) {
      if (e.defaultPrevented || e.hashChange || e.downloadRequest || e.navigationType === "reload") return;
      if (!e.destination || e.destination.sameDocument) return;
      var u; try { u = new URL(e.destination.url); } catch (x) { return; }
      if (e.navigationType !== "traverse" && !ok(u, false)) return;
      if (e.navigationType === "traverse" && (FILE.test(u.pathname) || (u.origin !== location.origin && HOSTS.indexOf(u.hostname) < 0))) return;
      start();
    });
    W.navigation.addEventListener("navigateerror", function () { reset(); });
  } else {
    D.addEventListener("click", function (e) {
      if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      var a = e.target && e.target.closest ? e.target.closest("a[href]") : null;
      if (!a || a.hasAttribute("download") || a.getAttribute("data-si-nav") === "off") return;
      var tg = (a.getAttribute("target") || "").toLowerCase();
      if (tg && tg !== "_self" && tg !== "_top" && tg !== "_parent") return;
      if ((a.getAttribute("href") || "").charAt(0) === "#") return;
      var u; try { u = new URL(a.href, location.href); } catch (x) { return; }
      if (!ok(u, true)) return;
      start(e);
    });
  }
  // opt-out links still fire navigate; honour data-si-nav="off" there too
  D.addEventListener("click", function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a[data-si-nav="off"]') : null;
    if (a) setTimeout(function () { reset(true); }, 0);
  }, true);

  W.addEventListener("pagehide", function (e) { if (e.persisted) { clearTimeout(timer); clearTimeout(safety); timer = safety = 0; } });
  W.addEventListener("pageshow", function (e) {
    if (e.persisted) { reset(true); try { sessionStorage.removeItem(KEY); } catch (x) {} }
  });

  // Arrival fade (only after one of our navigations, or arriving from the sibling site)
  var arrive = false, nt = "";
  try { var pe = performance.getEntriesByType("navigation")[0]; nt = pe ? pe.type : ""; } catch (e) {}
  if (nt !== "reload") {
    try { var t0 = +sessionStorage.getItem(KEY); if (t0 && Date.now() - t0 < 15000) arrive = true; sessionStorage.removeItem(KEY); } catch (e) {}
    if (!arrive && D.referrer) {
      try { var r = new URL(D.referrer); if (r.origin !== location.origin && HOSTS.indexOf(r.hostname) >= 0) arrive = true; } catch (e) {}
    }
  }
  function fadeIn() { d.classList.add("si-nav-arrive"); setTimeout(function () { d.classList.remove("si-nav-arrive"); }, 450); }
  if (arrive) {
    if ("onpagereveal" in W) W.addEventListener("pagereveal", function (e) { if (!e.viewTransition) fadeIn(); }, { once: true });
    else fadeIn();
  }
  W.SINav = { start: start, reset: reset, show: show };
})();
