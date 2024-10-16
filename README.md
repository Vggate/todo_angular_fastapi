# Todo App with FastAPI and Angular

## Description
This project is a Todo App that uses SQLAlchemy for ORM & FastAPI for the backend API, with Angular for the front end. It's designed to run in a Dockerized environment for easy setup and deployment.

## Technologies
- Backend: FastAPI, SQLAlchemy
- Frontend: Angular
- Database: (Specify your database, e.g., PostgreSQL, SQLite)
- Containerization: Docker

## Requirements
This project runs in a Dockerized environment, so there's no need to manually install Python or Node.js. The Docker environment is configured with:

- **Python**: 3.11.10
- **Node.js**: 18.x.x

For local development or debugging outside Docker, ensure you have compatible versions installed.

## Installation and Setup

### Using Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. Create a `.env` file in the root directory of the back-end source code with the following content:
   ```bash
   ENVIRONMENT=development  # Use 'production' for production environment
   SERVER_INTERFACE=127.0.0.1  # Use '0.0.0.0' to allow external access
   ```

3. Build and run the Docker containers:
   ```bash
   docker compose build
   docker compose up -d
   ```

4. Access the application at http://localhost:4200

### Running Without Docker

#### Backend Setup:
1. Create a Python virtual environment:
   - Windows: `python -m venv .venv`
   - Unix or MacOS: `python3 -m venv .venv`
2. Activate the virtual environment:
   - Windows: `.venv\Scripts\Activate.ps1`
   - Unix or MacOS: `source .venv/bin/activate`
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the FastAPI server:
   ```bash
   fastapi dev main.py
   ```

#### Frontend Setup:
1. Navigate to the frontend directory
2. Install npm packages:
   ```bash
   npm install
   ```
3. Start the Angular development server:
   ```bash
   npm run start
   ```
4. Access the application at http://localhost:4200

## Testing

### Frontend Testing
1. Navigate to the root directory of the front-end source code
2. Run the test command:
   ```bash
   npm run test
   ```
