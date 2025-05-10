@echo off
echo Starting Seamless in production mode...

REM Start all services in Docker
cd Docker
docker-compose -f docker-compose.prod.yml up -d

echo All services started in production mode.
echo To view logs, use: docker-compose -f docker-compose.prod.yml logs -f
echo To stop all services, use: docker-compose -f docker-compose.prod.yml down