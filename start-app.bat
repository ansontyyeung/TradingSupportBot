@echo off
chcp 65001 >nul
title Stock Chatbot Application

echo ========================================
echo    Starting Stock Support Chatbot
echo ========================================
echo.
echo Starting backend and frontend servers...
echo.

echo [1/2] Starting Backend Server on http://localhost:8000
start "Backend Server" cmd /k "backend\start-backend.bat"

timeout /t 3 /nobreak >nul

echo [2/2] Starting Frontend Server on http://localhost:3000
start "Frontend Server" cmd /k "frontend\start-frontend.bat"

echo.
echo ========================================
echo    Both servers are starting...
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to open the application...
pause >nul

start http://localhost:3000

echo.
echo Application opened in your browser!
echo.
pause