#!/bin/bash

# Determine if we're in the module directory or parent directory
MODULE_DIR=$(pwd)
if [ ! -d "envs" ]; then
    # Check if we're in parent directory and need to navigate to module
    if [ -d "src/Core/envs" ]; then
        MODULE_DIR="src/Core"
        cd $MODULE_DIR
        echo "Changed directory to $MODULE_DIR"
    fi
fi

echo "Creating virtual environment..."
python3 -m venv .venv

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing UV..."
pip install uv

# Check if .env file exists and load DATABASE_URL
if [ -f ".env" ]; then
    echo "Loading environment variables from .env file..."
    export $(grep -v '^#' .env | xargs)
elif [ -f "envs/.env.development" ]; then
    echo "Loading environment variables from envs/.env.development file..."
    export $(grep -v '^#' envs/.env.development | xargs)
fi

echo "Installing project dependencies..."
uv pip install --upgrade pip
uv pip install -e ".[unix]"

echo "Installation complete!"
echo "Database URL: $DATABASE_URL"
