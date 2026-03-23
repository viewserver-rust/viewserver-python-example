@echo off
setlocal

echo.
echo ============================================================
echo   ViewServer Python Example - Quick Start
echo ============================================================
echo.

:: Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment. Is Python installed?
        exit /b 1
    )
)

:: Activate venv
call .venv\Scripts\activate.bat

echo Installing dependencies...
pip install pandas pyarrow numpy
if errorlevel 1 (
    echo ERROR: Failed to install dependencies.
    exit /b 1
)

echo.
echo Installing viewserver-python wheel from GitHub Release...
pip install https://github.com/viewserver-rust/viewserver-core/releases/download/python-v0.1.0-164c267/viewserver_python-0.1.0-cp310-cp310-win_amd64.whl
if errorlevel 1 (
    echo ERROR: Failed to install viewserver-python wheel.
    exit /b 1
)

echo.
echo ============================================================
echo   Dependencies installed. Starting config setup...
echo ============================================================
echo.

python setup_config.py
if errorlevel 1 (
    echo ERROR: Config setup failed.
    exit /b 1
)

echo.
echo ============================================================
echo   Quick start complete!
echo.
echo   Activate your environment with:
echo     .venv\Scripts\activate
echo.
echo   Then run:
echo     python -m viewserver_example.standalone
echo     python -m viewserver_example.node --config config.json
echo ============================================================
echo.
