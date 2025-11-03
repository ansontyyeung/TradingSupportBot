@echo off
chcp 65001 >nul
title Backend Setup

echo Setting up Python backend environment...
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    exit /b 1
)

:: Check if virtual environment exists
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        exit /b 1
    )
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing Python dependencies...
pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    exit /b 1
)

echo.
echo Installing PyTorch with CPU support (for Windows)...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

echo.
echo Creating backend environment file...
if not exist ".env" (
    (
        echo DATABASE_URL=sqlite:///./stock_trades.db
        echo SECRET_KEY=your_secret_key_for_production
        echo DEBUG=True
        echo PORT=8000
        echo ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
        echo MODEL_NAME=microsoft/DialoGPT-small
        echo SENTENCE_MODEL=all-MiniLM-L6-v2
    ) > .env
    echo Created .env file with Hugging Face model configuration.
)

echo.
echo Backend setup completed successfully!
echo Note: First run will download AI models (may take a few minutes)
echo.