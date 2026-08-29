@echo off
cd /d "%~dp0"
title Dual-AI Bridge Watcher Daemon
echo ===================================================
echo   Starting Dual-AI Bridge Daemon (Gemini x ChatGPT)
echo ===================================================
python -u dualai/watcher.py
pause
