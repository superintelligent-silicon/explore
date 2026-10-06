# Explore Superintelligence

Public site for [exploresuperintelligence.online](https://exploresuperintelligence.online).

- Design system **v2** — shared calm dark UI (Instrument Serif + Inter)
- Short alias: [exploresi.online](https://exploresi.online) → 301 here
- Lab: [superintelligentsilicon.com](https://superintelligentsilicon.com)
- Org / private ops: [superintelligent-silicon](https://github.com/superintelligent-silicon)

Deploy: static files to `/var/www/exploresuperintelligence.online/` on the SI droplet.

## Research

- `/research/` — index of guides (crawlable, CollectionPage JSON-LD)
- `/research/word-swap/` — *The Word Swap: from Artificial to Super Intelligence* (interactive, self-contained; canonical + OG/Twitter + Article JSON-LD added in `<head>`)
- `/research/word-swap.md` — plain-text summary for AI crawlers (nginx serves `*.md` as `text/markdown; charset=utf-8`)
- `/llms.txt`, `/robots.txt`, `/sitemap.xml` — discovery files; add new pages to sitemap + llms.txt + research index when publishing
