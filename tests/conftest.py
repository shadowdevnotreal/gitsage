"""pytest configuration and fixtures"""

import os
import sys
import tempfile
from pathlib import Path

import pytest
import yaml

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test outputs"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_readme_config():
    """Sample README configuration for testing"""
    return {
        "project": {
            "name": "Test Project",
            "description": "A test project",
            "version": "1.0.0",
            "author": "Test Author",
            "license": "MIT",
            "github_url": "https://github.com/test/test-project",
        },
        "template": "cli-tool",
        "sections": {
            "badges": True,
            "features": True,
            "installation": True,
            "usage": True,
            "contributing": True,
            "license": True,
        },
        "shields": ["license", "version", "build"],
    }


@pytest.fixture
def sample_wiki_config():
    """Sample wiki configuration for testing"""
    return {
        "project": {
            "name": "Test Wiki",
            "description": "Test wiki documentation",
            "version": "1.0.0",
            "github_url": "https://github.com/test/test-wiki",
        },
        "content": {"sections": [{"title": "Getting Started", "pages": ["Home", "Installation"]}]},
    }


@pytest.fixture
def readme_config_file(temp_dir, sample_readme_config):
    """Create a temporary README config file"""
    config_path = temp_dir / "readme-config.yaml"
    with open(config_path, "w") as f:
        yaml.dump(sample_readme_config, f)
    return config_path


@pytest.fixture
def wiki_config_file(temp_dir, sample_wiki_config):
    """Create a temporary wiki config file"""
    config_path = temp_dir / "wiki-config.yaml"
    with open(config_path, "w") as f:
        yaml.dump(sample_wiki_config, f)
    return config_path
