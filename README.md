# OddsEngine

OddsEngine is a REST API for sports data collection, statistical odds calculation, and AI-assisted betting analysis.

## Current status

The project is currently in Phase 1: base infrastructure.

Implemented so far:

- Base FastAPI application.
- Centralized application settings.
- Dockerfile.
- Docker Compose with API, PostgreSQL and Redis.

## Tech stack

- Python 3.12
- FastAPI
- Uvicorn
- PostgreSQL 16
- Redis 7
- Docker
- Docker Compose

## Local setup without Docker

Create a virtual environment:

```bash
python -m venv .venv

Activate it on Windows PowerShell:

.venv\Scripts\Activate.ps1

Activate it on Windows CMD:

.venv\Scripts\activate.bat

Activate it on macOS/Linux:

source .venv/bin/activate

Install dependencies:

pip install -e ".[dev]"

Run the development server:

uvicorn app.main:app --reload

Open the API docs:

http://127.0.0.1:8000/docs
Local setup with Docker

Build and start all services:

docker compose up --build

The API will be available at:

http://127.0.0.1:8000

The interactive API documentation will be available at:

http://127.0.0.1:8000/docs

Stop all services:

docker compose down

Stop all services and remove volumes:

docker compose down -v
Current root endpoint
GET /

Expected response:

{
  "name": "OddsEngine",
  "environment": "local",
  "version": "0.1.0",
  "status": "running"
}

---