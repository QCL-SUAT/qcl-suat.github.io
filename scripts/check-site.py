#!/usr/bin/env python3
"""Site-wide gate for the QCL-SUAT Jekyll site.

Runs after every content/structure change, before push. Read-only: never
writes, never builds. Exits 0 when clean, 1 with an issue list otherwise.

What it checks (over the repo root = parent of this script's directory):
  1. Dead internal links/images in the built _site/ (href/src targets exist).
  2. i18n key parity: _data/i18n/zh.yml vs en.yml (recursive), plus every
     `t.*` reference in layouts/includes/pages resolves in BOTH files.
  3. Page symmetry: root pages <-> en/ mirrors (404/resources are zh-only
     by design); research details _research/*.md <-> en/research/*.md.
  4. News integrity: each _posts/*.md has permalink_en/body_en and an
     en/news/<slug>.md mirror whose permalink_zh points back to a real post.
  5. Data parity: team.yml/research.yml zh fields have _en counterparts
     (language-neutral keys excluded); publications categories exist in
     research.yml ids.
  6. Referenced media exists on disk (team photos; research images are
     extensionless bases checked against .webp/.jpg).
  7. Unused media: every file under assets/img/ is referenced by some
     source file (catches dead weight like unreferenced webp variants).
  8. Raw markdown in .html sources (Jekyll only renders markdown in .md).
  9. Curly quotes / corner brackets in sources (house punctuation rule).

Usage:
    bundle exec jekyll build          # _site must exist for check 1
    python3 scripts/check-site.py     # from anywhere; paths are script-relative
"""

import glob
import os
import re
import sys

import yaml  # PyYAML; part of the Jekyll toolchain environment

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "_site")
EXCLUDE_DIRS = {"_site", "vendor", "node_modules", ".git", ".bundle"}

issues = []

# ---------------------------------------------------------------- 1. dead links
if not os.path.isdir(SITE):
    print("FATAL: _site/ not found - run `bundle exec jekyll build` first")
    sys.exit(1)

pat = re.compile(r'(?:href|src)=["\']([^"\']+)["\']')
skip_pat = re.compile(r"^(https?:|mailto:|data:|javascript:|#|tel:)")
checked = dead = 0
for root, dirs, files in os.walk(SITE):
    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
    for f in files:
        if not f.endswith(".html"):
            continue
        p = os.path.join(root, f)
        with open(p, encoding="utf-8") as fh:
            html = fh.read()
        for url in pat.findall(html):
            if skip_pat.match(url) or url.startswith("//"):
                continue
            u = url.split("#")[0].split("?")[0]
            if not u:
                continue
            target = os.path.join(SITE, u.lstrip("/"))
            ok = os.path.isfile(os.path.join(target, "index.html")) if u.endswith("/") else os.path.isfile(target)
            checked += 1
            if not ok:
                dead += 1
                issues.append(f"DEAD LINK: {os.path.relpath(p, SITE)} -> {url}")
print(f"[1] dead-link scan: {checked} refs, {dead} dead")

# ---------------------------------------------------------------- 2. i18n
def load_i18n():
    zh = yaml.safe_load(open(os.path.join(ROOT, "_data/i18n/zh.yml"), encoding="utf-8"))
    en = yaml.safe_load(open(os.path.join(ROOT, "_data/i18n/en.yml"), encoding="utf-8"))
    return zh, en

def flat_keys(d, prefix=""):
    out = set()
    if isinstance(d, dict):
        for k, v in d.items():
            out.add(prefix + k)
            out |= flat_keys(v, prefix + k + ".")
    return out

zh, en = load_i18n()
kz, ke = flat_keys(zh), flat_keys(en)
for k in sorted(kz - ke):
    issues.append(f"i18n zh-only key: {k}")
for k in sorted(ke - kz):
    issues.append(f"i18n en-only key: {k}")

