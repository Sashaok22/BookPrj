from typing import Optional
from models.database import Base
from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship
from pydantic import BaseModel


class Genres(Base):
    # Table name
    __tablename__ = 'genres'

    # Table attributes
    id = Column(Integer, primary_key=True)
    genre_name = Column(String, nullable=False, unique=True)
    short_description = Column(String, nullable=False)
    book = relationship('Books_Genres')

    def __str__(self):
        return f'ID: {self.id}, Genre name: {self.genre_name}, Short description: {self.short_description}.'


class GenresSchema(BaseModel):
    id: Optional[int]
    genre_name: str
    short_description: str

    class Config:
        orm_mode = True
