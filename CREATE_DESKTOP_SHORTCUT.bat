@echo off
REM Create Desktop Shortcut for Fast Search
echo ========================================
echo   Fast Search - Desktop Shortcut Creator
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python first.
    pause
    exit /b 1
)

echo Creating desktop shortcut...
echo.

REM Run the shortcut creation script
python create_desktop_shortcut.py

echo.
echo ========================================
pause
