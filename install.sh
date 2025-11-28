#!/usr/bin/env bash
#
# GitSage Universal Installer for Linux/macOS
# ============================================
# Automated installation script with dependency checking
#

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# Configuration
GITSAGE_DIR="$HOME/.gitsage"
INSTALL_DIR="/usr/local/bin"
VENV_DIR="$GITSAGE_DIR/venv"
REPO_URL="https://github.com/shadowdevnotreal/gitsage.git"
INSTALL_PATH="$(pwd)"

# Detect OS
OS="$(uname -s)"
case "$OS" in
    Linux*)     OS_TYPE="Linux";;
    Darwin*)    OS_TYPE="macOS";;
    *)          OS_TYPE="Unknown";;
esac

# Helper functions
info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[FAIL]${NC} $1"
}

header() {
    echo
    echo -e "${CYAN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${CYAN}${BOLD}  $1${NC}"
    echo -e "${CYAN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo
}

check_command() {
    command -v "$1" &> /dev/null
}

# Main installation
header "GitSage Universal Installer v2.2.0"

info "Detected OS: $OS_TYPE"
info "Installation will be to: $GITSAGE_DIR"
echo

# Check if running from git repo
if [[ ! -f "pyproject.toml" ]] || [[ ! -d "src/gitsage" ]]; then
    error "This script must be run from the GitSage repository root"
    echo "Please cd to the GitSage directory first"
    exit 1
fi

########################################
# Check Prerequisites
########################################

header "Checking Prerequisites"

# Python
if check_command python3; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    success "Python 3: $PYTHON_VERSION"

    # Check Python version >= 3.8
    PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
    PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)

    if [[ "$PYTHON_MAJOR" -lt 3 ]] || [[ "$PYTHON_MAJOR" -eq 3 && "$PYTHON_MINOR" -lt 8 ]]; then
        error "Python 3.8+ is required (found $PYTHON_VERSION)"
        exit 1
    fi
else
    error "Python 3 is not installed"
    echo "Please install Python 3.8+ first:"
    if [[ "$OS_TYPE" == "macOS" ]]; then
        echo "  brew install python3"
    else
        echo "  sudo apt install python3 python3-pip python3-venv  # Ubuntu/Debian"
        echo "  sudo yum install python3 python3-pip              # CentOS/RHEL"
    fi
    exit 1
fi

# Git
if check_command git; then
    GIT_VERSION=$(git --version | cut -d' ' -f3)
    success "Git: $GIT_VERSION"
else
    error "Git is not installed"
    echo "Please install Git first:"
    if [[ "$OS_TYPE" == "macOS" ]]; then
        echo "  brew install git"
    else
        echo "  sudo apt install git  # Ubuntu/Debian"
        echo "  sudo yum install git  # CentOS/RHEL"
    fi
    exit 1
fi

# GitHub CLI
if check_command gh; then
    GH_VERSION=$(gh --version | head -1 | cut -d' ' -f3)
    success "GitHub CLI: $GH_VERSION"

    # Check authentication
    if gh auth status &> /dev/null; then
        success "GitHub CLI: Authenticated"
    else
        warning "GitHub CLI: Not authenticated"
        echo "  Run 'gh auth login' after installation"
    fi
else
    warning "GitHub CLI (gh) is not installed"
    echo "  Install with:"
    if [[ "$OS_TYPE" == "macOS" ]]; then
        echo "    brew install gh"
    else
        echo "    See: https://cli.github.com/manual/installation"
    fi
    echo "  GitHub CLI is optional but recommended"
fi

# pip
if check_command pip3; then
    success "pip3: Available"
else
    error "pip3 is not installed"
    echo "Please install pip3 first"
    exit 1
fi

echo

########################################
# Installation Options
########################################

header "Installation Options"

echo "Choose installation type:"
echo -e "  1. ${GREEN}User Install${NC} (Recommended) - Install to ~/.gitsage with virtual environment"
echo -e "  2. ${YELLOW}System Install${NC} - Install globally to $INSTALL_DIR (requires sudo)"
echo -e "  3. ${BLUE}Development Install${NC} - Install in editable mode for development"
echo

read -rp "Enter choice [1-3]: " INSTALL_TYPE

case "$INSTALL_TYPE" in
    1)
        INSTALL_MODE="user"
        info "Selected: User Install"
        ;;
    2)
        INSTALL_MODE="system"
        info "Selected: System Install"
        if [[ $EUID -ne 0 ]]; then
            warning "System install requires sudo privileges"
        fi
        ;;
    3)
        INSTALL_MODE="dev"
        info "Selected: Development Install"
        ;;
    *)
        error "Invalid choice"
        exit 1
        ;;
esac

echo

########################################
# Create Directories
########################################

header "Creating Directories"

mkdir -p "$GITSAGE_DIR"/{logs,backups,config}
success "Created: $GITSAGE_DIR/"
success "Created: $GITSAGE_DIR/logs"
success "Created: $GITSAGE_DIR/backups"
success "Created: $GITSAGE_DIR/config"

########################################
# Install Python Package
########################################

header "Installing Python Package"

if [[ "$INSTALL_MODE" == "user" ]]; then
    # Create virtual environment
    info "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    success "Virtual environment created"

    # Activate venv
    source "$VENV_DIR/bin/activate"

    # Upgrade pip
    info "Upgrading pip..."
    pip install --upgrade pip > /dev/null 2>&1

    # Install package
    info "Installing GitSage..."
    pip install -e . > /dev/null 2>&1
    success "GitSage installed in virtual environment"

    # Create wrapper script
    info "Creating launcher script..."
    cat > "$GITSAGE_DIR/gitsage" << 'EOF'
