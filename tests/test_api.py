from fastapi.testclient import TestClient

from api import app

client = TestClient(app)


def test_health_and_model_info():
    health = client.get("/health")
    info = client.get("/model-info")

    assert health.status_code == 200
    assert health.json() == {"status": "ok", "model": "random_forest"}
    assert info.status_code == 200
    assert info.json()["target"] == "listing_price_usd"


def test_predict_checked_example():
    response = client.post(
        "/predict",
        json={
            "district": "Chilonzor",
            "size_m2": 70,
            "rooms": 3,
            "level": 3,
            "max_levels": 5,
            "is_new_building": False,
        },
    )

    assert response.status_code == 200
    result = response.json()
    assert round(result["estimated_asking_price_usd"]) == 97098
    assert result["warnings"] == []


def test_predict_rejects_impossible_floor():
    response = client.post(
        "/predict",
        json={
            "district": "Chilonzor",
            "size_m2": 70,
            "rooms": 3,
            "level": 9,
            "max_levels": 5,
            "is_new_building": False,
        },
    )

    assert response.status_code == 422
    assert "cannot exceed" in response.json()["detail"]

