@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Electronic Components Image Recognition

echo ==========================================
echo   Electronic Components Recognition - Setup
echo ==========================================
echo.

REM ---- 1. Check Python ----
where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python not found.
    echo Please install Python 3.8 - 3.11: https://www.python.org/downloads/
    echo Remember to check "Add Python to PATH" during installation.
    pause
    exit /b
)

REM ---- 2. Create virtual environment if missing ----
if not exist "venv\Scripts\activate.bat" (
    echo [Step 1/3] Creating virtual environment "venv" ...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b
    )
) else (
    echo [Step 1/3] Virtual environment already exists. Skipping.
)

REM ---- 3. Activate ----
echo [Step 2/3] Activating virtual environment ...
call venv\Scripts\activate.bat

REM ---- 4. Install dependencies ----
echo [Step 3/3] Installing / updating dependencies (first run may take a while) ...
python -m pip install --upgrade pip >nul 2>nul
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Dependency installation failed. Check your internet connection.
    pause
    exit /b
)

echo.
echo ==========================================
echo   Environment ready!
echo ==========================================

:menu
echo.
echo ------------------------------------------
echo   Choose a step (type a number, then Enter):
echo.
echo   [1] Preprocess and convert images  (preprocess_and_rename.py)
echo   [2] Label images with LabelImg     (label_tool.bat)
echo   [3] Build detection dataset        (build_dataset_det.py)
echo   [4] Train model                    (train.py)
echo   [5] Live camera detection          (detect.py)
echo   [0] Exit
echo ------------------------------------------
set "choice="
set /p choice=Your choice:
if not defined choice ( echo No input received. Exiting. & exit /b )

if "%choice%"=="1" ( python preprocess_and_rename.py & goto menu )
if "%choice%"=="2" ( call label_tool.bat & goto menu )
if "%choice%"=="3" ( python build_dataset_det.py & goto menu )
if "%choice%"=="4" ( python train.py & goto menu )
if "%choice%"=="5" ( python detect.py & goto menu )
if "%choice%"=="0" ( exit /b )

echo [Info] Invalid choice, please try again.
goto menu
