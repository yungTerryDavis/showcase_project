from decimal import Decimal

from sqlalchemy import cast, func, select, Numeric

from database import Base, async_session_maker
from models import PC, Printer, Product, Laptop


async def get_objects_count(model: type[Base]) -> int:
    async with async_session_maker() as session:
        stmt = select(func.count()).select_from(model)
        return await session.scalar(stmt) or 0


class SQLExRepository:
    @classmethod
    async def get_pcs_cheaper(cls, value: Decimal):
        async with async_session_maker() as session:
            stmt = select(PC).where(cast(PC.price, Numeric) < value)
            return await session.scalars(stmt)

    @classmethod
    async def get_makers_of_type(cls, product_type: str):
        async with async_session_maker() as session:
            stmt = select(Product.maker).where(Product.type_ == product_type).distinct()
            return await session.scalars(stmt)

    @classmethod
    async def get_laptops_more_expensive(cls, value: Decimal):
        async with async_session_maker() as session:
            stmt = select(Laptop).where(cast(Laptop.price, Numeric) > value)
            return await session.scalars(stmt)

    @classmethod
    async def get_printers_colored(cls, colored: str):  # might be enum
        async with async_session_maker() as session:
            stmt = select(Printer).where(Printer.color == colored)
            return await session.scalars(stmt)

    @classmethod
    async def get_pcs_cheaper_filter_cds(cls, cds: list[str], price: Decimal):
        async with async_session_maker() as session:
            stmt = (
            select(PC)
            .where(PC.cd.in_(cds))
            .where(cast(PC.price, Numeric) < price)
            )
            return await session.scalars(stmt)
