from fastapi.testclient import TestClient


def test_read_root(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "name": "OddsEngine",
        "environment": "local",
        "version": "0.1.0",
        "status": "running",
    }