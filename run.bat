@echo off
setlocal EnableExtensions EnableDelayedExpansion
title Dual-AI Bridge Control Center
cd /d "%~dp0"

:MENU
cls
echo.
echo  ======================================================================
echo     🧠 D U A L - A I   B R I D G E   (Gemini Antigravity x ChatGPT)
echo  ======================================================================
echo.
echo     [1] ⚡  1-Click Install Dependencies (Playwright)
echo     [2] 🚀  Start Bridge Watcher Daemon
echo     [3] 🧪  Run Test Query (Verify Verbatim Output)
echo     [4] 🔮  Run Deep Thinking Query (/gptdeep)
echo     [5] 📖  Open Documentation (README.md)
echo     [0] ❌  Exit
echo.
echo  ======================================================================
set /p choice="  Enter choice [0-5]: "

if "%choice%"=="1" goto SETUP
if "%choice%"=="2" goto WATCHER
if "%choice%"=="3" goto TEST
if "%choice%"=="4" goto DEEP
if "%choice%"=="5" goto DOCS
if "%choice%"=="0" exit /b
goto MENU

:SETUP
echo [*] Installing requirements...
pip install -r requirements.txt
playwright install chromium
pause
goto MENU

:WATCHER
echo [*] Starting Dual-AI Bridge Watcher...
python -u dualai/watcher.py
pause
goto MENU

:TEST
echo [*] Running standard query test...
python -c "from dualai.client import DualAIClient; c = DualAIClient(); ok, res = c.query('Hello ChatGPT, confirm Dual-AI Bridge is online.'); print(res)"
pause
goto MENU

:DEEP
echo [*] Running Deep Thinking query test...
python -c "from dualai.client import DualAIClient; c = DualAIClient(); ok, res = c.query('Provide a 2-sentence summary of algorithmic complexity.', deep_mode=True); print(res)"
pause
goto MENU

:DOCS
start notepad README.md
goto MENU
