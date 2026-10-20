def test_health_endpoint(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok"
    }


def test_create_group(client):
    response = client.post(
        "/api/groups",
        json={
            "name": "Mostar Trip"
        },
    )

    assert response.status_code == 201

    assert response.json()["name"] == "Mostar Trip"


def test_reject_empty_group_name(client):
    response = client.post(
        "/api/groups",
        json={
            "name": "   "
        },
    )

    assert response.status_code == 400

    assert response.json() == {
        "detail": "Group name is required."
    }