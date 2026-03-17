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
| `_research/*.md` | `en/research/*.html` |
| `_data/i18n/zh.yml` | `_data/i18n/en.yml` |
| `_data/*.yml` fields (`title`, `summary`, etc.) | Same files, `_en` suffixed fields (`title_en`, `summary_en`) |

## Architecture

### i18n System

No plugin — hand-rolled with data files. Templates access translations via:
```liquid
{% assign t = site.data.i18n[page.lang] %}
{{ t.nav.home }}
```

Language is set by Jekyll defaults in `_config.yml`: root pages get `lang: zh`, pages under `en/` get `lang: en`. English pages use `{% assign lp = "/en" %}` as a path prefix for internal links.

### Theme System (Dark/Light)

CSS custom properties in `assets/css/main.css`: dark theme in `:root`, light overrides in `[data-theme="light"]`. Theme state persisted in `localStorage('qcl-theme')`.

Anti-flash: inline `<script>` in `_layouts/default.html` `<head>` reads localStorage and sets `data-theme` before first paint. Toggle function in `assets/js/main.js`.

### Research Collection

Data-driven: `_data/research.yml` defines 4 research areas (id, titles, images, summaries). Detail content lives in `_research/*.md` (Jekyll Collection with `research-detail` layout). Publications in `_data/publications.yml` link to research areas via `category` field matching `category_id` in research detail front matter.

### Resource Page Encryption (Multi-User)

`/resources/` is encrypted at build time. Architecture uses key wrapping:
1. `scripts/encrypt-multi-user.js` generates a random master key
2. StaticCrypt encrypts the page HTML with the master key
3. For each user in `scripts/credentials.conf`, the master key is encrypted with their password (PBKDF2 + AES-256-CBC)
4. Encrypted key map (`sha256(username) → {iv, ciphertext}`) is injected into the HTML
5. Client-side: user enters credentials → derives key → unwraps master key → decrypts page

`credentials.conf` is gitignored. GitHub Actions reads from the `RESOURCES_CREDENTIAL` secret (multi-line, one `username:password` per line).

### Deployment

Push to `main` → GitHub Actions (`.github/workflows/deploy.yml`): Ruby setup → Jekyll build → Node.js StaticCrypt encryption → deploy to GitHub Pages.

## Data Files

- `_data/team.yml` — team members grouped by category (faculty/phd/master/undergrad/alumni)
- `_data/research.yml` — 4 research directions with bilingual titles, images, summaries
- `_data/publications.yml` — papers with category linking to research areas
- `_data/i18n/zh.yml` / `en.yml` — all UI strings

## Includes

Reusable components in `_includes/`: `nav.html` (responsive nav with dropdowns + lang/theme toggles), `hero.html`, `footer.html`, `research-card.html`, `team-card.html`, `paper-item.html`, `news-card.html`. Each receives context via Liquid `assign` or `include` variables and respects `page.lang`.
