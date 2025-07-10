@echo off
echo === Running Subway Model ===

if not exist ".venv" (
    echo Virtual environment not found!
    echo Please run setup_env.bat first
    pause
    exit /b 1
)

if not exist "src\main.py" (
    echo src\main.py not found!
    echo Please ensure your main module is located at src\main.py
    pause
    exit /b 1
)

echo Activating environment...
call .venv\Scripts\activate.bat

echo Running subway model...
python -m src.main

echo Execution complete
pause
