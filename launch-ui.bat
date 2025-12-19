@echo off
REM Fast Search - Desktop UI Launcher
echo Starting Fast Search Desktop UI...
echo.
echo Opening browser at http://127.0.0.1:5000
echo Press Ctrl+C to stop the server
echo.

cd desktop-ui
start http://127.0.0.1:5000
..\venv\Scripts\python.exe app.py
