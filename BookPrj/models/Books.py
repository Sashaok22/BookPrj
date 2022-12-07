from typing import Optional
from pydantic import BaseModel, Field
from models.database import Base
from sqlalchemy import Integer, String, Column


class Books(Base):
    # Table name
    __tablename__ = 'books'

    # Table attributes
    id = Column(Integer, primary_key=True)
    book_name = Column(String, nullable=False)
    number_of_pages = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=False)

    def to_dict(self):
        return {"id": self.id, 'book_name': self.book_name, 'number_of_pages': self.number_of_pages,
                'rating': self.rating}


class BooksSchema(BaseModel):
    id: Optional[int]
    book_name: str = Field(..., min_length=2)
    number_of_pages: int = Field(..., gt=0)
    rating: int = Field(..., gt=0, lt=11)

    class Config:
        orm_mode = True
