from typing import Optional
from models.database import Base
from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field


class Genres(Base):
    # Table name
    __tablename__ = 'genres'

    # Table attributes
    id = Column(Integer, primary_key=True)
    genre_name = Column(String, nullable=False, unique=True)
    short_description = Column(String, nullable=False)
    book = relationship('Books_Genres')


class GenresSchema(BaseModel):
    id: Optional[int]
    genre_name: str = Field(..., min_length=2)
    short_description: str = Field(..., min_length=2)

    class Config:
        orm_mode = True
