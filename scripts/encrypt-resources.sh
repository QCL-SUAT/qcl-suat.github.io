#!/bin/bash
# encrypt-resources.sh
# 多用户加密组内资源页面
#
# 用法：
#   1. 先构建站点：bundle exec jekyll build
#   2. 运行加密：./scripts/encrypt-resources.sh
#
# 凭据管理：
#   凭据存储在 scripts/credentials.conf（已 gitignore）
#   每行一个用户，格式：username:password
#   username 建议使用学校邮箱
#   人员变动时修改后重新部署

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "正在加密组内资源页面..."
node "$SCRIPT_DIR/encrypt-multi-user.js"

echo ""
echo "本地预览：python3 -m http.server 4000 --directory _site"
echo "线上部署：push 到 GitHub 即可自动加密部署。"
