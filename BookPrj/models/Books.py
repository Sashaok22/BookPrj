from models.database import Base
from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship


class Books(Base):
    # Table name
    __tablename__ = 'books'

    # Table attributes
    id = Column(Integer, primary_key=True)
    book_name = Column(String, nullable=False)
    namber_of_pages = Column(Integer, nullable=False)
    reiting = Column(Integer, nullable=False)
    author = relationship('Authors_Books')
    genre = relationship('Books_Genres')
