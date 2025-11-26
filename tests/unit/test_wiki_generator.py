"""Tests for wiki generators"""

import os
import sys
from pathlib import Path

import yaml

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def test_wiki_config_loads(wiki_config_file):
    """Test that wiki config file loads correctly"""
    with open(wiki_config_file, "r") as f:
        config = yaml.safe_load(f)

    assert "project" in config
    assert config["project"]["name"] == "Test Wiki"
    assert "content" in config


def test_basic_wiki_generator_exists():
    """Test that basic wiki generator exists"""
    generator_path = Path(__file__).parent.parent.parent / "wiki-generator.py"
    assert generator_path.exists(), "wiki-generator.py not found"

    # Check it has essential content
    content = generator_path.read_text()
    assert "yaml" in content.lower()
    assert "wiki" in content.lower()


def test_enhanced_wiki_generator_exists():
    """Test that enhanced wiki generator exists"""
    generator_path = Path(__file__).parent.parent.parent / "wiki-generator.py"
    assert generator_path.exists(), "wiki-generator.py not found"

    # Check it has essential content
    content = generator_path.read_text()
    assert "yaml" in content.lower()
    assert "wiki" in content.lower() or "gitbook" in content.lower()


def test_wiki_config_structure(sample_wiki_config):
    """Test wiki config has required structure"""
    assert "project" in sample_wiki_config
    assert "name" in sample_wiki_config["project"]
    assert "content" in sample_wiki_config
    assert "sections" in sample_wiki_config["content"]


def test_wiki_sections_format(sample_wiki_config):
    """Test wiki sections have correct format"""
    sections = sample_wiki_config["content"]["sections"]
    assert len(sections) > 0

    first_section = sections[0]
    assert "title" in first_section
    assert "pages" in first_section
    assert isinstance(first_section["pages"], list)


def test_generated_docs_directory():
    """Test that wiki generators reference generated-docs directory"""
    basic_path = Path(__file__).parent.parent.parent / "wiki-generator.py"
    enhanced_path = Path(__file__).parent.parent.parent / "wiki-generator.py"

    if basic_path.exists():
        content = basic_path.read_text()
        assert "generated-docs" in content or "generated_docs" in content

    if enhanced_path.exists():
        content = enhanced_path.read_text()
        assert "generated-docs" in content or "generated_docs" in content


def test_wiki_deployment_script_referenced():
    """Test that deployment scripts are mentioned"""
    enhanced_path = Path(__file__).parent.parent.parent / "wiki-generator.py"

    if enhanced_path.exists():
        content = enhanced_path.read_text()
        # Check for deployment-related content
        assert "deploy" in content.lower() or "deployment" in content.lower()


def test_gitbook_support():
    """Test that enhanced generator mentions GitBook"""
    enhanced_path = Path(__file__).parent.parent.parent / "wiki-generator.py"

    if enhanced_path.exists():
        content = enhanced_path.read_text()
        # Check for GitBook features
        assert "SUMMARY.md" in content or "summary" in content.lower()


def test_wiki_page_generation():
    """Test that wiki generators create markdown pages"""
    enhanced_path = Path(__file__).parent.parent.parent / "wiki-generator.py"

    if enhanced_path.exists():
        content = enhanced_path.read_text()
        # Check for markdown generation
        assert ".md" in content
        assert "markdown" in content.lower() or "# " in content


def test_yaml_config_validity(temp_dir, sample_wiki_config):
    """Test that wiki config can be written and read as YAML"""
    config_path = temp_dir / "test-wiki-config.yaml"

    # Write config
    with open(config_path, "w") as f:
        yaml.dump(sample_wiki_config, f)

    # Read it back
    with open(config_path, "r") as f:
        loaded = yaml.safe_load(f)

    assert loaded == sample_wiki_config
