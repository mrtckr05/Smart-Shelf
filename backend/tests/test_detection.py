import app.api.v1.endpoints.detection as detection_endpoint


def test_detect_image(client, monkeypatch):

    def mock_detect_and_count(image_path):
        return {
            "cup": 2,
            "pen": 3
        }

    monkeypatch.setattr(
        detection_endpoint,
        "detect_and_count",
        mock_detect_and_count
    )

    response = client.post(
        "/api/v1/detection/image",
        files={
            "file": (
                "test.jpg",
                b"fake image data",
                "image/jpeg"
            )
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["counts"] == {
        "cup": 2,
        "pen": 3
    }