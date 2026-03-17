#!/bin/bash
# encrypt-resources.sh
# 使用 StaticCrypt 加密组内资源页面
#
# 用法：
#   1. 先构建站点：bundle exec jekyll build
#   2. 运行加密：./scripts/encrypt-resources.sh
#
# 密码管理：
#   密码存储在 scripts/credentials.txt 第一行（已 gitignore）
#   人员变动时修改密码并通知所有成员

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
CRED_FILE="$SCRIPT_DIR/credentials.txt"
INPUT="$PROJECT_DIR/_site/resources/index.html"

if [ ! -f "$CRED_FILE" ]; then
  echo "错误：密码文件不存在 $CRED_FILE"
  echo "请创建文件，第一行写入密码"
  exit 1
fi

if [ ! -f "$INPUT" ]; then
  echo "错误：$INPUT 不存在"
  echo "请先运行 bundle exec jekyll build"
  exit 1
fi

# 读取密码（第一个非空非注释行）
PASSWORD=""
while IFS= read -r line || [ -n "$line" ]; do
  line="$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
  [[ -z "$line" || "$line" == \#* ]] && continue
  PASSWORD="$line"
  break
done < "$CRED_FILE"

if [ -z "$PASSWORD" ]; then
  echo "错误：密码文件中没有有效密码"
  exit 1
fi

echo "正在加密组内资源页面..."

# staticrypt 输出到临时目录，再替换原文件
TMPDIR="$(mktemp -d)"

npx staticrypt "$INPUT" \
  -p "$PASSWORD" \
  --short \
  -d "$TMPDIR" \
  -c false \
  --template-title "组内资源 — QCL" \
  --template-instructions "请输入课题组密码以访问内部资源" \
  --template-placeholder "请输入密码" \
  --template-button "登 录" \
  --template-error "密码错误，请重试" \
  --template-remember "记住密码" \
  --template-color-primary "#4adeaa" \
  --template-color-secondary "#080c10"

# 替换原文件
cp "$TMPDIR/index.html" "$INPUT"
rm -rf "$TMPDIR"

echo ""
echo "加密完成！"
echo "本地预览：python3 -m http.server 4000 --directory _site"
echo "线上部署：push 到 GitHub 即可自动加密部署。"
