@echo off
setlocal

:: Process each module
echo Processing modules...
for %%m in (Core Academics Library) do (
    if exist "src\%%m" (
        echo Processing %%m module...
        cd "src\%%m"
        call uv run lint-fix
        if %ERRORLEVEL% NEQ 0 goto :error
        call uv run format-fix
        if %ERRORLEVEL% NEQ 0 goto :error
        cd ..\..
    ) else (
        echo Module %%m not found, skipping
    )
)

:: Add all changes to git
echo Adding changes to git...
git add .
if %ERRORLEVEL% NEQ 0 goto :error

:: Use Python to run commitizen
echo Running commitizen via Python...
python -c "import os; os.system('cz commit')"
if %ERRORLEVEL% NEQ 0 goto :error

echo Commit process completed successfully!
goto :end

:error
echo An error occurred during the commit process.
exit /b 1

:end
exit /b 0