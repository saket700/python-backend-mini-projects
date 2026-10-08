from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Container Tracker")


class Container(BaseModel):
    container_id: str = Field(min_length=11, max_length=11)  # e.g. MSKU1234567
    weight_kg: float = Field(gt=0)
    status: str = "booked"


db: dict[str, Container] = {}   # container_id -> Container (hash lookup, O(1))


@app.post("/containers", status_code=201)
def create(c: Container) -> Container:
    if c.container_id in db:
        raise HTTPException(status_code=409, detail="Container already exists")
    db[c.container_id] = c
    return c


@app.get("/containers")
def list_all() -> list[Container]:
    return list(db.values())


@app.get("/containers/{container_id}")
def get_one(container_id: str) -> Container:
    if container_id not in db:
        raise HTTPException(status_code=404, detail="Not found")
    return db[container_id]


@app.put("/containers/{container_id}")
def update(container_id: str, c: Container) -> Container:
    if container_id not in db:
        raise HTTPException(status_code=404, detail="Not found")
    db[container_id] = c
    return c


@app.delete("/containers/{container_id}", status_code=204)
def delete(container_id: str) -> None:
    if db.pop(container_id, None) is None:
        raise HTTPException(status_code=404, detail="Not found")