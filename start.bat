@echo off
echo ========================================
echo CampusNexus AI - Quick Start
echo ========================================
echo.

REM Check if Ollama is running
echo [1/4] Checking Ollama...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Ollama is not running!
    echo Please start Ollama and ensure it's running.
    echo Then run: ollama pull mistral
    pause
    exit /b 1
)
echo [OK] Ollama is running

REM Check if Mistral model is available
echo [2/4] Checking Mistral model...
ollama list | findstr "mistral" >nul
if %errorlevel% neq 0 (
    echo [ERROR] Mistral model not found!
    echo Please run: ollama pull mistral
    pause
    exit /b 1
)
echo [OK] Mistral model found

REM Check if virtual environment exists
echo [3/4] Checking Python environment...
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment and install requirements
call venv\Scripts\activate
if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install requirements if needed
pip show fastapi >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing dependencies...
    pip install -r requirements.txt
)
echo [OK] Python environment ready

REM Start the server
echo [4/4] Starting CampusNexus AI...
echo.
echo ========================================
echo Server starting at http://localhost:8000
echo Press Ctrl+C to stop
echo ========================================
echo.

python -m uvicorn backend.main:app --reload
