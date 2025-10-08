from fastapi.testclient import TestClient


def test_create_and_get_check(client: TestClient):
    response = client.post(
        "/api/v1/checks/",
        json={"name": "database", "description": "Check DB", "status": "passing"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "database"
    check_id = data["id"]

    get_response = client.get(f"/api/v1/checks/{check_id}")
    assert get_response.status_code == 200
    fetched = get_response.json()
    assert fetched["status"] == "passing"


def test_list_checks(client: TestClient):
    response = client.get("/api/v1/checks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_and_delete_check(client: TestClient):
    create_response = client.post(
        "/api/v1/checks/",
        json={"name": "cache", "description": "Check cache", "status": "failing"},
    )
    check_id = create_response.json()["id"]

    update_response = client.patch(
        f"/api/v1/checks/{check_id}",
        json={"status": "passing"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "passing"

    delete_response = client.delete(f"/api/v1/checks/{check_id}")
    assert delete_response.status_code == 204

    missing_response = client.get(f"/api/v1/checks/{check_id}")
    assert missing_response.status_code == 404
