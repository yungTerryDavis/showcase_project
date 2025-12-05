from pydantic import BaseModel
from pydantic.config import ConfigDict


class MovieSchema(BaseModel):
    id: int
    name: str
    plot: str
    genres: list[str]
    casts: list[str]

    model_config = ConfigDict(from_attributes=True)


class CreateMovieSchema(BaseModel):
    name: str
    plot: str
    genres: list[str]
    casts: list[str]


class UpdateMovieSchema(BaseModel):
    name: str | None = None
    plot: str | None = None
    genres: list[str] | None = None
    casts: list[str] | None = None
