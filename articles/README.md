# Adding an article to Explore

Articles live at `/articles/{slug}/`. The directory is `/articles/` (`index.html`); the shared stylesheet is `/articles/articles.css`.

## Steps

1. **Copy the template:** `cp -r articles/_template articles/{slug}` (lowercase, hyphenated slug). Move `article.md` to `articles/{slug}.md` and delete `llms-entry.txt` from the copy.
2. **Fill every `{{…}}`** in `index.html`: title, description, dates (ISO), author, dek, body, sources, disclosure. Search for `{{` before shipping; there must be none left.
3. **Turn on indexing:** change `<meta name="robots" content="noindex, nofollow">` to `index, follow, max-image-preview:large, max-snippet:-1`.
4. **OG image:** add `articles/{slug}/og.png` (1200×630, dark/gold, legible title). It's also the hero cover.
5. **Markdown companion:** fill `articles/{slug}.md` (summary, key points, sources).
6. **Directory:** in `articles/index.html` add a `<li>` tile to the grid (newest first), optionally make it the featured card, and add a `ListItem` to the CollectionPage JSON-LD.
7. **Discovery files:**
   - `sitemap.xml`: add `<url><loc>https://exploresuperintelligence.online/articles/{slug}/</loc><lastmod>YYYY-MM-DD</lastmod><changefreq>monthly</changefreq><priority>0.7</priority><image:image><image:loc>…/articles/{slug}/og.png</image:loc></image:image></url>`, and bump the `/articles/` lastmod.
   - `llms.txt`: paste the line from `_template/llms-entry.txt` under `## Articles`.
8. **Deploy:** commit to `main`, back up the web root on the droplet, rsync to `/var/www/exploresuperintelligence.online/`, and check `https://…/articles/{slug}/` returns 200 at 390px and 1440px with no console errors.
9. **IndexNow ping** (Bing, Yandex, etc. — Google ignores it, use Search Console "Request indexing"):
   ```sh
   curl -s -H 'Content-Type: application/json' https://api.indexnow.org/indexnow -d '{
     "host":"exploresuperintelligence.online",
     "key":"fab4248d-492c-4a4a-8fc4-7dcd6a019ebb",
     "keyLocation":"https://exploresuperintelligence.online/fab4248d-492c-4a4a-8fc4-7dcd6a019ebb.txt",
     "urlList":["https://exploresuperintelligence.online/articles/{slug}/","https://exploresuperintelligence.online/articles/","https://exploresuperintelligence.online/sitemap.xml"]}'
   ```
   200 or 202 = accepted.

## Cross-posting to World's Best Magazine (worldsbestmagazine.com)

Pick **one** original and point every copy's canonical at it — never two pages that each claim to be canonical.

- **Explore is original (default):** keep the canonical on Explore pointing at itself. Ask WBM to publish with `<link rel="canonical" href="https://exploresuperintelligence.online/articles/{slug}/">` and an "Originally published on Explore Superintelligence" line linking back. Publish on Explore first, then WBM a day or more later.
- **WBM is original:** set Explore's canonical to the WBM URL, keep `og:url` the same, add an "Originally published in World's Best Magazine" line, and leave the article out of `sitemap.xml` (only canonical URLs belong there). The tile on `/articles/` can still link to it.
- Keep the JSON-LD `mainEntityOfPage` and `url` on the canonical URL. Don't syndicate a summary as if it were the full piece.

## Template rules

- `/articles/_template/` is **noindexed and not in the sitemap**. Never link to it from public pages.
- Tip block: same three Stripe links as The Word Swap (`?thanks=1` return shows the thank-you line).
- Reading time is computed from the article text on load; the hard-coded value is the no-JS fallback.
