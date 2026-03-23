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

echo Installing project and dependencies...
pip install -e .
if errorlevel 1 (
    echo ERROR: Failed to install project dependencies.
    exit /b 1
)

echo.
echo Downloading viewserver-python wheel from GitHub Release...
echo (requires GitHub CLI authenticated with access to viewserver-rust/viewserver-core)
where gh >nul 2>&1
if errorlevel 1 (
    echo ERROR: GitHub CLI ^(gh^) not found. Install from https://cli.github.com
    exit /b 1
)
gh release download python-v0.1.0-164c267 --repo viewserver-rust/viewserver-core --pattern "*win_amd64.whl" --dir .venv\wheels --clobber
if errorlevel 1 (
    echo ERROR: Failed to download wheel. Check gh auth status.
    exit /b 1
)
echo Installing viewserver-python wheel...
for %%f in (.venv\wheels\*win_amd64.whl) do pip install "%%f"
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
echo     python -m viewserver_example.node --config config.json
echo ============================================================
echo.
