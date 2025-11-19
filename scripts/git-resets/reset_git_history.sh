#!/usr/bin/env bash
set -euo pipefail

# Hard reset script: deletes ALL git history and replaces it
# with a single initial commit of the current working tree.
#
# Usage:
#   ./reset_git_history.sh
#
# Assumes:
#   - You are in the repo you want to reset.
#   - You have no uncommitted changes you want to keep aside
#     from what should become the new initial commit.

DEFAULT_BRANCH="main"  # change to "master" if needed
BACKUP_TAG="before-history-reset-$(date +%Y%m%d-%H%M%S)"

echo "=== HARD GIT HISTORY RESET ==="
echo
echo "Repo: $(basename "$(pwd)")"
echo "Default branch (target): $DEFAULT_BRANCH"
echo "A backup tag will be created: $BACKUP_TAG"
echo
echo "WARNING: This will:"
echo "  - Delete ALL git history on the current branch"
echo "  - Force-push to origin/$DEFAULT_BRANCH"
echo "  - Require all collaborators to reclone or reset"
echo

read -rp "Type 'DELETE-ALL-HISTORY' to confirm: " CONFIRM
if [[ "$CONFIRM" != "DELETE-ALL-HISTORY" ]]; then
  echo "Aborted. No changes made."
  exit 1
fi

# Ensure we're in a git repository
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Error: This is not a git repository."
  exit 1
fi

echo
echo "Creating backup tag: $BACKUP_TAG"
git tag "$BACKUP_TAG"
git push origin "$BACKUP_TAG" || {
  echo "Warning: Could not push backup tag to origin. Continuing anyway."
}

echo
echo "Fetching remote..."
git fetch origin

echo
echo "Checking out $DEFAULT_BRANCH..."
git checkout "$DEFAULT_BRANCH"

echo
echo "Pulling latest $DEFAULT_BRANCH..."
git pull origin "$DEFAULT_BRANCH"

echo
echo "Creating orphan branch 'clean-temp'..."
git checkout --orphan clean-temp

echo "Staging all files..."
git add -A

echo "Creating new initial commit..."
git commit -m "Initial clean history"

echo
echo "Deleting old $DEFAULT_BRANCH..."
git branch -D "$DEFAULT_BRANCH"

echo "Renaming clean-temp -> $DEFAULT_BRANCH..."
git branch -m "$DEFAULT_BRANCH"

echo
echo "Force-pushing new history to origin/$DEFAULT_BRANCH..."
git push --force-with-lease origin "$DEFAULT_BRANCH"

echo
echo "Done."
echo "Backup tag created locally and (if possible) on origin: $BACKUP_TAG"
echo "All old history is now only reachable via that tag or other backups."
