# Windows Compatibility - Quick Fix Guide

## Overview
8 issues found across 4 files. Most are simple one-line fixes to wrap with platform checks.

## Quick Fix Checklist

### 1. File Permissions Issues (4 occurrences)
Add platform checks before chmod calls:

**Files affected:**
- script-generator.py (line 1239)
- wiki-generator.py (lines 449, 481)
- wiki-generator-enhanced.py (lines 773, 811)

**Quick Fix Template:**
```python
# Before:
os.chmod(filepath, 0o755)

# After:
import sys
if sys.platform != 'win32':
    os.chmod(filepath, 0o755)
```

### 2. Tilde Path Issues (2 occurrences)
Replace hardcoded tilde with Path.home():

**Files affected:**
- script-generator.py (lines 403, 1292)

**Quick Fix Template:**
```python
# Before:
default_backup_dir = '~/github-backups'

# After:
from pathlib import Path
default_backup_dir = str(Path.home() / 'github-backups')
```

### 3. Bash Subprocess Issue (1 occurrence)
Add bash availability check:

**File affected:**
- launcher.py (line 379)

**Quick Fix Template:**
```python
# Before:
elif script_type == "bash":
    subprocess.run(["bash", script_path])

# After:
import shutil
elif script_type == "bash":
    if shutil.which("bash") is None:
        self.print_status(
            "Bash not in PATH. Install Git Bash or use PowerShell.",
            "ERROR"
        )
        return
    subprocess.run(["bash", script_path], check=True)
```

### 4. os.system() Issue (2 occurrences - lower priority)
Replace with subprocess.run():

**Files affected:**
- launcher.py (line 48)
- uninstall.py (line 232)

**Quick Fix Template:**
```python
# Before:
os.system('color')

# After:
import subprocess
try:
    subprocess.run(["cmd", "/c", "color"], capture_output=True, check=False)
except Exception:
    pass
```

## Implementation Priority

### Phase 1 (Critical - Breaks functionality):
1. Fix os.chmod() in all 4 files
2. Fix tilde paths in script-generator.py
3. Add bash check in launcher.py

### Phase 2 (Important - Improves reliability):
1. Replace os.system() calls
2. Add comprehensive error handling
3. Add Windows-specific path tests

### Phase 3 (Nice to have):
1. Generate PowerShell script alternatives
2. Create Windows-specific installer
3. Add Windows compatibility tests

## Testing After Fixes

```bash
# Test on Windows
python launcher.py
python script-generator.py
python wiki-generator.py
python wiki-generator-enhanced.py
python backup-manager.py
```

Expected results:
- No os.chmod() errors
- Proper path expansion on all platforms
- Clear error message if bash is missing
- All scripts run without platform-specific failures

## Estimated Effort
- Phase 1: 15-20 minutes
- Phase 2: 30-45 minutes  
- Phase 3: 2-3 hours

## Validation Checklist
- [ ] All chmod calls wrapped with platform check
- [ ] All tilde paths replaced with Path.home()
- [ ] Bash subprocess checks added
- [ ] os.system() replaced with subprocess
- [ ] Tested on Windows (cmd.exe and PowerShell)
- [ ] Tested on Linux/macOS
- [ ] No new warnings in Python syntax check
- [ ] All tests pass
