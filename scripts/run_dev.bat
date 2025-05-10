@echo off
setlocal enabledelayedexpansion
echo Starting Seamless in hybrid development mode...

cd ..
REM Start Kong and ELK in Docker
cd Docker
docker-compose -f docker-compose.dev.yml up -d kong elasticsearch logstash kibana filebeat
cd ..

REM Wait for services to start
echo Waiting for infrastructure services to start...
timeout /t 10 /nobreak > nul

REM Start each service in a separate window with appropriate title
start "Core Module" cmd /k "cd src\Core && uv run dev --active"
start "Academics Module" cmd /k "cd src\Academics && uv run dev --active"
start "Library Module" cmd /k "cd src\Library && uv run dev --active"

echo All services started. Press any key to shut down...
pause > nul

REM Kill all running Python processes for the services
echo Shutting down service processes...

REM Find and kill Python processes
taskkill /F /FI "IMAGENAME eq python.exe"

REM Close all cmd windows with the module titles
echo Closing module windows...
taskkill /F /FI "WINDOWTITLE eq Core Module*" 2>nul
taskkill /F /FI "WINDOWTITLE eq Academics Module*" 2>nul
taskkill /F /FI "WINDOWTITLE eq Library Module*" 2>nul

REM Shut down Docker services
echo Shutting down Docker services...
cd Docker
docker-compose -f docker-compose.dev.yml down


