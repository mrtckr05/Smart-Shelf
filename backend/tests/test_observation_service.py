from app.services.observation_service import create_observation_from_counts


def test_create_observation_from_counts(client, db):

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

    # Counts → Observation
    observation = create_observation_from_counts(
        db=db,
        shelf_id=shelf["id"],
        counts={
            "pen": 5
        }
    )

    assert observation.shelf_id == shelf["id"]
    assert len(observation.products) == 1

    observed_product = observation.products[0]

    assert observed_product.product_id == product["id"]
    assert observed_product.quantity == 5


import pytest

from fastapi import HTTPException
from app.services.observation_service import create_observation_from_counts


def test_create_observation_from_counts_unknown_product(client, db):

    # Shelf oluştur
    shelf_response = client.post(
        "/api/v1/shelf/",
        json={
            "name": "Ana Raf"
        }
    )

    assert shelf_response.status_code == 200

    shelf = shelf_response.json()

    # DB'de olmayan bir class gönder
    with pytest.raises(HTTPException) as exc_info:

        create_observation_from_counts(
            db=db,
            shelf_id=shelf["id"],
            counts={
                "banana": 3
            }
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Product bulunamadı: banana"    