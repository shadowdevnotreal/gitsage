#!/bin/bash

# Interactive GitHub Repository Deletion Script
# Safely removes both remote and local repositories with full synchronization

set -e  # Exit on any error

# Detect the right command to use (WSL, Windows, Linux, Git Bash)
if command -v gh.exe >/dev/null 2>&1; then
    GH=gh.exe
elif command -v gh >/dev/null 2>&1; then
    GH=gh
else
    echo "[ERROR] GitHub CLI (gh) is not installed. Please install it first."
    exit 1
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status()    { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success()   { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning()   { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error()     { echo -e "${RED}[ERROR]${NC} $1"; }

confirm_action() {
    local message="$1"
    local response
    while true; do
        read -p "$(echo -e "${YELLOW}$message (y/n): ${NC}")" response
        case $response in
            [Yy]* ) return 0;;
            [Nn]* ) return 1;;
            * ) echo "Please answer yes (y) or no (n).";;
        esac
    done
}

check_gh_cli() {
    if ! command -v $GH &> /dev/null; then
        print_error "GitHub CLI ($GH) is not installed. Please install it first."
        print_status "Installation: https://cli.github.com/"
        exit 1
    fi
    if ! $GH auth status &> /dev/null; then
        print_error "GitHub CLI is not authenticated. Please run '$GH auth login' first."
        exit 1
    fi
    print_success "GitHub CLI is installed and authenticated"
}

# ==== Repo Picker Menu (Pretty or Numbered) ====
select_repository() {
    echo
    echo "How would you like to select a repository?"
    echo "  1. Pretty table (copy/paste or type name, more info)"
    echo "  2. Numbered menu (select by number)"
    read -p "Enter 1 or 2: " table_mode

    if [[ "$table_mode" == "1" ]]; then
        $GH repo list --limit 30
        echo
        read -p "Enter the repository name (owner/repo): " repo_name
    elif [[ "$table_mode" == "2" ]]; then
        mapfile -t repo_lines < <($GH repo list --limit 30 --json name,owner,description,isPrivate,visibility,updatedAt \
            -q '.[] | "\(.owner.login)/\(.name)\t\(.description|tostring)\t\(.visibility)\t\(.updatedAt)"')
        printf "\n%-3s %-40s %-30s %-8s %-20s\n" "No." "Name" "Description" "Type" "Updated"
        echo "---------------------------------------------------------------------------------------------------------------------------"
        for i in "${!repo_lines[@]}"; do
            IFS=$'\t' read -r repo_name_only repo_desc repo_vis repo_upd <<< "${repo_lines[$i]}"
            printf "%-3d %-40s %-30.30s %-8s %-20s\n" "$((i+1))" "$repo_name_only" "$repo_desc" "$repo_vis" "$repo_upd"
        done
        read -p "Select repository by number: " idx
        selected="${repo_lines[$((idx-1))]}"
        IFS=$'\t' read -r repo_name _ <<< "$selected"
    else
        echo "Invalid option. Exiting."
        exit 1
    fi
    echo "$repo_name"
}
# ==== END PATCH ====

validate_repository() {
    local repo_name="$1"
    if ! $GH repo view "$repo_name" &> /dev/null; then
        print_error "Repository '$repo_name' not found or not accessible."
        return 1
    fi
    return 0
}

get_repo_details() {
    local repo_name="$1"
    print_status "Repository details for: $repo_name"
    $GH repo view "$repo_name" --json name,description,isPrivate,defaultBranch,diskUsage,stargazerCount,forkCount,visibility
    echo ""
}

check_local_repo() {
    local repo_name="$1"
    local repo_dir="${repo_name##*/}"  # Extract repo name from owner/repo format
    if [ -d "$repo_dir" ]; then
        print_warning "Local directory '$repo_dir' found in current location"
        return 0
    fi
    return 1
}

delete_remote_repo() {
    local repo_name="$1"
    print_status "Deleting remote repository: $repo_name"
    if confirm_action "Are you absolutely sure you want to delete the remote repository '$repo_name'? This action cannot be undone!"; then
        $GH repo delete "$repo_name" --yes
        print_success "Remote repository '$repo_name' deleted successfully"
        return 0
    else
        print_warning "Remote repository deletion cancelled"
        return 1
    fi
}

delete_local_repo() {
    local repo_name="$1"
    local repo_dir="${repo_name##*/}"
    if [ -d "$repo_dir" ]; then
        print_status "Found local directory: $repo_dir"
        if [ -d "$repo_dir/.git" ]; then
            print_warning "This appears to be a git repository"
            print_status "Git status for local repository:"
            (cd "$repo_dir" && git status --porcelain)
            if (cd "$repo_dir" && git status --porcelain | grep -q .); then
                print_warning "There are uncommitted changes in the local repository"
                if ! confirm_action "Delete local repository anyway?"; then
                    print_warning "Local repository deletion cancelled"
                    return 1
                fi
            fi
        fi
        if confirm_action "Delete local directory '$repo_dir'?"; then
            rm -rf "$repo_dir"
            print_success "Local directory '$repo_dir' deleted successfully"
            return 0
        else
            print_warning "Local directory deletion cancelled"
            return 1
        fi
    else
        print_status "No local directory found for repository"
        return 0
    fi
}

verify_deletion() {
    local repo_name="$1"
    local repo_dir="${repo_name##*/}"
    print_status "Verifying deletion..."
    if $GH repo view "$repo_name" &> /dev/null; then
        print_error "Remote repository still exists!"
        return 1
    else
        print_success "Remote repository confirmed deleted"
    fi
    if [ -d "$repo_dir" ]; then
        print_error "Local directory still exists!"
        return 1
    else
        print_success "Local directory confirmed deleted"
    fi
    return 0
}

main() {
    echo -e "${BLUE}GitHub Repository Deletion Script${NC}"
    echo -e "${BLUE}==================================${NC}\n"
    check_gh_cli

    # ==== PATCH: Use interactive repo selection ====
    repo_name=$(select_repository)
    if [[ -z "$repo_name" ]]; then
        print_error "Repository name cannot be empty"
        exit 1
    fi
    if ! validate_repository "$repo_name"; then
        exit 1
    fi

    get_repo_details "$repo_name"

    if ! confirm_action "This will permanently delete '$repo_name' and any local copy. Continue?"; then
        print_warning "Operation cancelled by user"
        exit 0
    fi

    local remote_deleted=false
    local local_deleted=false

    if delete_remote_repo "$repo_name"; then
        remote_deleted=true
    fi

    if check_local_repo "$repo_name"; then
        if delete_local_repo "$repo_name"; then
            local_deleted=true
        fi
    else
        local_deleted="N/A"
    fi

    if [[ "$remote_deleted" == true ]]; then
        verify_deletion "$repo_name"
    fi

    print_success "Repository deletion completed successfully!"
}

main "$@"
