import enum

class ProductType(str, enum.Enum):
    LAPTOP = "Laptop"
    PC = "PC"
    PRINTER = "Printer"


class PrinterType(str, enum.Enum):
    JET = "Jet"
    LASER = "Laser"
    MATRIX = "Matrix"
