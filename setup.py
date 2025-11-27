#!/usr/bin/env python3
"""
GitSage Setup Script

This setup.py provides backward compatibility for older pip/setuptools versions
that don't fully support PEP 517/660 pyproject.toml builds.

For modern installations, pip will use pyproject.toml directly.
"""

from setuptools import setup

# All configuration is in pyproject.toml
# This file exists only for backward compatibility
setup()
