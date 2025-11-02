@echo off
chcp 65001 >nul
title Stock Chatbot Project Setup

echo ========================================
echo    Stock Support Chatbot Setup
echo ========================================
echo.

echo Setting up backend...
call backend\setup-backend.bat
if errorlevel 1 (
    echo Backend setup failed!
    pause
    exit /b 1
)

echo.
echo Setting up frontend...
call frontend\setup-frontend.bat
if errorlevel 1 (
    echo Frontend setup failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo    Setup Completed Successfully!
echo ========================================
echo.
echo To start the application, run:
echo   start-app.bat
echo.
pause