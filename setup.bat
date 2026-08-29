@echo off
cd /d "%~dp0"
title Dual-AI Bridge Setup
echo ===================================================
echo   Installing Dual-AI Bridge Requirements
echo ===================================================
pip install -r requirements.txt
playwright install chromium
echo ===================================================
echo   Setup Complete! Launch run.bat to start.
echo ===================================================
pause
