# OddsEngine

OddsEngine is a REST API for sports data collection, statistical odds calculation, and AI-assisted betting analysis.

## Current status

The project is currently in Phase 1: base infrastructure.

Implemented so far:

- Base FastAPI application.
- Centralized application settings.
- Dockerfile.
- Docker Compose with API, PostgreSQL and Redis.
- Async SQLAlchemy engine.
- Async Redis client.
- Base ORM models.
- Alembic initial migration.
- Health endpoint.
- Initial automated tests.

## Tech stack

- Python 3.12
- FastAPI
- Uvicorn
- PostgreSQL 16
- Redis 7
- SQLAlchemy 2.0
- Alembic
- Docker
- Docker Compose
- pytest
- ruff
- mypy

## Local setup without Docker

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

Activate it on Windows CMD:

```bash
.venv\Scripts\activate.bat
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -e ".[dev]"
```

Create a local environment file:

```bash
cp .env.example .env
```

On Windows PowerShell:

```bash
Copy-Item .env.example .env
```

Run the development server:

```bash
uvicorn app.main:app --reload
```

Open the API docs:

```txt
http://127.0.0.1:8000/docs
```

## Local setup with Docker

Build and start all services:

```bash
docker compose up --build
```

The API will be available at:

```txt
http://127.0.0.1:8000
```

The interactive API documentation will be available at:

```txt
http://127.0.0.1:8000/docs
```

Stop all services:

```bash
docker compose down
```

Stop all services and remove volumes:

```bash
docker compose down -v
```

## Database migrations

Start PostgreSQL and Redis:

```bash
docker compose up -d db redis
```

Run migrations:

```bash
alembic upgrade head
```

Check current migration:

```bash
alembic current
```

## Endpoints

### Root

```txt
GET /
```

Expected response:

```json
{
  "name": "OddsEngine",
  "environment": "local",
  "version": "0.1.0",
  "status": "running"
}
```

### Health

```txt
GET /api/v1/health
```

Expected response when PostgreSQL and Redis are available:

```json
{
  "status": "ok",
  "application": {
    "status": "ok",
    "detail": "OddsEngine is running in local mode."
  },
  "database": {
    "status": "ok",
    "detail": "PostgreSQL connection is available."
  },
  "redis": {
    "status": "ok",
    "detail": "Redis connection is available."
  }
}
```

If PostgreSQL or Redis are unavailable, the endpoint returns HTTP `503` with status `degraded`.

## Tests

Run unit tests:

```bash
pytest
```

Run integration tests against real PostgreSQL and Redis services:

```bash
ODDS_ENGINE_RUN_INTEGRATION_TESTS=1 pytest tests/integration
```

On Windows PowerShell:

```powershell
$env:ODDS_ENGINE_RUN_INTEGRATION_TESTS="1"
pytest tests/integration
```

## Quality checks

Run lint:

```bash
ruff check .
```

Run type checking:

```bash
mypy .
```