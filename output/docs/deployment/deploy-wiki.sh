#!/bin/bash
# Enhanced GitHub Wiki Deployment
set -e

REPO_URL="$1"
WIKI_DIR="./generated-docs/github-wiki"

if [ -z "$REPO_URL" ]; then
    echo "Usage: $0 <repository-url>"
    exit 1
fi

WIKI_URL="${REPO_URL%.git}.wiki.git"

echo "[ROCKET] Deploying GitHub Wiki..."
echo "[PKG] Repository: $REPO_URL"
echo "📖 Wiki URL: $WIKI_URL"

TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

cd "$TEMP_DIR"

if git clone "$WIKI_URL" wiki 2>/dev/null; then
    echo "[OK] Wiki repository cloned"
    cd wiki
else
    echo "[EDIT] Creating new wiki repository"
    mkdir wiki
    cd wiki
    git init
    git remote add origin "$WIKI_URL"
fi

echo "📄 Copying wiki files..."
cp -r "$(cd "$(dirname "$0")/../.." && pwd)/$WIKI_DIR"/* .

echo "💾 Committing changes..."
git add .

if ! git diff --staged --quiet; then
    git config user.name "Documentation Bot" 2>/dev/null || true
    git config user.email "docs@generator.local" 2>/dev/null || true

    git commit -m "[DOCS] Auto-update documentation - $(date '+%Y-%m-%d %H:%M:%S')"
    git push -u origin main || git push -u origin master

    echo "[OK] Wiki deployed successfully!"
    echo "🔗 View at: ${REPO_URL%.git}/wiki"
else
    echo "[OK] No changes to commit"
fi
