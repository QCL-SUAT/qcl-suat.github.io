# CLAUDE.md — QCL Website

## 项目概述

QCL（量子计算实验室）学术主页，Jekyll 静态站点，部署在 GitHub Pages。

## 关键规则

### 中英文同步

修改中文页面内容时，**必须同步修改对应的英文页面**。涉及的文件对应关系：

- 中文页面在根目录（`index.html`、`research.html`、`team.html` 等）
- 英文页面在 `en/` 目录下
- 研究详情页：中文在 `_research/`，英文在 `en/research/`
- i18n 字符串：`_data/i18n/zh.yml` 与 `_data/i18n/en.yml` 必须同步
- 数据文件（`_data/team.yml`、`_data/research.yml` 等）中带 `_en` 后缀的字段也要同步更新

### 修改后自动部署

修改完成后应 commit 并 push 到 main 分支，GitHub Actions 会自动构建部署。

## 本地开发

```bash
export PATH="/opt/homebrew/opt/ruby/bin:$PATH"
bundle exec jekyll serve
```

依赖安装在 `vendor/bundle/`（项目本地）。
