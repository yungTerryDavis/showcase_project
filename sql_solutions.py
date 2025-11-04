from collections import defaultdict
from decimal import Decimal

from sql_tasks import SQLTasks
from repository import SQLExRepository as REPO

print("sql_solutions")

@SQLTasks.add_to_registry(1)
async def solution_1():
    pcs = await REPO.get_pcs_cheaper(Decimal(500))
    fields = {"pc": ["model", "speed", "hd"]}
    return SQLTasks.get_solution(pcs, fields)


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
    return SQLTasks.get_solution(laptops, fields)


@SQLTasks.add_to_registry(4)
async def solution_4():
    printers = await REPO.get_printers_colored("y")
    fields = {"printer": ["code", "model", "color", "type_", "price"]}
    return SQLTasks.get_solution(printers, fields)


@SQLTasks.add_to_registry(5)
async def solution_5():
    pcs = await REPO.get_pcs_cheaper_filter_cds(
        ["12x", "24x"], Decimal(600)
    )
    fields = {"pc": ["model", "speed", "hd"]}
    return SQLTasks.get_solution(pcs, fields)


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


@SQLTasks.add_to_registry(7)
async def solution_7():
    rows = await REPO.get_all_product_price_of_maker("B")
    rows_n = 0
    res: dict[str, list[str]] = defaultdict(list)
    for row in rows.all():
        res["model"].append(str(row[0]))
        res["price"].append(str(row[1]))
        rows_n += 1

    return dict(res), rows_n


@SQLTasks.add_to_registry(8)
async def solution_8():
    rows = await REPO.get_makers_pc_not_laptop()
    rows_n = 0
    res: dict[str, list[str]] = defaultdict(list)
    for row in rows.all():
        res["maker"].append(str(row[0]))
        rows_n += 1

    return dict(res), rows_n


@SQLTasks.add_to_registry(9)
async def solution_9():
    rows = await REPO.get_pc_makers_filter_speed(450)
    rows_n = 0
    res: dict[str, list[str]] = defaultdict(list)
    for row in rows.all():
        res["maker"].append(str(row[0]))
        rows_n += 1

    return dict(res), rows_n


@SQLTasks.add_to_registry(10)
async def solution_10():
    rows = await REPO.get_printers_with_max_price()
    rows_n = 0
    res: dict[str, list[str]] = defaultdict(list)

    for row in rows.all():
        res["model"].append(str(row[0]))
        res["price"].append(str(row[1]))
        rows_n += 1

    return dict(res), rows_n
