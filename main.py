from contextlib import asynccontextmanager

from fastapi import FastAPI

from utils import is_db_data_present, populate_db
from sql_tasks import SQLTasks


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
async def get_sql_solution(task_id: int):
    SQLT = SQLTasks()
    solution_dict, rows_n = await SQLT.get_solution(task_id)
    res: dict[str, list[str]] = {"headers": [], "rows": []}

    for h in solution_dict.keys():
        res["headers"].append(h)
    for i in range(rows_n):
        row: list[str] = []
        for h in solution_dict.keys():
            row.append(solution_dict[h][i])
        res["rows"].append(" ".join(row))

    return res
