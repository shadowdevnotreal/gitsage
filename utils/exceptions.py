"""Custom exceptions for GitSage."""


class GitSageError(Exception):
    """Base exception for all GitSage errors."""
    pass


class RepositoryError(GitSageError):
    """Base exception for repository-related errors."""
    pass


class RepositoryNotFoundError(RepositoryError):
    """Repository not found or invalid."""
    pass


class RepositoryNotGitError(RepositoryError):
    """Directory is not a Git repository."""
    pass


class RemoteRepositoryError(RepositoryError):
    """Error accessing remote repository."""
    pass


class BackupError(GitSageError):
    """Error during backup operations."""
    pass


class BackupCreationError(BackupError):
    """Failed to create backup."""
    pass


class BackupRestoreError(BackupError):
    """Failed to restore backup."""
    pass


class BackupNotFoundError(BackupError):
    """Backup not found."""
    pass


class BackupIntegrityError(BackupError):
    """Backup integrity check failed."""
    pass


class ConfigurationError(GitSageError):
    """Error in configuration."""
    pass


class InvalidConfigError(ConfigurationError):
    """Configuration is invalid or malformed."""
    pass


class MissingConfigError(ConfigurationError):
    """Required configuration is missing."""
    pass


class ValidationError(GitSageError):
    """Input validation failed."""
    pass


class InvalidRepositoryNameError(ValidationError):
    """Repository name format is invalid."""
    pass


class InvalidBranchNameError(ValidationError):
    """Branch name is invalid."""
    pass


class InvalidVersionError(ValidationError):
    """Version format is invalid."""
    pass


class EnvironmentError(GitSageError):
    """Error with system environment."""
    pass


class GitNotInstalledError(EnvironmentError):
    """Git is not installed."""
    pass


class GitHubCLINotInstalledError(EnvironmentError):
    """GitHub CLI is not installed."""
    pass


class GitHubNotAuthenticatedError(EnvironmentError):
    """GitHub CLI is not authenticated."""
    pass


class GeneratorError(GitSageError):
    """Error during generation operations."""
    pass


class WikiGenerationError(GeneratorError):
    """Failed to generate wiki."""
    pass


class ReadmeGenerationError(GeneratorError):
    """Failed to generate README."""
    pass


class ScriptGenerationError(GeneratorError):
    """Failed to generate script."""
    pass


class OperationCancelledError(GitSageError):
    """User cancelled the operation."""
    pass


class PermissionError(GitSageError):
    """Permission denied for operation."""
    pass


class NetworkError(GitSageError):
    """Network-related error."""
    pass


class GitHubAPIError(NetworkError):
    """GitHub API error."""
    pass
