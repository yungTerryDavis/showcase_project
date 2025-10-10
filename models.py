from decimal import Decimal
from typing import Annotated, override

from sqlalchemy import ForeignKey, SmallInteger, String
from sqlalchemy.dialects.postgresql import MONEY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import REAL

from database import Base, BaseAutoNameMixin
from enums import PrinterType, ProductType

# pyright: reportUninitializedInstanceVariable=false

# pc_firm
str_1 = Annotated[str, mapped_column(String(1))]
str_10 = Annotated[str, mapped_column(String(10))]
str_50 = Annotated[str, mapped_column(String(50))]
small_int = Annotated[int, mapped_column(SmallInteger)]
real = Annotated[float, mapped_column(REAL)]
money = Annotated[Decimal | None, mapped_column(MONEY)]
int_pk = Annotated[int, mapped_column(primary_key=True)]


class Product(Base, BaseAutoNameMixin):
    maker: Mapped[str_10]
    model: Mapped[str_50] = mapped_column(primary_key=True)
    type_: Mapped[ProductType]

    pc: Mapped["PC"] = relationship(back_populates="product")
    printer: Mapped["Printer"] = relationship(back_populates="product")
    laptop: Mapped["Laptop"] = relationship(back_populates="product")

    @override
    def __repr__(self):
        return f"<Product(maker={self.maker}, model={self.model}, type_={self.type_.value})>"


class PC(Base, BaseAutoNameMixin):
    code: Mapped[int_pk]
    model: Mapped[str] = mapped_column(ForeignKey("product.model"))
    speed: Mapped[small_int]
    ram: Mapped[small_int]
    hd: Mapped[real]
    cd: Mapped[str_10]
    price: Mapped[money]

    product: Mapped["Product"] = relationship(back_populates="pc")
    
    @override
    def __repr__(self):
        return (f"<PC(code={self.code}, model={self.model}, speed={self.speed}, " 
        f"ram={self.ram}, hd={self.hd}, cd={self.cd}, price={self.price})>")


class Laptop(Base, BaseAutoNameMixin):
    code: Mapped[int_pk]
    model: Mapped[str] = mapped_column(ForeignKey("product.model"))
    speed: Mapped[small_int]
    ram: Mapped[small_int]
    hd: Mapped[real]
    price: Mapped[money]
    screen: Mapped[small_int]

    product: Mapped["Product"] = relationship(back_populates="laptop")

    @override
    def __repr__(self):
        return (f"<Laptop(code={self.code}, model={self.model}, speed={self.speed}, " 
        f"ram={self.ram}, hd={self.hd}, screen={self.screen}, price={self.price})>")

class Printer(Base, BaseAutoNameMixin):
    code: Mapped[int_pk]
    model: Mapped[str] = mapped_column(ForeignKey("product.model"))
    color: Mapped[str_1]
    type_: Mapped[PrinterType]
    price: Mapped[money]

    product: Mapped["Product"] = relationship(back_populates="printer")

    @override
    def __repr__(self):
        return (f"<Printer(code={self.code}, model={self.model}, color={self.color}, " 
        f"type_={self.type_.value}, price={self.price})>")
