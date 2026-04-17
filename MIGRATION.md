# Migration Progress: Wowchemy 5.x → Hugo Blox v0.12

**Project:** remi-theriault.com  
**Old site:** `starter-academic` (Wowchemy ~5.1, Hugo 0.80, Bootstrap/SCSS)  
**New site:** `prime-fox` (Hugo Blox v0.12.0, Hugo 0.160.1, Tailwind v4)  
**Date started:** 2026-04-16  
**Last updated:** 2026-04-17 (rev 2)  

---

## Overall Progress: ~97%

| Area | Status | % |
|------|--------|---|
| Site configuration & identity | ✅ Complete | 100% |
| Menus & navigation | ✅ Complete | 100% |
| Language configuration | ✅ Complete | 100% |
| Static assets | ✅ Complete | 100% |
| Publications (EN) | ✅ Complete | 100% |
| Publications (FR) | ✅ Complete | 100% |
| Content sections (EN) | ✅ Complete | 100% |
| Content sections (FR) | ✅ Complete | 100% |
| Special pages (EN) | ✅ Complete | 100% |
| Special pages (FR) | ✅ Complete | 100% |
| Custom layouts & hooks | ✅ Complete | 100% |
| Avatar & profile | ✅ Complete | 100% |
| Netlify config & headers | ✅ Complete | 100% |
| Deprecation warnings | ✅ Complete | 100% |
| Visual QA fixes | ✅ Complete | 100% |
| Final testing & polish | ⏳ In progress | 70% |

---

## Detailed Breakdown

### 1. Site Configuration & Identity — ✅ 100%

| Item | File | Status |
|------|------|--------|
| Site title, baseURL, language | `config/_default/hugo.yaml` | ✅ |
| Theme, header, analytics, SEO | `config/_default/params.yaml` | ✅ |
| Author profile (name, role, affiliations, links, interests, education, skills) | `data/authors/me.yaml` | ✅ |
| Module pinning (Blox v0.12.0) | `go.mod` | ✅ |
| Node/pnpm setup | `package.json`, `pnpm-lock.yaml` | ✅ |

### 2. Menus & Navigation — ✅ 100%

| Item | File | Status |
|------|------|--------|
| EN menu (9 items: Bio, Publications, News, Blog, Media, Tutorials, CV, Contact, Donate) | `config/_default/menus.yaml` | ✅ |
| FR menu (9 items, translated labels and slugs) | `config/_default/menus.fr.yaml` | ✅ |

### 3. Language Configuration — ✅ 100%

| Item | File | Status |
|------|------|--------|
| EN (en-us) + FR (fr) with contentDir | `config/_default/languages.yaml` | ✅ |

### 4. Static Assets — ✅ 100%

| Item | Status |
|------|--------|
| CV PDFs (cv.pdf, cv_one-page.pdf, cv-academic.pdf, etc.) | ✅ |
| Paper PDFs (24 papers in /papers/) | ✅ |
| Poster PDFs (6 posters in /posters/) | ✅ |
| Preprint PDFs (2 in /preprints/) | ✅ |
| Slide decks (6 HTML presentations in /slides/) | ✅ |
| R scripts (17 scripts in /scripts/) | ✅ |
| Dashboard HTML files (/dashboards/) | ✅ |
| Award images (/awards/) | ✅ |
| Other static images (/images/) | ✅ |
| mastodon.txt, sitemap.txt | ✅ |
| Site icon (assets/media/icon.png) | ✅ |
| Hero image (assets/media/hero-academic.jpg) | ✅ |
| Custom Bluesky SVG icon | ✅ |
| Author avatar (assets/media/authors/me.jpg) | ✅ |

### 5. Publications — ✅ 100%

| Item | Status | Notes |
|------|--------|-------|
| EN: 21 publications (2017–2026) | ✅ | Converted via Python script |
| FR: 21 publications (2017–2026) | ✅ | Converted via Python script |
| Format conversion (old → new) | ✅ | `publication_types: ["2"]` → `hugoblox.ids.doi`, `type: article-journal` |
| Named links (PDF, Code, Dataset, etc.) | ✅ | Preserved per publication |
| Altmetric/Dimensions badges (`add_badge: true`) | ✅ | Via custom citation view |
| Section _index.md (view: citation) | ✅ | Both EN and FR |

### 6. Content Sections — ✅ 100%

#### EN Content

| Section | Items | View | Status |
|---------|-------|------|--------|
| Blog | 14 posts | article-grid, 2 cols | ✅ |
| News | 8 items | article-grid, 2 cols | ✅ |
| Media | 28 items | article-grid, 1 col | ✅ |
| Tutorials | 17 items | article-grid, 1 col | ✅ |

#### FR Content

