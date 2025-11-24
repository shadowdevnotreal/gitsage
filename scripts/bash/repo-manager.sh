#!/bin/bash

# Advanced GitHub Repository Manager (Bash)
# Cross-platform: WSL, Linux, Mac, Git Bash, Cygwin, Windows (with Bash)

set -e

# --- COLORS ---
RED='\033[91m'
GREEN='\033[92m'
YELLOW='\033[93m'
BLUE='\033[94m'
CYAN='\033[96m'
WHITE='\033[97m'
BOLD='\033[1m'
END='\033[0m'

if command -v gh.exe >/dev/null 2>&1; then
    GH=gh.exe
elif command -v gh >/dev/null 2>&1; then
    GH=gh
else
    echo -e "${RED}[ERROR]${END} GitHub CLI (gh) not found. Please install."
    exit 1
fi

print_colored() { echo -e "${2:-$WHITE}$1${END}"; }
print_info()    { print_colored "[INFO] $1"    "$BLUE"; }
print_success() { print_colored "[SUCCESS] $1" "$GREEN"; }
print_error()   { print_colored "[ERROR] $1"   "$RED"; }
print_warning() { print_colored "[WARNING] $1" "$YELLOW"; }
ask_confirm() {
    while true; do
        read -p "$(echo -e "${YELLOW}$1 (y/n): ${END}")" yn
        case "$yn" in
            [Yy]*) return 0;;
            [Nn]*) return 1;;
            *) print_colored "Please enter y or n." "$YELLOW";;
        esac
    done
}
pause() { read -n 1 -s -r -p "$(echo -e "${CYAN}Press any key to continue...${END}")"; echo; }

check_tools() {
    print_info "Checking prerequisites..."
    if ! command -v git &>/dev/null; then
        print_error "Git is not installed!"
        exit 1
    fi
    print_success "Git is installed"
    if ! command -v $GH &>/dev/null; then
        print_error "GitHub CLI ($GH) is not installed!"
        exit 1
    fi
    if ! $GH auth status &>/dev/null; then
        print_error "GitHub CLI is not authenticated!"
        print_info "Run: $GH auth login"
        exit 1
    fi
    print_success "GitHub CLI is installed and authenticated"
    check_local_repos_quick "."
}

check_local_repos_quick() {
    local base_path="$1"
    local found=$(find "$base_path" -maxdepth 2 -type d -name ".git" 2>/dev/null | head -n 1)
    if [ -z "$found" ]; then
        print_warning "No local git repositories found in $base_path"
        print_info "Use 'List Local Repositories' to search another location."
    else
        print_success "Local git repository detected in $base_path"
    fi
}

list_repositories_remote() {
    count="$($GH repo list --limit 100 | wc -l)"
    login="$($GH api user | grep login | awk '{print $2}' | tr -d '",')"
    echo -e "\n${CYAN}Showing $count repositories in @${END}${login}\n"
    printf "%-44s %-44s %-12s %-18s\n" "NAME" "DESCRIPTION" "INFO" "UPDATED"
    $GH repo list --limit 100 | awk '{
        repo=$1; $1="";
        desc=substr($0,2,40);
        info="public";
        if(index($0,"private")>0) info="private";
        printf "%-44s %-44s %-12s %-18s\n", repo, desc, info, $(NF)
    }'
    echo
}

list_repositories_local() {
    read -e -p "Enter path to search for local git repos [$(pwd)]: " search_path
    search_path="${search_path:-$(pwd)}"
    echo -e "\n${CYAN}Searching for local git repositories in:${END} $search_path\n"
    found=0
    printf "%-3s %-50s %-30s\n" "#" "Repository Directory" "Last Commit"
    echo "${CYAN}$(printf '─%.0s' {1..90})${END}"
    i=1
    while IFS= read -r repo_dir; do
        dir=$(dirname "$repo_dir")
        repo_name=$(basename "$dir")
        commit_info=$(cd "$dir" && git log -1 --pretty="%cr: %s" 2>/dev/null || echo "n/a")
        printf "%-3s %-50s %-30s\n" "$i" "$dir" "$commit_info"
        found=1
        ((i++))
    done < <(find "$search_path" -maxdepth 2 -type d -name ".git" 2>/dev/null)
    if [ $found -eq 0 ]; then
        print_warning "No local git repositories found in $search_path"
    fi
    echo
    pause
}

select_repo_menu_remote() {
    $GH repo list --limit 100 | nl -nln
    total=$($GH repo list --limit 100 | wc -l)
    read -p "Enter number (1-$total) or q to quit: " sel
    [[ $sel == "q" ]] && return
    if [[ "$sel" =~ ^[0-9]+$ ]] && [ "$sel" -ge 1 ] && [ "$sel" -le "$total" ]; then
        repo=$($GH repo list --limit 100 | sed -n "${sel}p" | awk '{print $1}')
        print_success "Selected: $repo"
        echo "$repo"
    else
        print_error "Invalid selection."
        return
    fi
}

