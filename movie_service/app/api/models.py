from typing import Annotated, override

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import ARRAY

from movie_service.app.database import Base, BaseAutoNameMixin

# pyright: reportUninitializedInstanceVariable=false


# microservices
int_pk = Annotated[int, mapped_column(primary_key=True)]
str_array = Annotated[list[str], mapped_column(ARRAY(String))]

class Movie(Base, BaseAutoNameMixin):
    id: Mapped[int_pk]
    name: Mapped[str]
    plot: Mapped[str]
    genres: Mapped[str_array]
    casts: Mapped[str_array]

    @override
    def __repr__(self):
        return (f"<Movie(id={self.id}, name={self.name}, plot={self.plot}, " 
        f"genres={self.genres}, casts={self.casts})>")
