from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, Field, root_validator
from alembic_BaseModels.Books_BaseModels import BooksSchema
from alembic_BaseModels.Genres_BaseModels import GenresSchema


class AuthorSchema(BaseModel):
    _id: Optional[int] = Field(description="Author id field")
    author_name: str = Field(..., min_length=2, description="Author name field")
    author_surname: str = Field(..., min_length=2, description="Author surname field")
    author_patronymic: Optional[str] = Field(min_length=2, description="Author patronymic field")
    date_of_birth: date = Field(..., description="Author date of birth field")
    date_of_death: Optional[date] = Field(description="Author date of death field")

    @root_validator
    def date_validate(cls, v):
        if v['date_of_birth'] > datetime.now().date():
            raise ValueError('Date of birth must be before the current moment')
        if v['date_of_death'] > v['date_of_birth'] and v['date_of_death'] is not None:
            raise ValueError('Date of death must be before the date of birth')
        return v

    class Config:
        orm_mode = True


class Author_content(AuthorSchema):
    genres: Optional[list[GenresSchema]] = Field(description="List of genres in which the author writes field")
    books: Optional[list[BooksSchema]] = Field(description="List of books by this author field")


class AuthorsSchema(BaseModel):
    Authors: Optional[list[Author_content]] = Field(description="List of models of authors")
