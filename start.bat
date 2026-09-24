@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
title Personal Budget Planner - Starting Platform...

echo ============================================================
echo         Personal Budget Planner - Web Platform
echo ============================================================
echo.

rem Navigate to repository root directory
cd /d "%~dp0"

rem 1. Check for Node.js / npm
where npm >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Node.js and npm are required but were not found in PATH.
    echo Please install Node.js from https://nodejs.org/
    echo.
    pause
    exit /b 1
)

rem 2. Check for uv or Python
set HAS_UV=0
where uv >nul 2>nul
if %ERRORLEVEL% equ 0 (
    set HAS_UV=1
) else (
    where python >nul 2>nul
    if !ERRORLEVEL! neq 0 (
        echo [ERROR] Neither uv nor python was found in PATH.
        echo Please install uv https://docs.astral.sh/uv/ or Python 3.11+.
        echo.
        pause
        exit /b 1
    )
)

rem 3. Prepare Backend
echo [1/4] Preparing backend...
cd /d "%~dp0backend"
if not exist ".venv" (
    echo Installing backend dependencies...
    if !HAS_UV! equ 1 (
        call uv sync
    ) else (
        python -m venv .venv
        call .venv\Scripts\activate.bat
        python -m pip install --upgrade pip
        python -m pip install -r requirements.txt
    )
) else (
    echo Backend environment is ready.
)

rem 4. Prepare Frontend
echo.
echo [2/4] Preparing frontend...
cd /d "%~dp0frontend"
if not exist "node_modules" (
    echo Installing frontend dependencies via npm install...
    call npm install
) else (
    echo Frontend dependencies are ready.
)

rem 5. Launch Backend server in a separate window
echo.
echo [3/4] Starting backend server on http://127.0.0.1:8001...
if !HAS_UV! equ 1 (
    start "Budget Planner Backend (FastAPI)" /D "%~dp0backend" cmd /k "uv run uvicorn app.main:app --reload --port 8001"
) else (
    start "Budget Planner Backend (FastAPI)" /D "%~dp0backend" cmd /k "call .venv\Scripts\activate.bat && python -m uvicorn app.main:app --reload --port 8001"
)

rem 6. Launch Frontend server in a separate window
echo.
echo [4/4] Starting frontend server on http://localhost:5174...
start "Budget Planner Frontend (Vite)" /D "%~dp0frontend" cmd /k "npm run dev"

echo.
echo ============================================================
echo   Personal Budget Planner is running!
echo   - Frontend: http://localhost:5174
echo   - Backend:  http://127.0.0.1:8001
echo   - API Docs: http://127.0.0.1:8001/docs
echo ============================================================
echo.
echo Opening browser in 3 seconds...
timeout /t 3 /nobreak >nul 2>&1 || ping 127.0.0.1 -n 4 >nul
start http://localhost:5174

echo.
echo Servers are running in their own console windows.
echo To stop the application, simply close those console windows.
echo.
pause
