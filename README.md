# Python Backend Mini-Projects

A series of small, time-boxed backend projects built in shipping and logistics terms. Each one centres on **one data structure, one Python concept, and one backend idea**, with a tiny UI to prove the loop works.

## Rules for every project

- **Time box:** 3 days each. If stuck on day 4, ship what works and move on.
- **Size cap:** 5 endpoints or fewer, one UI page, 3-5 pytest tests, and a short README.
- **One new idea at a time:** the data structure is the star; everything else stays minimal.
- **No database at first:** start with an in-memory store so the data structure itself is what gets learned. A real database gets its own dedicated project later.
- **UI:** Vite + React + TypeScript with plain `fetch`, one page, no styling libraries.

## Projects

| # | Project | Data structure | Python concept | Backend idea | Tiny UI | Status |
|---|---------|----------------|----------------|--------------|---------|--------|
| 1 | [Container tracker](./01-container-tracker) | dict, set | dataclasses, type hints, Pydantic | CRUD, validation, duplicate detection | Table plus add form | In progress |
| 2 | Urgent shipment queue | heap (`heapq`), `deque` | generators, tuples | enqueue and process-next endpoints | List with "process next" button | Planned |
| 3 | Route finder | graph (BFS, then Dijkstra) | `defaultdict`, recursion | query params, error cases | Two dropdowns, shows the path | Planned |
| 4 | Freight rate cache | LRU (`OrderedDict`) | decorators, `functools` | cache-aside, TTL | Lookup box showing hit or miss | Planned |
| 5 | Login rate limiter | sliding window with `deque` | middleware, `async` | 429 responses, rate limiting | Button you can spam to see the limit | Planned |
| 6 | Parallel port lookups | none (concurrency focus) | `asyncio.gather` | async endpoints, timeouts | Sequential vs. parallel timing | Planned |

## Tech stack

- **Backend:** Python 3.12+, FastAPI, Pydantic, pytest
- **Frontend:** Vite, React, TypeScript

## Running a project

Each project lives in its own numbered folder with its own virtual environment and README.

```bash
cd 01-container-tracker
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

FastAPI serves interactive API docs at http://127.0.0.1:8000/docs, so every endpoint can be tried without a UI.

Run the tests with:

```bash
pytest
```

## Repo layout

```
python-backend-mini-projects/
├── 01-container-tracker/
├── 02-.../
├── .gitignore
└── README.md
```
