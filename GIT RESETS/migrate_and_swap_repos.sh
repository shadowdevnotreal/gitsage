#!/usr/bin/env bash
set -euo pipefail

API="https://api.github.com"
TOKEN="${GITHUB_TOKEN:-}"

if [[ -z "$TOKEN" ]]; then
    echo "ERROR: GITHUB_TOKEN environment variable not set."
    exit 1
fi

echo "Enter your GitHub username:"
read -r GH_USER

echo "Enter the ORIGINAL repository name (e.g. DISCERN-Protocol):"
read -r OLD_REPO

echo "Enter the NEW TEMPORARY repository name (something unique):"
read -r NEW_REPO

if [[ "$OLD_REPO" == "$NEW_REPO" ]]; then
    echo "ERROR: New repo name must be different from old repo."
    exit 1
fi

OLD_REPO_RENAMED="${OLD_REPO}-1"

# Create temp directory
TMPDIR=$(mktemp -d -t repo_migrate_XXXXXX)
echo "Using temporary work directory: $TMPDIR"
cd "$TMPDIR"

echo
echo "You are about to:"
echo "  - Clone $OLD_REPO into isolated temp directory"
echo "  - Create repo: $NEW_REPO"
echo "  - Push code to TEMP repo"
echo "  - Rename OLD repo -> $OLD_REPO_RENAMED"
echo "  - Rename TEMP repo -> $OLD_REPO"
echo
read -rp "TYPE 'YES' TO CONTINUE: " CONFIRM

if [[ "$CONFIRM" != "YES" ]]; then
    echo "Aborted."
    exit 1
fi

echo "Cloning original repo (ignores local copies)..."
git clone "https://github.com/$GH_USER/$OLD_REPO.git"

cd "$OLD_REPO"

echo "Creating NEW repo on GitHub: $NEW_REPO"
CREATE_OUTPUT=$(curl -i -H "Authorization: token $TOKEN" \
    -d "{\"name\": \"$NEW_REPO\", \"private\": false}" \
    "$API/user/repos")

echo "GitHub API Response:"
echo "$CREATE_OUTPUT"
echo

# Extract success code
if ! echo "$CREATE_OUTPUT" | grep -q "201 Created"; then
    echo "ERROR: Repo creation failed. Aborting."
    exit 1
fi

echo "Repointing git remote to TEMP repo..."
git remote remove origin
git remote add origin "https://github.com/$GH_USER/$NEW_REPO.git"

echo "Pushing code to TEMP repo..."
git push -u origin main || git push -u origin master

echo "Renaming OLD repo -> $OLD_REPO_RENAMED"
curl -s -X PATCH \
    -H "Authorization: token $TOKEN" \
    -d "{\"name\": \"$OLD_REPO_RENAMED\"}" \
    "$API/repos/$GH_USER/$OLD_REPO" > /dev/null

echo "Renaming TEMP repo -> $OLD_REPO"
curl -s -X PATCH \
    -H "Authorization: token $TOKEN" \
    -d "{\"name\": \"$OLD_REPO\"}" \
    "$API/repos/$GH_USER/$NEW_REPO" > /dev/null

echo
echo "=== COMPLETED SUCCESSFULLY ==="
echo "Old repo saved as: https://github.com/$GH_USER/$OLD_REPO_RENAMED"
echo "New clean repo at: https://github.com/$GH_USER/$OLD_REPO"
echo
echo "Temporary work dir was: $TMPDIR"
echo "You may delete it manually if desired."