tref = re.compile(r"\bt\.([a-zA-Z_][\w]*(?:\.[\w]+)*)")
refs = set()
src_html = (
    glob.glob(os.path.join(ROOT, "*.html"))
    + glob.glob(os.path.join(ROOT, "en", "*.html"))
    + glob.glob(os.path.join(ROOT, "_includes", "*.html"))
    + glob.glob(os.path.join(ROOT, "_layouts", "*.html"))
)
for p in src_html:
    for m in tref.findall(open(p, encoding="utf-8").read()):
        refs.add(m)
for r in sorted(refs):
    for d, name in ((zh, "zh"), (en, "en")):
        cur, ok = d, True
        for part in r.split("."):
            if isinstance(cur, dict) and part in cur:
                cur = cur[part]
            else:
                ok = False
                break
        if not ok:
            issues.append(f"i18n missing {name} key for template ref t.{r}")
print(f"[2] i18n: zh={len(kz)} en={len(ke)} keys, diff={len(kz ^ ke)}, {len(refs)} template refs checked")

# ---------------------------------------------------------------- 3. symmetry
ZH_ONLY = {"404.html", "resources.html"}
root_pages = {os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "*.html"))} - ZH_ONLY
en_pages = {os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "en", "*.html"))}
for p in sorted(root_pages - en_pages):
    issues.append(f"page without en/ mirror: {p}")
for p in sorted(en_pages - root_pages):
    issues.append(f"en/ page without root mirror: {p}")

zh_r = {os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(ROOT, "_research", "*.md"))}
en_r = {os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(ROOT, "en", "research", "*.md"))}
for s in sorted(zh_r - en_r):
    issues.append(f"research detail without en: {s}")
for s in sorted(en_r - zh_r):
    issues.append(f"en research detail without zh: {s}")
print(f"[3] symmetry: pages {len(root_pages)}/{len(en_pages)}, research details {len(zh_r)}/{len(en_r)}")

# ---------------------------------------------------------------- 4. news
posts = glob.glob(os.path.join(ROOT, "_posts", "*.md"))
for p in posts:
    fm = next(yaml.safe_load_all(open(p, encoding="utf-8")))
    slug = re.search(r"\d{4}-\d{2}-\d{2}-(.+)\.md$", p).group(1)
    pe = fm.get("permalink_en")
    if not pe:
        issues.append(f"post missing permalink_en: {os.path.basename(p)}")
        continue
    exp_slug = pe.rstrip("/").split("/")[-1].removesuffix(".html")
    if exp_slug != slug:
        issues.append(f"post permalink_en slug mismatch: {os.path.basename(p)} -> {pe} (expected {slug})")
    if not os.path.isfile(os.path.join(ROOT, "en", "news", exp_slug + ".md")):
        issues.append(f"post missing en/news mirror: {exp_slug}.md")
    if not str(fm.get("body_en", "")).strip():
        issues.append(f"post missing body_en: {os.path.basename(p)}")

for p in glob.glob(os.path.join(ROOT, "en", "news", "*.md")):
    fm = next(yaml.safe_load_all(open(p, encoding="utf-8")))
    pz = fm.get("permalink_zh")
    if not pz:
        issues.append(f"en/news missing permalink_zh: {os.path.basename(p)}")
        continue
    m = re.search(r"/(\d{4})/(\d{2})/(\d{2})/([^/]+?)\.html$", pz)
    if not m:
        issues.append(f"en/news permalink_zh odd format: {os.path.basename(p)} -> {pz}")
        continue
    y, mo, d, slug = m.groups()
    if not os.path.isfile(os.path.join(ROOT, "_posts", f"{y}-{mo}-{d}-{slug}.md")):
        issues.append(f"en/news permalink_zh target missing: {os.path.basename(p)} -> {pz}")
print(f"[4] news: {len(posts)} posts + mirrors checked")

# ---------------------------------------------------------------- 5. data parity
NEUTRAL = {"email", "scholar_url", "photo", "year", "category", "id", "image",
           "date", "arxiv", "doi", "pdf", "icon", "image_en"}
