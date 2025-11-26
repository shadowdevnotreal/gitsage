#!/usr/bin/env bash
#
# GitSage Repository Migration Tool
# ==================================
# Unified script to migrate GitHub repositories with clean history
#
# Features:
# - Validate local repository state
# - Sync local and remote before migration
# - Create temporary repository
# - Swap repository names atomically
# - Safety checks and confirmations
#
# Usage:
#   ./migrate_repository.sh [--mode=<simple|full>] [--skip-validation]
#

set -euo pipefail

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
API="https://api.github.com"
TOKEN="${GITHUB_TOKEN:-}"
MODE="${1:---mode=full}"
SKIP_VALIDATION=false

# Parse arguments
for arg in "$@"; do
    case $arg in
        --mode=simple)
            MODE="simple"
            shift
            ;;
        --mode=full)
            MODE="full"
            shift
            ;;
        --skip-validation)
            SKIP_VALIDATION=true
            shift
            ;;
        --help|-h)
            cat << EOF
GitSage Repository Migration Tool

Usage: $0 [OPTIONS]

OPTIONS:
  --mode=simple         Simple migration (clone from remote only)
  --mode=full           Full migration with local validation (default)
  --skip-validation     Skip local repository validation
  --help, -h            Show this help message

REQUIREMENTS:
  - GITHUB_TOKEN environment variable must be set
  - For full mode: Must be run from inside the repository

EXAMPLES:
  # Full migration with validation
  $0 --mode=full

  # Simple migration (no local validation)
  $0 --mode=simple

  # Skip validation checks
  $0 --skip-validation

EOF
            exit 0
            ;;
    esac
done

# Helper functions
info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
if [[ -z "$TOKEN" ]]; then
    error "GITHUB_TOKEN environment variable not set."
    echo "Please set it with: export GITHUB_TOKEN=your_token_here"
    exit 1
fi

info "GitSage Repository Migration Tool"
info "Mode: $MODE"
echo

########################################
# FULL MODE: Validate Local Repository
########################################

if [[ "$MODE" == "full" ]] && [[ "$SKIP_VALIDATION" == "false" ]]; then
    info "Validating local repository..."

    if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        error "Not inside a git repository."
        echo "For migration without local repo, use: --mode=simple"
        exit 1
    fi

    info "Detected local repo at: $(pwd)"

    # Determine current branch
    BRANCH=$(git rev-parse --abbrev-ref HEAD)
    info "Current branch: $BRANCH"

    # Check for uncommitted changes
    if ! git diff --quiet 2>/dev/null; then
        error "You have UNCOMMITTED changes in the working directory."
        echo "Please commit or stash them before migration."
        exit 1
    fi

    if ! git diff --cached --quiet 2>/dev/null; then
        error "You have staged but uncommitted changes."
        exit 1
    fi

    success "Working directory is clean"

    # Check synchronization with remote
    info "Checking sync with remote..."
    git fetch origin "$BRANCH" 2>/dev/null || warning "Could not fetch remote branch"

    LOCAL=$(git rev-parse "$BRANCH" 2>/dev/null || echo "")
    REMOTE=$(git rev-parse "origin/$BRANCH" 2>/dev/null || echo "")

    if [[ -n "$LOCAL" ]] && [[ -n "$REMOTE" ]]; then
        BASE=$(git merge-base "$BRANCH" "origin/$BRANCH" 2>/dev/null || echo "")

        if [[ "$LOCAL" = "$REMOTE" ]]; then
            success "Local and remote branches are synchronized"
        elif [[ "$LOCAL" = "$BASE" ]]; then
            warning "Your local branch is BEHIND remote"
            read -rp "Pull remote changes now? (YES/no): " PULL
            if [[ "$PULL" == "YES" ]]; then
                git pull --rebase
                success "Pulled remote changes"
            else
                error "Must sync before migration"
                exit 1
            fi
        elif [[ "$REMOTE" = "$BASE" ]]; then
            warning "Your local branch is AHEAD of remote"
            read -rp "Push local commits now? (YES/no): " PUSH
            if [[ "$PUSH" == "YES" ]]; then
                git push origin "$BRANCH"
                success "Pushed local commits"
            else
                error "Must sync before migration"
                exit 1
            fi
        else
            error "Local and remote branches have diverged"
            echo "Please resolve manually before migration"
            exit 1
        fi
    fi

    echo
fi

########################################
# Get User Input
########################################

read -rp "Enter your GitHub username: " GH_USER

if [[ "$MODE" == "full" ]] && git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    OLD_REPO=$(basename "$(git rev-parse --show-toplevel)")
    info "Detected original repo name: $OLD_REPO"
else
    read -rp "Enter the ORIGINAL repository name: " OLD_REPO
fi

