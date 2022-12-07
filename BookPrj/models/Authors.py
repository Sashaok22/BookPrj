from typing import Optional
from pydantic import BaseModel, Field
from pydantic.validators import date
from sqlalchemy import Integer, String, Column, Date, ForeignKey, Table
from sqlalchemy.orm import relationship

from models.Books import BooksSchema
from models.Genres import GenresSchema
from models.database import Base

books_authors = Table("books_authors", Base.metadata,
                      Column('book_id', ForeignKey('books.id'), primary_key=True),
                      Column("author_id", ForeignKey('authors.id', ondelete='CASCADE'), primary_key=True),
                      )


class Authors(Base):
    # Table name
    __tablename__ = 'authors'

    # Table attributes
    id = Column(Integer, primary_key=True)
    author_name = Column(String, nullable=False)
    author_surname = Column(String, nullable=False)
    author_patronymic = Column(String, nullable=True)
    date_of_birth = Column(Date, nullable=False)
    date_of_death = Column(Date, nullable=True)

    book = relationship('Books', secondary=books_authors, backref="Books_Authors",
                        cascade="all, delete", cascade_backrefs=False)

    def to_dict(self):
        return {"id": self.id, 'author_name': self.author_name, 'author_surname': self.author_surname,
                'author_patronymic': self.author_patronymic, 'date_of_birth': self.date_of_birth,
                'date_of_death': self.date_of_death}


class AuthorSchema(BaseModel):
    id: Optional[int] = Field(description="Author person id field")
    author_name: str = Field(..., min_length=2, description="Author name field")
    author_surname: str = Field(..., min_length=2, description="Author surname field")
    author_patronymic: Optional[str] = Field(min_length=2, description="Author patronymic field")
    date_of_birth: date = Field(..., description="Author date of birth field")
    date_of_death: Optional[date] = Field(description="Author date of death field")
    genres: Optional[list[GenresSchema]] = Field(description="List of genres in which the author writes field")
    books: Optional[list[BooksSchema]] = Field(description="List of books by this author field")

    class Config:
        orm_mode = True


class WebError(BaseModel):
    error_code: int
    msg: str


class AuthorsSchema(BaseModel):
    Authors: Optional[list[AuthorSchema]]
