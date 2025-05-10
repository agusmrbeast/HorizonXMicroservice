# Seamless - Microservices Platform

A comprehensive microservices platform built with FastAPI, featuring Core, Academics, and Library services with integrated ELK stack for logging, Kong for API gateway, and Docker for containerization.

<div align="center">
  <img src="docs/images/seamless-logo.png" alt="Seamless Logo" width="300px">
  
  <p>
    <strong>Modern • Scalable • Maintainable</strong>
  </p>
  
  <p>
    <a href="#installation"><strong>Get Started »</strong></a>
    &nbsp;&nbsp;•&nbsp;&nbsp;
    <a href="#api-documentation"><strong>API Docs</strong></a>
    &nbsp;&nbsp;•&nbsp;&nbsp;
    <a href="#development"><strong>Development</strong></a>
    &nbsp;&nbsp;•&nbsp;&nbsp;
    <a href="#production"><strong>Production</strong></a>
  </p>
</div>

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
  - [Using Docker (Recommended)](#using-docker-recommended)
  - [Local Development](#local-development)
  - [Installation Scripts](#installation-scripts)
- [Development](#development)
  - [Docker Development Mode](#docker-development-mode)
  - [Hybrid Development Mode](#hybrid-development-mode)
  - [Development Tools](#development-tools)
  - [Utility Scripts](#utility-scripts)
- [Production](#production)
  - [Docker Production Mode](#docker-production-mode)
  - [Scaling in Production](#scaling-in-production)
- [API Documentation](#api-documentation)
- [Logging & Monitoring](#logging--monitoring)
  - [ELK Stack](#elk-stack)
  - [Accessing Logs](#accessing-logs)
  - [Log Structure](#log-structure)
- [Service Ports](#service-ports)
- [Environment Variables](#environment-variables)
- [Troubleshooting](#troubleshooting)
  - [Common Issues](#common-issues)
  - [Debugging](#debugging)
  - [Getting Help](#getting-help)

## Overview

Seamless is a modular microservices platform designed for educational institutions. It consists of three main services:

- **Core**: Central authentication, user management, and system-wide functionality
- **Academics**: Academic management including courses, grades, and curriculum
- **Library**: Library management including books, loans, and resources

The platform uses FastAPI for high-performance APIs, PostgreSQL for data storage, Redis for caching, and includes comprehensive logging with the ELK stack (Elasticsearch, Logstash, Kibana).

## Features

- **Microservices Architecture**: Modular services with clear boundaries
- **FastAPI Framework**: High-performance, easy-to-use web framework
- **SQLAlchemy ORM**: Async database operations with PostgreSQL
- **Redis Caching**: High-speed caching and rate limiting
- **Kong API Gateway**: Request routing, authentication, and rate limiting
- **ELK Stack**: Comprehensive logging and monitoring
- **Docker**: Containerization for development and production
- **Role-Based Access Control**: Fine-grained permission system
- **Environment Management**: Separate development and production configurations
- **UV Package Manager**: Fast, reliable Python package management
- **Ruff Linting & Formatting**: Maintain code quality and consistency

## Project Structure

```
seamless/
├── Docker/                   # Docker configuration files
│   └── docker-compose.dev.yml  # Development Docker Compose
│   └── docker-compose.prod.yml # Production Docker Compose
├── filebeat/                 # Filebeat configuration
│   └── filebeat.yml          # Filebeat configuration
├── kong/                     # Kong API Gateway configuration
│   └── kong.dev.yml          # Development Kong configuration
│   └── kong.prod.yml         # Production Kong configuration
├── logstash/                 # Logstash configuration
│   └── pipeline/             # Logstash pipeline configurations
├── scripts/                  # Utility scripts
│   ├── create-multiple-postgresql-databases.sh  # DB initialization
│   ├── docker-entrypoint.sh  # Docker entrypoint script
│   ├── run_dev.sh            # Start development environment (Unix)
│   ├── run_dev.bat           # Start development environment (Windows)
│   ├── run_prod.sh           # Start production environment (Unix)
│   ├── run_prod.bat          # Start production environment (Windows)
│   └── run_dev.py            # Python script for hybrid development
├── src/                      # Source code
│   ├── core/                 # Core service
│   │   ├── app/              # Application code
│   │   │   ├── api/          # API endpoints
│   │   │   ├── models/       # Database models
│   │   │   ├── schemas/      # Pydantic schemas
│   │   │   ├── services/     # Business logic
│   │   │   ├── main.py       # Application entry point
│   │   │   └── setup.py      # Application setup
│   │   ├── core/             # Core functionality
│   │   │   ├── cache/        # Caching utilities
│   │   │   ├── db/           # Database utilities
│   │   │   ├── utils/        # Utility functions
│   │   │   ├── config.py     # Configuration
│   │   │   ├── exceptions.py # Custom exceptions
│   │   │   ├── logging.py    # Logging configuration
│   │   │   ├── middleware.py # Middleware
│   │   │   └── security.py   # Security utilities
│   │   └── settings/         # Settings and environment
│   │       └── run.py        # Run script
│   │   ├── install_latest.sh # Unix installation script
│   │   ├── install_latest.bat # Windows installation script
│   │   └── init_db.sh        # Database initialization
│   ├── academics/            # Academics service (similar structure)
│   └── library/              # Library service (similar structure)
├── logs/                     # Application logs
├── Dockerfile.dev            # Development Dockerfile
├── Dockerfile.prod           # Production Dockerfile
├── docker-compose.dev.yml    # Development Docker Compose
├── docker-compose.prod.yml   # Production Docker Compose
├── pyproject.toml            # Project dependencies
└── README.md                 # Project documentation
```

## Requirements

- Docker and Docker Compose (for containerized development and deployment)
- Python 3.13+ (for local development without Docker)
- Git (for version control)
- PostgreSQL (for local development without Docker)
- Redis (for local development without Docker)

## Installation

### Using Docker (Recommended)

The easiest way to get started with Seamless is using Docker, which provides a consistent environment across all platforms.

1. **Clone the repository**:

```bash
git clone <repository-url>
cd seamless
```

2. **Start the development environment**:

```bash
# On Unix/Linux/Mac
./scripts/run_dev.sh

# On Windows
scripts\run_dev.bat

# Or using Docker Compose directly
docker-compose -f docker-compose.dev.yml up
```

This will:
- Build all necessary Docker images
- Start all services in development mode
- Set up the ELK stack for logging
- Configure Kong as the API gateway
- Create PostgreSQL databases for each service
- Enable hot reload for code changes

3. **Access the services**:

- Core API: http://localhost:8000/api/core
- Academics API: http://localhost:8000/api/academics
- Library API: http://localhost:8000/api/library
- API Documentation: http://localhost:8000/api/core/docs
- Kibana Dashboard: http://localhost:5601

### Local Development

For those who prefer to run services directly on their machine:

1. **Clone the repository**:

```bash
git clone <repository-url>
cd seamless
```

2. **Set up each service**:

For each service (core, academics, library), you'll need to:

```bash
# Navigate to the service directory
cd src/core

# On Unix/Linux/Mac
./install_latest.sh

# On Windows
install_latest.bat
```

The installation scripts will:
- Create a Python virtual environment (.venv)
- Install UV package manager
- Install all dependencies using UV
- Set up the development environment

3. **Set up PostgreSQL and Redis**:

You can either:
- Install PostgreSQL and Redis directly on your machine
- Use Docker to run just these services:

```bash
docker-compose -f docker-compose.dev.yml up -d postgres redis
```

4. **Run each service**:

```bash
# Activate the virtual environment first
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Run the service
uv run dev
```

### Installation Scripts

Seamless includes several installation scripts to simplify setup:

- **install_latest.sh / install_latest.bat**: These scripts create a virtual environment, install UV, and install all dependencies for a specific service.

```bash
# What the scripts do:
# 1. Create a Python virtual environment
python -m venv .venv

# 2. Activate the virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install UV package manager
pip install uv

# 4. Install dependencies using UV
uv pip install -e .
```

- **init_db.sh / init_db.bat**: Initialize the database for a service, creating tables and initial data.

- **run_dev.sh / run_dev.bat**: Start the entire platform in development mode, including infrastructure services.

- **run_prod.sh / run_prod.bat**: Start the entire platform in production mode.

## Development

### Docker Development Mode

The development environment uses Docker Compose to run all services with hot reload:

```bash
docker-compose -f docker-compose.dev.yml up
```

This starts:
- Core service on port 8010
- Academics service on port 8020
- Library service on port 8030
- Kong API Gateway on port 8000
- PostgreSQL on port 5432
- Redis on port 6379
- Elasticsearch on port 9200
- Kibana on port 5601
- Logstash on ports 5044 and 5000

Your local code is mounted into the containers, so changes are reflected immediately with hot reload.

### Hybrid Development Mode

You can also run some services in Docker and others locally, which is useful when you're focusing on a specific service:

```bash
# Start infrastructure services
python scripts/run_dev.py --infra-only

# Or manually:
docker-compose -f docker-compose.dev.yml up postgres redis kong elasticsearch logstash kibana filebeat

# Then run a specific service locally
cd src/core
uv run dev
```

### Development Tools

- **API Documentation**: Available at http://localhost:8000/api/core/docs, http://localhost:8000/api/academics/docs, and http://localhost:8000/api/library/docs
- **Kong Dashboard**: Available at http://localhost:8001
- **Kibana**: Available at http://localhost:5601
- **PostgreSQL**: Available at localhost:5432
- **Redis**: Available at localhost:6379

### Utility Scripts

Seamless includes several utility scripts to help with development:

- **Format Code**:
```bash
uv run format
```

- **Lint Code**:
```bash
uv run lint
```

- **Fix Linting Issues**:
```bash
uv run lint-fix
```

- **Create Database Migrations**:
```bash
uv run makemigrations
```

- **Apply Database Migrations**:
```bash
uv run migrate
```

- **Create Superuser**:
```bash
uv run createsuperuser
```

- **Pre-commit Checks**:
```bash
uv run pre-commit
```

## Production

### Docker Production Mode

For production deployment:

```bash
# Using the script
./scripts/run_prod.sh  # On Windows: scripts\run_prod.bat

# Or directly with Docker Compose
docker-compose -f docker-compose.prod.yml up -d
```

This starts all services in production mode with:
- Optimized configurations
- No hot reload
- Proper logging levels
- Production-ready settings
- Secure environment variables

### Scaling in Production

You can scale services in production to handle increased load:

```bash
docker-compose -f docker-compose.prod.yml up -d --scale academics=3 --scale library=2
```

This will start:
- 1 instance of the Core service
- 3 instances of the Academics service
- 2 instances of the Library service

Kong will automatically load balance requests between the instances.

## API Documentation

Each service provides its own API documentation:

- **Core API**: http://localhost:8000/api/core/docs
- **Academics API**: http://localhost:8000/api/academics/docs
- **Library API**: http://localhost:8000/api/library/docs

The documentation is generated automatically from the code and includes:
- Endpoint descriptions
- Request and response schemas
- Authentication requirements
- Example requests and responses

## Logging & Monitoring

### ELK Stack

The platform includes a complete ELK (Elasticsearch, Logstash, Kibana) stack for logging:

1. **Filebeat**: Collects logs from all services and forwards them to Logstash
   - Monitors log files in the `logs` directory
   - Collects Docker container logs
   - Adds metadata like service name

2. **Logstash**: Processes and transforms logs
   - Parses JSON logs
   - Enriches logs with additional metadata
   - Forwards logs to Elasticsearch

3. **Elasticsearch**: Stores and indexes logs
   - Provides full-text search capabilities
   - Enables complex queries and aggregations
   - Stores logs in a structured format

4. **Kibana**: Visualizes and searches logs
   - Provides a web interface for log exploration
   - Enables creation of dashboards and visualizations
   - Allows setting up alerts based on log patterns

### Accessing Logs

- **Kibana Dashboard**: http://localhost:5601
- **Predefined Dashboards**: Import dashboards from the `kibana/dashboards` directory

To view logs for a specific service:
1. Go to Kibana
2. Navigate to "Discover"
3. Create a filter: `service: "core"` (or academics, library)

### Log Structure

All logs follow a consistent JSON format with fields:
- `timestamp`: ISO 8601 timestamp
- `level`: Log level (INFO, ERROR, etc.)
- `message`: Log message
- `service`: Service name (core, academics, library)
- `environment`: Environment (development, production)
- `name`: Logger name
- `function`: Function that generated the log
- `line`: Line number in the source code
- `exception`: Exception details (if applicable)

## Service Ports

| Service       | Internal Port | External Port (Dev) | External Port (Prod) |
|---------------|---------------|---------------------|----------------------|
| Core          | 8000          | 8010                | -                    |
| Academics     | 8000          | 8020                | -                    |
| Library       | 8000          | 8030                | -                    |
| Kong Gateway  | 8000          | 8000                | 80                   |
| Kong Admin    | 8001          | 8001                | -                    |
| PostgreSQL    | 5432          | 5432                | -                    |
| Redis         | 6379          | 6379                | -                    |
| Elasticsearch | 9200          | 9200                | -                    |
| Logstash      | 5044          | 5044                | -                    |
| Kibana        | 5601          | 5601                | -                    |

In production, all services are accessed through the Kong API Gateway on port 80.

## Environment Variables

Each service uses environment variables for configuration. These are defined in the Docker Compose files and can be overridden.

### Core Service

```
MODULE=core
PORT=8000
POSTGRES_HOST=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=core
REDIS_HOST=redis
LOG_LEVEL=DEBUG
APP_ENV=development
APP_NAME=Seamless Core
APP_DESCRIPTION=Core service for Seamless platform
APP_VERSION=1.0.0
SHOW_DOCS=true
```

### Academics Service

```
MODULE=academics
PORT=8000
POSTGRES_HOST=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=academics
REDIS_HOST=redis
LOG_LEVEL=DEBUG
APP_ENV=development
APP_NAME=Seamless Academics
APP_DESCRIPTION=Academic management service for Seamless platform
APP_VERSION=1.0.0
SHOW_DOCS=true
```

### Library Service

```
MODULE=library
PORT=8000
POSTGRES_HOST=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=library
REDIS_HOST=redis
LOG_LEVEL=DEBUG
APP_ENV=development
APP_NAME=Seamless Library
APP_DESCRIPTION=Library management service for Seamless platform
APP_VERSION=1.0.0
SHOW_DOCS=true
```

## Troubleshooting

### Common Issues

1. **Services not starting**:
   - Check Docker logs: `docker-compose -f docker-compose.dev.yml logs [service]`
   - Ensure ports are not already in use
   - Verify Docker is running correctly

2. **Database connection issues**:
   - Ensure PostgreSQL is running: `docker ps | grep postgres`
   - Check connection parameters (host, port, username, password)
   - Verify database exists: `docker exec -it seamless_postgres psql -U postgres -c "\l"`

3. **Redis connection issues**:
   - Ensure Redis is running: `docker ps | grep redis`
   - Check connection parameters (host, port)
   - Test connection: `docker exec -it seamless_redis redis-cli ping`

4. **Logs not appearing in Kibana**:
   - Check Filebeat is running
