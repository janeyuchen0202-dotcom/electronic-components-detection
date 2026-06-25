@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Electronic Components Image Recognition

echo ==========================================
echo   Electronic Components Recognition - Setup
echo ==========================================
echo.

REM ---- 1. Find a compatible Python (torch supports 3.10-3.13; prefer verified 3.11) ----
set "PYEXE="
for %%V in (3.11 3.12 3.10 3.13) do if not defined PYEXE (
    py -%%V -c "import sys" >nul 2>nul
    if not errorlevel 1 set "PYEXE=py -%%V"
)
if not defined PYEXE (
    where python >nul 2>nul
    if not errorlevel 1 set "PYEXE=python"
)
if not defined PYEXE (
    echo [ERROR] No suitable Python found.
    echo Please install Python 3.11 ^(recommended^): https://www.python.org/downloads/
    echo Remember to check "Add Python to PATH" during installation.
    pause
    exit /b
)
echo [Info] Using Python: %PYEXE%

REM ---- 2. Create or repair virtual environment ----
REM A venv copied from another PC has hardcoded paths and cannot run; detect and rebuild.
set "VENV_OK="
if exist "venv\Scripts\python.exe" (
    venv\Scripts\python.exe -c "import sys" >nul 2>nul
    if not errorlevel 1 set "VENV_OK=1"
)
if defined VENV_OK (
    echo [Step 1/3] Virtual environment OK. Skipping creation.
) else (
    if exist "venv" (
        echo [Step 1/3] Existing venv is invalid ^(likely copied from another PC^). Rebuilding ...
        rmdir /s /q venv
    ) else (
        echo [Step 1/3] Creating virtual environment "venv" ...
    )
    %PYEXE% -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b
    )
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
