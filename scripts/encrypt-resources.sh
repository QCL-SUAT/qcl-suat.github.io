#!/bin/bash
# encrypt-resources.sh
# Encrypts the resources page using StaticCrypt with username:password keys.
#
# Prerequisites: npm install -g staticrypt
#
# Usage:
#   ./scripts/encrypt-resources.sh <username> <password>
#
# Multiple credentials can be added by running the script multiple times
# with different username/password pairs before deploying.
#
# The combined key format is: username:password

set -e

if [ $# -lt 2 ]; then
  echo "Usage: $0 <username> <password>"
  echo "Example: $0 student1 mypassword123"
  exit 1
fi

USERNAME="$1"
PASSWORD="$2"
PASSPHRASE="${USERNAME}:${PASSWORD}"

INPUT="_site/resources/index.html"
TEMPLATE="scripts/staticrypt-template.html"

if [ ! -f "$INPUT" ]; then
  echo "Error: $INPUT not found. Run 'bundle exec jekyll build' first."
  exit 1
fi

echo "Encrypting resources page with credentials for: $USERNAME"

npx staticrypt "$INPUT" \
  --password "$PASSPHRASE" \
  --template "$TEMPLATE" \
  --template-title "组内资源 — QCL" \
  --template-instructions "请使用课题组账号登录" \
  --template-color-primary "#4adeaa" \
  --template-color-secondary "#080c10" \
  -o "$INPUT"

echo "Done. Resources page encrypted."
