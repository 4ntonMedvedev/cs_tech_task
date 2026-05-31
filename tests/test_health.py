from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


def test_health_returns_200_when_database_is_reachable(client: TestClient) -> None:
    with patch("app.main.check_database_connectivity", return_value=True):
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_returns_503_when_database_is_unreachable() -> None:
    with patch("app.main.check_database_connectivity", return_value=False):
        with TestClient(app) as client:
            response = client.get("/health")

    assert response.status_code == 503
    assert response.json() == {
        "status": "unavailable",
        "detail": "database unreachable",
    }
