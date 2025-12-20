@echo off
REM Fast Search - One-Click Installer
REM This script sets up Fast Search on your computer

echo ============================================================
echo Fast Search - Installation Wizard
echo ============================================================
echo.
echo This will install Fast Search on your computer.
echo.
echo What you'll get:
echo   - Lightning-fast file search (Ctrl+Space)
echo   - System tray integration
echo   - Auto-start option
echo   - Beautiful dark UI
echo.
echo Requirements:
echo   - Python 3.10 or higher
echo   - Internet connection (for dependencies)
echo.
pause

REM Check if Python is installed
echo.
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Python is not installed!
    echo.
    echo Please install Python 3.10+ from:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANT: Check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)

python --version
echo Python found!

REM Create virtual environment
echo.
echo [2/5] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists, skipping...
) else (
    python -m venv venv
    echo Virtual environment created!
)

REM Upgrade pip
echo.
echo [3/5] Upgrading pip...
venv\Scripts\python.exe -m pip install --upgrade pip --quiet

REM Install dependencies
echo.
echo [4/6] Installing dependencies...
echo This may take a few minutes...
venv\Scripts\python.exe -m pip install -r requirements.txt --quiet
echo Dependencies installed!

REM Create custom icon
echo.
echo [5/6] Creating custom FS icon...
if exist assets\icon.png (
    venv\Scripts\python.exe create_icon.py
    if exist assets\icon.ico (
        echo Custom icon created!
    ) else (
        echo Warning: Icon creation failed, using default icon
    )
) else (
    echo Warning: Icon file not found, using default icon
)

REM Create desktop shortcut
echo.
echo [6/6] Creating desktop shortcut...
set SCRIPT_DIR=%~dp0
set SHORTCUT=%USERPROFILE%\Desktop\Fast Search.lnk
set ICON_PATH=%SCRIPT_DIR%assets\icon.ico

REM Check if custom icon exists, otherwise use default
if not exist "%ICON_PATH%" (
    set ICON_PATH=%SystemRoot%\System32\SHELL32.dll,23
)

echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%SHORTCUT%" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%SCRIPT_DIR%launch-desktop-app.bat" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%SCRIPT_DIR%" >> CreateShortcut.vbs
echo oLink.Description = "Fast Search - Press Ctrl+Space to search" >> CreateShortcut.vbs
echo oLink.IconLocation = "%ICON_PATH%" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs

cscript //nologo CreateShortcut.vbs
del CreateShortcut.vbs

echo Desktop shortcut created with custom FS icon!

REM Success message
echo.
echo ============================================================
echo Installation Complete! 
echo ============================================================
echo.
echo Fast Search is ready to use!
echo.
echo To start:
echo   1. Double-click "Fast Search" on your desktop, OR
echo   2. Run: launch-desktop-app.bat
echo.
echo Then press Ctrl+Space from anywhere to search!
echo.
echo Features:
echo   - Press Ctrl+Space to open search
echo   - Click Settings to manage directories
echo   - Enable auto-start in Settings
echo.
echo Enjoy your lightning-fast search! 
echo ============================================================
echo.
pause
