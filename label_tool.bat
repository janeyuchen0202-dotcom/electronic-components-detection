@echo off
chcp 65001 >nul
title LabelImg - Bounding Box Annotation

echo ==========================================
echo   LabelImg annotation tool
echo ------------------------------------------
echo   1. Click "Open Dir" and pick a class
echo      folder under dataset_images.
echo   2. Make sure the format button on the
echo      left toolbar shows "YOLO".
echo   3. Press W to draw a box, choose the
echo      class, then Ctrl+S to save, D for next.
echo ==========================================
echo.

"C:\pyenvs\labeltool\Scripts\labelImg.exe" "%~dp0dataset_images" "%~dp0classes_predefined.txt"
