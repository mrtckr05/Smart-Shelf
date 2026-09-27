def test_create_inventory(client):

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

    # Inventory oluştur
    inventory_response = client.post(
        "/api/v1/inventory/",
        json={
            "shelf_id": shelf["id"],
            "product_id": product["id"],
            "quantity": 5
        }
    )

    assert inventory_response.status_code == 200

    data = inventory_response.json()

    assert data["id"] == 1
    assert data["shelf_id"] == shelf["id"]
    assert data["product_id"] == product["id"]
    assert data["name"] == "Kalem"
    assert data["class_name"] == "pen"
    assert data["quantity"] == 5

def test_get_inventory(client):

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

    # Inventory oluştur
    inventory_response = client.post(
        "/api/v1/inventory/",
        json={
            "shelf_id": shelf["id"],
            "product_id": product["id"],
            "quantity": 5
        }
    )

    assert inventory_response.status_code == 200

    # Inventory getir
    response = client.get(
        f"/api/v1/inventory/shelf/{shelf['id']}"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1

    item = data[0]

    assert item["shelf_id"] == shelf["id"]
    assert item["product_id"] == product["id"]
    assert item["name"] == "Kalem"
    assert item["class_name"] == "pen"
    assert item["quantity"] == 5    