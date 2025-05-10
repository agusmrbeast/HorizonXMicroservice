@echo off
echo Initializing database...

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
:: Set environment variables
set DATABASE_URL=%DATABASE_URL%

:: Run migrations
uv run alembic revision --autogenerate -m "Initial migration"
uv run alembic upgrade head

echo Database initialization complete!