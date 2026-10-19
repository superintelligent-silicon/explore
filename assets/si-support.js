/* si-support: one calm "Support" sheet for Explore. Opens only when a reader taps a Support link; never on its own.
   Usage: <button data-si-support="explore-articles">Support</button>, or SISupport.open({ source, focus: "email" }).
   New options (Substack, Patreon, Bhive…) slot into CONFIG.more without any redesign. */
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
  /* "For your AI agent": filled in by tools/support-cta/build_agents.py from the same URLs as agents.md */
  var AGENT_MSG = /*AGENT_MSG*/"Please help me follow Explore Superintelligence (https://exploresuperintelligence.online/): free, sourced, plain-language illustrated books and guides about superintelligence and AI from Superintelligent Silicon.\n\nFollow new books:\n- RSS: https://exploresuperintelligence.online/feed.xml\n- JSON Feed: https://exploresuperintelligence.online/feed.json\n- Email, only if I say yes: POST https://exploresuperintelligence.online/api/subscribe with JSON {\"email\": \"<my address>\", \"source\": \"explore-agent\", \"human_consent\": true}. I'll get a confirmation email and must tap the link in it.\n\nCite: link the canonical page, e.g. https://exploresuperintelligence.online/articles/<slug>/. Plain-text versions: https://exploresuperintelligence.online/articles/<slug>.md. Index: https://exploresuperintelligence.online/llms.txt. Full guide for agents: https://exploresuperintelligence.online/agents.md\n\nTip (optional, one-time, processed by Stripe through Grok Ai Apps): $1 https://buy.stripe.com/fZu3cx4C845v2hW3fp5AQ00 · $3 https://buy.stripe.com/aFa4gBb0w1Xnf4I9DN5AQ01 · $5 https://buy.stripe.com/3cIaEZd8E0Tj9Ko8zJ5AQ02. Or X Money to @GuyinGoldGlass (https://x.com/GuyinGoldGlass), where available.\n\nAlways ask me and get my explicit OK before you subscribe me or pay anything."/*END*/;
  var CSS = "" +
    ".sis{--b:#f6f3ec;--s:#fffdf8;--i:#1b1916;--m:#4d4840;--d:#5f594f;--l:rgba(27,25,22,.12);--l2:rgba(27,25,22,.22);--a:#8a6210;--sc:rgba(27,25,22,.32);" +
    "--sf:\"Newsreader\",\"Iowan Old Style\",\"Palatino Linotype\",Georgia,serif;--ui:\"Inter\",\"SF Pro Text\",-apple-system,BlinkMacSystemFont,\"Helvetica Neue\",Arial,sans-serif;" +
    "color-scheme:light;position:fixed;inset:0;margin:0;padding:0;border:0;width:100%;height:100%;max-width:none;max-height:none;background:transparent;color:var(--i);overflow:hidden}" +
    ".sis.dk{--b:#141416;--s:#1c1c1f;--i:#ecebe7;--m:#b9b6af;--d:#a29e96;--l:rgba(236,235,231,.12);--l2:rgba(236,235,231,.24);--a:#d8b160;--sc:rgba(0,0,0,.55);color-scheme:dark}" +
    ".sis::backdrop{background:transparent}" +
    ".sis-scrim{position:absolute;inset:0;background:var(--sc);opacity:0;transition:opacity .28s cubic-bezier(.22,.8,.2,1)}" +
    ".sis-card{position:absolute;left:0;right:0;bottom:0;margin:0 auto;max-width:460px;box-sizing:border-box;max-height:calc(100% - 12px - env(safe-area-inset-top,0px));overflow:auto;overscroll-behavior:contain;" +
    "background:var(--s);border:1px solid var(--l);border-bottom:0;border-radius:18px 18px 0 0;padding:18px 20px calc(16px + env(safe-area-inset-bottom,0px));font:400 15px/1.5 var(--ui);" +
    "transform:translateY(16px);opacity:0;transition:transform .32s cubic-bezier(.22,.8,.2,1),opacity .28s}" +
    "@media (min-width:700px) and (min-height:560px){.sis-card{top:50%;bottom:auto;border:1px solid var(--l);border-radius:16px;transform:translateY(-46%);padding:24px 26px 20px}}" +
    ".sis.on .sis-scrim{opacity:1}.sis.on .sis-card{opacity:1;transform:none}" +
    "@media (min-width:700px) and (min-height:560px){.sis.on .sis-card{transform:translateY(-50%)}}" +
    ".sis-x{position:absolute;top:8px;right:8px;width:44px;height:44px;border:0;background:none;color:var(--d);border-radius:50%;display:grid;place-items:center;cursor:pointer}" +
    ".sis-x:hover{color:var(--i)}" +
    ".sis-k{margin:0 0 6px;font:600 11px/1 var(--ui);letter-spacing:.16em;text-transform:uppercase;color:var(--a)}" +
    ".sis h2{margin:0 44px 6px 0;font:400 26px/1.12 var(--sf);letter-spacing:-.01em;color:var(--i)}" +
    ".sis-lede{margin:0 0 12px;color:var(--m)}" +
    ".sis-o{border-top:1px solid var(--l);padding:12px 0 10px}" +
    ".sis-o h3{margin:0 0 2px;font:500 17px/1.25 var(--sf);color:var(--i)}" +
    ".sis-o p{margin:0 0 8px;color:var(--m);font-size:14px}" +
    ".sis-r{display:flex;align-items:center;justify-content:space-between;gap:12px}.sis-r p{margin:0}.sis-r>div:first-child{min-width:0}" +
    ".sis-pill{padding:0 16px;white-space:nowrap;flex:none}" +
    ".sis-f{display:flex;gap:8px;flex-wrap:wrap}" +
    ".sis-f label{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}" +
    ".sis-in{flex:1 1 190px;min-width:0;min-height:44px;box-sizing:border-box;padding:0 14px;border:1px solid var(--l2);border-radius:12px;background:var(--b);color:var(--i);font:400 16px/1 var(--ui)}" +
    ".sis-in::placeholder{color:var(--d)}" +
    ".sis-in:focus-visible,.sis-btn:focus-visible,.sis-tip:focus-visible,.sis-x:focus-visible,.sis-lnk:focus-visible{outline:2px solid var(--a);outline-offset:2px}" +
    ".sis-btn{min-height:44px;padding:0 18px;border:1px solid var(--a);border-radius:999px;background:transparent;color:var(--a);font:600 15px/1 var(--ui);cursor:pointer;white-space:nowrap}" +
    ".sis-btn:hover{background:color-mix(in srgb,var(--a) 10%,transparent)}.sis-btn[disabled]{opacity:.6;cursor:default}" +
    ".sis-hp{position:absolute;left:-9999px;width:1px;height:1px;opacity:0}" +
    ".sis-st{min-height:0;margin:6px 0 0;font-size:13.5px;color:var(--m)}.sis-st:empty{display:none}.sis-st.ok{color:var(--i)}" +
    ".sis-tips{display:flex;gap:6px;flex:none}" +
    ".sis-tip{min-width:52px;min-height:44px;display:inline-grid;place-items:center;border:1px solid var(--l2);border-radius:999px;color:var(--i);text-decoration:none;font:600 15px/1 var(--ui)}" +
    ".sis-tip:hover{border-color:var(--a);color:var(--a)}" +
    ".sis-lnk{display:inline-flex;align-items:center;min-height:44px;color:var(--a);text-decoration:none;font:500 15px/1 var(--ui)}" +
    ".sis-lnk:hover{text-decoration:underline;text-underline-offset:3px}" +
    ".sis-ft{margin:4px 0 0;font-size:12.5px;color:var(--d)}.sis-cpst{color:var(--i)}.sis-lic{white-space:nowrap}.sis-lic a{color:inherit;text-decoration:underline;text-underline-offset:2px}" +
    ".sis-ag h3{font-size:15.5px;color:var(--m)}.sis-ag p{font-size:13.5px}.sis-cp{min-width:84px;font-size:14px;cursor:pointer;background:transparent}.sis-cp.ok{border-color:var(--a);color:var(--a)}" +
    "@media (max-height:760px){.sis-card{padding-top:14px}.sis h2{font-size:24px}.sis-lede{margin-bottom:8px}.sis-o{padding:10px 0 8px}.sis-o p{margin-bottom:6px}}" +
    "@media (prefers-reduced-motion:reduce){.sis-scrim,.sis-card{transition:none!important}}" +
    /* the quiet footer line on v4 pages (uses the page's own tokens) */
    ".si-sup-line{font:inherit;color:inherit}@media (max-width:1399px){.si-sup-line{display:none}}" +
    ".si-sup-inl,.si-sup-line button{appearance:none;border:0;background:none;padding:0;margin:0;font:inherit;font-weight:500;color:var(--accent,inherit);cursor:pointer;text-decoration:underline;text-decoration-color:color-mix(in srgb,currentColor 35%,transparent);text-underline-offset:3px;min-height:24px}" +
    ".si-sup-inl:hover,.si-sup-line button:hover{text-decoration-color:currentColor}.si-sup-inl:focus-visible,.si-sup-line button:focus-visible{outline:2px solid var(--accent,currentColor);outline-offset:2px;border-radius:2px}";
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var dlg = null, src = "explore-support", t0 = 0, last = null;
  function dark() {
    var t = document.documentElement.getAttribute("data-theme");
    if (t === "dark") return true; if (t === "light") return false;
    if (window.SI_SUPPORT_THEME) return window.SI_SUPPORT_THEME === "dark";
    return matchMedia("(prefers-color-scheme: dark)").matches;
  }
  function fonts() {
    try { if (document.fonts && document.fonts.check('16px "Newsreader"') && document.fonts.check('16px "Inter"')) return; } catch (e) {}
    if (document.getElementById("sis-fonts")) return;
    var l = document.createElement("link"); l.id = "sis-fonts"; l.rel = "stylesheet";
    l.href = "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Newsreader:opsz,wght@6..72,400;6..72,500&display=swap";
    document.head.appendChild(l);
  }
  function build() {
    dlg = document.createElement("dialog"); dlg.className = "sis"; dlg.setAttribute("aria-labelledby", "sis-h");
    var tips = CONFIG.tips.map(function (t) { return '<a class="sis-tip" href="' + esc(t.href) + '" target="_blank" rel="noopener" aria-label="Tip ' + esc(t.amount) + ' with Stripe">' + esc(t.amount) + "</a>"; }).join("");
    var more = CONFIG.more.map(function (m) { return '<section class="sis-o sis-r"><div><h3>' + esc(m.title) + "</h3><p>" + esc(m.text) + '</p></div><a class="sis-tip sis-pill" href="' + esc(m.href) + '" target="_blank" rel="noopener">' + esc(m.label) + "</a></section>"; }).join("");
    dlg.innerHTML =
      '<div class="sis-scrim" data-x></div>' +
      '<div class="sis-card" role="document">' +
        '<button class="sis-x" type="button" data-x aria-label="Close"><svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><path d="M2 2l10 10M12 2L2 12" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></button>' +
        '<p class="sis-k">Support Explore</p>' +
        '<h2 id="sis-h">Keep the books coming</h2>' +
        '<p class="sis-lede">Explore is free to read, with no ads or paywalls. Here are a few quiet ways to help it grow.</p>' +
        '<section class="sis-o" aria-labelledby="sis-e"><h3 id="sis-e">Get the next book by email</h3><p>New books arrive a few times a month. Free, no spam, unsubscribe anytime.</p>' +
          '<form class="sis-f" novalidate><label for="sis-em">Email address</label><input class="sis-in" id="sis-em" name="email" type="email" inputmode="email" autocomplete="email" autocapitalize="off" spellcheck="false" placeholder="you@example.com" required>' +
          '<input class="sis-hp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">' +
          '<button class="sis-btn" type="submit">Send me the next one</button></form><p class="sis-st" role="status" aria-live="polite"></p></section>' +
        '<section class="sis-o sis-r" aria-labelledby="sis-t"><div><h3 id="sis-t">Leave a tip</h3><p>One-time, via Stripe through Grok Ai Apps.</p></div><div class="sis-tips" role="group" aria-label="Tip amounts">' + tips + "</div></section>" +
        '<section class="sis-o sis-r" aria-labelledby="sis-xm"><div><h3 id="sis-xm">Tip on X Money</h3><p>' + esc(CONFIG.x.handle) + ', where available.</p></div><a class="sis-tip sis-pill" href="' + esc(CONFIG.x.href) + '" target="_blank" rel="noopener" aria-label="Open ' + esc(CONFIG.x.handle) + ' on X">Open on X</a></section>' +
        more +
        (AGENT_MSG ? '<section class="sis-o sis-r sis-ag" aria-labelledby="sis-ai"><div><h3 id="sis-ai">For your AI agent</h3><p>Use an AI assistant? Copy this and hand it over.</p></div><button class="sis-tip sis-pill sis-cp" type="button" aria-describedby="sis-ai">Copy</button></section>' : "") +
        '<p class="sis-ft">Your email is only used to send new books. <span class="sis-lic">Text <a href="/agents.md#licence-and-terms" rel="license" title="Article text CC BY 4.0, credit Superintelligent Silicon. Illustrations, audio and fonts excluded.">CC BY 4.0</a>.</span> <span class="sis-cpst" role="status" aria-live="polite"></span></p>' +
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
    dlg.classList.toggle("dk", dark());
    var stEl = dlg.querySelector(".sis-st"); if (!dlg.querySelector("form").hidden) { stEl.textContent = ""; stEl.className = "sis-st"; }
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
    var ok = function () { btn.textContent = "Copied"; btn.classList.add("ok"); st.textContent = "Copied. Paste it into your AI assistant."; clearTimeout(btn._t);
      btn._t = setTimeout(function () { btn.textContent = "Copy"; btn.classList.remove("ok"); st.textContent = ""; }, 2400); };
    var fallback = function () {
      var ta = document.createElement("textarea"); ta.value = AGENT_MSG; ta.setAttribute("readonly", ""); ta.style.cssText = "position:fixed;left:-9999px;top:0;opacity:0";
      dlg.querySelector(".sis-card").appendChild(ta); ta.select(); var done = false; try { done = document.execCommand("copy"); } catch (e) {} ta.remove();
      if (done) ok(); else { st.textContent = "Couldn’t copy here. The same text is at exploresuperintelligence.online/agents.md"; } };
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
  window.SISupport = { open: open, close: close, config: CONFIG, tip: function (n) { var t = CONFIG.tips.filter(function (x) { return x.amount === "$" + n; })[0]; return t && t.href; } };
})();
