@echo off
chcp 65001 >nul
title Frontend Setup

echo Setting up Node.js frontend environment...
echo.

:: Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org
    exit /b 1
)

:: Check if npm is installed
npm --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: npm is not installed or not in PATH
    exit /b 1
)

echo Installing Node.js dependencies...
call npm install

if errorlevel 1 (
    echo ERROR: Failed to install npm dependencies
    exit /b 1
)

echo.
echo Installing Tailwind CSS and dependencies...
call npm install -D tailwindcss postcss autoprefixer
call npx tailwindcss init -p

if errorlevel 1 (
    echo ERROR: Failed to set up Tailwind CSS
    exit /b 1
)

echo.
echo Creating TypeScript configuration files...
if not exist "tsconfig.json" (
    echo Creating tsconfig.json...
    (
        echo {
        echo   "compilerOptions": {
        echo     "target": "ES2020",
        echo     "useDefineForClassFields": true,
        echo     "lib": ["ES2020", "DOM", "DOM.Iterable"],
        echo     "module": "ESNext",
        echo     "skipLibCheck": true,
        echo     "moduleResolution": "bundler",
        echo     "allowImportingTsExtensions": true,
        echo     "resolveJsonModule": true,
        echo     "isolatedModules": true,
        echo     "noEmit": true,
        echo     "jsx": "react-jsx",
        echo     "strict": true,
        echo     "noUnusedLocals": true,
        echo     "noUnusedParameters": true,
        echo     "noFallthroughCasesInSwitch": true,
        echo     "baseUrl": ".",
        echo     "paths": {
        echo       "@/*": ["./src/*"]
        echo     }
        echo   },
        echo   "include": ["src", "**/*.ts", "**/*.tsx"],
        echo   "references": [{ "path": "./tsconfig.node.json" }]
        echo }
    ) > tsconfig.json
)

if not exist "tsconfig.node.json" (
    echo Creating tsconfig.node.json...
    (
        echo {
        echo   "compilerOptions": {
        echo     "composite": true,
        echo     "skipLibCheck": true,
        echo     "module": "ESNext",
        echo     "moduleResolution": "bundler",
        echo     "allowSyntheticDefaultImports": true
        echo   },
        echo   "include": ["vite.config.ts"]
        echo }
    ) > tsconfig.node.json
)

if not exist "src\vite-env.d.ts" (
    echo Creating vite-env.d.ts...
    (
        echo /// ^<reference types="vite/client" /^>
        echo.
        echo declare module '*.svg' {
        echo   const content: string;
        echo   export default content;
        echo }
        echo.
        echo declare module '*.css' {
        echo   const content: Record^<string, string^>;
        echo   export default content;
        echo }
    ) > src\vite-env.d.ts
)

echo.
echo Creating frontend environment file...
if not exist ".env" (
    (
        echo VITE_API_BASE_URL=http://localhost:8000
        echo VITE_APP_NAME=Stock Support Chatbot
    ) > .env
)

echo.
echo Frontend setup completed successfully!
echo.