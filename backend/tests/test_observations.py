def test_create_observation_does_not_update_inventory(client):

    # Shelf oluştur
    shelf_response = client.post(
        "/api/v1/shelf/",
        json={
            "name": "Ana Raf"
        }
    )

    assert shelf_response.status_code == 200
    shelf = shelf_response.json()

    # Product oluştur
    product_response = client.post(
        "/api/v1/products/",
        json={
            "name": "Kalem",
            "class_name": "pen"
        }
    )

    assert product_response.status_code == 200
    product = product_response.json()

    # Başlangıç inventory = 5
    inventory_response = client.post(
        "/api/v1/inventory/",
        json={
            "shelf_id": shelf["id"],
            "product_id": product["id"],
            "quantity": 5
        }
    )

    assert inventory_response.status_code == 200

    # Observation = 6
    observation_response = client.post(
        "/api/v1/observations/",
        json={
            "shelf_id": shelf["id"],
            "products": [
                {
                    "product_id": product["id"],
                    "quantity": 6
                }
            ]
        }
    )

    assert observation_response.status_code == 200

    observation = observation_response.json()

    assert observation["id"] == 1
    assert observation["shelf_id"] == shelf["id"]
    assert len(observation["products"]) == 1

    observed_product = observation["products"][0]

    assert observed_product["product_id"] == product["id"]
    assert observed_product["quantity"] == 6

    # Inventory hâlâ 5 olmalı
    inventory_check = client.get(
        f"/api/v1/inventory/shelf/{shelf['id']}"
    )

    assert inventory_check.status_code == 200

    inventory = inventory_check.json()

    assert len(inventory) == 1
    assert inventory[0]["quantity"] == 5


def test_get_observation(client):

    # Shelf oluştur
    shelf_response = client.post(
        "/api/v1/shelf/",
        json={
            "name": "Ana Raf"
        }
    )

    assert shelf_response.status_code == 200
    shelf = shelf_response.json()

    # Product oluştur
    product_response = client.post(
        "/api/v1/products/",
        json={
            "name": "Kupa Bardak",
            "class_name": "cup"
        }
    )

    assert product_response.status_code == 200
    product = product_response.json()

    # Observation oluştur
    observation_response = client.post(
        "/api/v1/observations/",
        json={
            "shelf_id": shelf["id"],
            "products": [
                {
                    "product_id": product["id"],
                    "quantity": 3
                }
            ]
        }
    )

    assert observation_response.status_code == 200

    observation = observation_response.json()

    # Observation'ı GET et
    response = client.get(
        f"/api/v1/observations/{observation['id']}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == observation["id"]
    assert data["shelf_id"] == shelf["id"]
    assert len(data["products"]) == 1

    assert data["products"][0]["product_id"] == product["id"]
    assert data["products"][0]["quantity"] == 3