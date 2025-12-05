from contextlib import asynccontextmanager

from fastapi import FastAPI, Response
from starlette.status import HTTP_404_NOT_FOUND

from sql_tasks import SQLTasks
from utils import is_db_data_present, populate_db
from database import async_session_maker


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not await is_db_data_present():
        print("No data found. Populating DB...")
        async with async_session_maker() as session:
            await populate_db(session)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root():
    import sys, os
    print(sys.path)
    print(os.getcwd())
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
