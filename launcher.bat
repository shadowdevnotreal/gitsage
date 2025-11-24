@echo off
REM GitHub Repository Manager Launcher for Windows
REM Detects Python and launches the main launcher

title GitHub Repository Manager

echo.
echo ====================================
echo  GitHub Repository Manager
echo ====================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    echo Alternative: You can also use the PowerShell version:
    echo   scripts\powershell\repo-manager.ps1
    echo.
    pause
    exit /b 1
)

REM Get Python version for display
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [INFO] Python %PYTHON_VERSION% detected

REM Check if launcher exists
if not exist "launcher.py" (
    echo [ERROR] launcher.py not found in current directory
    echo Please make sure you're running this from the repository root directory
    echo.
    pause
    exit /b 1
)

echo [INFO] Starting Repository Manager...
echo.

REM Launch the main launcher
python launcher.py %*

REM Check exit code and pause if there was an error
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Repository Manager exited with an error
    echo Press any key to exit...
    pause >nul
) else (
    echo.
    echo [SUCCESS] Repository Manager completed successfully
    echo Press any key to exit...
    pause >nul
)
