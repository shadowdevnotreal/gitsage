#!/bin/bash
#
# GitSage Universal Launcher - Bash Version
# ==========================================
# Universal launcher for all GitSage tools on Linux/macOS.
# Supports both CLI and Web interface modes.
#
# Usage:
#   ./launch.sh              # Interactive menu
#   ./launch.sh --cli        # Launch CLI directly
#   ./launch.sh --web        # Launch web interface
#   ./launch.sh --setup-repo # Repository setup wizard
#   ./launch.sh --help       # Show help

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAUNCHER_PY="$SCRIPT_DIR/launcher.py"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check if launcher.py exists
if [ ! -f "$LAUNCHER_PY" ]; then
    echo -e "${RED}Error: launcher.py not found${NC}"
    echo "Expected location: $LAUNCHER_PY"
    exit 1
fi

# Forward all arguments to the Python launcher
if [ $# -eq 0 ]; then
    # No arguments - interactive mode
    python3 "$LAUNCHER_PY"
else
    # Pass arguments through
    python3 "$LAUNCHER_PY" "$@"
fi
