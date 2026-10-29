/* si-support: one quiet "Support" sheet for Explore. Opens only when a reader taps a Support link; never on its own.
   Usage: <button data-si-support="explore-articles">Support</button>, or SISupport.open({ source, focus: "email" }).
   New options (Substack, Patreon, Bhive…) slot into CONFIG.more without any redesign.

   v5 (2026-10-29): one card, no dividers. Kicker, one serif line, one sentence, a single email row with an
   inline circular arrow, a quiet tip row, and a quiet footer line of plain text links. The palette is read from
   the page at open time (not the data-theme attribute alone), so it can never open light on a dark page. */
(function () {
  "use strict";
  if (window.SISupport) return;
  var CONFIG = {
    endpoint: "/api/subscribe",
    tips: [
      { amount: "$1", href: "https://buy.stripe.com/fZu3cx4C845v2hW3fp5AQ00" },
      { amount: "$3", href: "https://buy.stripe.com/aFa4gBb0w1Xnf4I9DN5AQ01" },
      { amount: "$5", href: "https://buy.stripe.com/3cIaEZd8E0Tj9Ko8zJ5AQ02" }
    ],
    x: { handle: "@GuyinGoldGlass", href: "https://x.com/GuyinGoldGlass" },
    /* later: { id: "substack", title: "Read on Substack", text: "…", label: "Open Substack", href: "https://…" } */
    more: []
  };
  var AGENT_MSG = /*AGENT_MSG*/"Please help me follow Explore Superintelligence (https://exploresuperintelligence.online/): free, sourced, plain-language illustrated books and guides about superintelligence and AI from Superintelligent Silicon.\n\nFollow new books:\n- RSS: https://exploresuperintelligence.online/feed.xml\n- JSON Feed: https://exploresuperintelligence.online/feed.json\n- Email, only if I say yes: POST https://exploresuperintelligence.online/api/subscribe with JSON {\"email\": \"<my address>\", \"source\": \"explore-agent\", \"human_consent\": true}. I'll get a confirmation email and must tap the link in it.\n\nCite: link the canonical page, e.g. https://exploresuperintelligence.online/articles/<slug>/. Plain-text versions: https://exploresuperintelligence.online/articles/<slug>.md. Index: https://exploresuperintelligence.online/llms.txt. Full guide for agents: https://exploresuperintelligence.online/agents.md\n\nTip (optional, one-time, processed by Stripe through Grok Ai Apps): $1 https://buy.stripe.com/fZu3cx4C845v2hW3fp5AQ00 · $3 https://buy.stripe.com/aFa4gBb0w1Xnf4I9DN5AQ01 · $5 https://buy.stripe.com/3cIaEZd8E0Tj9Ko8zJ5AQ02. Or X Money to @GuyinGoldGlass (https://x.com/GuyinGoldGlass), where available.\n\nAlways ask me and get my explicit OK before you subscribe me or pay anything."/*END*/;
  /* light default; .dk overrides every value that matters for contrast */
  var CSS = "" +
    ".sis{--s:#fffdf8;--b:#faf7f1;--i:#1b1916;--m:#56514a;--d:#6d665c;--ln:rgba(27,25,22,.10);--ln2:rgba(27,25,22,.18);--a:#8a6210;--sc:rgba(27,25,22,.34);" +
    "--sf:\"Newsreader\",\"Iowan Old Style\",\"Palatino Linotype\",Georgia,serif;--ui:\"Inter\",\"SF Pro Text\",-apple-system,BlinkMacSystemFont,\"Helvetica Neue\",Arial,sans-serif;" +
    "color-scheme:light;position:fixed;inset:0;margin:0;padding:0;border:0;width:100%;height:100%;max-width:none;max-height:none;background:transparent;color:var(--i);overflow:hidden}" +
    ".sis.dk{--s:#141416;--b:#1c1c1f;--i:#ecebe7;--m:#b6b2aa;--d:#8f8b83;--ln:rgba(236,235,231,.10);--ln2:rgba(236,235,231,.18);--a:#d8b160;--sc:rgba(0,0,0,.58);color-scheme:dark}" +
    ".sis::backdrop{background:transparent}" +
    ".sis-scrim{position:absolute;inset:0;background:var(--sc);opacity:0;transition:opacity .26s cubic-bezier(.22,.8,.2,1)}" +
    ".sis-card{position:absolute;left:0;right:0;bottom:0;margin:0 auto;max-width:430px;box-sizing:border-box;max-height:calc(100% - 10px - env(safe-area-inset-top,0px));overflow:auto;overscroll-behavior:contain;" +
      "background:var(--s);border:1px solid var(--ln);border-bottom:0;border-radius:20px 20px 0 0;box-shadow:0 -1px 0 rgba(0,0,0,.02),0 -18px 40px -28px rgba(0,0,0,.35);" +
      "padding:26px 22px calc(20px + env(safe-area-inset-bottom,0px));font:400 15px/1.5 var(--ui);" +
      "transform:translateY(14px);opacity:0;transition:transform .3s cubic-bezier(.22,.8,.2,1),opacity .24s}" +
    "@media (min-width:700px) and (min-height:520px){.sis-card{top:50%;bottom:auto;border:1px solid var(--ln);border-radius:18px;transform:translateY(-46%);padding:26px 28px 24px;" +
      "box-shadow:0 30px 70px -40px rgba(0,0,0,.5),0 2px 10px -6px rgba(0,0,0,.2)}}" +
    ".sis.on .sis-scrim{opacity:1}.sis.on .sis-card{opacity:1;transform:none}" +
    "@media (min-width:700px) and (min-height:520px){.sis.on .sis-card{transform:translateY(-50%)}}" +
    ".sis-x{position:absolute;top:6px;right:6px;box-sizing:border-box;padding:0;width:44px;height:44px;border:0;background:none;color:var(--d);border-radius:50%;display:grid;place-items:center;cursor:pointer;transition:color .18s}" +
    ".sis-x:hover{color:var(--i)}" +
    ".sis-k{margin:0 0 8px;font:600 10.5px/1 var(--ui);letter-spacing:.17em;text-transform:uppercase;color:var(--a)}" +
    ".sis h2{margin:0 34px 10px 0;font:400 27px/1.1 var(--sf);letter-spacing:-.012em;color:var(--i);text-wrap:balance}" +
    ".sis-lede{margin:0 0 20px;font-size:14.5px;line-height:1.5;color:var(--m);max-width:34ch}" +
    /* one email row: input with the submit arrow inside its right edge */
    ".sis-f{margin:0}" +
    ".sis-f label{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}" +
    ".sis-mail{position:relative;display:block}" +
    ".sis-in{display:block;width:100%;box-sizing:border-box;min-height:52px;padding:0 58px 0 16px;border:1px solid var(--ln2);border-radius:14px;background:var(--b);color:var(--i);font:400 16px/1 var(--ui);transition:border-color .18s,background-color .18s}" +
    ".sis-in::placeholder{color:var(--d)}" +
    ".sis-in:hover{border-color:color-mix(in srgb,var(--ln2) 55%,var(--a))}" +
    ".sis-in:focus-visible{outline:none;border-color:var(--a);box-shadow:0 0 0 3px color-mix(in srgb,var(--a) 22%,transparent)}" +
    ".sis-btn{position:absolute;right:4px;top:50%;transform:translateY(-50%);width:44px;height:44px;min-width:44px;min-height:44px;padding:0;border:0;border-radius:50%;display:grid;place-items:center;cursor:pointer;" +
      "background:var(--a);color:var(--s);transition:opacity .18s,transform .18s}" +
    ".sis-btn svg{width:17px;height:17px;display:block;transition:transform .2s}" +
    ".sis-btn:hover{opacity:.9}.sis-btn:hover svg{transform:translateX(1px)}" +
    ".sis-btn:focus-visible{outline:2px solid var(--a);outline-offset:3px}" +
    ".sis-btn[disabled]{opacity:.55;cursor:default}.sis-btn[disabled] svg{transform:none}" +
    ".sis-hp{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip-path:inset(50%);white-space:nowrap;border:0;opacity:0;pointer-events:none}" +
    ".sis-st{margin:9px 0 0;font-size:13px;line-height:1.45;color:var(--m)}.sis-st:empty{display:none}.sis-st.ok{color:var(--i)}" +
    /* tip + footer rows: no rules, whitespace only */
    ".sis-row{display:flex;align-items:center;justify-content:space-between;gap:12px;margin:20px 0 0}" +
    ".sis-row>span{font-size:13.5px;color:var(--m);min-width:0}" +
    ".sis-tips{display:flex;gap:7px;flex:none}" +
    ".sis-tip{min-width:46px;min-height:44px;padding:0 12px;display:inline-grid;place-items:center;box-sizing:border-box;border:1px solid var(--ln2);border-radius:999px;color:var(--i);text-decoration:none;font:500 14px/1 var(--ui);transition:border-color .18s,color .18s}" +
    ".sis-tip:hover{border-color:var(--a);color:var(--a)}" +
    ".sis-tip:focus-visible{outline:2px solid var(--a);outline-offset:2px}" +
    ".sis-ft{margin:20px 0 0;display:flex;flex-wrap:wrap;align-items:center;gap:0 15px;font-size:12.5px;line-height:1.4;color:var(--d)}" +
    ".sis-lnk{display:inline-flex;align-items:center;min-height:44px;padding:0;border:0;background:none;color:inherit;font:inherit;text-decoration:underline;" +
      "text-decoration-color:color-mix(in srgb,currentColor 30%,transparent);text-underline-offset:3px;cursor:pointer;transition:color .18s,text-decoration-color .18s}" +
    ".sis-lnk:hover{color:var(--i);text-decoration-color:currentColor}" +
    ".sis-lnk:focus-visible{outline:2px solid var(--a);outline-offset:2px;border-radius:3px}" +
    ".sis-cpst:empty{display:none}.sis-cpst{flex-basis:100%;font-size:12px;color:var(--d)}" +
    ".sis-more{margin:14px 0 0;display:flex;flex-wrap:wrap;gap:6px 14px}" +
    "@media (max-width:400px){.sis-card{padding:24px 20px calc(18px + env(safe-area-inset-bottom,0px))}.sis h2{font-size:25px}.sis-lede{margin-bottom:18px}.sis-row{margin-top:18px}.sis-ft{margin-top:18px;font-size:12px;gap:0 10px}}" +
    "@media (max-height:700px){.sis-card{padding-top:20px}.sis h2{font-size:24px;margin-bottom:8px}.sis-lede{margin-bottom:16px;font-size:14px}.sis-row{margin-top:15px}.sis-ft{margin-top:14px}.sis-in{min-height:48px}}" +
    "@media (prefers-reduced-motion:reduce){.sis-scrim,.sis-card,.sis-btn svg{transition:none!important}}" +
    /* the quiet footer line on v4 pages (uses the page's own tokens) */
    ".si-sup-line{font:inherit;color:inherit}@media (max-width:1399px){.si-sup-line{display:none}}" +
    ".si-sup-inl,.si-sup-line button{appearance:none;border:0;background:none;padding:0;margin:0;font:inherit;font-weight:500;color:var(--accent,inherit);cursor:pointer;text-decoration:underline;text-decoration-color:color-mix(in srgb,currentColor 35%,transparent);text-underline-offset:3px;min-height:24px}" +
    ".si-sup-inl:hover,.si-sup-line button:hover{text-decoration-color:currentColor}.si-sup-inl:focus-visible,.si-sup-line button:focus-visible{outline:2px solid var(--accent,currentColor);outline-offset:2px;border-radius:2px}";

  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };

  var dlg = null, src = "explore-support", t0 = 0, last = null, cpT = 0;

  /* ---- which palette? Read the page as it actually renders, every time we open. ---- */
  function parseRGB(str) {
    var m = /rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)(?:[,\s/]+([\d.]+))?\s*\)/.exec(str || "");
    if (!m) return null;
    var a = m[4] === undefined ? 1 : +m[4];
    if (a < 0.5) return null;                    /* see-through layer: not a ground colour */
    return [+m[1], +m[2], +m[3]];
  }
  function luminance(rgb) { return (0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]) / 255; }
  /* walk up from an element to the first ancestor that actually paints a background */
  function paintedBG(el) {
    for (var n = el; n && n.nodeType === 1; n = n.parentElement) {
      var c = parseRGB(getComputedStyle(n).backgroundColor);
      if (c) return c;
    }
    return null;
  }
  function pageIsDark() {
    var root = document.documentElement, body = document.body;
    var t = root.getAttribute("data-theme");
    if (t === "dark") return true;
    if (t === "light") return false;
    /* a page-level signal, for pages that commit to a palette without the attribute */
    var s = root.getAttribute("data-sis-theme") || root.getAttribute("data-theme-forced") || window.SI_SUPPORT_THEME || window.SI_NAV_THEME;
    if (s === "dark") return true;
    if (s === "light") return false;
    /* luminance of what the reader is actually looking at */
    var rgb = paintedBG(body) || paintedBG(root);
    if (rgb) return luminance(rgb) < 0.5;
    return !!(window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches);
  }

  function fonts() {
    try { if (document.fonts && document.fonts.check('16px "Newsreader"') && document.fonts.check('16px "Inter"')) return; } catch (e) {}
    if (document.getElementById("sis-fonts")) return;
    var l = document.createElement("link"); l.id = "sis-fonts"; l.rel = "stylesheet";
    l.href = "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Newsreader:opsz,wght@6..72,400;6..72,500&display=swap";
    document.head.appendChild(l);
  }

  var ARROW = '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M4 10h11M10.5 5.5L15 10l-4.5 4.5" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>';

  function build() {
    dlg = document.createElement("dialog"); dlg.className = "sis"; dlg.setAttribute("aria-labelledby", "sis-h");
    var tips = CONFIG.tips.map(function (t) {
      return '<a class="sis-tip" href="' + esc(t.href) + '" target="_blank" rel="noopener" aria-label="Tip ' + esc(t.amount) + ' with Stripe">' + esc(t.amount) + "</a>";
    }).join("");
    var more = CONFIG.more.map(function (m) {
      return '<a class="sis-lnk" href="' + esc(m.href) + '" target="_blank" rel="noopener">' + esc(m.label) + "</a>";
    }).join("");
    dlg.innerHTML =
      '<div class="sis-scrim" data-x></div>' +
      '<div class="sis-card" role="document">' +
        '<button class="sis-x" type="button" data-x aria-label="Close">' +
          '<svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><path d="M2 2l10 10M12 2L2 12" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></button>' +
        '<p class="sis-k">Support Explore SI</p>' +
        '<h2 id="sis-h">Keep the books coming</h2>' +
        '<p class="sis-lede">Free to read, no ads, no paywalls. Here is the quiet way to help.</p>' +
        '<form class="sis-f" novalidate>' +
          '<label for="sis-em">Email address</label>' +
          '<span class="sis-mail">' +
            '<input class="sis-in" id="sis-em" name="email" type="email" inputmode="email" autocomplete="email" autocapitalize="off" spellcheck="false" placeholder="Your email" required aria-label="Email address">' +
            '<button class="sis-btn" type="submit" aria-label="Subscribe by email">' + ARROW + '</button>' +
          '</span>' +
          '<input class="sis-hp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">' +
        '</form>' +
        '<p class="sis-st" role="status" aria-live="polite"></p>' +
        '<div class="sis-row"><span id="sis-t">Leave a tip</span><div class="sis-tips" role="group" aria-labelledby="sis-t">' + tips + '</div></div>' +
        '<p class="sis-ft">' +
          '<a class="sis-lnk" href="' + esc(CONFIG.x.href) + '" target="_blank" rel="noopener" aria-label="X Money, ' + esc(CONFIG.x.handle) + ' on X">X Money ' + esc(CONFIG.x.handle) + '</a>' +
          (AGENT_MSG ? '<button class="sis-lnk sis-cp" type="button" aria-label="Copy the agent message">For your AI agent</button>' : '') +
          '<a class="sis-lnk sis-lic" href="/agents.md#licence-and-terms" rel="license" title="Article text CC BY 4.0, credit Superintelligent Silicon. Illustrations, audio and fonts excluded.">CC BY 4.0</a>' +
          '<span class="sis-cpst" role="status" aria-live="polite"></span>' +
        '</p>' +
        (more ? '<div class="sis-more">' + more + "</div>" : "") +
      "</div>";
    document.body.appendChild(dlg);
    dlg.addEventListener("click", function (e) { if (e.target.closest("[data-x]")) close(); });
    dlg.addEventListener("cancel", function (e) { e.preventDefault(); close(); });
    dlg.querySelector("form").addEventListener("submit", submit);
    var cp = dlg.querySelector(".sis-cp"); if (cp) cp.addEventListener("click", function () { copyAgent(cp); });
    /* keys typed in the sheet must not turn the book's pages behind it */
    window.addEventListener("keydown", function (e) { if (dlg.open && e.key !== "Tab") { e.stopPropagation(); if (e.key === "Escape") { e.preventDefault(); close(); } } }, true);
    ["pointerdown", "touchstart", "wheel"].forEach(function (t) { dlg.addEventListener(t, function (e) { e.stopPropagation(); }, { passive: true }); });
  }

  function open(o) {
    o = o || {}; if (!dlg) build(); fonts();
    src = o.source || src; last = document.activeElement; t0 = Date.now();
    [].forEach.call(document.querySelectorAll("dialog[open]"), function (d) { if (d !== dlg) { try { d.close(); } catch (e) {} } });
    /* always resolve the palette at open time, so a theme switch behind the sheet is honoured */
    dlg.classList.toggle("dk", pageIsDark());
    var stEl = dlg.querySelector(".sis-st"); stEl.textContent = ""; stEl.className = "sis-st";
    var btn = dlg.querySelector(".sis-btn"); if (btn) btn.disabled = false;
    if (!dlg.open) { try { dlg.showModal(); } catch (e) { dlg.setAttribute("open", ""); } }
    requestAnimationFrame(function () { dlg.classList.add("on"); });
    var f = o.focus === "email" ? dlg.querySelector("#sis-em") : dlg.querySelector(".sis-x");
    setTimeout(function () { try { f.focus({ preventScroll: true }); } catch (e) {} }, 60);
  }

  function close() {
    if (!dlg || !dlg.open) return; dlg.classList.remove("on");
    var done = function () { try { dlg.close(); } catch (e) { dlg.removeAttribute("open"); } if (last && last.focus) try { last.focus({ preventScroll: true }); } catch (e) {} };
    if (matchMedia("(prefers-reduced-motion: reduce)").matches) done(); else setTimeout(done, 240);
  }

  function copyAgent(btn) {
    var st = dlg.querySelector(".sis-cpst");
    var ok = function () {
      btn.textContent = "Copied"; btn.classList.add("ok"); st.textContent = "Copied. Paste it into your AI assistant."; clearTimeout(btn._t);
      btn._t = setTimeout(function () { btn.textContent = "For your AI agent"; btn.classList.remove("ok"); st.textContent = ""; }, 2400);
    };
    var fallback = function () {
      var ta = document.createElement("textarea"); ta.value = AGENT_MSG; ta.setAttribute("readonly", ""); ta.style.cssText = "position:fixed;left:-9999px;top:0;opacity:0";
      dlg.querySelector(".sis-card").appendChild(ta); ta.select(); var done = false; try { done = document.execCommand("copy"); } catch (e) {} ta.remove();
      if (done) ok(); else { st.textContent = "Couldn’t copy here. The same text is at exploresuperintelligence.online/agents.md"; }
    };
    if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(AGENT_MSG).then(ok, fallback); else fallback();
  }

  function submit(e) {
    e.preventDefault();
    var f = e.currentTarget, em = f.email.value.trim(), st = dlg.querySelector(".sis-st"), b = f.querySelector(".sis-btn");
    st.className = "sis-st";
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em)) { st.textContent = "Please enter a valid email address."; f.email.focus(); return; }
    b.disabled = true; st.textContent = "Sending…";
    setTimeout(function () { send(f, em, st, b); }, Math.max(0, 1700 - (Date.now() - t0)));
  }

  function send(f, em, st, b) {
    fetch(CONFIG.endpoint, { method: "POST", headers: { "Content-Type": "application/json" }, credentials: "omit",
      body: JSON.stringify({ email: em, source: src, website: f.website.value, dwell_ms: Math.max(Date.now() - t0, 0) }) })
      .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
      .then(function (j) {
        b.disabled = false;
        if (j && j.ok) { st.className = "sis-st ok"; st.textContent = "Almost there. Check your inbox for a link to confirm, and the next book will find you."; f.reset(); }
        else st.textContent = (j && j.error) || "That didn’t go through. Please try again in a moment.";
      })
      .catch(function () { b.disabled = false; st.textContent = "That didn’t go through. Please check your connection and try again."; });
  }

  (function () { var st = document.createElement("style"); st.id = "sis-css"; st.textContent = CSS; (document.head || document.documentElement).appendChild(st); })();
  document.addEventListener("click", function (e) {
    var t = e.target.closest && e.target.closest("[data-si-support]"); if (!t) return;
    e.preventDefault(); open({ source: t.getAttribute("data-si-support"), focus: t.getAttribute("data-si-focus") || "" });
  });
  window.SISupport = { open: open, close: close, config: CONFIG, theme: pageIsDark, tip: function (n) { var t = CONFIG.tips.filter(function (x) { return x.amount === "$" + n; })[0]; return t && t.href; } };
})();
