"""Configuration management for GitSage."""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field, asdict


@dataclass
class ProjectConfig:
    """Project metadata configuration."""
    name: str = "GitHub Repository Manager"
    tagline: str = "Safe and powerful GitHub repository management"
    description: str = "A comprehensive toolkit for GitHub repository management"
    version: str = "2.2.0"
    author: str = "GitSage Contributors"
    license: str = "MIT"
    github_url: str = ""
    homepage: str = ""
    keywords: list = field(default_factory=lambda: ["github", "repository", "management"])


@dataclass
class BackupConfig:
    """Backup system configuration."""
    enabled: bool = True
    backup_dir: Path = field(default_factory=lambda: Path.home() / ".gitsage" / "backups")
    max_backups_per_repo: int = 10
    retention_days: int = 30
    compression_level: int = 9
    verify_integrity: bool = True


@dataclass
class GeneratorConfig:
    """Generator settings configuration."""
    output_dir: Path = field(default_factory=lambda: Path("generated-docs"))
    scripts_dir: Path = field(default_factory=lambda: Path("generated-scripts"))
    wikis_dir: Path = field(default_factory=lambda: Path("generated-wikis"))
    templates_dir: Path = field(default_factory=lambda: Path("templates"))
    educational_mode: bool = True


@dataclass
class LoggingConfig:
    """Logging configuration."""
    enabled: bool = True
    log_dir: Path = field(default_factory=lambda: Path.home() / ".gitsage" / "logs")
    level: str = "INFO"
    console_output: bool = True
    file_output: bool = True
    max_log_size_mb: int = 10
    backup_count: int = 5


@dataclass
class SecurityConfig:
    """Security settings."""
    require_confirmations: bool = True
    allow_force_operations: bool = False
    validate_repo_names: bool = True
    backup_before_delete: bool = True


@dataclass
class GitSageConfig:
    """Main GitSage configuration."""
    project: ProjectConfig = field(default_factory=ProjectConfig)
    backup: BackupConfig = field(default_factory=BackupConfig)
    generator: GeneratorConfig = field(default_factory=GeneratorConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)

    @classmethod
    def from_file(cls, config_file: Path) -> 'GitSageConfig':
        """
        Load configuration from YAML file.

        Args:
            config_file: Path to configuration file

        Returns:
            GitSageConfig instance
        """
        if not config_file.exists():
            return cls()

        with open(config_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}

        config = cls()

        # Load project config
        if 'project' in data:
            for key, value in data['project'].items():
                if hasattr(config.project, key):
                    setattr(config.project, key, value)

        # Load backup config
        if 'backup' in data:
            for key, value in data['backup'].items():
                if hasattr(config.backup, key):
                    if key == 'backup_dir':
                        setattr(config.backup, key, Path(value))
                    else:
                        setattr(config.backup, key, value)

        # Load generator config
        if 'generator' in data:
            for key, value in data['generator'].items():
                if hasattr(config.generator, key):
                    if key.endswith('_dir'):
                        setattr(config.generator, key, Path(value))
                    else:
                        setattr(config.generator, key, value)

        # Load logging config
        if 'logging' in data:
            for key, value in data['logging'].items():
                if hasattr(config.logging, key):
                    if key == 'log_dir':
                        setattr(config.logging, key, Path(value))
                    else:
                        setattr(config.logging, key, value)

        # Load security config
        if 'security' in data:
            for key, value in data['security'].items():
                if hasattr(config.security, key):
                    setattr(config.security, key, value)

        return config

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.

        Returns:
            Configuration as dictionary
        """
        def convert_paths(obj: Any) -> Any:
            """Convert Path objects to strings."""
            if isinstance(obj, Path):
                return str(obj)
            elif isinstance(obj, dict):
                return {k: convert_paths(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_paths(item) for item in obj]
            return obj

        return convert_paths({
            'project': asdict(self.project),
            'backup': asdict(self.backup),
            'generator': asdict(self.generator),
            'logging': asdict(self.logging),
            'security': asdict(self.security),
        })

    def save(self, config_file: Path) -> None:
        """
        Save configuration to YAML file.

        Args:
            config_file: Path to save configuration
        """
        config_file.parent.mkdir(parents=True, exist_ok=True)

        with open(config_file, 'w', encoding='utf-8') as f:
            yaml.dump(self.to_dict(), f, default_flow_style=False, sort_keys=False)

    @classmethod
    def load_or_create(cls, config_file: Optional[Path] = None) -> 'GitSageConfig':
        """
        Load configuration from file or create default.

        Args:
            config_file: Path to configuration file (defaults to ~/.gitsage/config.yaml)

        Returns:
            GitSageConfig instance
        """
        if config_file is None:
            config_file = Path.home() / ".gitsage" / "config.yaml"

        if config_file.exists():
            return cls.from_file(config_file)

        # Create default config
        config = cls()
        config.save(config_file)
        return config


class ConfigManager:
    """Manages GitSage configuration across the application."""

    _instance: Optional['ConfigManager'] = None
    _config: Optional[GitSageConfig] = None

    def __new__(cls):
        """Singleton pattern for config manager."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize configuration manager."""
        if self._config is None:
            self.reload()

    def reload(self, config_file: Optional[Path] = None) -> None:
        """
        Reload configuration from file.

        Args:
            config_file: Path to configuration file
        """
        self._config = GitSageConfig.load_or_create(config_file)

    @property
    def config(self) -> GitSageConfig:
        """Get current configuration."""
        if self._config is None:
            self.reload()
        return self._config

    def get_project_config(self) -> ProjectConfig:
        """Get project configuration."""
        return self.config.project

    def get_backup_config(self) -> BackupConfig:
        """Get backup configuration."""
        return self.config.backup

    def get_generator_config(self) -> GeneratorConfig:
        """Get generator configuration."""
        return self.config.generator

    def get_logging_config(self) -> LoggingConfig:
        """Get logging configuration."""
        return self.config.logging

    def get_security_config(self) -> SecurityConfig:
        """Get security configuration."""
        return self.config.security

    def save(self, config_file: Optional[Path] = None) -> None:
        """
        Save configuration to file.

        Args:
            config_file: Path to save configuration (defaults to ~/.gitsage/config.yaml)
        """
        if config_file is None:
            config_file = Path.home() / ".gitsage" / "config.yaml"

        self.config.save(config_file)


# Global config manager instance
config_manager = ConfigManager()


def get_config() -> GitSageConfig:
    """
    Get global GitSage configuration.

    Returns:
        GitSageConfig instance
    """
    return config_manager.config
