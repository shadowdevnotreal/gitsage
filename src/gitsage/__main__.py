#!/usr/bin/env python3
"""
GitSage __main__.py - Package Entry Point
==========================================
Allows running GitSage as a module: python -m gitsage
"""

import sys
from pathlib import Path

# Add parent directory to path to find launcher
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

# Import and run main launcher
from launcher import main

if __name__ == "__main__":
    main()
