# Incident Tracker

FastAPI service for creating and listing incidents, with PostgreSQL persistence, Prometheus metrics, structured logging, and Docker-based deployment.

Built with FastAPI, SQLAlchemy, and Docker. Logs go to stdout, metrics on `/metrics`.

## Run it

```bash
docker compose up --build
```

App: http://localhost:8000  
Swagger UI: http://localhost:8000/docs

### Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | *(see docker-compose)* | SQLAlchemy database URL |
| `LOG_LEVEL` | `INFO` | Python log level |
| `POSTGRES_USER` | `incident_user` | PostgreSQL user |
| `POSTGRES_PASSWORD` | `incident_pass` | PostgreSQL password |
| `POSTGRES_DB` | `incidents` | PostgreSQL database name |
| `APP_PORT` | `8000` | Host port for the API |
| `POSTGRES_PORT` | `5432` | Host port for PostgreSQL |

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/incidents` | Create an incident |
| `GET` | `/incidents` | List all incidents |
| `GET` | `/health` | Readiness probe (200 if DB reachable, 503 otherwise) |
| `GET` | `/error` | Intentional 500 for error-handling tests |
| `GET` | `/metrics` | Prometheus metrics |

### Example: create an incident

```bash
curl -X POST http://localhost:8000/incidents \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Database outage",
    "description": "Primary cluster unreachable",
    "severity": "critical",
    "status": "open"
  }'
```

## Check the database

With compose running:

```bash
docker compose exec db psql -U incident_user -d incidents -c "SELECT * FROM incidents;"
```

Or open a shell:

```bash
docker compose exec db psql -U incident_user -d incidents
```

## Tests

No Docker needed for tests — they use in-memory SQLite.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -v
```

Tests use an in-memory SQLite database and do not require PostgreSQL.

## Project structure

```
app/          — application code
tests/        — pytest tests
Dockerfile
docker-compose.yml
requirements.txt
```
