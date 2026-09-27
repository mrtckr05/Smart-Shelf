import pytest

from app.services.monitoring_service import MonitoringService


class FakeCameraManager:

    def __init__(self, counts):
        self.counts = counts

    def get_latest_counts(self):
        return self.counts.copy()


def test_inventory_change_detection():

    service = MonitoringService(
        camera_manager=None,
        shelf_id=1
    )

    inventory = {
        "pen": 5,
        "cup": 2
    }

    # Aynı miktarlar → değişiklik yok
    counts = {
        "pen": 5,
        "cup": 2
    }

    assert service._has_changed(
        inventory,
        counts
    ) is False

    # Kalem miktarı değişti → değişiklik var
    counts = {
        "pen": 6,
        "cup": 2
    }

    assert service._has_changed(
        inventory,
        counts
    ) is True


@pytest.mark.anyio
async def test_confirmation_updates_inventory(
    client,
    db,
    monkeypatch
):

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

    # Kamera her seferinde 6 görüyor
    fake_camera = FakeCameraManager(
        {
            "pen": 6
        }
    )

    # MonitoringService'in DB'sini test DB'sine bağla
    monkeypatch.setattr(
        "app.services.monitoring_service.SessionLocal",
        lambda: db
    )

    # Confirmation beklemelerini kaldır
    async def fake_sleep(seconds):
        pass

    monkeypatch.setattr(
        "app.services.monitoring_service.asyncio.sleep",
        fake_sleep
    )

    service = MonitoringService(
        camera_manager=fake_camera,
        shelf_id=shelf["id"]
    )

    # Gerçek confirmation akışı
    await service.confirm_change()

    # Inventory kontrolü
    response = client.get(
        f"/api/v1/inventory/shelf/{shelf['id']}"
    )

    assert response.status_code == 200

    inventory = response.json()

    assert len(inventory) == 1
    assert inventory[0]["quantity"] == 6