from decimal import Decimal

from sqlalchemy import cast, func, select, Numeric

from database import Base, async_session_maker
from models import PC


async def get_objects_count(model: type[Base]) -> int:
    async with async_session_maker() as session:
        stmt = select(func.count()).select_from(model)
        return await session.scalar(stmt) or 0


async def get_pcs_cheaper(value: Decimal):
    async with async_session_maker() as session:
        stmt = select(PC).where(cast(PC.price, Numeric) < value)
        res = await session.scalars(stmt)
        return res
