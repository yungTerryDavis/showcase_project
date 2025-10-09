from contextlib import asynccontextmanager

from fastapi import FastAPI

from utils import is_db_data_present, populate_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not await is_db_data_present():
        print("No data found. Populating DB...")
        await populate_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root():
    return {"Hello": "World!"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
