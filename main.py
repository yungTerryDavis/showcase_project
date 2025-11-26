from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Response
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from schemas import CreateMovieSchema, MovieSchema, UpdateMovieSchema
from service import MovieService
from sql_tasks import SQLTasks
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


@app.get("/sql_solutions/{task_id}")
async def get_sql_solution_dict(task_id: int, pseudo_table: bool = True):
    SQLT = SQLTasks()
    try:
        res = await SQLT.get_solution_dict(task_id, pseudo_table)
    except (ValueError, RuntimeError) as e:
        return Response(str(e), status_code=HTTP_404_NOT_FOUND)

    return res


@app.get("/sql_solutions/{task_id}/table")
async def get_sql_solution_image(task_id: int, download: bool = False):
    SQLT = SQLTasks()
    try:
        res = await SQLT.get_solution_image(task_id)
    except (ValueError, RuntimeError) as e:
        return Response(str(e), status_code=HTTP_404_NOT_FOUND)

    headers: dict[str, str] = {}
    if download:
        headers["Content-Disposition"] = f"attachment; filename='solution_{task_id}.png'"

    return Response(
        res,
        media_type="image/png",
        headers=headers
    )


@app.get("/movie/all", response_model=list[MovieSchema])
async def index_movies():
    movie_service = MovieService()
    return await movie_service.list_movies()


@app.post("/movie", status_code=HTTP_201_CREATED)
async def add_movie(payload: CreateMovieSchema):
    movie_service = MovieService()
    movie_id = await movie_service.add_movie(payload)
    return {"id": movie_id}


@app.put("/movie/{id}")
async def update_movie(id: int, payload: UpdateMovieSchema):
    movie_service = MovieService()
    try:
        _ = await movie_service.update_movie(id, payload)
    except Exception as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    return {"status": "ok", "id": id}


@app.delete("/movie/{id}")
async def delete_movie(id: int):
    movie_service = MovieService()
    try:
        _ = await movie_service.delete_movie(id)
    except Exception as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    return {"status": "ok", "id": id}