#!/usr/bin/env bash
GITSAGE_VENV="$HOME/.gitsage/venv"
source "$GITSAGE_VENV/bin/activate"
python -m gitsage.cli.launcher "$@"
EOF
    chmod +x "$GITSAGE_DIR/gitsage"
    success "Launcher script created"

    # Try to create symlink in user bin
    mkdir -p "$HOME/.local/bin"
    ln -sf "$GITSAGE_DIR/gitsage" "$HOME/.local/bin/gitsage" 2>/dev/null || true

    INSTALL_LOCATION="$HOME/.local/bin/gitsage"

elif [[ "$INSTALL_MODE" == "system" ]]; then
    # System-wide install
    info "Installing GitSage system-wide..."

    if [[ $EUID -ne 0 ]]; then
        sudo pip3 install -e .
    else
        pip3 install -e .
    fi

    success "GitSage installed system-wide"
    INSTALL_LOCATION="$INSTALL_DIR/gitsage"

else
    # Development install
    info "Installing in development mode..."
    pip3 install -e ".[dev]"
    success "GitSage installed in development mode with dev dependencies"
    INSTALL_LOCATION="$(which gitsage || echo 'Run from source')"
fi

########################################
# Create Configuration
########################################

header "Creating Configuration"

if [[ ! -f "$GITSAGE_DIR/config.yaml" ]]; then
    cat > "$GITSAGE_DIR/config.yaml" << EOF
# GitSage Configuration
# See docs for all available options

project:
  name: "GitSage"
  version: "2.2.0"

backup:
  enabled: true
  backup_dir: "$GITSAGE_DIR/backups"
  max_backups_per_repo: 10
  retention_days: 30

logging:
  level: "INFO"
  log_dir: "$GITSAGE_DIR/logs"
  console_output: true
  file_output: true

security:
  require_confirmations: true
  backup_before_delete: true
EOF
    success "Created default configuration: $GITSAGE_DIR/config.yaml"
else
    info "Configuration file already exists"
fi

########################################
# Setup Shell Integration
########################################

header "Shell Integration"

# Detect shell
SHELL_RC=""
if [[ -n "${BASH_VERSION:-}" ]]; then
    SHELL_RC="$HOME/.bashrc"
elif [[ -n "${ZSH_VERSION:-}" ]]; then
    SHELL_RC="$HOME/.zshrc"
fi

if [[ -n "$SHELL_RC" ]] && [[ "$INSTALL_MODE" == "user" ]]; then
    echo
    read -rp "Add GitSage to PATH in $SHELL_RC? (y/N): " ADD_TO_PATH

    if [[ "$ADD_TO_PATH" =~ ^[Yy]$ ]]; then
        # Check if already added
        if ! grep -q ".local/bin" "$SHELL_RC" 2>/dev/null; then
            echo >> "$SHELL_RC"
            echo "# GitSage" >> "$SHELL_RC"
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
            success "Added to PATH in $SHELL_RC"
            warning "Run 'source $SHELL_RC' or restart your shell"
        else
            info "PATH already configured in $SHELL_RC"
        fi
    fi
fi

########################################
# Completion
########################################

echo
echo -e "${CYAN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
success "Installation Complete!"
echo -e "${CYAN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo

echo "GitSage has been installed successfully!"
echo

if [[ "$INSTALL_MODE" == "user" ]]; then
    echo "To use GitSage:"
    echo -e "  ${GREEN}$INSTALL_LOCATION${NC}"
    echo
    echo "If not in PATH, add this to your shell RC file:"
    echo -e "  ${CYAN}export PATH=\"\$HOME/.local/bin:\$PATH\"${NC}"
elif [[ "$INSTALL_MODE" == "system" ]]; then
    echo "GitSage is available system-wide:"
    echo -e "  ${GREEN}gitsage${NC}"
else
    echo "GitSage is installed in development mode"
    echo -e "  ${GREEN}gitsage${NC}"
fi

echo
echo "Quick start:"
echo -e "  ${CYAN}gitsage${NC}              # Launch interactive menu"
echo -e "  ${CYAN}gitsage --help${NC}       # Show help"
echo -e "  ${CYAN}python launcher.py${NC}   # Alternative launcher"
echo

if ! gh auth status &> /dev/null 2>&1; then
    warning "Don't forget to authenticate GitHub CLI:"
    echo -e "  ${CYAN}gh auth login${NC}"
    echo
fi

echo "Documentation:"
echo "  README.md"
echo "  docs/"
echo -e "  ${BLUE}https://github.com/shadowdevnotreal/gitsage${NC}"
echo

success "Happy GitSaging!"
echo

# Offer to launch GitSage
echo -e "${CYAN}${BOLD}Would you like to launch GitSage now?${NC}"
read -rp "Launch GitSage? [Y/n]: " LAUNCH_NOW

if [[ "$LAUNCH_NOW" =~ ^[Yy]?$ ]] || [[ -z "$LAUNCH_NOW" ]]; then
    echo
    info "Launching GitSage..."
    echo

    if [[ "$INSTALL_MODE" == "user" ]]; then
        # Activate virtual environment and run
        source "$VENV_DIR/bin/activate"
        python -m gitsage
    else
        # System/dev install
        gitsage
    fi
fi

echo
