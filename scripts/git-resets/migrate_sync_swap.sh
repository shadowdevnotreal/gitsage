#!/usr/bin/env bash
set -euo pipefail

API="https://api.github.com"
TOKEN="${GITHUB_TOKEN:-}"

if [[ -z "$TOKEN" ]]; then
    echo "ERROR: GITHUB_TOKEN environment variable not set."
    exit 1
fi

########################################
# 0. VALIDATE LOCAL GIT REPO
########################################

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "ERROR: This must be run inside the LOCAL git repository."
    exit 1
fi

echo "Detected local repo at: $(pwd)"

########################################
# 1. DETERMINE DEFAULT BRANCH
########################################

BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "Current branch: $BRANCH"

########################################
# 2. CHECK FOR LOCAL CHANGES
########################################

if ! git diff --quiet; then
    echo "You have UNCOMMITTED changes in the working directory."
    echo "You must commit or stash them before migration."
    exit 1
fi

if ! git diff --cached --quiet; then
    echo "You have staged but uncommitted changes."
    exit 1
fi

########################################
# 3. CHECK FOR UNSYNCED REMOTE CHANGES
########################################

echo "Fetching remote state…"
git fetch origin "$BRANCH"

LOCAL=$(git rev-parse "$BRANCH")
REMOTE=$(git rev-parse "origin/$BRANCH")
BASE=$(git merge-base "$BRANCH" "origin/$BRANCH")

if [[ "$LOCAL" = "$REMOTE" ]]; then
    echo "Local and remote branches are synchronized."
elif [[ "$LOCAL" = "$BASE" ]]; then
    echo "Your local branch is BEHIND — remote has new commits."
    read -rp "Pull remote changes now? (YES/no): " PULL
    if [[ "$PULL" == "YES" ]]; then
        git pull --rebase
    else
        echo "Must sync before migration. Aborting."
        exit 1
    fi
elif [[ "$REMOTE" = "$BASE" ]]; then
    echo "Your local branch is AHEAD — you have unpushed commits."
    read -rp "Push local commits now? (YES/no): " PUSH
    if [[ "$PUSH" == "YES" ]]; then
        git push origin "$BRANCH"
    else
        echo "Must sync before migration. Aborting."
        exit 1
    fi
else
    echo "Local and remote branches have diverged — manual resolution needed."
    exit 1
fi

########################################
# 4. REQUEST USER INPUT FOR MIGRATION
########################################

echo
echo "Enter your GitHub username:"
read -r GH_USER

OLD_REPO=$(basename "$(git rev-parse --show-toplevel)")

echo "Detected original repo name: $OLD_REPO"
echo "Enter the NEW TEMPORARY repository name:"
read -r NEW_REPO

if [[ "$OLD_REPO" == "$NEW_REPO" ]]; then
    echo "ERROR: New repo name must be different."
    exit 1
fi

OLD_REPO_RENAMED="${OLD_REPO}-1"

########################################
# CONFIRM
########################################

echo
echo "This script will:"
echo "  - Sync your local repo"
echo "  - Clone clean copy into TEMP directory"
echo "  - Create new repo: $NEW_REPO"
echo "  - Push code to NEW repo"
echo "  - Rename OLD repo -> $OLD_REPO_RENAMED"
echo "  - Rename NEW repo -> $OLD_REPO"
echo
read -rp "TYPE 'YES' TO CONTINUE: " CONFIRM
[[ "$CONFIRM" == "YES" ]] || exit 1

########################################
# 5. CREATE TEMP DIRECTORY & CLONE REMOTE
########################################

TMPDIR=$(mktemp -d -t repo_migrate_XXXXXX)
echo "Using temporary directory: $TMPDIR"
cd "$TMPDIR"

git clone "https://github.com/$GH_USER/$OLD_REPO.git"
cd "$OLD_REPO"

########################################
# 6. CREATE TEMP REPO VIA API
########################################

echo "Creating new repo: $NEW_REPO"
CREATE_OUTPUT=$(curl -i -H "Authorization: token $TOKEN" \
    -d "{\"name\": \"$NEW_REPO\", \"private\": false}" \
    "$API/user/repos")

echo "$CREATE_OUTPUT"

if ! echo "$CREATE_OUTPUT" | grep -q "201 Created"; then
    echo "ERROR: Failed to create repository."
    exit 1
fi

########################################
# 7. PUSH CLEAN CLONE TO NEW REPO
########################################

git remote remove origin
git remote add origin "https://github.com/$GH_USER/$NEW_REPO.git"
git push -u origin "$BRANCH" || git push -u origin main

########################################
# 8. RENAME OLD REPO
########################################

curl -s -X PATCH \
    -H "Authorization: token $TOKEN" \
    -d "{\"name\": \"$OLD_REPO_RENAMED\"}" \
    "$API/repos/$GH_USER/$OLD_REPO"

########################################
# 9. RENAME NEW REPO TO ORIGINAL NAME
########################################

curl -s -X PATCH \
    -H "Authorization: token $TOKEN" \
    -d "{\"name\": \"$OLD_REPO\"}" \
    "$API/repos/$GH_USER/$NEW_REPO"

echo
echo "=== MIGRATION COMPLETE ==="
echo "Original repo renamed to: $OLD_REPO_RENAMED"
echo "New clean repo now lives at: $OLD_REPO"
echo "Temp work was done in: $TMPDIR"
