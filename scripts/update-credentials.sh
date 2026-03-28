#!/bin/bash
# update-credentials.sh
# 更新组内资源凭据并自动触发部署
#
# 用法：
#   1. 编辑 scripts/credentials.conf（每行 username:password）
#   2. 运行 ./scripts/update-credentials.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CRED_FILE="$SCRIPT_DIR/credentials.conf"
REPO="QCL-SUAT/qcl-suat.github.io"

if [ ! -f "$CRED_FILE" ]; then
  echo "错误：凭据文件不存在 $CRED_FILE"
  exit 1
fi

# 读取有效凭据（去掉注释和空行）
CREDS=""
COUNT=0
while IFS= read -r line || [ -n "$line" ]; do
  trimmed="$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
  [[ -z "$trimmed" || "$trimmed" == \#* ]] && continue
  if [ -z "$CREDS" ]; then
    CREDS="$trimmed"
  else
    CREDS="$CREDS
$trimmed"
  fi
  COUNT=$((COUNT + 1))
done < "$CRED_FILE"

if [ -z "$CREDS" ]; then
  echo "错误：没有有效凭据"
  exit 1
fi

echo "读取到 $COUNT 个用户凭据"
echo ""

# 更新 GitHub Secret
echo "正在更新 GitHub Secret..."
echo "$CREDS" | gh secret set RESOURCES_CREDENTIAL --repo "$REPO"
echo "  ✓ Secret 已更新"

# 触发部署
echo "正在触发部署..."
gh workflow run deploy.yml --repo "$REPO"
echo "  ✓ 部署已触发"

echo ""
echo "完成！几分钟后线上生效。"
echo "查看部署状态：gh run list --repo $REPO --limit 1"