for name in ("team", "research"):
    data = yaml.safe_load(open(os.path.join(ROOT, "_data", f"{name}.yml"), encoding="utf-8"))
    for i, item in enumerate(data):
        label = item.get("name", item.get("title", i))
        for k in item:
            if k.endswith("_en") or k in NEUTRAL:
                continue
            if f"{k}_en" not in item:
                issues.append(f"{name}.yml [{label}]: field '{k}' lacks _en counterpart")

research_ids = {r["id"] for r in yaml.safe_load(open(os.path.join(ROOT, "_data", "research.yml"), encoding="utf-8"))}
for i, pub in enumerate(yaml.safe_load(open(os.path.join(ROOT, "_data", "publications.yml"), encoding="utf-8"))):
    if pub.get("category") not in research_ids:
        issues.append(f"publications[{i}] category '{pub.get('category')}' not in research ids")
print("[5] data parity + category refs checked")

# ---------------------------------------------------------------- 6. media exists
for item in yaml.safe_load(open(os.path.join(ROOT, "_data", "team.yml"), encoding="utf-8")):
    ph = item.get("photo", "")
    if ph and not os.path.isfile(ROOT + ph):
        issues.append(f"team photo missing on disk: {ph} ({item.get('name')})")
for item in yaml.safe_load(open(os.path.join(ROOT, "_data", "research.yml"), encoding="utf-8")):
    for k in ("image",):
        v = item.get(k)
        if v and not (os.path.isfile(ROOT + v + ".webp") or os.path.isfile(ROOT + v + ".jpg")):
            issues.append(f"research image missing on disk: {v}")
print("[6] referenced media checked")

# ---------------------------------------------------------------- 7. unused media
# A file counts as referenced if its basename appears verbatim in some source,
# OR its extensionless basename does (templates assemble base + '.webp'/'.jpg'
# via Liquid append, e.g. research-card.html picture sources).
src_all = ""
for root, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
    for f in files:
        if f.endswith((".html", ".css", ".js", ".yml", ".md")):
            src_all += open(os.path.join(root, f), encoding="utf-8", errors="ignore").read()
unused = 0
for p in glob.glob(os.path.join(ROOT, "assets", "img", "**", "*"), recursive=True):
    if not os.path.isfile(p) or os.path.basename(p) == ".gitkeep":
        continue
    base = os.path.basename(p)
    stem = os.path.splitext(base)[0]
    if base not in src_all and stem not in src_all:
        unused += 1
        issues.append(f"unused media (not referenced by any source): {os.path.relpath(p, ROOT)}")
print(f"[7] unused media: {unused}")

# ---------------------------------------------------------------- 8. raw markdown in .html
md_pat = re.compile(r"\*\*[^*]+\*\*|^#{1,4} |^[-*] \[", re.M)
for p in glob.glob(os.path.join(ROOT, "*.html")) + glob.glob(os.path.join(ROOT, "en", "*.html")):
    if md_pat.search(open(p, encoding="utf-8").read()):
        issues.append(f"raw markdown in .html source: {os.path.relpath(p, ROOT)}")
print("[8] markdown-in-html scan done")

# ---------------------------------------------------------------- 9. punctuation
quote_pat = re.compile("[“”‘’「」『』]")
for p in (glob.glob(os.path.join(ROOT, "*.html")) + glob.glob(os.path.join(ROOT, "*.md"))
          + glob.glob(os.path.join(ROOT, "en", "*.html"))
          + glob.glob(os.path.join(ROOT, "en", "**", "*.md"), recursive=True)
          + glob.glob(os.path.join(ROOT, "_posts", "*.md"))
          + glob.glob(os.path.join(ROOT, "_research", "*.md"))
          + glob.glob(os.path.join(ROOT, "_data", "*.yml")) + glob.glob(os.path.join(ROOT, "_data", "i18n", "*.yml"))):
    if quote_pat.search(open(p, encoding="utf-8").read()):
        issues.append(f"curly quotes / corner brackets present: {os.path.relpath(p, ROOT)}")
print("[9] punctuation scan done")

print("=" * 50)
if issues:
    print(f"{len(issues)} ISSUE(S):")
    for i in issues:
        print(" -", i)
    sys.exit(1)
print("ALL CLEAN")
