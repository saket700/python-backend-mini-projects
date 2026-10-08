from fastapi.testclient import TestClient
from main import app, db

client = TestClient(app)


def setup_function():
    db.clear()


def test_create_and_get():
    body = {"container_id": "MSKU1234567", "weight_kg": 1200}
    assert client.post("/containers", json=body).status_code == 201
    assert client.get("/containers/MSKU1234567").json()["weight_kg"] == 1200


def test_duplicate_rejected():
    body = {"container_id": "MSKU1234567", "weight_kg": 1200}
    client.post("/containers", json=body)
    assert client.post("/containers", json=body).status_code == 409


def test_invalid_weight_rejected():
    body = {"container_id": "MSKU1234567", "weight_kg": -5}
    assert client.post("/containers", json=body).status_code == 422