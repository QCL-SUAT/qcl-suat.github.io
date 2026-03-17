# QCL-SUAT 超导量子计算实验室主页

深圳理工大学（SUAT）超导量子计算实验室学术网站，部署于 GitHub Pages。

🔗 **在线访问**：https://qcl-suat.github.io

## 技术栈

- **静态站点生成**：Jekyll 4.4
- **部署平台**：GitHub Pages（GitHub Actions 自动构建部署）
- **多语言**：中文（默认）/ 英文，`_data/i18n/` 管理翻译
- **主题**：自定义暗色/亮色主题，CSS 变量切换
- **资源加密**：StaticCrypt + 多用户密钥包装（AES-256-CBC / PBKDF2）

## 项目结构

```
├── _config.yml          # Jekyll 配置
├── _data/
│   ├── i18n/            # 中英文翻译字符串
│   │   ├── zh.yml
│   │   └── en.yml
│   ├── team.yml         # 团队成员数据
│   ├── research.yml     # 研究方向数据
│   └── publications.yml # 论文列表
├── _includes/           # 页面组件（导航、页脚、卡片等）
├── _layouts/            # 页面布局模板
├── _posts/              # 新闻动态（Jekyll 博客）
├── _research/           # 研究方向详情（Jekyll Collection）
├── assets/
│   ├── css/main.css     # 样式（含暗色/亮色主题变量）
│   ├── js/main.js       # 主题切换、交互逻辑
│   └── images/          # 图片资源
├── en/                  # 英文页面（与中文页面一一对应）
├── scripts/
│   ├── encrypt-multi-user.js      # 多用户加密构建脚本
│   ├── encrypt-resources.sh       # 加密入口脚本
│   ├── update-credentials.sh      # 一键更新凭据并部署
│   ├── staticrypt-template.html   # 登录页模板
│   └── credentials.conf           # 用户凭据（gitignored）
├── .github/workflows/deploy.yml   # CI/CD 自动构建部署
├── index.html           # 首页
├── research.html        # 研究方向
├── team.html            # 团队成员
├── news.html            # 新闻动态
├── join.html            # 加入我们
├── resources.html       # 组内资源（加密）
└── 404.html             # 404 页面
```

## 本地开发

```bash
# 安装依赖（首次）
export PATH="/opt/homebrew/opt/ruby/bin:$PATH"
bundle install

# 启动开发服务器
bundle exec jekyll serve
# 访问 http://localhost:4000

# 构建 + 加密资源页面（本地测试）
bundle exec jekyll build
./scripts/encrypt-resources.sh
python3 -m http.server 4000 --directory _site
```

## 页面管理

### 添加新闻

在 `_posts/` 下创建文件，命名格式 `YYYY-MM-DD-title.md`：

```markdown
---
title: "新闻标题"
title_en: "English Title"
date: 2026-03-17
---
新闻内容...
```

### 添加团队成员

编辑 `_data/team.yml`，在对应分组下添加：

```yaml
- name: 张三
  name_en: San Zhang
  role: 博士研究生
  role_en: Ph.D. Student
  year: 2026
  avatar: /assets/images/avatars/zhangsan.jpg
```

### 添加研究方向

1. 在 `_data/research.yml` 中添加条目
2. 在 `_research/` 下创建详情页（中文）
3. 在 `en/research/` 下创建对应英文页

### 中英文同步

**修改中文页面时，必须同步修改对应的英文页面。** 对应关系：
- 页面：根目录 `*.html` ↔ `en/*.html`
- 研究详情：`_research/*.md` ↔ `en/research/*.html`
- 翻译字符串：`_data/i18n/zh.yml` ↔ `_data/i18n/en.yml`
- 数据文件中 `_en` 后缀字段也要同步

## 资源页面凭据管理

组内资源页面（`/resources/`）使用多用户独立账号保护。

```bash
# 编辑凭据（每行 username:password）
code scripts/credentials.conf

# 一键更新线上并部署
./scripts/update-credentials.sh
```

详细说明见 `scripts/credentials.conf` 文件注释。

## 部署

推送到 `main` 分支后，GitHub Actions 自动执行：
1. Jekyll 构建站点
2. StaticCrypt 加密资源页面
3. 部署到 GitHub Pages
