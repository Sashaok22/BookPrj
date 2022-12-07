from typing import Optional
from pydantic import BaseModel, Field


class BooksSchema(BaseModel):
    id: Optional[int]
    book_name: str = Field(..., min_length=2)
    number_of_pages: int = Field(..., gt=0)
    rating: int = Field(..., gt=0, lt=11)

    class Config:
        orm_mode = True