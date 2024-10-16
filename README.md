# Project Name
Todo App with FastAPI and Angular

## Description
Todo App using SQLAlchemy for ORM & FastAPI for communication between application & network, Angular for front end.

## Requirements

This project runs in a Dockerized environment, so there’s no need to manually install Python or Node.js.

The Docker environment is configured with the following versions:
- **Python**: Defined in the `Dockerfile` (`PYTHON_VERSION=3.11.10`)
- **Node.js**: Defined in the `Dockerfile` (`NODE_VERSION=18.x.x`)

For local development or debugging outside Docker, ensure you have compatible versions installed.

## Installation

1. Create .env file
   Save a .env file in project's backend root directory with format for FastApi server
```bash
ENVIRONMENT=<Evironment_name>           # accept one of values `production` or `development`. Default is `development`
SERVER_INTERFACE=<Server_interface>     # Default is 127.0.0.1 for security (if you want to access server from other host, set to 0.0.0.0)
```

2. Build docker
```sh
docker compose build
docker compose up -d
```

Access with http://localhost:4200
