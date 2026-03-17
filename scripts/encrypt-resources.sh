#!/bin/bash
# encrypt-resources.sh
# 使用 StaticCrypt 加密组内资源页面（支持用户名+密码）
#
# 用法：
#   1. 先构建站点：bundle exec jekyll build
#   2. 运行加密：./scripts/encrypt-resources.sh
#
# 凭据管理：
#   凭据存储在 scripts/credentials.txt（已 gitignore）
#   格式：username:password（如 zhangsan@suat.edu.cn:Qcl@2026）
#   人员变动时修改凭据并通知所有成员

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
CRED_FILE="$SCRIPT_DIR/credentials.txt"
TEMPLATE="$SCRIPT_DIR/staticrypt-template.html"
INPUT="$PROJECT_DIR/_site/resources/index.html"

if [ ! -f "$CRED_FILE" ]; then
  echo "错误：凭据文件不存在 $CRED_FILE"
  echo "请创建文件，格式：username:password"
  exit 1
fi

if [ ! -f "$INPUT" ]; then
  echo "错误：$INPUT 不存在"
  echo "请先运行 bundle exec jekyll build"
  exit 1
fi

if [ ! -f "$TEMPLATE" ]; then
  echo "错误：模板文件不存在 $TEMPLATE"
  exit 1
fi

# 读取凭据（第一个非空非注释行，格式 username:password）
CREDENTIAL=""
while IFS= read -r line || [ -n "$line" ]; do
  line="$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
  [[ -z "$line" || "$line" == \#* ]] && continue
  CREDENTIAL="$line"
  break
done < "$CRED_FILE"

if [ -z "$CREDENTIAL" ]; then
  echo "错误：凭据文件中没有有效凭据"
  exit 1
fi

echo "正在加密组内资源页面..."

# staticrypt 输出到临时目录，再替换原文件
TMPDIR="$(mktemp -d)"

npx staticrypt "$INPUT" \
  -p "$CREDENTIAL" \
  --short \
  -d "$TMPDIR" \
  -c false \
  -t "$TEMPLATE" \
  --template-title "组内资源 — QCL" \
  --template-instructions "请输入课题组凭据以访问内部资源" \
  --template-placeholder "请输入密码" \
  --template-button "登 录" \
  --template-error "用户名或密码错误，请重试" \
  --template-remember "记住登录状态" \
  --template-color-primary "#4adeaa" \
  --template-color-secondary "#080c10"

# 替换原文件
cp "$TMPDIR/index.html" "$INPUT"
rm -rf "$TMPDIR"

echo ""
echo "加密完成！"
echo "本地预览：python3 -m http.server 4000 --directory _site"
echo "线上部署：push 到 GitHub 即可自动加密部署。"
