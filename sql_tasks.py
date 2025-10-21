from collections import defaultdict
from decimal import Decimal
from typing import TypeVar, final

from sqlalchemy import ScalarResult

from database import Base
from repository import SQLExRepository as REPO


T = TypeVar("T", bound=Base)


@final
class SQLTasks:
    def __init__(self) -> None:
        self.solutions = {
            1: self.solution_1,
            2: self.solution_2,
            3: self.solution_3,
            4: self.solution_4,
            5: self.solution_5,
        }

    def _get_solution_dict(self, scalars: ScalarResult[T], fields_map: dict[str, list[str]]
    ) -> tuple[dict[str, list[str]], int]:
        """
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

    async def get_solution(self, task_id: int, pseudo_table: bool = True) -> dict[str, list[str]]:
        solution_dict: dict[str, list[str]]
        rows_n: int

        solution_func = self.solutions.get(task_id)
        if not solution_func:
            raise ValueError(f"No solution for task {task_id}")

        solution_dict, rows_n = await solution_func()

        if pseudo_table:
            res: dict[str, list[str]] = {"headers": [], "rows": []}
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

    async def solution_1(self):
        pcs = await REPO.get_pcs_cheaper(Decimal(500))
        fields = {"pc": ["model", "speed", "hd"]}
        return self._get_solution_dict(pcs, fields)

    async def solution_2(self):
        makers = await REPO.get_makers_of_type("Printer")
        rows_n = 0
        res: dict[str, list[str]] = defaultdict(list)
        for maker in makers:
            res["product.maker"].append(str(maker))
            rows_n += 1

        return dict(res), rows_n

    async def solution_3(self):
        laptops = await REPO.get_laptops_more_expensive(Decimal(1000))
        fields = {"laptop": ["model", "ram", "screen"]}
        return self._get_solution_dict(laptops, fields)

    async def solution_4(self):
        printers = await REPO.get_printers_colored("y")
        fields = {"printer": ["code", "model", "color", "type_", "price"]}
        return self._get_solution_dict(printers, fields)

    async def solution_5(self):
        pcs = await REPO.get_pcs_cheaper_filter_cds(
            ["12x", "24x"], Decimal(600)
        )
        fields = {"pc": ["model", "speed", "hd"]}
        return self._get_solution_dict(pcs, fields)
