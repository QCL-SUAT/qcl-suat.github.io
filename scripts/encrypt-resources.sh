#!/bin/bash
# encrypt-resources.sh
# 使用 credentials.txt 中的所有凭据加密组内资源页面
#
# 用法：
#   1. 先构建站点：bundle exec jekyll build
#   2. 运行加密：./scripts/encrypt-resources.sh
#
# 凭据格式（scripts/credentials.txt）：
#   每行一个，格式为 用户名:密码
#   加密密钥 = "用户名:密码"（整行作为密钥）
#
# 管理操作：
#   添加成员 → 在 credentials.txt 新增一行，重新运行本脚本
#   撤销权限 → 删除对应行，重新运行本脚本
#   修改密码 → 修改对应行，重新运行本脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
CRED_FILE="$SCRIPT_DIR/credentials.txt"
INPUT="$PROJECT_DIR/_site/resources/index.html"

if [ ! -f "$CRED_FILE" ]; then
  echo "错误：凭据文件不存在 $CRED_FILE"
  echo "请创建凭据文件，每行格式：用户名:密码"
  exit 1
fi

if [ ! -f "$INPUT" ]; then
  echo "错误：$INPUT 不存在"
  echo "请先运行 bundle exec jekyll build"
  exit 1
fi

# 读取所有凭据，构建密码参数
PASSWORDS=()
while IFS= read -r line || [ -n "$line" ]; do
  # 跳过空行和注释
  line="$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
  [[ -z "$line" || "$line" == \#* ]] && continue
  PASSWORDS+=("$line")
done < "$CRED_FILE"

if [ ${#PASSWORDS[@]} -eq 0 ]; then
  echo "错误：凭据文件中没有有效账号"
  exit 1
fi

echo "找到 ${#PASSWORDS[@]} 个账号，开始加密..."

# 构建 staticrypt 命令
CMD=(npx staticrypt "$INPUT" -o "$INPUT")
for pw in "${PASSWORDS[@]}"; do
  CMD+=(-p "$pw")
done

# 执行加密
"${CMD[@]}"

echo ""
echo "加密完成！有效账号："
while IFS= read -r line || [ -n "$line" ]; do
  line="$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
  [[ -z "$line" || "$line" == \#* ]] && continue
  username="${line%%:*}"
  echo "  - $username"
done < "$CRED_FILE"
echo ""
echo "部署 _site/ 目录即可生效。"
