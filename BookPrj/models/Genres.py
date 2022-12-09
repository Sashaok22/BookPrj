from models.database import Base
from sqlalchemy import Integer, String, Column, Table, ForeignKey
from sqlalchemy.orm import relationship


books_genres = Table("books_genres", Base.metadata,
                     Column('book_id', ForeignKey('books.id'), primary_key=True),
                     Column("genre_id", ForeignKey('genres.id', ondelete='CASCADE'), primary_key=True),
                     )


class Genres(Base):
    # Table name
    __tablename__ = 'genres'

    # Table attributes
    id = Column(Integer, primary_key=True)
    genre_name = Column(String(50), nullable=False)
    short_description = Column(String(100), nullable=False)
    book = relationship('Books', secondary=books_genres, backref="Books_Genres")

    def to_dict(self):
        return {"id": self.id, 'genre_name': self.genre_name, 'short_description': self.short_description}
