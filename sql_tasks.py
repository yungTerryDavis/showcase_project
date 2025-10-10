from collections import defaultdict
from decimal import Decimal

from repository import SQLExRepository

class SQLTasks:
    def _get_solution_dict(self) -> dict[str, str]:
        ...

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
        pcs = await SQLExRepository.get_pcs_cheaper(Decimal(500))
        rows_n = 0
        res = defaultdict(list)
        for pc in pcs:
            res["pc.model"].append(str(pc.model))
            res["pc.speed"].append(str(pc.speed))
            res["pc.hd"].append(str(pc.hd))
            rows_n += 1

        return dict(res), rows_n

    async def solution_2(self) -> tuple[dict[str, list[str]], int]:
        makers = await SQLExRepository.get_makers_of_type("Printer")
        rows_n = 0
        res = defaultdict(list)
        for maker in makers:
            res["product.maker"].append(str(maker))
            rows_n += 1

        return dict(res), rows_n

    async def solution_3(self):
        laptops = await SQLExRepository.get_laptops_more_expensive(Decimal(1000))
        rows_n = 0
        res = defaultdict(list)
        for laptop in laptops:
            res["laptop.model"].append(str(laptop.model))
            res["laptop.ram"].append(str(laptop.ram))
            res["laptop.screen"].append(str(laptop.screen))
            rows_n += 1

        return dict(res), rows_n

    async def solution_4(self):
        printers = await SQLExRepository.get_printers_colored("y")
        rows_n = 0
        res = defaultdict(list)
        for printer in printers:
            res["printer.code"].append(str(printer.code))
            res["printer.model"].append(str(printer.model))
            res["printer.color"].append(str(printer.color))
            res["printer.type_"].append(str(printer.type_.value))
            res["printer.price"].append(str(printer.price))
            rows_n += 1

        return dict(res), rows_n

    async def solution_5(self):
        pcs = await SQLExRepository.get_pcs_cheaper_filter_cds(
            ["12x", "24x"], Decimal(600)
        )
        rows_n = 0
        res = defaultdict(list)
        for pc in pcs:
            res["pc.model"].append(str(pc.model))
            res["pc.speed"].append(str(pc.speed))
            res["pc.hd"].append(str(pc.hd))
            rows_n += 1

        return dict(res), rows_n
