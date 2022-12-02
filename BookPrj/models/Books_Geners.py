from models.database import Base
from sqlalchemy import Integer, Column, ForeignKey


class Books_Genres(Base):
    __tablename__ = 'books_genres'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    genre_id = Column(Integer, ForeignKey('genres.id'))
