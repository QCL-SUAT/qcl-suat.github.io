#!/usr/bin/env python3
"""QCL 站点全站体检。只读：本脚本从不修改任何文件。

用法（在仓库任意位置执行均可）：
    python scripts/check_site.py             # 源码树检查，不需要先构建
    python scripts/check_site.py --built     # 追加构建产物检查，需先 bundle exec jekyll build

检查项：
  1  死链          —— _site 内全部 href/src 逐个落到真实文件
  2  中英对称      —— 根页面必须在 en/ 下有对应页
  3  语言切换落点  —— 按 _includes/nav.html 的分支顺序复算每页的切换目标，验证目标存在
  4  i18n 键       —— zh/en 键集合完全一致；模板用到的键都在键集合里
  5  资源存在性    —— /assets 引用、<picture> 的 webp/jpg 配对
  6  文本卫生      —— 弯引号、控制字符、CR、行尾空格（全局规则要求一律 LF + 无弯引号）
  7  可访问性      —— img 有 alt、每页恰好一个 h1、标题层级不跳级
  8  数据文件      —— team/publications/research/funding 的必填字段与占位符残留
  9  体积          —— 列出最重的静态资源，供优化决策

退出码：0 全通过；1 有发现。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "_site"
HERE = ROOT

findings: list[str] = []
INFO: list[str] = []


def add(msg: str) -> None:
    findings.append(msg)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def front_matter(text: str) -> dict[str, str]:
    """极简 front matter 解析：只取顶层 key: value，够本站用。"""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    out: dict[str, str] = {}
    for line in text[3:end].splitlines():
        m = re.match(r'^([A-Za-z_][A-Za-z_0-9]*):\s*(.*)$', line)
        if m:
            out[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return out


# ---------------------------------------------------------------- 1 死链
def check_dead_links() -> None:
    if not SITE.is_dir():
        INFO.append("死链/切换/可访问性：未找到 _site，跳过构建产物检查（先跑 bundle exec jekyll build）")
        return
    pat = re.compile(r'(?:href|src)="([^"]+)"')
    dead, checked, anchors = [], 0, 0
    anchors_by_page: dict[Path, str] = {}
    bad_anchor: dict[str, set[str]] = {}   # "目标#锚点" -> 引用它的页面集合（同一处只报一次）
    for page in SITE.rglob("*.html"):
        for raw in pat.findall(read(page)):
            if raw.startswith(("http://", "https://", "mailto:", "data:", "javascript:")):
                continue
            frag = raw.split("#", 1)[1] if "#" in raw else ""
            url = raw.split("#")[0].split("?")[0]
            if not url and not frag:
                continue
            if url.startswith("/"):
                target = SITE / url.lstrip("/")
            elif url:
                target = page.parent / url
            else:
                target = page  # 纯锚点，指向本页
            if url.endswith("/") or target.is_dir():
                target = target / "index.html"
            checked += 1
            if not target.exists():
                dead.append(f"死链：{rel(page)} -> {url}")
                continue
            if frag and target.suffix == ".html":
                anchors += 1
                if target not in anchors_by_page:
                    anchors_by_page[target] = read(target)
                if f'id="{frag}"' not in anchors_by_page[target] and \
                   f'name="{frag}"' not in anchors_by_page[target]:
                    key = f"{rel(target).replace('index.html', '')}#{frag}"
                    bad_anchor.setdefault(key, set()).add(rel(page))
    INFO.append(f"死链：检查 {checked} 条，{len(dead)} 条失效；"
                f"页内锚点 {anchors} 个，{len(bad_anchor)} 个落空")
    findings.extend(dead)
    for key, pages in sorted(bad_anchor.items()):
        sample = sorted(pages)[0]
        extra = f"（另 {len(pages) - 1} 页同）" if len(pages) > 1 else ""
        findings.append(f"锚点落空：{key}，例如 {sample}{extra}")


# ------------------------------------------------- 2/3 中英对称 + 语言切换
def page_files() -> list[Path]:
    """所有会产出页面的源文件：根 *.html、en 下 *.html，以及 _posts 与 en/news。"""
    out = [p for p in HERE.glob("*.html")]
    out += [p for p in (HERE / "en").rglob("*.html")]
    out += [p for p in (HERE / "_posts").glob("*.md")]
    out += [p for p in (HERE / "en" / "news").glob("*.md")]
    out += [p for p in (HERE / "_research").glob("*.md")]
    out += [p for p in (HERE / "en" / "research").glob("*.md")]
    return sorted(out)


def check_symmetry() -> None:
    roots = sorted(p.name for p in HERE.glob("*.html") if p.name != "404.html")
    missing = [n for n in roots if not (HERE / "en" / n).exists()]
    # resources.html 是站点声明的「中文独有」页（加密页），不算缺陷
    known = {"resources.html"}
    real = [m for m in missing if m not in known]
    INFO.append(f"中英对称：根页面 {len(roots)} 个，缺英文对应 {len(missing)} 个"
                f"（其中 {sorted(known & set(missing))} 为站点声明的中文独有页）")
    for m in real:
        add(f"中英对称：{m} 在 en/ 下没有对应页")


def url_to_rel(url: str) -> str:
    return url.split("#")[0].split("?")[0]


def check_toggles() -> None:
    if not SITE.is_dir():
        return
    bad = 0
    for page in SITE.rglob("*.html"):
        html = read(page)
        m = re.search(r'href="([^"]*)" class="lang-toggle"', html)
        if not m:
            add(f"语言切换：{rel(page)} 没有 lang-toggle 链接")
            continue
        target = url_to_rel(m.group(1))
        probe = SITE / target.lstrip("/")
        if target.endswith("/") or probe.is_dir():
            probe = probe / "index.html"
        if not probe.exists():
            bad += 1
            add(f"语言切换：{rel(page)} 的切换目标 {target} 不存在")
    INFO.append(f"语言切换：{len(list(SITE.rglob('*.html')))} 页，{bad} 页落点失效")


# ---------------------------------------------------------------- 4 i18n
def check_i18n() -> dict[str, dict[str, str]]:
    def flat(path: Path) -> set[str]:
        out, stack = set(), []
        for line in read(path).splitlines():
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            indent = len(line) - len(line.lstrip())
            m = re.match(r"([A-Za-z_0-9]+):", s)
            if not m:
                continue
            while stack and stack[-1][0] >= indent:
                stack.pop()
            stack.append((indent, m.group(1)))
            out.add(".".join(x[1] for x in stack))
        return out

    def nested(path: Path) -> dict[str, dict[str, str]]:
        out: dict[str, dict[str, str]] = {}
        section = None
        for line in read(path).splitlines():
            m = re.match(r"^([A-Za-z_0-9]+):\s*$", line)
            if m:
                section = m.group(1)
                out[section] = {}
                continue
            m = re.match(r'^\s+([A-Za-z_0-9]+):\s*"(.*)"\s*$', line)
            if m and section:
                out[section][m.group(1)] = m.group(2)
        return out

    zh_p, en_p = ROOT / "_data/i18n/zh.yml", ROOT / "_data/i18n/en.yml"
    zh, en = flat(zh_p), flat(en_p)
    if zh != en:
        for k in sorted(zh - en):
            add(f"i18n：键 {k} 只在 zh.yml 里")
        for k in sorted(en - zh):
            add(f"i18n：键 {k} 只在 en.yml 里")
    INFO.append(f"i18n：键集合 {'一致' if zh == en else '不一致'}，共 {len(zh)} 个")

    # 模板里用到的键
    used: set[str] = set()
    for d in ("_includes", "_layouts"):
        for f in (ROOT / d).rglob("*"):
            if f.is_file():
                used |= set(re.findall(r"\bt\.([a-z_]+)\.([a-z_0-9]+)", read(f)))
    used_keys = {".".join(u) for u in used}
    for k in sorted(used_keys - zh):
        add(f"i18n：模板用到键 {k}，但 zh.yml/en.yml 里没有")

    # 反向：定义了但没有任何模板读取的键（只报信息，不判失败）
    templates = "".join(read(f) for d in ("_includes", "_layouts") for f in (ROOT / d).rglob("*") if f.is_file())
    for p in list(HERE.glob("*.html")) + list((HERE / "en").rglob("*.html")):
        templates += read(p)
    unused = sorted(k for k in zh if f"t.{k}" not in templates)
    if unused:
        INFO.append(f"i18n：定义了但无模板读取的键 {len(unused)} 个 → {unused}")

    return {"zh": nested(zh_p).get("nav", {}), "en": nested(en_p).get("nav", {})}


# ------------------------------------------------------- 5 资源存在性
def check_assets() -> None:
    """数据文件里的图片字段 → 实际产出的文件。

    模板用的是 {{ page.image | append: '.jpg' }} 这类拼接，字面扫描看不到，
    所以这里从 research.yml / team.yml 的 image 与 photo 字段反推。
    """
    pairs: list[tuple[str, str]] = []
    for m in re.finditer(r'^\s*image:\s*"([^"]+)"', read(ROOT / "_data/research.yml"), re.M):
        pairs.append(("research.yml", m.group(1)))
    for m in re.finditer(r'^\s*photo:\s*"([^"]+)"', read(ROOT / "_data/team.yml"), re.M):
        if m.group(1):
            pairs.append(("team.yml", m.group(1)))

    for src, p in pairs:
        base = ROOT / p.lstrip("/")
        if not base.with_suffix(".jpg").exists():
            add(f"资源：{src} 的 {p} 缺 .jpg")
        if src == "research.yml" and not base.with_suffix(".webp").exists():
            add(f"资源：{src} 的 {p} 缺 .webp（research-detail 的 <picture> 会请求它）")

    # 头像：模板用 member.photo 直接引用，无 .webp 分支
    avatars = sorted(p.name for p in (ROOT / "assets/img/team").glob("*.jpg"))
    INFO.append(f"资源：数据文件引用 {len(pairs)} 张图，team 头像库 {len(avatars)} 张")


# ---------------------------------------------------------------- 6 文本卫生
CURLY = {0x201C, 0x201D, 0x2018, 0x2019}
SCAN_SUFFIX = {".md", ".html", ".yml", ".css", ".js"}


def check_hygiene() -> None:
    tracked = [p for p in ROOT.rglob("*") if p.is_file() and p.suffix in SCAN_SUFFIX
               and not any(part in {".git", "_site", "vendor", "node_modules", ".jekyll-cache"}
                           for part in p.parts)]
    curly, ctrl, cr, trail = [], [], [], []
    for p in tracked:
        raw = p.read_bytes()
        text = raw.decode("utf-8", errors="replace")
        if any(ord(c) in CURLY for c in text):
            curly.append(rel(p))
        if cr_ := raw.count(b"\r"):
            cr.append(f"{rel(p)}({cr_})")
        bad = [(i, c) for i, c in enumerate(text) if ord(c) < 32 and c not in "\n\t"]
        if bad:
            ctrl.append(f"{rel(p)} 首个 {hex(ord(bad[0][1]))}")
        tw = sum(1 for line in text.splitlines() if line != line.rstrip())
        if tw:
            trail.append(f"{rel(p)}({tw} 行)")
    INFO.append(f"文本卫生：扫描 {len(tracked)} 个文件")
    for label, hits in (("弯引号", curly), ("控制字符", ctrl), ("CR", cr), ("行尾空格", trail)):
        if hits:
            add(f"文本卫生·{label}：{hits[:8]}{' …' if len(hits) > 8 else ''}")


# ------------------------------------------------- 6b 卡片标题的 CSS 覆盖
def check_card_heading_css() -> None:
    """research-card 的标题级别由 include 的 level 参数决定，CSS 必须覆盖每一个可能出现的级别。

    实测踩过：research.html 传 level="h2"，而 CSS 只写了 `.research-card h3, .research-card h4`，
    列表页的卡片标题于是掉回浏览器默认 h2 字号，被放大到近 3 倍。
    """
    css = read(ROOT / "assets/css/main.css")
    callers = list(HERE.glob("*.html")) + list((HERE / "en").rglob("*.html"))
    levels, uses_default = set(), False
    for f in callers:
        text = read(f)
        levels |= set(re.findall(r'include research-card\.html[^%]*?level="(h[1-6])"', text))
        if re.search(r"include research-card\.html(?!\s[^%]*level=)", text):
            uses_default = True
    if uses_default:
        levels.add("h3")          # include 里的 default
    for lv in sorted(levels):
        if f".research-card {lv}" not in css:
            add(f"卡片标题：research-card 会渲染 {lv}，但 main.css 里没有 `.research-card {lv}` 规则，"
                f"该级别会掉回浏览器默认字号")
    if levels:
        INFO.append(f"卡片标题：research-card 使用 {sorted(levels)}，CSS 覆盖{'' if not any(f'.research-card {l}' not in css for l in levels) else '不全'}")


# ---------------------------------------------------------------- 7 可访问性
def check_a11y() -> None:
    if not SITE.is_dir():
        return
    for page in SITE.rglob("*.html"):
        html = read(page)
        for img in re.findall(r"<img\b[^>]*>", html):
            if not re.search(r'alt="[^"]+"', img):
                add(f"可访问性：{rel(page)} 有 <img> 缺 alt → {img[:80]}")
        heads = [int(m) for m in re.findall(r"<h([1-6])\b", html)]
        if heads.count(1) != 1:
            add(f"可访问性：{rel(page)} 有 {heads.count(1)} 个 h1（应为 1）")
        prev = None
        for h in heads:
            if prev and h - prev > 1:
                add(f"可访问性：{rel(page)} 标题层级从 h{prev} 跳到 h{h}")
                break
            prev = h


# ---------------------------------------------------------------- 8 数据文件
def check_data() -> None:
    team = read(ROOT / "_data/team.yml")
    # 用 finditer 取全部条目：文件以 "- name:" 开头，若按 "\n- name:" 切分会丢掉第一条
    starts = [m.start() for m in re.finditer(r"(?m)^- name:", team)]
    blocks = []
    for i, s in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else len(team)
        blocks.append(team[s:end])
    for block in blocks:
        name = block.split("\n", 1)[0].split(":", 1)[1].strip().strip('"')
        for field in ("category",):
            if f"\n  {field}:" not in block and not block.startswith(f" {field}:"):
                add(f"数据：team.yml 的「{name}」缺 {field}")
        m = re.search(r'scholar_url:\s*"([^"]*)"', block)
        if m and re.search(r"XXXXXX", m.group(1)):
            add(f"数据：team.yml 的「{name}」scholar_url 是占位符（{m.group(1)}）")
        if re.search(r'name:\s*"[^"]*[A-Z] "', block) or "学生 D" in block or "Student D" in block:
            INFO.append(f"数据：team.yml 的「{name}」疑似占位条目")

    pubs = read(ROOT / "_data/publications.yml")
    for i, block in enumerate(re.split(r"\n- title:", pubs)[1:], 1):
        for field in ("authors", "journal", "year", "category"):
            if not re.search(rf"\n\s+{field}:", block):
                add(f"数据：publications.yml 第 {i} 条缺 {field}")

    ids = set(re.findall(r'^\s*id:\s*"([^"]+)"', read(ROOT / "_data/research.yml"), re.M))
    for f in (ROOT / "_research").glob("*.md"):
        c = front_matter(read(f)).get("category_id")
        if c and c not in ids:
            add(f"数据：{rel(f)} 的 category_id={c} 不在 research.yml 的 id 里")
    for c in re.findall(r'category:\s*"([^"]+)"', pubs):
        if c not in ids:
            add(f"数据：publications.yml 的 category={c} 不在 research.yml 的 id 里")
    INFO.append(f"数据：research.yml 定义 {len(ids)} 个方向")


# ---------------------------------------------------------------- 9 体积
def check_weight() -> None:
    if not SITE.is_dir():
        return
    files = sorted((p for p in SITE.rglob("*") if p.is_file()), key=lambda p: -p.stat().st_size)
    total = sum(p.stat().st_size for p in files)
    INFO.append(f"体积：_site {len(files)} 个文件，合计 {total / 1e6:.1f} MB")
    heavy = [f"{rel(p)} {p.stat().st_size / 1e6:.2f} MB" for p in files[:8]]
    INFO.append("体积·最重 8 个：" + "；".join(heavy))


def main() -> int:
    check_i18n()
    check_dead_links()
    check_symmetry()
    check_toggles()
    check_assets()
    check_hygiene()
    check_card_heading_css()
    check_a11y()
    check_data()
    check_weight()

    for line in INFO:
        print("  ·", line)
    print()
    if findings:
        print(f"发现 {len(findings)} 条：")
        for f in findings:
            print("  ✗", f)
        print("\nVERDICT FAIL")
        return 1
    print("VERDICT ALL OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
