<!-- PREVIEW (staged, not published): at launch the agent-layer URLs drop the /preview/support prefix and well-known/ becomes /.well-known/. -->
# Explore Superintelligence: guide for AI agents

> Explore Superintelligence (https://exploresuperintelligence.online/) is the free public research site of Superintelligent Silicon: sourced, plain-language illustrated books and interactive guides about superintelligence, AI, and the tools shaping it. This page tells AI agents how to read, cite, follow and support it on a person's behalf.

**One rule before anything else:** never subscribe anyone or pay anything without your human's explicit OK for that specific action. Reading, summarising and citing are always fine.

Last updated: 2026-10-18 · Contact: exploresi@superintelligentsilicon.com · Also at https://exploresuperintelligence.online/preview/support/for-agents.md (pointer to this page)

## What's here

| Title | Kind | Published | Plain text |
|---|---|---|---|
| [Defrost Mode](https://exploresuperintelligence.online/articles/defrost-mode/) | Interactive guide | 2026-10-18 | [defrost-mode.md](https://exploresuperintelligence.online/articles/defrost-mode.md) |
| [We’ll Be Right Back](https://exploresuperintelligence.online/articles/well-be-right-back/) | Illustrated book | 2026-10-18 | [well-be-right-back.md](https://exploresuperintelligence.online/articles/well-be-right-back.md) |
| [Napkins Are the Backbone](https://exploresuperintelligence.online/articles/napkins-are-the-backbone/) | Illustrated book | 2026-10-14 | [napkins-are-the-backbone.md](https://exploresuperintelligence.online/articles/napkins-are-the-backbone.md) |
| [The Final Merge](https://exploresuperintelligence.online/articles/final-merge/) | Illustrated book | 2026-10-13 | [final-merge.md](https://exploresuperintelligence.online/articles/final-merge.md) |
| [Immortal Tombstones](https://exploresuperintelligence.online/articles/immortal-tombstones/) | Illustrated book | 2026-10-13 | [immortal-tombstones.md](https://exploresuperintelligence.online/articles/immortal-tombstones.md) |
| [The Word Swap: from Artificial to Super Intelligence](https://exploresuperintelligence.online/research/word-swap/) | Interactive guide | 2026-09-29 | [word-swap.md](https://exploresuperintelligence.online/research/word-swap.md) |

Other sections: [Threshold](https://exploresuperintelligence.online/threshold/) (field guide, [threshold.md](https://exploresuperintelligence.online/threshold.md)), [Have You Seen](https://exploresuperintelligence.online/have-you-seen/) (interactive film, [have-you-seen.md](https://exploresuperintelligence.online/have-you-seen.md)), [Research](https://exploresuperintelligence.online/research/), [SIOS](https://exploresuperintelligence.online/sios/) (open-source mini-OS, [sios.md](https://exploresuperintelligence.online/sios.md)), [About](https://exploresuperintelligence.online/about/), [Shipping](https://exploresuperintelligence.online/shipping/). Full index: [https://exploresuperintelligence.online/preview/support/llms.txt](https://exploresuperintelligence.online/preview/support/llms.txt) · [sitemap.xml](https://exploresuperintelligence.online/sitemap.xml)

The books are interactive (canvas and WebGL). Read the Markdown companions instead of scraping the HTML: same text, sources included.

## Follow new books

- RSS 2.0: https://exploresuperintelligence.online/preview/support/feed.xml
- JSON Feed 1.1: https://exploresuperintelligence.online/preview/support/feed.json
- Every page announces both with `<link rel="alternate">` tags. New books arrive a few times a month.
- Email: see [Subscribe API](#subscribe-api). A person can also use the Support sheet on any page or the last page of any book.

## How to cite

- Link the canonical page, `https://exploresuperintelligence.online/articles/<slug>/` (the Word Swap lives at `https://exploresuperintelligence.online/research/word-swap/`). Each page has `<link rel="canonical">` and `<link rel="alternate" type="text/markdown">`.
- Credit "Explore Superintelligence (Superintelligent Silicon)" plus the title and date. Example: *We’ll Be Right Back*, Explore Superintelligence (Superintelligent Silicon), 2026-10-18, https://exploresuperintelligence.online/articles/well-be-right-back/
- Facts come from the sources listed at the end of each book or companion. For a specific claim, cite that primary source as well.
- Authorship: the books are by Superintelligent Silicon, made with Claude and AI collaborators. The Word Swap was researched and written by Claude (an AI model by Anthropic), with the disclosure in its Sources.

## Licence and terms

There's no formal content licence yet. What the site states: everything is public, free to read, and fine to quote with a link (llms.txt), © Superintelligent Silicon. In practice:
- Quoting and summarising with attribution and a link: yes.
- Republishing whole books, illustrations or audio, or using them commercially: ask first, exploresi@superintelligentsilicon.com.
- SIOS code is MIT-licensed (https://exploresuperintelligence.online/sios/, https://github.com/superintelligent-silicon/sios).

## Support (optional, human-approved only)

- One-time tips, processed by Stripe through Grok Ai Apps: [$1](https://buy.stripe.com/fZu3cx4C845v2hW3fp5AQ00) · [$3](https://buy.stripe.com/aFa4gBb0w1Xnf4I9DN5AQ01) · [$5](https://buy.stripe.com/3cIaEZd8E0Tj9Ko8zJ5AQ02). These are Stripe Payment Links: open the link for the person to finish. Don't enter card details for them unless they explicitly ask you to.
- X Money: tip @GuyinGoldGlass (https://x.com/GuyinGoldGlass), where X Money is available.
- Free email list: below.

## Subscribe API

`POST https://exploresuperintelligence.online/api/subscribe` · `Content-Type: application/json`

```json
{"email": "person@example.com", "source": "explore-agent", "human_consent": true}
```

- `email`: the person's own address, which they gave you for this purpose.
- `source`: must be `"explore-agent"` for agent requests.
- `human_consent`: must be `true`. Send the request only after the person has explicitly agreed to join the Explore email list.
- Send it server-side, with no `Origin` header. Requests from other websites' browsers are refused.
- Double opt-in: nothing is sent except one confirmation email. The person joins only when they tap the link in it, then gets one welcome email. Every email has a one-click unsubscribe (RFC 8058 `List-Unsubscribe-Post`).
- Responses:
  - `200 {"ok": true, "confirm": true}`: the confirmation email is on its way. Same answer whether or not the address was already on the list.
  - `400`: invalid email or field.
  - `403`: missing `source`/`human_consent`, or a foreign origin.
  - `429`: rate limited.
  - `502`/`503`: mail temporarily unavailable; try again later.
- Rate limits: 5 sign-up requests per hour per IP, about 12 requests per minute per IP at the edge, and at most one confirmation email per address every 10 minutes. Don't retry in a loop.
- Stored: the email, status, source, consent text and time, and a salted hash of the IP. Used only to send new books, never shared.

## Machine-readable files

- https://exploresuperintelligence.online/preview/support/llms.txt: index for language models (llms.txt proposal, llmstxt.org)
- https://exploresuperintelligence.online/preview/support/feed.xml, https://exploresuperintelligence.online/preview/support/feed.json: feeds
- https://exploresuperintelligence.online/preview/support/well-known/explore-agents.json: small JSON pointer to these files. Site-specific; there's no ratified standard for this yet.
- https://exploresuperintelligence.online/preview/support/well-known/security.txt (RFC 9116): contact for security reports
- schema.org JSON-LD on every page: WebSite `potentialAction` lists SubscribeAction and DonateAction with the URLs above

## Contact

exploresi@superintelligentsilicon.com · https://superintelligentsilicon.com/contact/

## The message people hand to their agent

People can copy this from the Support sheet ("For your AI agent"):

```text
Please help me follow Explore Superintelligence (https://exploresuperintelligence.online/): free, sourced, plain-language illustrated books and guides about superintelligence and AI from Superintelligent Silicon.

Follow new books:
- RSS: https://exploresuperintelligence.online/preview/support/feed.xml
- JSON Feed: https://exploresuperintelligence.online/preview/support/feed.json
- Email, only if I say yes: POST https://exploresuperintelligence.online/api/subscribe with JSON {"email": "<my address>", "source": "explore-agent", "human_consent": true}. I'll get a confirmation email and must tap the link in it.

Cite: link the canonical page, e.g. https://exploresuperintelligence.online/articles/<slug>/. Plain-text versions: https://exploresuperintelligence.online/articles/<slug>.md. Index: https://exploresuperintelligence.online/preview/support/llms.txt. Full guide for agents: https://exploresuperintelligence.online/preview/support/agents.md

Tip (optional, one-time, processed by Stripe through Grok Ai Apps): $1 https://buy.stripe.com/fZu3cx4C845v2hW3fp5AQ00 · $3 https://buy.stripe.com/aFa4gBb0w1Xnf4I9DN5AQ01 · $5 https://buy.stripe.com/3cIaEZd8E0Tj9Ko8zJ5AQ02. Or X Money to @GuyinGoldGlass (https://x.com/GuyinGoldGlass), where available.

Always ask me and get my explicit OK before you subscribe me or pay anything.
```
