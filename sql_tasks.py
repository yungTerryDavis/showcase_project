from collections import defaultdict
from decimal import Decimal
from typing import TypeVar, final

from sqlalchemy import ScalarResult

from database import Base
from repository import SQLExRepository


T = TypeVar("T", bound=Base)


@final
class SQLTasks:
    def __init__(self) -> None:
        self.repository = SQLExRepository()   

    def _get_solution_dict(self, scalars: ScalarResult[T], fields_map: dict[str, list[str]]) -> tuple[dict[str, list[str]], int]:
        """
        Works for 1-type (1-model) scalars only
        """
        rows_n = 0
        res = defaultdict(list)

        for item in scalars:
            for model, fields in fields_map.items():
                for field in fields:
                    res[".".join([model, field])].append(str(getattr(item, field)))
            rows_n += 1

        return dict(res), rows_n

    async def get_solution(self, task_id: int, pseudo_table: bool = True) -> dict[str, list[str]]:
        solution_dict: dict[str, list[str]]
        rows_n: int
        res: dict[str, list[str]]

        func_name = f"solution_{task_id}"
        try:
            func = getattr(self, func_name)
            solution_dict, rows_n = await func()
        except (AttributeError, TypeError) as e:
            print(e)
            raise ValueError(f"No solution for task {task_id}")

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

    async def solution_1(self) -> tuple[dict[str, list[str]], int]:
        pcs = await self.repository.get_pcs_cheaper(Decimal(500))
        fields = {"pc": ["model", "speed", "hd"]}
        return self._get_solution_dict(pcs, fields)

    async def solution_2(self) -> tuple[dict[str, list[str]], int]:
        makers = await self.repository.get_makers_of_type("Printer")
        rows_n = 0
        res = defaultdict(list)
        for maker in makers:
            res["product.maker"].append(str(maker))
            rows_n += 1

        return dict(res), rows_n

    async def solution_3(self) -> tuple[dict[str, list[str]], int]:
        laptops = await self.repository.get_laptops_more_expensive(Decimal(1000))
        fields = {"laptop": ["model", "ram", "screen"]}
        return self._get_solution_dict(laptops, fields)

    async def solution_4(self) -> tuple[dict[str, list[str]], int]:
        printers = await self.repository.get_printers_colored("y")
        fields = {"printer": ["code", "model", "color", "type_", "price"]}
        return self._get_solution_dict(printers, fields)

    async def solution_5(self) -> tuple[dict[str, list[str]], int]:
        pcs = await self.repository.get_pcs_cheaper_filter_cds(
            ["12x", "24x"], Decimal(600)
        )
        fields = {"pc": ["model", "speed", "hd"]}
        return self._get_solution_dict(pcs, fields)