| Section | Items | View | Status |
|---------|-------|------|--------|
| Blog | 14 posts | article-grid, 2 cols | ✅ |
| Nouvelles (news) | 8 items | article-grid, 2 cols | ✅ |
| Média (media) | 28 items | article-grid, 1 col | ✅ |
| Tutoriels (tutorials) | 17 items | article-grid, 1 col | ✅ |

#### Content fixes applied (both EN and FR)

| Fix | Description |
|-----|-------------|
| Happiness_Legacy featured image | Renamed .png → .webp (was actually WebP format) |
| Happiness_Legacy external_link | Single-quoted URL with percent-encoded characters |
| FJL date | Fixed invalid month `2013-00-*` → `2013-01-*` |
| forcesavenir date | Fixed invalid day `2012-01-00` → `2012-01-01` |
| FR publication deprecation cleanup | Removed all deprecated fields (`doi`, `url_code`, `url_dataset`, `url_pdf`, `url_project`, `url_video`, `slides`, `external_link`) from 21 FR publications via script |
| FR `publication_types` | Updated from `["2"]` to `["article-journal"]` in all 21 FR publications |

### 6a. Visual QA Fixes (rev 2) — ✅ 100%

| Issue | Fix Applied |
|-------|-------------|
| Meyer.jpg not showing on contact page | Moved image to separate `markdown` block above `contact-info` (EN+FR) |
| Donate page bullets not rendering | Converted markdown bullet list to HTML `<ul><li>` in `cta-card` text (EN+FR) |
| CV link not opening new tab | Already handled by theme — `resume-biography-3` auto-adds `target="_blank"` for `.pdf` URLs |
| Sections not using grid layout | Changed `view: card` → `view: article-grid` in news, blog, media, tutorials (EN+FR) |
| Homepage showing unwanted sections | Removed `collection` blocks (recent publications, recent news) from homepage, kept only hero markdown (EN+FR) |
| Copyright showing UQAM | Changed copyright notice from `{name}` variable to hardcoded "Rémi Thériault" |
| Skills section missing | Fixed skills format in `data/authors/me.yaml` — restructured from flat list to grouped format with `items` array as required by `resume-skills` block |
| 80+ deprecation warnings | Cleaned all 21 FR publications via `scripts/clean-fr-publications.py` — zero warnings now |
| forcesavenir date | Fixed invalid month `2012-00-*` → `2012-01-*` |
| Wowchemy field cleanup | Removed `url_code`, `url_pdf`, `url_slides`, `url_video`, `slides`, `summary`, `image`, `links` template cruft |

### 7. Special Pages — ✅ 100%

#### EN

| Page | Blocks | Status |
|------|--------|--------|
| Homepage (`_index.md`) | hero (markdown only) | ✅ |
| Bio (`bio/index.md`) | resume-biography-3 (CV opens new tab for .pdf), markdown bio, resume-skills | ✅ |
| Contact (`contact/index.md`) | markdown (Meyer.jpg image), contact-info, markdown land acknowledgment | ✅ |
| Donate (`donate/index.md`) | cta-card with HTML bullet list + PayPal link | ✅ |

#### FR

| Page | Blocks | Status |
|------|--------|--------|
| Accueil (`_index.md`) | hero FR (markdown only) | ✅ |
| Bio (`bio/index.md`) | resume-biography-3, FR bio text, compétences | ✅ |
| Contact (`contact/index.md`) | markdown (Meyer.jpg), contact-info, reconnaissance territoriale FR | ✅ |
| Donnez (`donate/index.md`) | cta-card FR with HTML bullets + PayPal link | ✅ |

### 8. Custom Layouts & Hooks — ✅ 100%

| Layout | File | Status | Notes |
|--------|------|--------|-------|
| Google Tag Manager | `layouts/_partials/hooks/head-end/gtm.html` | ✅ | GTM-NVWSFMHJ |
| Badge scripts (Altmetric + Dimensions) | `layouts/_partials/hooks/body-end/badges.html` | ✅ | Altmetric embed.js + Dimensions badge.js |
| Citation view with badges | `layouts/_partials/views/citation.html` | ✅ | Float-right badges, gated on `add_badge: true` |
| Custom footer (bilingual) | `layouts/_partials/hooks/footer-start/custom-footer.html` | ✅ | EN/FR credits, GitHub, Netlify, donate |
| External link redirect | `layouts/single.html` | ✅ | Meta-refresh for `external_link` front matter |

### 9. Netlify Configuration — ✅ 100%

