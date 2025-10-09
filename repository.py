from sqlalchemy import select, func

from database import async_session_maker, Base


async def get_objects_count(model: type[Base]) -> int:
    async with async_session_maker() as session:
        stmt = select(func.count()).select_from(model)
        res = await session.scalar(stmt)
        print("res:", res)
        return res or 0
