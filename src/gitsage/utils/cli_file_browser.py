#!/usr/bin/env python3
"""
Simple text-based file browser for CLI
No tkinter needed - works in terminal
"""

from pathlib import Path
from typing import List, Optional


def list_folders(directory: Path, show_hidden: bool = False) -> List[Path]:
    """List all folders in directory"""
    folders = []
    try:
        for item in sorted(directory.iterdir()):
            if item.is_dir():
                if show_hidden or not item.name.startswith('.'):
                    folders.append(item)
    except PermissionError:
        pass
    return folders


def browse_for_folder(start_dir: Optional[Path] = None) -> Optional[Path]:
    """
    Text-based folder browser for CLI

    Args:
        start_dir: Starting directory (defaults to home)

    Returns:
        Selected folder path or None if cancelled
    """
    if start_dir is None:
        current = Path.home()
    else:
        current = Path(start_dir)

    while True:
        print(f"\n📁 Current location: {current}")
        print("─" * 60)

        folders = list_folders(current)

        # Show parent directory option
        if current != current.parent:
            print("  0. ⬆️  .. (Go up)")

        # Show folders
        for i, folder in enumerate(folders[:20], 1):  # Limit to 20 for readability
            print(f"  {i}. 📂 {folder.name}")

        if len(folders) > 20:
            print(f"  ... and {len(folders) - 20} more")

        print()
        print("─" * 60)
        print("Commands:")
        print("  • Enter number to navigate")
        print("  • Type 's' to select current folder")
        print("  • Type 'q' to cancel")
        print("  • Type path directly (e.g., /home/user/project)")
        print()

        choice = input("Choice: ").strip()

        # Quit
        if choice.lower() == 'q':
            return None

        # Select current folder
        if choice.lower() == 's':
            return current

        # Direct path entry
        if '/' in choice or '\\' in choice:
            path = Path(choice).expanduser()
            if path.exists() and path.is_dir():
                return path
            else:
                print(f"❌ Invalid path: {choice}")
                continue

        # Navigate by number
        try:
            num = int(choice)

            # Go up
            if num == 0 and current != current.parent:
                current = current.parent
                continue

            # Navigate into folder
            if 1 <= num <= len(folders):
                current = folders[num - 1]
                continue
            else:
                print(f"❌ Invalid choice: {num}")
        except ValueError:
            print(f"❌ Invalid input: {choice}")


def quick_folder_select() -> Optional[Path]:
    """
    Quick folder selection with common locations

    Returns:
        Selected folder path or None
    """
    print("\n📁 Select Project Folder")
    print("─" * 60)

    # Scan common locations
    common_dirs = [
        ("Desktop", Path.home() / "Desktop"),
        ("Documents", Path.home() / "Documents"),
        ("Downloads", Path.home() / "Downloads"),
        ("Projects", Path.home() / "Projects"),
        ("Code", Path.home() / "Code"),
        ("Current directory", Path.cwd()),
    ]

    print("\nQuick access:")
    for i, (name, path) in enumerate(common_dirs, 1):
        if path.exists():
            print(f"  {i}. 📂 {name} ({path})")

    print(f"\n  {len(common_dirs) + 1}. 🔍 Browse for folder")
    print("  0. ❌ Cancel")
    print()

    choice = input("Choice: ").strip()

    if choice == '0':
        return None

    try:
        num = int(choice)

        if num == len(common_dirs) + 1:
            # Browse
            return browse_for_folder()

        if 1 <= num <= len(common_dirs):
            path = common_dirs[num - 1][1]
            if path.exists():
                return path
            else:
                print(f"❌ Path does not exist: {path}")
                return None
    except ValueError:
        print(f"❌ Invalid input: {choice}")
        return None


def get_project_folder(prompt: str = "Select your project folder") -> Optional[Path]:
    """
    Main entry point for folder selection

    Simple interface that works for novices and pros:
    - Shows common locations first
    - Allows browsing
    - Allows direct path entry

    Args:
        prompt: Message to display

    Returns:
        Selected folder path or None if cancelled
    """
    print(f"\n{prompt}")
    return quick_folder_select()


# Example usage:
if __name__ == "__main__":
    folder = get_project_folder()

    if folder:
        print(f"\n✅ Selected: {folder}")
    else:
        print("\n❌ Cancelled")
