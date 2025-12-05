from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from movie_service.app.api.movies import MovieService
from movie_service.app.api.schemas import CreateMovieSchema, MovieSchema, UpdateMovieSchema

movies = APIRouter()

@movies.get("/all", response_model=list[MovieSchema])
async def index_movies():
    movie_service = MovieService()
    return await movie_service.list_movies()


@movies.post("", status_code=HTTP_201_CREATED)
async def add_movie(payload: CreateMovieSchema):
    movie_service = MovieService()
    movie_id = await movie_service.add_movie(payload)
    return {"id": movie_id}


@movies.put("/{id}")
async def update_movie(id: int, payload: UpdateMovieSchema):
    movie_service = MovieService()
    try:
        _ = await movie_service.update_movie(id, payload)
    except Exception as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    return {"status": "ok", "id": id}


@movies.delete("/{id}")
async def delete_movie(id: int):
    movie_service = MovieService()
    try:
        _ = await movie_service.delete_movie(id)
    except Exception as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    return {"status": "ok", "id": id}
