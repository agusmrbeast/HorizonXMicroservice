"""
Development script for running Seamless in hybrid mode.
- Kong and ELK in Docker
- Services running locally
"""

import os
import subprocess
import sys
import time
from pathlib import Path
import threading

# Define service ports
SERVICES = {
    "core": 8010,
    "academics": 8020,
    "library": 8030
}

def start_docker_infrastructure():
    """Start Kong and ELK stack in Docker"""
    print("Starting Kong and ELK stack in Docker...")
    subprocess.run(["docker-compose", "-f", "Docker/docker-compose.dev.yml", "up", "-d"])
    print("Waiting for services to be ready...")
    time.sleep(10)  # Give services time to start

def setup_service(service_name, port):
    """Set up a service for local development"""
    service_dir = Path(f"src/{service_name.capitalize()}")
    
    # Install dependencies if needed
    install_script = service_dir / "install_latest.bat" if sys.platform == "win32" else service_dir / "install_latest.sh"
    if install_script.exists():
        print(f"Installing dependencies for {service_name}...")
        subprocess.run([str(install_script)], cwd=service_dir)
    
    # Initialize database if needed
    init_db_script = service_dir / "init_db.bat" if sys.platform == "win32" else service_dir / "init_db.sh"
    if init_db_script.exists():
        print(f"Initializing database for {service_name}...")
        subprocess.run([str(init_db_script)], cwd=service_dir)
    
    # Modify port in .env.development
    env_file = service_dir / "envs" / ".env.development"
    if env_file.exists():
        with open(env_file, "r") as f:
            content = f.read()
        
        # Replace port
        if "PORT=8000" in content:
            content = content.replace("PORT=8000", f"PORT={port}")
            with open(env_file, "w") as f:
                f.write(content)
            print(f"Updated port to {port} in {env_file}")

def run_service(service_name, port):
    """Run a service locally"""
    service_dir = Path(f"{service_name.capitalize()}")
    
    print(f"Starting {service_name} service on port {port}...")
    
    # Change to service directory and run
    os.chdir(service_dir)
    subprocess.run(["uv", "run", "dev"])

def main():
    """Main function to run all services"""
    # Start infrastructure
    subprocess.run(["cd",".."])
    start_docker_infrastructure()
    
    # Set up each service
    for service_name, port in SERVICES.items():
        setup_service(service_name, port)
    
    # Start each service in a separate thread
    threads = []
    for service_name, port in SERVICES.items():
        thread = threading.Thread(
            target=run_service, 
            args=(service_name, port),
            daemon=True
        )
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete (they won't unless interrupted)
    try:
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        print("\nShutting down services...")
        # Stop Docker services
        subprocess.run(["docker-compose", "-f", "Docker/docker-compose.dev.yml", "down"])
        sys.exit(0)

if __name__ == "__main__":
    main()
