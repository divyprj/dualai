@echo off
setlocal EnableExtensions EnableDelayedExpansion
title Dual-AI CLI
cd /d "%~dp0"
set "ROOT=%~dp0"
set "PYTHON=%ROOT%.venv\Scripts\python.exe"

if not exist "%PYTHON%" (
    if "%1"=="" (
        echo [INFO] Initializing virtual environment in .venv...
        python -m venv .venv
        "%PYTHON%" dualai\cli.py setup
    ) else if "%1"=="setup" (
        python -m venv .venv
        "%PYTHON%" dualai\cli.py setup
        exit /b 0
    ) else (
        echo [ERROR] Virtual environment not found. Please run 'dualai setup' first.
        exit /b 1
    )
)

if "%1"=="" (
    "%PYTHON%" dualai\cli.py --help
) else (
    "%PYTHON%" dualai\cli.py %*
)
