@echo off
setlocal enabledelayedexpansion
echo Starting Seamless initialization...

cd ..
REM Start Kong and ELK in Docker
cd Docker
docker-compose -f docker-compose.dev.yml up -d kong elasticsearch logstash kibana filebeat
cd ..

REM Wait for services to start
echo Waiting for infrastructure services to start...
timeout /t 10 /nobreak > nul

REM Initialize each service in a separate window with appropriate title
start "Core Module" cmd /k "cd src\Core && if exist install_latest.bat (call install_latest.bat) && if exist init_db.bat (call init_db.bat)"
start "Academics Module" cmd /k "cd src\Academics && if exist install_latest.bat (call install_latest.bat) && if exist init_db.bat (call init_db.bat)"
start "Library Module" cmd /k "cd src\Library && if exist install_latest.bat (call install_latest.bat) && if exist init_db.bat (call init_db.bat)"

echo All initialization processes started. Press any key to shut down...
pause > nul

REM Find and kill Python processes
for /f "tokens=2" %%p in ('tasklist /fi "imagename eq python.exe" /fo csv /nh') do (
    set "pid=%%p"
    set "pid=!pid:"=!"
    if not "!pid!"=="" (
        echo Terminating Python process: !pid!
        taskkill /F /PID !pid! 2>nul
    )
)

REM Close all cmd windows with the module titles
echo Closing module windows...
taskkill /F /FI "WINDOWTITLE eq Core Module*" 2>nul
taskkill /F /FI "WINDOWTITLE eq Academics Module*" 2>nul
taskkill /F /FI "WINDOWTITLE eq Library Module*" 2>nul

REM Shut down Docker services
echo Shutting down Docker services...
cd Docker
docker-compose -f docker-compose.dev.yml down



