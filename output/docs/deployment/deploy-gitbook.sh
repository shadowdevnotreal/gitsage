#!/bin/bash
# GitBook Deployment
set -e

GITBOOK_DIR="./generated-docs/gitbook"

echo "[ROCKET] Building GitBook..."

cd "$GITBOOK_DIR"

# Install GitBook CLI if needed
if ! command -v gitbook &> /dev/null; then
    echo "Installing GitBook CLI..."
    npm install -g gitbook-cli
fi

# Install plugins
echo "[PKG] Installing plugins..."
gitbook install

# Build
echo "🔨 Building..."
gitbook build

echo "[OK] GitBook built successfully!"
echo "📂 Output: $GITBOOK_DIR/_book"
echo ""
echo "Deploy options:"
echo "  1. GitBook.com: Push to GitHub and connect"
echo "  2. GitHub Pages: Copy _book/* to gh-pages branch"
echo "  3. Netlify: Deploy _book folder"
