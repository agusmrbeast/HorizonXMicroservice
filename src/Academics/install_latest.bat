@echo off
echo Installing latest packages with uv...

:: Determine if we're in the module directory or parent directory
set MODULE_DIR=%CD%
if not exist envs (
    :: Check if we're in parent directory and need to navigate to module
    if exist src\Core\envs (
        set MODULE_DIR=src\Core
        cd %MODULE_DIR%
        echo Changed directory to %MODULE_DIR%
    )
)

:: Create virtual environment if it doesn't exist
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
)

:: Activate virtual environment
call .venv\Scripts\activate.bat

:: Check if .env file exists and load DATABASE_URL
if exist .env (
    echo Loading environment variables from .env file...
    for /F "tokens=*" %%A in (.env) do (
        set %%A
    )
) else if exist envs\.env.development (
    echo Loading environment variables from envs\.env.development file...
    for /F "tokens=*" %%A in (envs\.env.development) do (
        set %%A
    )
)

:: Install latest packages with uv
echo Installing latest packages with uv...
uv pip install -e .

echo Installation complete!
echo Run 'uv run dev' to start the development server.
echo Database URL: %DATABASE_URL%


