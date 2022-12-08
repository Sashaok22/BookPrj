from typing import Optional
from pydantic import BaseModel, Field
from alembic_BaseModels.Authors_BaseModels import AuthorSchema
from alembic_BaseModels.Genres_BaseModels import GenresSchema


class BookSchema(BaseModel):
    _id: Optional[int]
    book_name: str = Field(..., min_length=2, description='Book name field')
    number_of_pages: int = Field(..., gt=0, description='Number of pages field')
    rating: int = Field(..., gt=0, lt=11, description='Personal rating of books fields')

    class Config:
        orm_mode = True


class Book_content(BookSchema):
    genres: Optional[list[GenresSchema]] \
        = Field(description="Genre id of the book, returned as a comma-separated string")
    authors: Optional[list[AuthorSchema]] \
        = Field(description="Author id of the book, returned as a comma-separated string")


class Book_content_id(BookSchema):
    genres_id: list[int] = Field(..., description="Book genre id")
    authors_id: list[int] = Field(..., description="Book author id")


class BooksSchema(BaseModel):
    books: Optional[list[Book_content]] = Field(description="List of models of books")
