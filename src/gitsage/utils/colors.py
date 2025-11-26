"""ANSI color codes for cross-platform terminal output."""

import os
import platform
from typing import ClassVar


class Colors:
    """ANSI color codes for cross-platform terminal colors."""

    RED: ClassVar[str] = "\033[91m"
    GREEN: ClassVar[str] = "\033[92m"
    YELLOW: ClassVar[str] = "\033[93m"
    BLUE: ClassVar[str] = "\033[94m"
    MAGENTA: ClassVar[str] = "\033[95m"
    CYAN: ClassVar[str] = "\033[96m"
    WHITE: ClassVar[str] = "\033[97m"
    BOLD: ClassVar[str] = "\033[1m"
    UNDERLINE: ClassVar[str] = "\033[4m"
    END: ClassVar[str] = "\033[0m"
    QUESTION: ClassVar[str] = "\033[96m"
    QUESTION_MAGENTA: ClassVar[str] = "\033[95m"
    QUESTION_YELLOW: ClassVar[str] = "\033[93m"
    QUESTION_BLUE: ClassVar[str] = "\033[94m"

    @classmethod
    def disable_on_windows(cls) -> None:
        """Disable colors on older Windows terminals."""
        if platform.system() == "Windows" and not os.environ.get("TERM"):
            for attr in dir(cls):
                if not attr.startswith("_") and attr != "disable_on_windows":
                    setattr(cls, attr, "")

    @classmethod
    def initialize(cls) -> None:
        """Initialize colors for the current platform."""
        if platform.system() == "Windows":
            try:
                os.system("color")
            except Exception:
                cls.disable_on_windows()


# Auto-initialize on import
Colors.initialize()
