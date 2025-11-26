@echo off
REM GitSage - Windows CLI Wrapper
REM Makes GitSage tools easier to use on Windows

setlocal enabledelayedexpansion

REM Get script directory
set "SCRIPT_DIR=%~dp0"

REM Colors not fully supported in CMD, but we can try
REM Using simple text markers instead

REM Check if Python is available
where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    set PYTHON=python
) else (
    where python3 >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        set PYTHON=python3
    ) else (
        echo [ERROR] Python not found. Please install Python 3.8+
        exit /b 1
    )
)

REM Check if Git Bash is available (for bash scripts)
where bash >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Git Bash not found. Some features require Git Bash.
    echo [INFO] Install Git for Windows: https://git-scm.com/download/win
)

REM Handle commands
if "%1"=="" goto :help
if "%1"=="help" goto :help
if "%1"=="--help" goto :help
if "%1"=="-h" goto :help
if "%1"=="version" goto :version
if "%1"=="--version" goto :version
if "%1"=="-v" goto :version
if "%1"=="launch" goto :launch
if "%1"=="menu" goto :launch
if "%1"=="start" goto :launch
if "%1"=="check" goto :check
if "%1"=="verify" goto :check
if "%1"=="test" goto :check
if "%1"=="wiki" goto :wiki
if "%1"=="doc" goto :wiki
if "%1"=="docs" goto :wiki
if "%1"=="gitbook" goto :wiki
if "%1"=="delete" goto :delete
if "%1"=="remove" goto :delete
if "%1"=="rm" goto :delete
if "%1"=="manage" goto :manage
if "%1"=="manager" goto :manage
if "%1"=="repo" goto :manage

echo [ERROR] Unknown command: %1
echo Run 'gitsage help' for usage information
exit /b 1

:help
echo GitSage - Ultimate GitHub Management Tool
echo Version: 1.0.0
echo.
echo USAGE:
echo     gitsage ^<command^> [options]
echo.
echo COMMANDS:
echo     launch              Launch interactive menu
echo     check               Check installation and prerequisites
echo     wiki                Generate wiki documentation
echo     delete              Safe repository deletion (requires Git Bash)
echo     manage              Advanced repository management (requires Git Bash)
echo     help                Show this help message
echo     version             Show version information
echo.
echo EXAMPLES:
echo     gitsage launch                  # Interactive menu (easiest)
echo     gitsage wiki                    # Generate wiki
echo     gitsage delete                  # Safely delete repository
echo     gitsage check                   # Verify installation
echo.
echo WINDOWS NOTES:
echo     - Install Git for Windows for Bash script support
echo     - Use Git Bash for delete/manage commands
echo     - Python commands work in CMD/PowerShell
echo.
echo DOCUMENTATION:
echo     README.md                       # Project overview
echo     QUICK-REFERENCE.md              # Quick command reference
echo     docs\user-guides\               # Comprehensive guides
echo.
echo Website: https://github.com/shadowdevnotreal/gitsage
goto :eof

:version
echo GitSage v2.2.0.0
echo Ultimate GitHub Management Tool
echo.
echo Platform: Windows
%PYTHON% --version 2>nul || echo Python: Not found
git --version 2>nul || echo Git: Not found
gh --version 2>nul | findstr /C:"gh version" || echo GitHub CLI: Not found
goto :eof

:launch
echo [INFO] Launching GitSage interactive menu...
%PYTHON% "%SCRIPT_DIR%launcher.py" %*
goto :eof

:check
echo [INFO] Checking installation...
%PYTHON% "%SCRIPT_DIR%check_installation.py" %*
goto :eof

:wiki
echo [INFO] Generating wiki documentation...
if not exist "%SCRIPT_DIR%wiki-config.yaml" (
    echo [WARNING] wiki-config.yaml not found. Using defaults.
    echo [INFO] Create wiki-config.yaml to customize output.
)
%PYTHON% "%SCRIPT_DIR%wiki-generator-enhanced.py" %*
goto :eof

:delete
echo [WARNING] Repository deletion requires Git Bash
echo [INFO] Opening Git Bash to run deletion script...
echo.
where bash >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    bash "%SCRIPT_DIR%scripts/bash/delete-repo.sh" %*
) else (
    echo [ERROR] Git Bash not found.
    echo [INFO] Install Git for Windows: https://git-scm.com/download/win
    echo [INFO] Then use Git Bash to run: bash scripts/bash/delete-repo.sh
    exit /b 1
)
goto :eof

:manage
echo [INFO] Repository management requires Git Bash
where bash >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    bash "%SCRIPT_DIR%scripts/bash/repo-manager.sh" %*
) else (
    echo [ERROR] Git Bash not found.
    echo [INFO] Install Git for Windows: https://git-scm.com/download/win
    echo [INFO] Then use Git Bash to run: bash scripts/bash/repo-manager.sh
    exit /b 1
)
goto :eof
