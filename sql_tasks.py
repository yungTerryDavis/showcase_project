from collections import defaultdict
from decimal import Decimal
from typing import Any

from repository import get_pcs_cheaper

class SQLTasks:
    async def get_solution(self, task_id: int, pseudo_table: bool = True) -> dict[str, list[str]]:
        func_name = f"solution_{task_id}"
        func = getattr(self, func_name)
        if func is None:
            raise ValueError(f"No solution for task {task_id}")

        solution_dict: dict[str, list[str]]
        rows_n: int
        res: dict[str, list[str]]
        solution_dict, rows_n = await func()

        if pseudo_table:
            res = {"headers": [], "rows": []}
            for h in solution_dict.keys():
                res["headers"].append(h)
            for i in range(rows_n):
                row: list[str] = []
                for h in solution_dict.keys():
                    row.append(solution_dict[h][i])
                res["rows"].append(" ".join(row))
        else:
            res = solution_dict

        return res

    async def _get_solution_dict(self) -> dict[str, str]:
        ...

    async def solution_1(self) -> tuple[dict[str, list[str]], int]:
        pcs = await get_pcs_cheaper(Decimal("500"))
        rows_n = 0
        res = defaultdict(list)
        for pc in pcs:
            res["pc.model"].append(str(pc.model))
            res["pc.speed"].append(str(pc.speed))
            res["pc.hd"].append(str(pc.hd))
            rows_n += 1
        return dict(res), rows_n
        