read -rp "Enter the NEW TEMPORARY repository name (something unique): " NEW_REPO

if [[ "$OLD_REPO" == "$NEW_REPO" ]]; then
    error "New repo name must be different from old repo"
    exit 1
fi

OLD_REPO_RENAMED="${OLD_REPO}-old"

########################################
# Confirmation
########################################

echo
info "Migration Plan:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  1. Clone ${OLD_REPO} to temporary directory"
echo "  2. Create new repository: ${NEW_REPO}"
echo "  3. Push code to ${NEW_REPO}"
echo "  4. Rename ${OLD_REPO} → ${OLD_REPO_RENAMED}"
echo "  5. Rename ${NEW_REPO} → ${OLD_REPO}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo
warning "This operation cannot be easily undone!"
echo
read -rp "TYPE 'YES' TO CONTINUE: " CONFIRM

if [[ "$CONFIRM" != "YES" ]]; then
    warning "Migration aborted by user"
    exit 0
fi

########################################
# Create Temp Directory & Clone
########################################

TMPDIR=$(mktemp -d -t gitsage_migrate_XXXXXX)
info "Using temporary directory: $TMPDIR"
cd "$TMPDIR"

info "Cloning repository from GitHub..."
if git clone "https://github.com/$GH_USER/$OLD_REPO.git" 2>/dev/null; then
    success "Repository cloned successfully"
else
    error "Failed to clone repository"
    echo "Please check:"
    echo "  - Repository name is correct"
    echo "  - You have access to the repository"
    echo "  - GitHub authentication is configured"
    exit 1
fi

cd "$OLD_REPO"

########################################
# Create New Repository via API
########################################

info "Creating new repository: $NEW_REPO"
CREATE_OUTPUT=$(curl -i -H "Authorization: token $TOKEN" \
    -d "{\"name\": \"$NEW_REPO\", \"private\": false}" \
    "$API/user/repos" 2>/dev/null)

if echo "$CREATE_OUTPUT" | grep -q "201 Created"; then
    success "New repository created"
else
    error "Failed to create repository"
    echo "$CREATE_OUTPUT"
    exit 1
fi

########################################
# Push to New Repository
########################################

info "Configuring remote for new repository..."
git remote remove origin
git remote add origin "https://github.com/$GH_USER/$NEW_REPO.git"

info "Pushing code to new repository..."
if git push -u origin main 2>/dev/null || git push -u origin master 2>/dev/null; then
    success "Code pushed to new repository"
else
    error "Failed to push code"
    exit 1
fi

########################################
# Rename Repositories
########################################

info "Renaming ${OLD_REPO} → ${OLD_REPO_RENAMED}..."
RENAME_OUTPUT=$(curl -s -X PATCH \
    -H "Authorization: token $TOKEN" \
    -d "{\"name\": \"$OLD_REPO_RENAMED\"}" \
    "$API/repos/$GH_USER/$OLD_REPO")

if echo "$RENAME_OUTPUT" | grep -q "\"name\":"; then
    success "Original repository renamed"
else
    error "Failed to rename original repository"
    echo "$RENAME_OUTPUT"
    exit 1
fi

info "Renaming ${NEW_REPO} → ${OLD_REPO}..."
RENAME_OUTPUT=$(curl -s -X PATCH \
    -H "Authorization: token $TOKEN" \
    -d "{\"name\": \"$OLD_REPO\"}" \
    "$API/repos/$GH_USER/$NEW_REPO")

if echo "$RENAME_OUTPUT" | grep -q "\"name\":"; then
    success "New repository renamed to original name"
else
    error "Failed to rename new repository"
    echo "$RENAME_OUTPUT"
    exit 1
fi

########################################
# Completion
########################################

echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
success "MIGRATION COMPLETED SUCCESSFULLY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo
echo "  ${GREEN}✓${NC} Original repo (archived):  https://github.com/$GH_USER/$OLD_REPO_RENAMED"
echo "  ${GREEN}✓${NC} New clean repo:            https://github.com/$GH_USER/$OLD_REPO"
echo
echo "Temporary work directory: $TMPDIR"
echo "You may delete it with: rm -rf $TMPDIR"
echo

# Optionally update local repo remote
if [[ "$MODE" == "full" ]] && git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo
    read -rp "Update your local repository remote? (YES/no): " UPDATE_REMOTE
    if [[ "$UPDATE_REMOTE" == "YES" ]]; then
        ORIGINAL_DIR=$(git rev-parse --show-toplevel)
        cd "$ORIGINAL_DIR"
        git remote set-url origin "https://github.com/$GH_USER/$OLD_REPO.git"
        success "Local remote updated"
        echo "You may want to verify with: git remote -v"
    fi
fi

echo
success "All done!"
