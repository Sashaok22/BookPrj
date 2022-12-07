from typing import Optional
from pydantic import BaseModel, Field
from pydantic.validators import date
from models.Books import BooksSchema
from models.Genres import GenresSchema


class AuthorSchema(BaseModel):
    _id: Optional[int] = Field(description="Author person id field")
    author_name: str = Field(..., min_length=2, description="Author name field")
    author_surname: str = Field(..., min_length=2, description="Author surname field")
    author_patronymic: Optional[str] = Field(min_length=2, description="Author patronymic field")
    date_of_birth: date = Field(..., description="Author date of birth field")
    date_of_death: Optional[date] = Field(description="Author date of death field")

    class Config:
        orm_mode = True


class Author_content(AuthorSchema):
    genres: Optional[list[GenresSchema]] = Field(description="List of genres in which the author writes field")
    books: Optional[list[BooksSchema]] = Field(description="List of books by this author field")


class WebError(BaseModel):
    error_code: int = Field(..., description="Code of handled server response error")
    msg: str = Field(..., description="Message error")


class AuthorsSchema(BaseModel):
    Authors: Optional[list[Author_content]] = Field(description="List of models of authors")
