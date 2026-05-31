from fastapi.testclient import TestClient


def test_create_incident(client: TestClient) -> None:
    payload = {
        "title": "Database outage",
        "description": "Primary PostgreSQL cluster is unreachable.",
        "severity": "critical",
        "status": "open",
    }

    response = client.post("/incidents", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["title"] == payload["title"]
    assert body["description"] == payload["description"]
    assert body["severity"] == payload["severity"]
    assert body["status"] == payload["status"]


def test_list_incidents(client: TestClient) -> None:
    payload = {
        "title": "API latency spike",
        "description": "P95 latency exceeded 2s.",
        "severity": "high",
        "status": "investigating",
    }
    client.post("/incidents", json=payload)

    response = client.get("/incidents")

    assert response.status_code == 200
    incidents = response.json()
    assert len(incidents) == 1
    assert incidents[0]["title"] == payload["title"]
