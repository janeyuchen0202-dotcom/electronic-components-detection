@echo off
chcp 65001 >nul
cd /d "%~dp0"

if not exist "venv\Scripts\activate.bat" (
    echo [Error] Virtual environment not found! Please run setup_env.bat first.
    pause
    exit /b
)

echo ==========================================
echo  Starting Virtual Environment...
echo  You can now run commands like:
echo  python detect.py
echo ==========================================

cmd /k "venv\Scripts\activate.bat"
