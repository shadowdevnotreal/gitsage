#!/usr/bin/env python3
"""
Native OS file/folder picker dialogs
Uses native dialogs on Windows, macOS, and Linux - NO tkinter needed
"""

import subprocess
import platform
from pathlib import Path
from typing import Optional


def _windows_folder_picker(title: str = "Select folder", start_dir: Optional[Path] = None) -> Optional[Path]:
    """Windows native folder picker using PowerShell"""
    if start_dir is None:
        start_dir = Path.home()

    # PowerShell command to show folder browser dialog
    ps_command = f"""
    Add-Type -AssemblyName System.Windows.Forms
    $FolderBrowser = New-Object System.Windows.Forms.FolderBrowserDialog
    $FolderBrowser.Description = '{title}'
    $FolderBrowser.SelectedPath = '{start_dir}'
    $FolderBrowser.ShowNewFolderButton = $false
    $result = $FolderBrowser.ShowDialog()
    if ($result -eq [System.Windows.Forms.DialogResult]::OK) {{
        Write-Output $FolderBrowser.SelectedPath
    }}
    """

    try:
        result = subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        if result.returncode == 0 and result.stdout.strip():
            return Path(result.stdout.strip())
        return None
    except Exception:
        return None


def _macos_folder_picker(title: str = "Select folder", start_dir: Optional[Path] = None) -> Optional[Path]:
    """macOS native folder picker using osascript (AppleScript)"""
    if start_dir is None:
        start_dir = Path.home()

    # AppleScript to show folder chooser
    applescript = f'''
    tell application "System Events"
        activate
        set folderPath to choose folder with prompt "{title}" default location "{start_dir}"
        return POSIX path of folderPath
    end tell
    '''

    try:
        result = subprocess.run(
            ["osascript", "-e", applescript],
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode == 0 and result.stdout.strip():
            # Remove trailing newline and slash
            path = result.stdout.strip().rstrip('/')
            return Path(path)
        return None
    except Exception:
        return None


def _linux_folder_picker(title: str = "Select folder", start_dir: Optional[Path] = None) -> Optional[Path]:
    """Linux native folder picker using zenity or kdialog"""
    if start_dir is None:
        start_dir = Path.home()

    # Try zenity first (works on GNOME, XFCE, etc.)
    try:
        result = subprocess.run(
            ["zenity", "--file-selection", "--directory",
             "--title", title, "--filename", f"{start_dir}/"],
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode == 0 and result.stdout.strip():
            return Path(result.stdout.strip())
    except FileNotFoundError:
        pass  # zenity not installed, try kdialog

    # Try kdialog (works on KDE)
    try:
        result = subprocess.run(
            ["kdialog", "--getexistingdirectory", str(start_dir),
             "--title", title],
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode == 0 and result.stdout.strip():
            return Path(result.stdout.strip())
    except FileNotFoundError:
        pass  # kdialog not installed

    # Try yad (yet another dialog - lightweight alternative)
    try:
        result = subprocess.run(
            ["yad", "--file-selection", "--directory",
             "--title", title, "--filename", f"{start_dir}/"],
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode == 0 and result.stdout.strip():
            return Path(result.stdout.strip())
    except FileNotFoundError:
        pass

    return None


def browse_for_folder(title: str = "Select folder", start_dir: Optional[Path] = None) -> Optional[Path]:
    """
    Open native OS folder picker dialog

    Works on:
    - Windows: PowerShell FolderBrowserDialog
    - macOS: AppleScript choose folder
    - Linux: zenity/kdialog/yad

    Args:
        title: Dialog window title
        start_dir: Starting directory (defaults to home)

    Returns:
        Selected folder path or None if cancelled
    """
    system = platform.system()

    if system == "Windows":
        return _windows_folder_picker(title, start_dir)
    elif system == "Darwin":  # macOS
        return _macos_folder_picker(title, start_dir)
    elif system == "Linux":
        return _linux_folder_picker(title, start_dir)
    else:
        # Fallback: just return None
        print(f"⚠️  Native file picker not available on {system}")
        return None


def browse_for_file(title: str = "Select file", start_dir: Optional[Path] = None, file_types: str = "*") -> Optional[Path]:
    """
    Open native OS file picker dialog

    Args:
        title: Dialog window title
        start_dir: Starting directory (defaults to home)
        file_types: File filter (e.g., "*.py", "*.txt", "*" for all)

    Returns:
        Selected file path or None if cancelled
    """
    system = platform.system()

    if start_dir is None:
        start_dir = Path.home()

    if system == "Windows":
        # PowerShell file picker
        ps_command = f"""
        Add-Type -AssemblyName System.Windows.Forms
        $FileBrowser = New-Object System.Windows.Forms.OpenFileDialog
        $FileBrowser.Title = '{title}'
        $FileBrowser.InitialDirectory = '{start_dir}'
        $FileBrowser.Filter = 'All files (*.*)|*.*'
        $result = $FileBrowser.ShowDialog()
        if ($result -eq [System.Windows.Forms.DialogResult]::OK) {{
            Write-Output $FileBrowser.FileName
        }}
        """
        try:
            result = subprocess.run(
                ["powershell", "-Command", ps_command],
                capture_output=True,
                text=True,
                timeout=300
            )
            if result.returncode == 0 and result.stdout.strip():
                return Path(result.stdout.strip())
        except Exception:
            pass

    elif system == "Darwin":  # macOS
        applescript = f'''
        tell application "System Events"
            activate
            set filePath to choose file with prompt "{title}" default location "{start_dir}"
            return POSIX path of filePath
        end tell
        '''
        try:
            result = subprocess.run(
                ["osascript", "-e", applescript],
                capture_output=True,
                text=True,
                timeout=300
            )
            if result.returncode == 0 and result.stdout.strip():
                return Path(result.stdout.strip().rstrip('/'))
        except Exception:
            pass

    elif system == "Linux":
        # Try zenity
        try:
            result = subprocess.run(
                ["zenity", "--file-selection", "--title", title,
                 "--filename", f"{start_dir}/"],
                capture_output=True,
                text=True,
                timeout=300
            )
            if result.returncode == 0 and result.stdout.strip():
                return Path(result.stdout.strip())
        except FileNotFoundError:
            pass

        # Try kdialog
        try:
            result = subprocess.run(
                ["kdialog", "--getopenfilename", str(start_dir),
                 file_types, "--title", title],
                capture_output=True,
                text=True,
                timeout=300
            )
            if result.returncode == 0 and result.stdout.strip():
                return Path(result.stdout.strip())
        except FileNotFoundError:
            pass

    return None


def get_project_folder(prompt: str = "Select your project folder") -> Optional[Path]:
    """
    Open native OS folder picker dialog

    Opens actual native file picker window:
    - Windows: Standard Windows folder browser
    - macOS: Native macOS folder chooser
    - Linux: zenity/kdialog/yad dialog

    Args:
        prompt: Message to display as dialog title

    Returns:
        Selected folder path or None if cancelled
    """
    print(f"\n{prompt}")
    print("Opening folder picker dialog...")

    folder = browse_for_folder(title=prompt, start_dir=Path.home())

    if folder:
        print(f"✅ Selected: {folder}")
    else:
        print("❌ Cancelled")

    return folder


# Example usage and testing
if __name__ == "__main__":
    print("Testing native OS folder picker...")
    print(f"Platform: {platform.system()}")
    print()

    folder = get_project_folder("Select your project folder")

    if folder:
        print(f"\n✅ Selected folder: {folder}")
        print(f"   Exists: {folder.exists()}")
        print(f"   Is directory: {folder.is_dir()}")
    else:
        print("\n❌ No folder selected")
