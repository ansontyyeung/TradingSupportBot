@echo off
chcp 65001 >nul
title Frontend Server - Stock Chatbot

echo Starting Frontend Development Server...
echo.

:: Check if node_modules exists
if not exist "node_modules" (
    echo Node modules not found. Running npm install...
    npm install
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        echo Please run setup-frontend.bat first
        pause
        exit /b 1
    )
)

echo.
echo Starting Vite development server on http://localhost:3000
echo Press Ctrl+C to stop the server
echo.

npm run dev

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start frontend server
    echo Make sure Node.js is installed and dependencies are set up
    echo Run setup-frontend.bat first if you haven't
    pause
)