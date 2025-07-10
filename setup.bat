@echo off
setlocal EnableDelayedExpansion

echo === Subway Model Environment Setup ===
echo Setting up environment for: subway-model
echo.

REM Check if uv is installed
uv --version >nul 2>&1
if errorlevel 1 (
    echo Error: uv is not installed or not in PATH
    echo Please install uv first:
    echo   Download from: https://github.com/astral-sh/uv
    echo   Or use: pip install uv
    pause
    exit /b 1
)

echo uv is installed

REM Check if virtual environment exists
if exist ".venv" (
    echo Virtual environment already exists at .venv
    set /p "response=Do you want to recreate it? (y/N): "
    if /i "!response!"=="y" (
        echo Removing existing virtual environment...
        rmdir /s /q ".venv"
    ) else (
        echo Using existing virtual environment
    )
)

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo Creating virtual environment with Python 3.12...
    uv venv --python 3.12
    if errorlevel 1 (
        echo Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created
)

REM Install dependencies
echo Installing dependencies from pyproject.toml...
uv sync
if errorlevel 1 (
    echo Failed to install dependencies
    pause
    exit /b 1
)

echo ✓ Dependencies installed successfully

REM Create activation batch file
echo @echo off > activate_env.bat
echo call .venv\Scripts\activate.bat >> activate_env.bat
echo echo Subway Model environment activated! >> activate_env.bat
echo echo Python version: >> activate_env.bat
echo python --version >> activate_env.bat
echo echo To deactivate, run: deactivate >> activate_env.bat

echo.
echo === Setup Complete! ===
echo Your subway-model environment is ready to use.
echo.
echo To activate the environment:
echo   .venv\Scripts\activate.bat
echo   Or run: activate_env.bat
echo.
echo To run your project:
echo   python -m src.main
echo.
echo Note: Make sure your src/main.py file exists before running!
pause
