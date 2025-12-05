from contextlib import asynccontextmanager

from fastapi import FastAPI

from movie_service.app.database import async_session_maker
from movie_service.app.api.utils import is_db_data_present, populate_movies_db
from movie_service.app.api.routes import movies

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not await is_db_data_present():
        print("No data found. Populating DB...")
        async with async_session_maker() as session:
            await populate_movies_db(session)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(movies, prefix="/api/v1/movies", tags=["movies"])
