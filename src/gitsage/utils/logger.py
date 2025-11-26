"""Logging utilities for GitSage."""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


class GitSageLogger:
    """Centralized logging for GitSage operations."""

    DEFAULT_LOG_DIR = Path.home() / ".gitsage" / "logs"
    DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def setup_logger(
        name: str,
        log_file: Optional[Path] = None,
        level: int = logging.INFO,
        console_output: bool = True,
        file_output: bool = True,
    ) -> logging.Logger:
        """
        Set up a logger with file and console handlers.

        Args:
            name: Logger name (typically module name)
            log_file: Path to log file (defaults to ~/.gitsage/logs/{name}.log)
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            console_output: Enable console output
            file_output: Enable file output

        Returns:
            Configured logger instance
        """
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # Remove existing handlers to avoid duplicates
        logger.handlers.clear()

        # Create formatter
        formatter = logging.Formatter(
            GitSageLogger.DEFAULT_FORMAT, datefmt=GitSageLogger.DATE_FORMAT
        )

        # Console handler
        if console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(level)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        # File handler
        if file_output:
            if log_file is None:
                GitSageLogger.DEFAULT_LOG_DIR.mkdir(parents=True, exist_ok=True)
                log_file = GitSageLogger.DEFAULT_LOG_DIR / f"{name}.log"

            # Ensure log directory exists
            log_file.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger

    @staticmethod
    def setup_operation_logger(operation_name: str) -> logging.Logger:
        """
        Set up a logger for a specific operation with timestamped log file.

        Args:
            operation_name: Name of the operation (e.g., 'backup', 'delete')

        Returns:
            Configured logger instance
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = (
            GitSageLogger.DEFAULT_LOG_DIR / operation_name / f"{operation_name}_{timestamp}.log"
        )

        return GitSageLogger.setup_logger(
            name=f"gitsage.{operation_name}",
            log_file=log_file,
            level=logging.DEBUG,
            console_output=False,  # Operation logs go to file only
            file_output=True,
        )

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        Get an existing logger or create a default one.

        Args:
            name: Logger name

        Returns:
            Logger instance
        """
        logger = logging.getLogger(name)

        # If logger has no handlers, set it up with defaults
        if not logger.handlers:
            return GitSageLogger.setup_logger(name)

        return logger


class RichLogger:
    """Logger that integrates with Rich console output."""

    def __init__(self, name: str, use_rich: bool = True):
        """
        Initialize a logger with optional Rich integration.

        Args:
            name: Logger name
            use_rich: Whether to use Rich for console output
        """
        self.name = name
        self.use_rich = use_rich
        self.logger = GitSageLogger.get_logger(name)

        if use_rich:
            try:
                from rich.console import Console

                self.console = Console()
            except ImportError:
                self.use_rich = False
                self.console = None
        else:
            self.console = None

    def debug(self, message: str, **kwargs) -> None:
        """Log debug message."""
        self.logger.debug(message)
        if self.use_rich and self.console:
            self.console.print(f"[dim]{message}[/dim]", **kwargs)

    def info(self, message: str, style: str = "", **kwargs) -> None:
        """Log info message."""
        self.logger.info(message)
        if self.use_rich and self.console:
            self.console.print(message, style=style, **kwargs)
        else:
            print(message)

    def success(self, message: str, **kwargs) -> None:
        """Log success message."""
        self.logger.info(f"SUCCESS: {message}")
        if self.use_rich and self.console:
            self.console.print(f"✓ {message}", style="bold green", **kwargs)
        else:
            print(f"✓ {message}")

    def warning(self, message: str, **kwargs) -> None:
        """Log warning message."""
        self.logger.warning(message)
        if self.use_rich and self.console:
            self.console.print(f"⚠ {message}", style="bold yellow", **kwargs)
        else:
            print(f"⚠ {message}")

    def error(self, message: str, **kwargs) -> None:
        """Log error message."""
        self.logger.error(message)
        if self.use_rich and self.console:
            self.console.print(f"✗ {message}", style="bold red", **kwargs)
        else:
            print(f"✗ {message}")

    def critical(self, message: str, **kwargs) -> None:
        """Log critical message."""
        self.logger.critical(message)
        if self.use_rich and self.console:
            self.console.print(f"🔥 {message}", style="bold red on white", **kwargs)
        else:
            print(f"🔥 {message}")


# Convenience function for quick logger access
def get_logger(name: str, use_rich: bool = True) -> RichLogger:
    """
    Get a RichLogger instance.

    Args:
        name: Logger name
        use_rich: Whether to use Rich for console output

    Returns:
        RichLogger instance
    """
    return RichLogger(name, use_rich=use_rich)
