def test_create_shelf(client):

    response = client.post(
        "/api/v1/shelf/",
        json={
            "name": "Ana Raf"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Ana Raf"