select_repo_menu_local() {
    read -e -p "Enter path to search for local git repos [$(pwd)]: " search_path
    search_path="${search_path:-$(pwd)}"
    local repos=()
    i=1
    while IFS= read -r repo_dir; do
        dir=$(dirname "$repo_dir")
        repo_name=$(basename "$dir")
        repos+=("$dir")
        echo -e "${YELLOW}$i.${END} $dir"
        ((i++))
    done < <(find "$search_path" -maxdepth 2 -type d -name ".git" 2>/dev/null)
    total="${#repos[@]}"
    [ "$total" -eq 0 ] && print_warning "No local repositories found!" && return
    read -p "Select repository number (1-$total) or q to quit: " sel
    [[ $sel == "q" ]] && return
    if [[ "$sel" =~ ^[0-9]+$ ]] && [ "$sel" -ge 1 ] && [ "$sel" -le "$total" ]; then
        echo "${repos[$((sel-1))]}"
    else
        print_error "Invalid selection."
        return
    fi
}

delete_repository() {
    repo_name="$1"
    print_info "Repository details for: $repo_name"
    $GH repo view "$repo_name"
    if ask_confirm "Are you ABSOLUTELY sure you want to delete '$repo_name'? This cannot be undone!"; then
        $GH repo delete "$repo_name" --yes
        print_success "Repository deleted."
        local_dir="${repo_name##*/}"
        if [ -d "$local_dir" ]; then
            if ask_confirm "Delete local directory '$local_dir'?"; then
                rm -rf "$local_dir"
                print_success "Local directory deleted."
            fi
        fi
    else
        print_warning "Repository deletion cancelled."
    fi
    pause
}

reset_git_history_prompt() {
    repo_name="$1"
    local_dir="${repo_name##*/}"
    if [ ! -d "$local_dir" ]; then
        print_error "Local dir $local_dir not found. Please clone it first."
        pause
        return
    fi
    read -p "Commit message for history reset [Initial commit with reset history]: " commit_msg
    commit_msg="${commit_msg:-Initial commit with reset history}"
    if ask_confirm "Reset Git history for '$repo_name'? This cannot be undone!"; then
        (
            cd "$local_dir"
            current_branch=$(git branch --show-current 2>/dev/null || echo "main")
            git reset --hard && git clean -d -f
            git checkout --orphan temp_branch
            git add -A
            if git diff --cached --quiet; then
                print_warning "No changes to commit."
                git checkout "$current_branch"
                git branch -D temp_branch 2>/dev/null || true
                return
            fi
            git commit -m "$commit_msg"
            git branch -D "$current_branch"
            git branch -m "$current_branch"
            if ask_confirm "Force push new history to origin? This deletes ALL commit history!"; then
                git push -f origin "$current_branch"
                print_success "Git history reset and pushed successfully."
            else
                print_warning "Force push cancelled."
            fi
        )
    else
        print_warning "History reset cancelled."
    fi
    pause
}

sync_repository_local() {
    repo_dir="$1"
    if [ ! -d "$repo_dir/.git" ]; then
        print_error "Not a valid git repo: $repo_dir"
        pause
        return
    fi
    print_info "Syncing local repository: $repo_dir"
    (
        cd "$repo_dir"
        git fetch --all --prune
        branch=$(git branch --show-current)
        git pull origin "$branch"
        print_success "Local repository synced."
    )
    pause
}

sync_repository_remote() {
    repo_name="$1"
    local_dir="${repo_name##*/}"
    if [ ! -d "$local_dir" ]; then
        print_warning "Local dir $local_dir not found. Cloning..."
        $GH repo clone "$repo_name"
        print_success "Repository cloned."
    fi
    print_info "Syncing repository: $repo_name"
    (
        cd "$local_dir"
        git fetch --all --prune
        branch=$(git branch --show-current)
        git pull origin "$branch"
        print_success "Repository synced."
    )
    pause
}

main_menu() {
    while true; do
        echo -e "\n${CYAN}=== REPOSITORY MANAGEMENT OPTIONS ===${END}"
        echo "1. Delete Remote Repository"
        echo "2. Reset Remote Git History (local copy required)"
        echo "3. Sync Remote Repository (clone+pull)"
        echo "4. List Remote Repositories"
        echo "5. List Local Repositories"
        echo "6. Sync Local Repository"
        echo "7. Exit"
        echo
        read -p "Select operation (1-7): " op
        case "$op" in
            1) repo=$(select_repo_menu_remote); [[ $repo ]] && delete_repository "$repo";;
            2) repo=$(select_repo_menu_remote); [[ $repo ]] && reset_git_history_prompt "$repo";;
            3) repo=$(select_repo_menu_remote); [[ $repo ]] && sync_repository_remote "$repo";;
            4) list_repositories_remote;;
            5) list_repositories_local;;
            6) repo_dir=$(select_repo_menu_local); [[ $repo_dir ]] && sync_repository_local "$repo_dir";;
            7) print_success "Goodbye!"; exit 0;;
            *) print_error "Invalid choice. Please select 1-7.";;
        esac
    done
}

check_tools
main_menu
