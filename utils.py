from enums import PrinterType, ProductType
from models import Laptop, PC, Printer, Product
from database import async_session_maker
from repository import get_objects_count


async def is_db_data_present() -> bool:
    laptops_count = await get_objects_count(Laptop)
    print("Laptops count:", laptops_count)
    return bool(laptops_count)


async def populate_db():
    products = {
        1232: Product(maker="A", model="1232", type_=ProductType.PC),
        1233: Product(maker="A", model="1233", type_=ProductType.PC),
        1276: Product(maker="A", model="1276", type_=ProductType.PRINTER),
        1298: Product(maker="A", model="1298", type_=ProductType.LAPTOP),
        1401: Product(maker="A", model="1401", type_=ProductType.PRINTER),
        1408: Product(maker="A", model="1408", type_=ProductType.PRINTER),
        1752: Product(maker="A", model="1752", type_=ProductType.LAPTOP),
        1121: Product(maker="B", model="1121", type_=ProductType.PC),
        1750: Product(maker="B", model="1750", type_=ProductType.LAPTOP),
        1321: Product(maker="C", model="1321", type_=ProductType.LAPTOP),
        1288: Product(maker="D", model="1288", type_=ProductType.PRINTER),
        1433: Product(maker="D", model="1433", type_=ProductType.PRINTER),
        1260: Product(maker="E", model="1260", type_=ProductType.PC),
        1434: Product(maker="E", model="1434", type_=ProductType.PRINTER),
        2132: Product(maker="E", model="2132", type_=ProductType.PC),
        2133: Product(maker="E", model="2133", type_=ProductType.PC),
    }

    pcs = [
        PC(code=1, product=products[1232], speed=500, ram=64, hd=5, cd="12x", price="600"),
        PC(code=10, product=products[1260], speed=500, ram=32, hd=10, cd="12x", price="350"),
        PC(code=11, product=products[1233], speed=900, ram=128, hd=40, cd="40x", price="980"),
        PC(code=12, product=products[1233], speed=800, ram=128, hd=20, cd="50x", price="970"),
        PC(code=2, product=products[1121], speed=750, ram=128, hd=14, cd="40x", price="850"),
        PC(code=3, product=products[1233], speed=500, ram=64, hd=5, cd="12x", price="600"),
        PC(code=4, product=products[1121], speed=600, ram=128, hd=14, cd="40x", price="850"),
        PC(code=5, product=products[1121], speed=600, ram=128, hd=8, cd="40x", price="850"),
        PC(code=6, product=products[1233], speed=750, ram=128, hd=20, cd="50x", price="950"),
        PC(code=7, product=products[1232], speed=500, ram=32, hd=10, cd="12x", price="400"),
        PC(code=8, product=products[1232], speed=450, ram=64, hd=8, cd="24x", price="350"),
        PC(code=9, product=products[1232], speed=450, ram=32, hd=10, cd="24x", price="350"),
    ]

    printers = [
        Printer(code=1, product=products[1276], color="n", type_=PrinterType.LASER, price="400"),
        Printer(code=2, product=products[1433], color="y", type_=PrinterType.JET, price="270"),
        Printer(code=3, product=products[1434], color="y", type_=PrinterType.JET, price="290"),
        Printer(code=4, product=products[1401], color="n", type_=PrinterType.MATRIX, price="150"),
        Printer(code=5, product=products[1408], color="n", type_=PrinterType.MATRIX, price="270"),
        Printer(code=6, product=products[1288], color="n", type_=PrinterType.LASER, price="400"),
    ]

    laptops = [
        Laptop(code=1, product=products[1298], speed=350, ram=32, hd=4, price="700", screen=11),
        Laptop(code=2, product=products[1321], speed=500, ram=64, hd=8, price="970", screen=12),
        Laptop(code=3, product=products[1750], speed=750, ram=128, hd=12, price="1200", screen=14),
        Laptop(code=4, product=products[1298], speed=600, ram=64, hd=10, price="1050", screen=15),
        Laptop(code=5, product=products[1752], speed=750, ram=128, hd=10, price="1150", screen=14),
        Laptop(code=6, product=products[1298], speed=450, ram=64, hd=10, price="950", screen=12),
    ]

    async with async_session_maker() as session:
        session.add_all(products.values())
        session.add_all(pcs)
        session.add_all(printers)
        session.add_all(laptops)

        await session.commit()
