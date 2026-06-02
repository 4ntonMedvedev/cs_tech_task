# Incident Tracker

FastAPI app for creating and listing incidents. Data goes to PostgreSQL.

Built with FastAPI, SQLAlchemy, and Docker. Logs go to stdout, metrics on `/metrics`.

## Run it

```bash
docker compose up --build
```

| Service | URL |
|---------|-----|
| API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |

### Environment variables

Default DB credentials: `incident_user` / `incident_pass`, database `incidents`.

Override ports with env vars like `APP_PORT`, `GRAFANA_PORT`, etc. (see `docker-compose.yml`).

## Observability

Compose starts a small observability stack alongside the app:

- **Prometheus** scrapes `http://app:8000/metrics` every 15s
- **Promtail** reads Docker container logs from the host and pushes them to **Loki**
- **Grafana** lets you query metrics and logs in one place

Config files: `prometheus.yml`, `promtail-config.yml`.

### Grafana first-time setup

Login at http://localhost:3000 (default: `admin` / `admin`).

Add two datasources (Connections → Data sources):

1. **Prometheus** → URL `http://prometheus:9090`
2. **Loki** → URL `http://loki:3100`

Then try **Explore**:

- Prometheus: `http_requests_total` or `http_request_duration_seconds_bucket`
- Loki: `{job="containerlogs"} |= "Created incident"` (after creating an incident)

Hit `GET /error` to generate a 500 and see it in both metrics and logs.

Promtail reads logs from all containers in this POC, not just the app.

## API endpoints

- `POST /incidents` — create an incident
- `GET /incidents` — list incidents
- `GET /health` — 200 if DB is up, 503 if not
- `GET /error` — throws on purpose (for testing alerts)
- `GET /metrics` — Prometheus metrics

Example:

```bash
curl -X POST http://localhost:8000/incidents \
  -H "Content-Type: application/json" \
  -d '{"title":"Outage","description":"DB is down","severity":"critical","status":"open"}'

curl http://localhost:8000/incidents
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

No Docker needed — tests use in-memory SQLite.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -v
```

## Project structure

```
app/                  — application code
tests/                — pytest tests
prometheus.yml        — Prometheus scrape config
promtail-config.yml   — Promtail → Loki config
Dockerfile
docker-compose.yml
requirements.txt
.github/workflows/    — CI/CD pipeline
```
