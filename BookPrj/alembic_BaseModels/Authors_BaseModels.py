from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, Field, root_validator

from alembic_BaseModels.Genres_BaseModels import GenreSchema


# Authors BaseModel, needed to validate the data of the added author
class AuthorSchema(BaseModel):
    _id: Optional[int] = Field(description="Author id field")
    author_name: str = Field(..., min_length=2, max_length=50, description="Author name field")
    author_surname: str = Field(..., min_length=2, max_length=50, description="Author surname field")
    author_patronymic: Optional[str] = Field(min_length=2, max_length=50, description="Author patronymic field")
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


# Authors BaseModel, required for validate the data of its associated books and genres
class Author_content(AuthorSchema):
    from alembic_BaseModels.Books_BaseModels import BookSchema
    genres: Optional[list[GenreSchema]] = Field(description="List of genres in which the author writes field")
    books: Optional[list[BookSchema]] = Field(description="List of books by this author field")


# Authors BaseModel, required for validation and submission of the list of authors
class AuthorsSchema(BaseModel):
    authors: Optional[list[Author_content]] or Optional[list[AuthorSchema]] \
        = Field(description="List of models of authors")

    class Config:
        orm_mode = True

