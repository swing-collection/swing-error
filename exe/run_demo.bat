@echo off
REM Swing Error Demo - Quick Start Script (Windows)
REM ================================================

echo.
echo 🚀 Starting Swing Error Demo...
echo.

REM Get the script directory
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..

REM Check if virtual environment is activated
if "%VIRTUAL_ENV%"=="" (
    echo 📦 Activating virtual environment...
    call "%PROJECT_ROOT%\.venv\Scripts\activate.bat"
) else (
    echo ✅ Virtual environment already activated
)

echo.
echo 🔍 Running Django system checks...
python "%SCRIPT_DIR%manage.py" check

if errorlevel 1 (
    echo ❌ System checks failed. Please fix the issues above.
    pause
    exit /b 1
)

echo.
echo ✅ All checks passed!
echo.
echo 🌐 Starting Django development server...
echo.
echo 📍 Open your browser to: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.

REM Run the development server
python "%SCRIPT_DIR%manage.py" runserver 0.0.0.0:8000
pause
