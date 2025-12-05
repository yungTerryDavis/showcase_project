import typing

from sqlalchemy import CursorResult, delete, func, select, update

from movie_service.app.api.models import Movie
from movie_service.app.database import Base, async_session_maker


async def get_objects_count(model: type[Base]) -> int:
    async with async_session_maker() as session:
        stmt = select(func.count()).select_from(model)
        return await session.scalar(stmt) or 0


class Repository:
    @staticmethod
    async def get_movie(id: int):
        async with async_session_maker() as session:
            stmt = select(Movie).where(Movie.id == id)
            return await session.scalar(stmt)

    @staticmethod
    async def list_movies():
        async with async_session_maker() as session:
            stmt = select(Movie)
            return await session.scalars(stmt)

    @staticmethod
    async def add_movie(movie: Movie) -> int:
        async with async_session_maker() as session:
            session.add(movie)
            await session.commit()
            return movie.id

    @staticmethod
    async def update_movie(id: int, movie_data: dict[str, typing.Any]):
        async with async_session_maker() as session:
            stmt = update(Movie).where(Movie.id == id).values(**movie_data)
            res = typing.cast(
                CursorResult[typing.Any], await session.execute(stmt)
            )
            await session.commit()
            return res.rowcount

    @staticmethod
    async def delete_movie(id: int):
        async with async_session_maker() as session:
            stmt = delete(Movie).where(Movie.id == id)
            res = typing.cast(
                CursorResult[typing.Any], await session.execute(stmt)
            )
            await session.commit()
            return res.rowcount