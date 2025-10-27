from decimal import Decimal

from sqlalchemy import cast, except_, func, select, Numeric, union

from database import Base, async_session_maker
from models import PC, Printer, Product, Laptop


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
            return await session.execute(stmt)

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
