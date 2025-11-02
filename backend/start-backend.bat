@echo off
chcp 65001 >nul
title Backend Server - Stock Chatbot

echo Starting Backend Server...
echo.

:: Activate virtual environment
call venv\Scripts\activate.bat

echo Checking dependencies...
pip install -r C:\Homeware\Hackathon\backend\requirement.txt

echo.
echo ========================================
echo    Stock Chatbot with Hugging Face AI
echo ========================================
echo.
echo Loading AI models (first time may take a few minutes)...
echo Backend will start automatically when models are ready...
echo.
echo Starting FastAPI server on http://localhost:8000
echo Press Ctrl+C to stop the server
echo.

python C:\Homeware\Hackathon\backend\app.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start backend server
    echo Make sure the virtual environment is set up correctly
    echo Run setup-backend.bat first if you haven't
    pause
)