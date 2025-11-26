from decimal import Decimal
import typing

from sqlalchemy import (
    CursorResult,
    Numeric,
    cast,
    delete,
    except_,
    func,
    select,
    union,
    update,
)

from database import Base, async_session_maker
from models import Laptop, Movie, PC, Printer, Product


async def get_objects_count(model: type[Base]) -> int:
    async with async_session_maker() as session:
        stmt = select(func.count()).select_from(model)
        return await session.scalar(stmt) or 0


class SQLExRepository:
    @staticmethod
    async def get_pcs_cheaper(value: Decimal):
        async with async_session_maker() as session:
            stmt = (
                select(PC)
                .where(cast(PC.price, Numeric) < value)
            )
            return await session.scalars(stmt)

    @staticmethod
    async def get_makers_of_type(product_type: str):
        async with async_session_maker() as session:
            stmt = (
                select(Product.maker)
                .where(Product.type_ == product_type)
                .distinct()
            )
            return await session.scalars(stmt)

    @staticmethod
    async def get_laptops_more_expensive(value: Decimal):
        async with async_session_maker() as session:
            stmt = (
                select(Laptop)
                .where(cast(Laptop.price, Numeric) > value)
            )
            return await session.scalars(stmt)

    @staticmethod
    async def get_printers_colored(colored: str):  # might be enum
        async with async_session_maker() as session:
            stmt = (
                select(Printer)
                .where(Printer.color == colored)
            )
            return await session.scalars(stmt)

    @staticmethod
    async def get_pcs_cheaper_filter_cds(cds: list[str], price: Decimal):
        async with async_session_maker() as session:
            stmt = (
                select(PC)
                .where(PC.cd.in_(cds))
                .where(cast(PC.price, Numeric) < price)
            )
            return await session.scalars(stmt)

    @staticmethod
    async def get_laptop_maker_speed_filter_hd(hd: float):
        async with async_session_maker() as session:
            stmt = (
                select(Product.maker, Laptop.speed)
                .join(Laptop)
                .where(Laptop.hd >= hd)
                .distinct()
            )
            return await session.scalars(stmt)

    @staticmethod
    async def get_all_product_price_of_maker(maker: str):
        async with async_session_maker() as session:
            u_subq = union(
                select(PC.model, PC.price),
                select(Laptop.model, Laptop.price),
                select(Printer.model, Printer.price)
            ).subquery(name="a")

            stmt = select(
                Product.model,
                u_subq.c.price
            ).join_from(
                Product,
                u_subq
            ).where(
                Product.maker == maker
            )

            print(stmt)
            return await session.execute(stmt)

    @staticmethod
    async def get_makers_pc_not_laptop():
        async with async_session_maker() as session:
            stmt = except_(
                select(Product.maker).where(Product.type_ == "PC"),
                select(Product.maker).where(Product.type_ == "Laptop")
            )
            return await session.execute(stmt)

    @staticmethod
    async def get_pc_makers_filter_speed(speed: int):
        async with async_session_maker() as session:
            stmt = (
            select(Product.maker)
            .join(PC)
            .where(PC.speed >= speed)
            .distinct()
            )

            return await session.execute(stmt)

    @staticmethod
    async def get_printers_with_max_price():
        async with async_session_maker() as session:
            subq = select(func.max(Printer.price)).scalar_subquery()
            stmt = (
                select(Printer.model, Printer.price)
                .where(Printer.price == subq)
            )

            return await session.execute(stmt)


class GeneralRepository:
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
