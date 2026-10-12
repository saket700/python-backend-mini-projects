import heapq
import itertools
from collections import deque
from collections.abc import Iterator

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

app = FastAPI(title="Urgent Shipment Queue")


class Shipment(BaseModel):
    shipment_id: str = Field(min_length=3, max_length=20)  # e.g. SHP-0001
    destination: str = Field(min_length=1, max_length=50)  # e.g. Rotterdam
    priority: int = Field(ge=1, le=5)  # 1 = most urgent, 5 = least urgent

    @field_validator("shipment_id", "destination")
    @classmethod
    def normalize_whitespace(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("must not be blank")
        return cleaned


# Heap entries are tuples: (priority, arrival_number, shipment).
# Python compares tuples element by element, so the lowest priority number comes
# out first. arrival_number breaks ties (first in, first out) and also means
# Python never has to compare two Shipment objects, which would raise TypeError.
heap: list[tuple[int, int, Shipment]] = []
arrival = itertools.count()  # 0, 1, 2, ... one number per enqueue
queued_ids: set[str] = set()  # O(1) duplicate check
history: deque[Shipment] = deque(maxlen=10)  # last 10 processed, newest first


def in_processing_order() -> Iterator[Shipment]:
    """Yield queued shipments in the order they will be processed.

    A generator: each shipment is produced only when the caller asks for the
    next one. It works on a copy, so the real heap is never changed.
    """
    copy = list(heap)  # a copy of a valid heap is still a valid heap
    while copy:
        _, _, shipment = heapq.heappop(copy)
        yield shipment


@app.post("/shipments", status_code=201)
def enqueue(s: Shipment) -> Shipment:
    shipment_key = s.shipment_id.lower()
    if shipment_key in queued_ids:
        raise HTTPException(status_code=409, detail="Shipment already in the queue")
    heapq.heappush(heap, (s.priority, next(arrival), s))
    queued_ids.add(shipment_key)
    return s


@app.get("/shipments")
def list_queue() -> list[Shipment]:
    return list(in_processing_order())


@app.get("/shipments/next")
def peek_next() -> Shipment:
    if not heap:
        raise HTTPException(status_code=404, detail="Queue is empty")
    return heap[0][2]  # heap[0] is always the smallest entry, so the next one up


@app.post("/shipments/process-next")
def process_next() -> Shipment:
    if not heap:
        raise HTTPException(status_code=404, detail="Queue is empty")
    _, _, shipment = heapq.heappop(heap)
    queued_ids.discard(shipment.shipment_id.lower())
    history.appendleft(shipment)  # deque with maxlen drops the oldest automatically
    return shipment


@app.get("/history")
def recent_history() -> list[Shipment]:
    return list(history)
