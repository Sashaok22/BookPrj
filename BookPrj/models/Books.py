from models.database import Base
from sqlalchemy import Integer, String, Column


class Books(Base):
    # Table name
    __tablename__ = 'books'

    # Table attributes
    id = Column(Integer, primary_key=True)
    book_name = Column(String(50), nullable=False)
    number_of_pages = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=False)

    def to_dict(self):
        return {"id": self.id, 'book_name': self.book_name, 'number_of_pages': self.number_of_pages,
                'rating': self.rating}
