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

1. If a .env file does not already exist in the root directory of the back-end source code, create one. Then, add the following two environment variables:
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

### Run project without Docker
#### For Backend:
1. Create python env with command: `python -m venv .venv` or `python3 -m venv .venv`
2. Active env: `.venv/Scripts/Activate.ps1` or `source .venv/bin/activate`
3. Install package with command: `pip install -r requirements.txt`
4. Run project: `fastapi dev main.py`

#### For Frontend
1. Install npm packages: `npm install`
2. Start project: `npm run start`
3. Access with http://localhost:4200


#### Frontend testing
1. Move to the root directory of the front-end source code
2. Type command: `npm run test`
