@echo off
chcp 65001 > nul
cd /d "%~dp0"

if not exist env\Scripts\python.exe (
    python -m venv env
)

env\Scripts\python.exe -c "import django" >nul 2>&1
if errorlevel 1 (
    env\Scripts\pip.exe install -r requirements.txt
)

env\Scripts\python.exe manage.py migrate > nul 2>&1

if not exist db_ready.flag (
    env\Scripts\python.exe setup_data.py > nul 2>&1
    echo. > db_ready.flag
)

echo http://127.0.0.1:8000
env\Scripts\python.exe manage.py runserver --skip-checks

pause
