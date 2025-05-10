#!/bin/bash

echo "Starting Seamless in hybrid development mode..."
cd ..
# Start Kong and ELK in Docker
cd Docker
docker-compose -f docker-compose.dev.yml up -d kong elasticsearch logstash kibana filebeat
cd ..

# Wait for services to start
echo "Waiting for infrastructure services to start..."
sleep 10

# Setup and start Core service in a new terminal
gnome-terminal -- bash -c "cd src/Core && if [ -f install_latest.sh ]; then bash install_latest.sh; fi && if [ -f init_db.sh ]; then bash init_db.sh; fi && uv run dev; exec bash"

# Setup and start Academics service in a new terminal
gnome-terminal -- bash -c "cd src/Academics && if [ -f install_latest.sh ]; then bash install_latest.sh; fi && if [ -f init_db.sh ]; then bash init_db.sh; fi && uv run dev; exec bash"

# Setup and start Library service in a new terminal
gnome-terminal -- bash -c "cd src/Library && if [ -f install_latest.sh ]; then bash install_latest.sh; fi && if [ -f init_db.sh ]; then bash init_db.sh; fi && uv run dev; exec bash"

echo "All services started. Press Ctrl+C to shut down..."
read -p "Press Enter to shut down all services..."

# Shut down Docker services
cd Docker
docker-compose -f docker-compose.dev.yml down


