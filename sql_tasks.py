from collections import defaultdict
from collections.abc import Awaitable
from decimal import Decimal
from typing import Callable, TypeVar, final

from sqlalchemy import ScalarResult

from database import Base
from repository import SQLExRepository as REPO


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
    def get_solution_dict(scalars: ScalarResult[T], fields_map: dict[str, list[str]]
    ) -> Solution:
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

        solution_func = self._registry.get(task_id)
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

@SQLTasks.add_to_registry(1)
async def solution_1():
    pcs = await REPO.get_pcs_cheaper(Decimal(500))
    fields = {"pc": ["model", "speed", "hd"]}
    return SQLTasks.get_solution_dict(pcs, fields)

@SQLTasks.add_to_registry(2)
async def solution_2():
    makers = await REPO.get_makers_of_type("Printer")
    rows_n = 0
    res: dict[str, list[str]] = defaultdict(list)
    for maker in makers:
        res["product.maker"].append(str(maker))
        rows_n += 1
    return dict(res), rows_n

@SQLTasks.add_to_registry(3)
async def solution_3():
    laptops = await REPO.get_laptops_more_expensive(Decimal(1000))
    fields = {"laptop": ["model", "ram", "screen"]}
    return SQLTasks.get_solution_dict(laptops, fields)

@SQLTasks.add_to_registry(4)
async def solution_4():
    printers = await REPO.get_printers_colored("y")
    fields = {"printer": ["code", "model", "color", "type_", "price"]}
    return SQLTasks.get_solution_dict(printers, fields)

@SQLTasks.add_to_registry(5)
async def solution_5():
    pcs = await REPO.get_pcs_cheaper_filter_cds(
        ["12x", "24x"], Decimal(600)
    )
    fields = {"pc": ["model", "speed", "hd"]}
    return SQLTasks.get_solution_dict(pcs, fields)

@SQLTasks.add_to_registry(6)
async def solution_6():
    rows = await REPO.get_laptop_maker_speed_filter_hd(10)
    rows_n = 0
    res: dict[str, list[str]] = defaultdict(list)
    for row in rows.all():
        res["product.maker"].append(str(row[0]))
        res["laptop.speed"].append(str(row[1]))
        rows_n += 1

    return dict(res), rows_n
