# 02 - Urgent Shipment Queue

Shipments are enqueued with a priority from 1 (most urgent) to 5 (least urgent). Processing always takes the most urgent one next, and ties go to whichever arrived first.

**Data structure:** heap (`heapq`) for the queue, `deque` for recent history
**Python concepts:** tuples, generators
**Backend idea:** enqueue and process-next endpoints

## How it works

- **Heap of tuples.** Each entry is `(priority, arrival_number, shipment)`. Python compares tuples element by element, so the lowest priority number pops first. `arrival_number` (from `itertools.count()`) breaks ties first in, first out, and stops Python from ever comparing two `Shipment` objects, which would raise a `TypeError`.
- **Generator for listing.** `in_processing_order()` pops from a *copy* of the heap and yields one shipment at a time, so `GET /shipments` shows the real processing order without removing anything.
- **Bounded deque for history.** `deque(maxlen=10)` keeps the last 10 processed shipments, newest first, and drops the oldest automatically.
- **Set for duplicates.** `queued_ids` gives an O(1) check so the same shipment can't be queued twice.

## Endpoints

| Method | Path | What it does |
|--------|------|--------------|
| POST | `/shipments` | Enqueue a shipment (409 if already queued) |
| GET | `/shipments` | List the queue in processing order |
| GET | `/shipments/next` | Peek at the next shipment without removing it (404 if empty) |
| POST | `/shipments/process-next` | Remove and return the next shipment (404 if empty) |
| GET | `/history` | Last 10 processed shipments, newest first |

Example body for `POST /shipments`:

```json
{"shipment_id": "SHP-0001", "destination": "Rotterdam", "priority": 1}
```

## Run

```bash
cd 02-urgent-shipment-queue
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Open http://127.0.0.1:8000/docs to try every endpoint.

## Test

Run from inside this folder:

```bash
pytest
```

## Notes

- The queue lives in memory, so it resets whenever the server restarts.
- UI (a list with a "process next" button) is still to do.
