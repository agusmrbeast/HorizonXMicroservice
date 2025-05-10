#!/bin/bash
echo "Initializing database..."

# Check if .env file exists and load DATABASE_URL
if [ -f ".env" ]; then
    echo "Loading environment variables from .env file..."
    export $(grep -v '^#' .env | xargs)
elif [ -f "envs/.env.development" ]; then
    echo "Loading environment variables from envs/.env.development file..."
    export $(grep -v '^#' envs/.env.development | xargs)
fi

# Set environment variables
export DATABASE_URL="$DATABASE_URL"

# Run migrations
alembic upgrade head

echo "Database initialization complete!"