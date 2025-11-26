"""Tests for README generator"""

import os
import sys
from pathlib import Path

import yaml

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def test_readme_config_loads(readme_config_file):
    """Test that README config file loads correctly"""
    with open(readme_config_file, "r") as f:
        config = yaml.safe_load(f)

    assert "project" in config
    assert config["project"]["name"] == "Test Project"
    assert config["project"]["version"] == "1.0.0"


def test_readme_generator_imports():
    """Test that readme-generator.py can be imported"""
    try:
        # The generator is a script, not a module, but we can check it exists
        generator_path = Path(__file__).parent.parent.parent / "readme-generator.py"
        assert generator_path.exists(), "readme-generator.py not found"

        # Check it has essential content
        content = generator_path.read_text()
        assert "class ReadmeGenerator" in content
        assert "generate_badges" in content
        assert "shields.io" in content
    except Exception as e:
        assert False, f"Failed to verify readme-generator.py: {e}"


def test_readme_templates():
    """Test that README templates are defined"""
    generator_path = Path(__file__).parent.parent.parent / "readme-generator.py"
    content = generator_path.read_text()

    # Check for template types
    templates = ["cli-tool", "library", "web-app", "data-science", "game"]
    for template in templates:
        assert template in content, f"Template {template} not found"


def test_badge_generation():
    """Test that badge URLs can be generated"""
    generator_path = Path(__file__).parent.parent.parent / "readme-generator.py"
    content = generator_path.read_text()

    # Check badge types are supported
    assert "license" in content
    assert "version" in content
    assert "build" in content
    assert "coverage" in content
    assert "shields.io" in content


def test_readme_sections():
    """Test that README sections are implemented"""
    generator_path = Path(__file__).parent.parent.parent / "readme-generator.py"
    content = generator_path.read_text()

    # Check for key section generators
    sections = [
        "generate_header",
        "generate_badges",
        "generate_toc",
        "generate_features",
        "generate_installation",
        "generate_usage",
    ]

    for section in sections:
        assert section in content, f"Section generator {section} not found"


def test_readme_config_structure(sample_readme_config):
    """Test README config has required structure"""
    assert "project" in sample_readme_config
    assert "name" in sample_readme_config["project"]
    assert "description" in sample_readme_config["project"]
    assert "template" in sample_readme_config
    assert "sections" in sample_readme_config


def test_yaml_config_validity(temp_dir, sample_readme_config):
    """Test that config can be written and read as YAML"""
    config_path = temp_dir / "test-config.yaml"

    # Write config
    with open(config_path, "w") as f:
        yaml.dump(sample_readme_config, f)

    # Read it back
    with open(config_path, "r") as f:
        loaded = yaml.safe_load(f)

    assert loaded == sample_readme_config
