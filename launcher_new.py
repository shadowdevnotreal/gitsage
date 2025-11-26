#!/usr/bin/env python3
"""
GitSage Launcher - Backwards Compatible Entry Point
===================================================
This file provides backwards compatibility while using the new modular structure.
"""

import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import and run from new location
from gitsage.cli.launcher import main

if __name__ == "__main__":
    main()
