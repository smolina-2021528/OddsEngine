# OddsEngine

OddsEngine is a REST API for sports data collection, statistical odds calculation, and AI-assisted betting analysis.

## Current status

The project is starting with the base FastAPI application.

## Tech stack

- Python 3.12
- FastAPI
- Uvicorn

## Local setup

Create a virtual environment:

```bash
python -m venv .venv

Activate it on Windows:

.venv\Scripts\activate

Activate it on macOS/Linux:

source .venv/bin/activate

Install dependencies:

pip install -e ".[dev]"

Run the development server:

uvicorn app.main:app --reload

Open the API docs:

http://127.0.0.1:8000/docs

---