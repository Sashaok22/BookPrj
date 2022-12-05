from typing import Optional
from models.database import Base
from sqlalchemy import Integer, String, Column, Table, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field


books_genres = Table("books_genres", Base.metadata,
                          Column('book_id', ForeignKey('books.id'), primary_key=True),
                          Column("genre_id", ForeignKey('genres.id', ondelete='CASCADE'), primary_key=True),
                          )

class Genres(Base):
    # Table name
    __tablename__ = 'genres'

    # Table attributes
    id = Column(Integer, primary_key=True)
    genre_name = Column(String, nullable=False, unique=True)
    short_description = Column(String, nullable=False)
    book = relationship('Books', secondary=books_genres, backref="Books_Genres")


class GenresSchema(BaseModel):
    id: Optional[int]
    genre_name: str = Field(..., min_length=2)
    short_description: str = Field(..., min_length=2)

    class Config:
        orm_mode = True
