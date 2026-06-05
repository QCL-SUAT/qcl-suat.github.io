# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

QCL（超导量子计算实验室）academic website for SUAT (深圳理工大学). Jekyll static site deployed on GitHub Pages. Bilingual Chinese/English with dark/light theme switching and StaticCrypt-encrypted resources page.

**Live site**: https://qcl-suat.github.io

## Commands

```bash
# Ruby must be on PATH (macOS Homebrew)
export PATH="/opt/homebrew/opt/ruby/bin:$PATH"

# Dev server (auto-rebuild on changes)
bundle exec jekyll serve          # http://localhost:4000

# Build only
bundle exec jekyll build          # outputs to _site/

# Build + encrypt resources page (for testing encryption locally)
bundle exec jekyll build && ./scripts/encrypt-resources.sh
python3 -m http.server 4000 --directory _site   # static preview

# Update credentials and trigger deploy
./scripts/update-credentials.sh
```

Dependencies install to `vendor/bundle/` (project-local via bundler config).

## Critical Rule: Chinese/English Sync

**Every content change to a Chinese page MUST include the corresponding English update.** File pairs:

| Chinese | English |
|---------|---------|
| `index.html`, `research.html`, etc. | `en/index.html`, `en/research.html`, etc. |
| `_research/*.md` | `en/research/*.html` (standalone, not collection items) |
| `_data/i18n/zh.yml` | `_data/i18n/en.yml` |
| `_data/*.yml` fields (`title`, `summary`, etc.) | Same files, `_en` suffixed fields (`title_en`, `summary_en`) |
| `_posts/*.md` body + `body_en` front matter | Same file |

## Architecture

### Tech Stack

- Jekyll 4.3, no SASS/webpack — plain CSS + vanilla JS
- Plugins: `jekyll-seo-tag`, `jekyll-sitemap` only
- Node.js: `staticcrypt` ^3.3.3 (resource page encryption)
- CI: Ruby 3.2, Node 20

### Page Routing

| URL (zh) | URL (en) | Source |
|----------|----------|--------|
| `/` | `/en/` | `index.html` / `en/index.html` |
| `/research/` | `/en/research/` | `research.html` / `en/research.html` |
| `/research/<slug>/` | `/en/research/<slug>/` | `_research/<slug>.md` / `en/research/<slug>.html` |
| `/team/` | `/en/team/` | `team.html` / `en/team.html` |
| `/news/` | `/en/news/` | `news.html` / `en/news.html` |
| `/join/` | `/en/join/` | `join.html` / `en/join.html` |
| `/resources/` | (Chinese only, encrypted) | `resources.html` |

### Layouts (`_layouts/`)

| Layout | Wraps | Used by |
|--------|-------|---------|
| `default` | root — HTML shell, head (anti-flash theme script, SEO), nav, footer, JS | all pages |
| `page` | `default` + optional page_title/subtitle | currently unused |
| `post` | `default` + title/date/tag/back-link/body_en fallback | `_posts/*.md` |
| `research-detail` | `default` + icon/title/image/desc + auto-fetched related papers | `_research/*.md`, `en/research/*.html` |

### i18n System

Hand-rolled, no plugin. `page.lang` set via `_config.yml` defaults (`zh` for root, `en` for `en/`).

```liquid
{% assign t = site.data.i18n[page.lang] %}
{{ t.nav.home }}
```

English pages set `{% assign lp = "/en" %}` as URL prefix. Blog posts use `body_en` front matter field with Markdown fallback inside `post` layout.

### Theme System (Dark/Light)

- Dark (default) in `:root`, light overrides in `[data-theme="light"]` — all in `assets/css/main.css`
- Anti-flash: inline `<script>` in `default.html` `<head>` reads `localStorage('qcl-theme')` synchronously
- Toggle: `toggleTheme()` in `assets/js/main.js`

### Data Files (`_data/`)

| File | Purpose |
|------|---------|
| `team.yml` | Members by category (faculty/phd/master/undergrad/alumni), bilingual fields |
| `research.yml` | 4 research directions with id, titles, images, summaries |
| `publications.yml` | Papers with `category` linking to research direction ids |
| `i18n/zh.yml`, `i18n/en.yml` | All UI strings (nav, hero, section labels, footer, join page, resources login) |

### Includes (`_includes/`)

All respect `page.lang`. Context passed via Liquid `assign` or `include` variables:

| Include | Variables | Used on |
|---------|-----------|---------|
| `nav.html` | `page.lang`, `page.url` | every page |
| `hero.html` | `page.lang` | homepage only |
| `footer.html` | `page.lang` | every page |
| `research-card.html` | `page.lang`, `item` | research listing |
| `team-card.html` | `page.lang`, `member` | team page |
| `paper-item.html` | `paper` | research detail |
| `news-card.html` | `page.lang`, `post` | news listing + homepage |

### Resource Page Encryption (Multi-User)

`/resources/` encrypted at build time via key wrapping:

1. `scripts/encrypt-multi-user.js` generates random master key
2. StaticCrypt encrypts page HTML with master key
3. For each user in `scripts/credentials.conf`, master key is wrapped with their password (PBKDF2 + AES-256-CBC)
4. Encrypted key map injected into HTML
5. Client-side: username + password → SHA-256 lookup → PBKDF2 derive → unwrap master key → decrypt page

`credentials.conf` is gitignored. CI reads from `RESOURCES_CREDENTIAL` secret.

### Deployment

Push to `main` → GitHub Actions (`.github/workflows/deploy.yml`): Ruby 3.2 setup → `bundle exec jekyll build` → Node.js StaticCrypt encryption → GitHub Pages deploy.

## Known Asymmetries

- **Research detail pages**: Chinese versions are Jekyll collection items (`_research/*.md`), English versions are standalone HTML files (`en/research/*.html`). Adding a new research direction requires creating files in both systems.
- **Resources page**: Chinese-only, no English counterpart.
- **Blog posts**: Bilingual via `body_en` front matter in same file (not separate files).
- **`hero.affiliation`**: Rendered in hero section, shows center + school affiliation chain.
