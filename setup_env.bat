@echo off
chcp 65001 >nul
echo ==========================================
echo  Setting up Python Virtual Environment...
echo ==========================================

cd /d "%~dp0"

if exist "venv\Scripts\activate.bat" (
    echo [Info] Virtual environment already exists. Skipping creation.
) else (
    echo [Step 1/3] Creating Python virtual environment (venv)...
    python -m venv venv
    if errorlevel 1 (
        echo [Error] Failed to create virtual environment. Is Python installed?
        pause
        exit /b
    )
)

echo.
echo [Step 2/3] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [Step 3/3] Installing dependencies from requirements.txt...
pip install -r requirements.txt

echo.
echo ==========================================
echo  DONE! Environment setup is complete.
echo  Please run "start_env.bat" to start.
echo ==========================================
pause
