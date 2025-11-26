"""Input validation utilities for GitSage."""

import re
from pathlib import Path
from typing import Optional, Tuple


class ValidationError(Exception):
    """Raised when validation fails."""

    pass


class Validators:
    """Input validation for various GitSage operations."""

    @staticmethod
    def validate_repo_name(name: str) -> bool:
        """
        Validate GitHub repository name format.

        Args:
            name: Repository name in format 'owner/repo'

        Returns:
            bool: True if valid

        Raises:
            ValidationError: If format is invalid
        """
        pattern = r"^[a-zA-Z0-9_-]+/[a-zA-Z0-9_.-]+$"
        if not re.match(pattern, name):
            raise ValidationError(
                f"Invalid repository name format: {name}. " "Expected format: 'owner/repo'"
            )
        return True

    @staticmethod
    def validate_repo_path(path: str) -> Tuple[bool, Optional[str]]:
        """
        Validate that a path is a valid Git repository.

        Args:
            path: Path to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        repo_path = Path(path)

        if not repo_path.exists():
            return False, f"Path does not exist: {path}"

        if not repo_path.is_dir():
            return False, f"Path is not a directory: {path}"

        git_dir = repo_path / ".git"
        if not git_dir.exists():
            return False, f"Not a Git repository (no .git directory): {path}"

        return True, None

    @staticmethod
    def validate_branch_name(branch: str) -> bool:
        """
        Validate Git branch name.

        Args:
            branch: Branch name to validate

        Returns:
            bool: True if valid

        Raises:
            ValidationError: If branch name is invalid
        """
        # Git branch name rules (simplified)
        invalid_patterns = [
            r"\.\.",  # Cannot contain '..'
            r"^\.",  # Cannot start with '.'
            r"/$",  # Cannot end with '/'
            r"//",  # Cannot contain consecutive slashes
            r"[~^:\?\*\[]",  # Cannot contain special characters
            r"\s",  # Cannot contain whitespace
        ]

        for pattern in invalid_patterns:
            if re.search(pattern, branch):
                raise ValidationError(
                    f"Invalid branch name: {branch}. "
                    "Branch names cannot contain: .., leading dots, trailing slashes, "
                    "consecutive slashes, or special characters (~^:?*[])"
                )

        if not branch:
            raise ValidationError("Branch name cannot be empty")

        return True

    @staticmethod
    def validate_version(version: str) -> bool:
        """
        Validate semantic version format.

        Args:
            version: Version string to validate (e.g., '1.0.0')

        Returns:
            bool: True if valid

        Raises:
            ValidationError: If version format is invalid
        """
        pattern = r"^\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?(\+[a-zA-Z0-9.-]+)?$"
        if not re.match(pattern, version):
            raise ValidationError(
                f"Invalid semantic version: {version}. "
                "Expected format: MAJOR.MINOR.PATCH (e.g., 1.0.0)"
            )
        return True

    @staticmethod
    def validate_url(url: str) -> bool:
        """
        Validate URL format.

        Args:
            url: URL to validate

        Returns:
            bool: True if valid

        Raises:
            ValidationError: If URL format is invalid
        """
        pattern = r"^https?://[^\s/$.?#].[^\s]*$"
        if not re.match(pattern, url):
            raise ValidationError(f"Invalid URL format: {url}")
        return True

    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email address format.

        Args:
            email: Email to validate

        Returns:
            bool: True if valid

        Raises:
            ValidationError: If email format is invalid
        """
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, email):
            raise ValidationError(f"Invalid email format: {email}")
        return True

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize a filename by removing/replacing invalid characters.

        Args:
            filename: Filename to sanitize

        Returns:
            str: Sanitized filename
        """
        # Remove invalid characters for filenames
        invalid_chars = r'[<>:"/\\|?*\x00-\x1f]'
        sanitized = re.sub(invalid_chars, "_", filename)

        # Remove leading/trailing dots and spaces
        sanitized = sanitized.strip(". ")

        # Ensure it's not empty
        if not sanitized:
            sanitized = "unnamed"

        return sanitized

    @staticmethod
    def validate_file_path(path: str, must_exist: bool = False) -> Tuple[bool, Optional[str]]:
        """
        Validate a file path.

        Args:
            path: Path to validate
            must_exist: If True, path must already exist

        Returns:
            Tuple of (is_valid, error_message)
        """
        file_path = Path(path)

        if must_exist and not file_path.exists():
            return False, f"File does not exist: {path}"

        if must_exist and not file_path.is_file():
            return False, f"Path is not a file: {path}"

        # Check if parent directory exists (for new files)
        if not must_exist and not file_path.parent.exists():
            return False, f"Parent directory does not exist: {file_path.parent}"

        return True, None
