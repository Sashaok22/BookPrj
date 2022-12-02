from models.database import Base
from sqlalchemy import Integer, Column, ForeignKey


class Authors_Books(Base):
    # Table name
    __tablename__ = 'authors_books'

    # Table attributes
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    author_id = Column(Integer, ForeignKey('authors.id', ondelete='CASCADE'))
