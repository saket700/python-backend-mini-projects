from fastapi.testclient import TestClient
from main import app, heap, history, queued_ids

client = TestClient(app)


def setup_function():
    heap.clear()
    queued_ids.clear()
    history.clear()


def add(shipment_id: str, priority: int, destination: str = "Rotterdam"):
    body = {"shipment_id": shipment_id, "destination": destination, "priority": priority}
    return client.post("/shipments", json=body)


def test_urgent_shipment_jumps_the_queue():
    add("SHP-001", priority=3)
    add("SHP-002", priority=1)
    assert client.post("/shipments/process-next").json()["shipment_id"] == "SHP-002"


def test_same_priority_is_first_in_first_out_then_queue_empties():
    add("SHP-001", priority=2)
    add("SHP-002", priority=2)
    assert client.post("/shipments/process-next").json()["shipment_id"] == "SHP-001"
    assert client.post("/shipments/process-next").json()["shipment_id"] == "SHP-002"
    assert client.post("/shipments/process-next").status_code == 404


def test_list_is_in_processing_order_and_does_not_remove():
    add("SHP-001", priority=3)
    add("SHP-002", priority=1)
    add("SHP-003", priority=2)
    ids = [s["shipment_id"] for s in client.get("/shipments").json()]
    assert ids == ["SHP-002", "SHP-003", "SHP-001"]
    assert len(client.get("/shipments").json()) == 3  # listing did not pop anything


def test_duplicate_rejected():
    add("SHP-001", priority=2)
    assert add("SHP-001", priority=1).status_code == 409


def test_history_keeps_only_last_10_newest_first():
    for i in range(12):
        add(f"SHP-{i:03d}", priority=3)
        client.post("/shipments/process-next")
    ids = [s["shipment_id"] for s in client.get("/history").json()]
    assert len(ids) == 10
    assert ids[0] == "SHP-011"
    assert ids[-1] == "SHP-002"