| Item | Status | Notes |
|------|--------|-------|
| Build command (Hugo + pnpm + Pagefind) | ✅ | With verbose logging |
| Hugo version (0.160.1) | ✅ | |
| Deploy preview / branch deploy commands | ✅ | |
| HSTS header | ✅ | `max-age=63072000; includeSubDomains; preload` |
| Content-Security-Policy | ✅ | Full CSP for GTM, Altmetric, Dimensions, Maps, fonts |
| noindex headers (taxonomy, author, RSS) | ✅ | Both EN and FR paths |
| Redirects: /papers → /publications/ | ✅ | |
| Redirects: /cv → /cv.pdf | ✅ | |
| Redirects: /rempsyc → rempsyc docs | ✅ | |
| Redirects: blog_*.html → rempsyc articles | ✅ | 9 redirects, with and without .html |
| Redirects: poster PDFs | ✅ | 2 redirects |
| Redirects: paper PDFs | ✅ | 10+ redirects |
| Redirects: publication slug changes | ✅ | lavaanExtra, rempsyc, PF, busara dashboard |
| Redirects: preprint PDFs | ✅ | 3 redirects |
| Redirects: /publication/* → /publications/* | ✅ | New in Blox v0.12 (singular → plural) |
| Hugo cache plugin | ✅ | `netlify-plugin-hugo-cache-resources` |

---

## Architecture Changes (Incompatibilities)

These are structural differences between Wowchemy 5.x and Hugo Blox v0.12 that required migration decisions:

| Old (Wowchemy 5.x) | New (Blox v0.12) | Impact |
|---------------------|-------------------|--------|
| Widget-based pages (`.md` files per widget) | Block-based landing pages (YAML sections array) | All pages redesigned. Widget files → single `index.md` with `sections:` |
| Project portfolio architecture (`project-blog/`, `project-news/`) | Regular content sections (`blog/`, `news/`) | Content reorganized. No more widget→project mapping |
| TOML config files | YAML config files | All config converted |
| Bootstrap + custom SCSS | Tailwind v4 (JIT) | Custom CSS dropped; `custom.scss` not migrated (not needed) |
| `publication_types: ["2"]` | `type: article-journal` + `hugoblox.ids.doi` | All publications reformatted |
| Avatar in `content/authors/*/avatar.*` | Avatar in `assets/media/authors/<slug>.*` | Flat file, not subdirectory |
| `icon_pack: ai/fas/fab` + icon name | Various: `academicons/*`, `hero/*`, `devicon/*`, `brands/*` | Icon references updated |
| Custom partials (site_footer, custom_head, etc.) | Hook system (head-start, head-end, body-end, footer-start, etc.) | All custom code moved to hooks |
| Google Analytics in config | GTM via hook | Analytics handled via head-end hook |
| Built-in contact widget | `contact-info` block | Different config structure |
| CMS (Netlify CMS / admin) | Not migrated | Optional; can be added later |

---

## Known Issues / Items Not Migrated

| Item | Status | Notes |
|------|--------|-------|
| Netlify CMS (admin panel) | ❌ Not migrated | Was in `static/admin/`. Optional feature, can be added later |
| FR author profile translation | ⚠️ Partial | `data/authors/me.yaml` is shared across languages. FR bio text is in the FR bio page. FR role/interests/education not separately translated in author data. |
| `privacy.md` / `terms.md` | ❌ Not migrated | Were `draft: true` placeholder pages in old site |
| Wowchemy `talk/` section (FR) | ❌ Not migrated | Existed in old FR content; appears unused or empty |
| Custom SCSS (`custom.scss`) | ❌ Not needed | Old SCSS targeted Bootstrap classes; Tailwind handles styling |
| Google Maps embed | ❌ Not migrated | Old contact widget had maps config; not reproduced |
| Tag/category filter buttons on section pages | ⚠️ Not available | Old project portfolio had filter buttons (Tous, Psychologie, etc.); Blox v0.12 card view does not support client-side filtering |
| Pagefind search | ✅ Configured | Build command includes `pnpm run pagefind` |

---

## Build Statistics

| Metric | EN | FR |
|--------|----|----|
| Pages | 144 | ~110+ (estimated with new content) |
| Static files | 305 | 305 |
| Publications | 21 | 21 |
| Blog posts | 14 | 14 |
| News items | 8 | 8 |
| Media items | 28 | 28 |
| Tutorials | 17 | 17 |
| Special pages | 4 (home, bio, contact, donate) | 4 |

---

## Remaining Tasks

| Task | Priority | Est. Effort |
|------|----------|-------------|
| Final Hugo build verification (FR page count) | High | Quick |
| Visual QA in browser (all pages, both languages) | High | Medium |
| Test all Netlify redirects post-deploy | Medium | Medium |
| CSP testing with browser dev tools | Medium | Quick |
| Pagefind search testing | Medium | Quick |
| Optional: Add Netlify CMS back | Low | Medium |
| Optional: FR-specific author data (role, interests labels) | Low | Quick |
| Optional: Tag filter functionality replacement | Low | Research needed |
| Push to GitHub and deploy | High | Quick |
