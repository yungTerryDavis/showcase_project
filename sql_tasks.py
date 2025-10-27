from collections.abc import Awaitable
import io
from typing import Callable, TypeVar, final

import dataframe_image as dfi
import pandas as pd
from sqlalchemy import ScalarResult

from database import Base


T = TypeVar("T", bound=Base)
type Solution = tuple[dict[str, list[str]], int]
type AwaitableSolution = Awaitable[Solution]


@final
class SQLTasks:
    """Class with tools for working with sql-ex tasks
    """
    _registry: dict[int, Callable[..., AwaitableSolution]] = {}

    @classmethod
    def add_to_registry(
        cls,
        task_id: int
    ) -> Callable[
        [Callable[..., AwaitableSolution]],
        Callable[..., AwaitableSolution]
        ]:
        def decorator(
            func: Callable[..., AwaitableSolution]
        ) -> Callable[..., AwaitableSolution]:
            cls._registry[task_id] = func
            return func
        return decorator

    @staticmethod
    def get_solution(scalars: ScalarResult[T], fields_map: dict[str, list[str]]
    ) -> Solution:
        """Method to make a dict out of scalars.
        Works for 1-type (1-model) scalars only
        """
        items = scalars.all()
        print(items[0].__dict__)
        rows_n = len(items)
        if not rows_n:
            return {}, 0

        model_name, fields = next(iter(fields_map.items()))
        res = {
            f"{model_name}.{field}": [str(obj.__dict__.get(field, "")) for obj in items]
            for field in fields
        }

        return res, rows_n

    @staticmethod
    def _res_as_pseudotable(solution_dict: dict[str, list[str]], rows_n: int) -> dict[str, list[str]]:
        res: dict[str, list[str]] = {"headers": [], "rows": []}
        for h in solution_dict.keys():
            res["headers"].append(h)
        for i in range(rows_n):
            row: list[str] = []
            for h in solution_dict.keys():
                row.append(solution_dict[h][i])
            res["rows"].append(" ".join(row))
        return res

    async def get_solution_dict(self, task_id: int, pseudo_table: bool = True) -> dict[str, list[str]]:
        solution_dict: dict[str, list[str]]
        rows_n: int
        if not self._registry:
            import sql_solutions as _

        solution_func = self._registry.get(task_id)
        if not solution_func:
            raise ValueError(f"No solution for task {task_id}")

        solution_dict, rows_n = await solution_func()

        if pseudo_table:
            res = self._res_as_pseudotable(solution_dict, rows_n)
        else:
            res = solution_dict

        return res

    async def get_solution_image(self, task_id: int) -> bytes:
        solution_dict: dict[str, list[str]]
        if not self._registry:
            import sql_solutions as _

        solution_func = self._registry.get(task_id)
        if not solution_func:
            raise ValueError(f"No solution for task {task_id}")

        solution_dict, _ = await solution_func()

        res_df = pd.DataFrame(solution_dict)
        res_df.index += 1
        buf = io.BytesIO()

        await dfi.export_async(
            res_df,
            buf,
            table_conversion="matplotlib"
        )
        _ = buf.seek(0)

        return buf.getvalue()
