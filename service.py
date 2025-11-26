from models import Movie
from repository import GeneralRepository as REPO
from schemas import CreateMovieSchema, UpdateMovieSchema


class MovieService:
    async def list_movies(self):
        return await REPO.list_movies()

    async def add_movie(self, movie: CreateMovieSchema):
        new_movie = Movie(**movie.model_dump())
        return await REPO.add_movie(new_movie)

    async def update_movie(self, id: int, movie: UpdateMovieSchema):
        if await REPO.get_movie(id):  # add walrus op?
            rows_affected = await REPO.update_movie(id, movie.model_dump())
        else:
            raise IndexError(f"No movie with id {id}")
        return bool(rows_affected)

    async def delete_movie(self, id: int):
        if await REPO.get_movie(id):  # add walrus op?
            rows_affected = await REPO.delete_movie(id)
        else:
            raise IndexError(f"No movie with id {id}")
        return bool(rows_affected)
