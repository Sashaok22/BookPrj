from models.database import Base
from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship


class Books(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    book_name = Column(String, nullable=False)
    namber_of_pages = Column(Integer, nullable=False)
    reiting = Column(Integer, nullable=False)
    author = relationship('authors')
    genre = relationship('genres')
