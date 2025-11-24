"""Integration tests for GitSage components"""
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def test_launcher_exists():
    """Test that launcher.py exists"""
    launcher_path = Path(__file__).parent.parent.parent / 'launcher.py'
    assert launcher_path.exists(), "launcher.py not found"


def test_launcher_integrates_all_tools():
    """Test that launcher integrates all major tools"""
    launcher_path = Path(__file__).parent.parent.parent / 'launcher.py'
    content = launcher_path.read_text()

    # Check for all integrated tools
    tools = [
        'delete-repo.sh',      # Repository deletion
        'repo-manager.sh',      # Repository manager
        'wiki-generator.py',    # Basic wiki
        'wiki-generator-enhanced.py',  # Enhanced wiki
        'readme-generator.py',  # README generator (NEW)
        'reset_git_history.sh', # Git history reset (NEW)
        'migrate_and_swap_repos.sh'  # Migration (NEW)
    ]

    for tool in tools:
        assert tool in content, f"Tool {tool} not integrated in launcher"


def test_cli_wrapper_exists():
    """Test that gitsage CLI wrapper exists"""
    wrapper_path = Path(__file__).parent.parent.parent / 'gitsage'
    assert wrapper_path.exists(), "gitsage CLI wrapper not found"


def test_cli_wrapper_commands():
    """Test that CLI wrapper has all commands"""
    wrapper_path = Path(__file__).parent.parent.parent / 'gitsage'
    content = wrapper_path.read_text()

    # Check for all commands
    commands = [
        'launch',
        'check',
        'wiki',
        'readme',  # NEW
        'delete',
        'manage',
        'reset-history',  # NEW
        'migrate'  # NEW
    ]

    for cmd in commands:
        assert cmd in content, f"Command {cmd} not in CLI wrapper"


def test_documentation_exists():
    """Test that all documentation files exist"""
    docs_dir = Path(__file__).parent.parent.parent / 'docs' / 'user-guides'
    assert docs_dir.exists(), "docs/user-guides directory not found"

    # Check for guide files
    guides = [
        'getting-started.md',
        'wiki-gitbook-guide.md',
        'repository-management.md'
    ]

    for guide in guides:
        guide_path = docs_dir / guide
        assert guide_path.exists(), f"Guide {guide} not found"


def test_quick_reference_exists():
    """Test that QUICK-REFERENCE.md exists"""
    ref_path = Path(__file__).parent.parent.parent / 'QUICK-REFERENCE.md'
    assert ref_path.exists(), "QUICK-REFERENCE.md not found"


def test_scripts_organized():
    """Test that scripts are properly organized"""
    project_root = Path(__file__).parent.parent.parent
    scripts_dir = project_root / 'scripts'

    assert scripts_dir.exists(), "scripts directory not found"

    # Check subdirectories
    subdirs = ['bash', 'git-resets']
    for subdir in subdirs:
        subdir_path = scripts_dir / subdir
        assert subdir_path.exists(), f"scripts/{subdir} directory not found"


def test_bash_scripts_exist():
    """Test that essential bash scripts exist"""
    scripts_dir = Path(__file__).parent.parent.parent / 'scripts' / 'bash'

    scripts = [
        'delete-repo.sh',
        'repo-manager.sh'
    ]

    for script in scripts:
        script_path = scripts_dir / script
        assert script_path.exists(), f"Script {script} not found"


def test_git_reset_scripts_exist():
    """Test that git reset scripts exist"""
    scripts_dir = Path(__file__).parent.parent.parent / 'scripts' / 'git-resets'

    scripts = [
        'reset_git_history.sh',
        'migrate_and_swap_repos.sh'
    ]

    for script in scripts:
        script_path = scripts_dir / script
        assert script_path.exists(), f"Script {script} not found"


def test_config_files_referenced():
    """Test that generators reference config files"""
    project_root = Path(__file__).parent.parent.parent

    # README generator should reference readme-config.yaml
    readme_gen = project_root / 'readme-generator.py'
    if readme_gen.exists():
        content = readme_gen.read_text()
        assert 'readme-config.yaml' in content

    # Wiki generators should reference wiki-config.yaml
    wiki_gen = project_root / 'wiki-generator-enhanced.py'
    if wiki_gen.exists():
        content = wiki_gen.read_text()
        assert 'wiki-config.yaml' in content


def test_no_duplicate_functionality():
    """Test that we don't have redundant duplicate files"""
    project_root = Path(__file__).parent.parent.parent

    # Should NOT have these old duplicates
    old_files = [
        'launcher.old.py',
        'DELETE-REPO-README.md'
    ]

    for old_file in old_files:
        old_path = project_root / old_file
        assert not old_path.exists(), f"Old duplicate file {old_file} should be removed"


def test_project_structure():
    """Test overall project structure is clean"""
    project_root = Path(__file__).parent.parent.parent

    # Essential directories should exist
    essential_dirs = ['scripts', 'docs', 'tests', 'assets']

    for dir_name in essential_dirs:
        dir_path = project_root / dir_name
        assert dir_path.exists(), f"Essential directory {dir_name} not found"
