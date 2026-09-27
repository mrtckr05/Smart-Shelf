def test_create_product(client):
    response = client.post(
        "/api/v1/products/",
        json={
            "name": "Kalem",
            "class_name": "pen"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Kalem"
    assert data["class_name"] == "pen"