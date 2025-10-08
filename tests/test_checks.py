from fastapi.testclient import TestClient

from app.enums import CheckStatus


def test_create_and_get_check(client: TestClient):
    response = client.post(
        "/api/v1/checks/",
        json={"name": "database", "description": "Check DB", "status": CheckStatus.PASSING},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "database"
    assert data["status"] == CheckStatus.PASSING
    assert data["created_at"]
    check_id = data["id"]

    get_response = client.get(f"/api/v1/checks/{check_id}")
    assert get_response.status_code == 200
    fetched = get_response.json()
    assert fetched["status"] == CheckStatus.PASSING


def test_list_checks(client: TestClient):
    response = client.get("/api/v1/checks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_and_delete_check(client: TestClient):
    create_response = client.post(
        "/api/v1/checks/",
        json={"name": "cache", "description": "Check cache", "status": CheckStatus.FAILING},
    )
    check_id = create_response.json()["id"]

    update_response = client.patch(
        f"/api/v1/checks/{check_id}",
        json={"status": CheckStatus.PASSING},
    )
    assert update_response.status_code == 200
    assert update_response.json()["status"] == CheckStatus.PASSING

    delete_response = client.delete(f"/api/v1/checks/{check_id}")
    assert delete_response.status_code == 204

    missing_response = client.get(f"/api/v1/checks/{check_id}")
    assert missing_response.status_code == 404


def test_list_checks_filter_by_status(client: TestClient):
    for status in (CheckStatus.PASSING, CheckStatus.FAILING):
        client.post(
            "/api/v1/checks/",
            json={"name": f"svc-{status}", "description": None, "status": status},
        )

    all_checks = client.get("/api/v1/checks/")
    assert all_checks.status_code == 200
    assert len(all_checks.json()) >= 2

    filtered = client.get(f"/api/v1/checks/?status={CheckStatus.PASSING}")
    assert filtered.status_code == 200
    payload = filtered.json()
    assert len(payload) >= 1
    assert all(item["status"] == CheckStatus.PASSING for item in payload)


def test_summary_counts(client: TestClient):
    client.post(
        "/api/v1/checks/",
        json={"name": "api", "description": None, "status": CheckStatus.PASSING},
    )
    client.post(
        "/api/v1/checks/",
        json={"name": "worker", "description": None, "status": CheckStatus.FAILING},
    )
    client.post(
        "/api/v1/checks/",
        json={"name": "proxy", "description": None, "status": CheckStatus.DEGRADED},
    )

    summary_response = client.get("/api/v1/checks/summary")
    assert summary_response.status_code == 200
    summary = summary_response.json()
    assert summary["total"] >= 3
    assert summary["by_status"][CheckStatus.PASSING] >= 1
    assert summary["by_status"][CheckStatus.FAILING] >= 1
    assert summary["by_status"][CheckStatus.UNKNOWN] >= 0
    assert summary["latest_check"] is not None
