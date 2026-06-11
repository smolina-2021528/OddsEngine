from fastapi.testclient import TestClient
from pytest import MonkeyPatch


async def fake_available_connection() -> bool:
    return True


async def fake_unavailable_connection() -> bool:
    return False


def test_health_check_returns_ok_when_dependencies_are_available(
    client: TestClient,
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "app.api.v1.health.check_database_connection",
        fake_available_connection,
    )
    monkeypatch.setattr(
        "app.api.v1.health.check_redis_connection",
        fake_available_connection,
    )

    response = client.get("/api/v1/health")

    assert response.status_code == 200

    payload = response.json()

    assert payload["status"] == "ok"
    assert payload["application"]["status"] == "ok"
    assert payload["database"]["status"] == "ok"
    assert payload["redis"]["status"] == "ok"


def test_health_check_returns_degraded_when_database_is_unavailable(
    client: TestClient,
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "app.api.v1.health.check_database_connection",
        fake_unavailable_connection,
    )
    monkeypatch.setattr(
        "app.api.v1.health.check_redis_connection",
        fake_available_connection,
    )

    response = client.get("/api/v1/health")

    assert response.status_code == 503

    payload = response.json()

    assert payload["status"] == "degraded"
    assert payload["application"]["status"] == "ok"
    assert payload["database"]["status"] == "error"
    assert payload["redis"]["status"] == "ok"


def test_health_check_returns_degraded_when_redis_is_unavailable(
    client: TestClient,
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "app.api.v1.health.check_database_connection",
        fake_available_connection,
    )
    monkeypatch.setattr(
        "app.api.v1.health.check_redis_connection",
        fake_unavailable_connection,
    )

    response = client.get("/api/v1/health")

    assert response.status_code == 503

    payload = response.json()

    assert payload["status"] == "degraded"
    assert payload["application"]["status"] == "ok"
    assert payload["database"]["status"] == "ok"
    assert payload["redis"]["status"] == "error"