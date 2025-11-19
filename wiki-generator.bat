@echo off
REM Wiki Generator Launcher for Windows

title GitHub Repository Manager - Wiki Generator

echo.
echo ====================================
echo  Wiki Generator System
echo ====================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python from: https://python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Check if PyYAML is installed
python -c "import yaml" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [INFO] Installing required dependencies...
    pip install PyYAML
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to install dependencies
        echo Please run: pip install PyYAML
        pause
        exit /b 1
    )
)

echo [INFO] Generating documentation...
echo.

REM Run the wiki generator
python wiki-generator.py --all

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [SUCCESS] Documentation generated successfully!
    echo.
    echo Generated files:
    echo   - Wiki: ./generated-docs/wiki/
    echo   - Deployment scripts: ./generated-docs/deployment/
    echo.
    echo Next steps:
    echo   1. Review generated content in ./generated-docs/
    echo   2. Deploy to GitHub: ./generated-docs/deployment/setup-docs.sh YOUR_REPO_URL
    echo.
) else (
    echo [ERROR] Documentation generation failed
)

pause
