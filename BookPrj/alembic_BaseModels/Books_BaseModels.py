from typing import Optional
from pydantic import BaseModel, Field
from alembic_BaseModels.Authors_BaseModels import AuthorSchema
from alembic_BaseModels.Genres_BaseModels import GenreSchema


# Books BaseModel, required for validate the data of the added book
class BookSchema(BaseModel):
    _id: Optional[int]
    book_name: str = Field(..., min_length=2, max_length=50, description='Book name field')
    number_of_pages: int = Field(..., gt=0, description='Number of pages field')
    rating: int = Field(..., gt=0, lt=11, description='Personal rating of books fields')

    class Config:
        orm_mode = True


# Books BaseModel, required for validate the data of its associated authors and genres
class Book_content(BookSchema):
    genres: Optional[list[GenreSchema]] \
        = Field(description="Genre id of the book, returned as a comma-separated string")
    authors: Optional[list[AuthorSchema]] \
        = Field(description="Author id of the book, returned as a comma-separated string")


# Books BaseModel, required for validate and relate the data of its associated authors and genres
class Book_content_id(BookSchema):
    genres_id: list[int] = Field(..., description="Book genre id")
    authors_id: list[int] = Field(..., description="Book author id")


# Books BaseModel, required for validation and submission of the list of books
class BooksSchema(BaseModel):
    books: Optional[list[Book_content]] or Optional[list[BookSchema]] = Field(description="List of models of books")

    class Config:
        orm_mode = True

