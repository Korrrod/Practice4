@echo off
chcp 65001 > nul
cd /d "%~dp0"

if not exist env\Scripts\python.exe (
    echo Creating virtual environment...
    python -m venv env
    if errorlevel 1 (
        echo ERROR: Python not found. Install Python 3.8+ and try again.
        pause
        exit /b 1
    )
)

env\Scripts\python.exe -c "import django" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    env\Scripts\pip.exe install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies.
        pause
        exit /b 1
    )
)

env\Scripts\python.exe manage.py migrate > nul 2>&1

if not exist db_ready.flag (
    env\Scripts\python.exe setup_data.py
    echo. > db_ready.flag
)

env\Scripts\python.exe manage.py check > nul 2>&1
if errorlevel 1 (
    echo Failed to start. Error:
    echo.
    env\Scripts\python.exe manage.py check
    pause
    exit /b 1
)

echo Success!
echo http://127.0.0.1:8000
echo.

env\Scripts\python.exe manage.py runserver --skip-checks 2>nul

pause
