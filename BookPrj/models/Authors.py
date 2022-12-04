from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, validator
from models.database import Base
from sqlalchemy import Integer, String, Column, Date
from sqlalchemy.orm import relationship


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
    book = relationship('Authors_Books')


class AuthorsSchema(BaseModel):
    id: Optional[int]
    author_name: str = Field(..., min_length=1)
    author_surname: str = Field(..., min_length=1)
    author_patronymic: Optional[str]
    date_of_birth: date
    date_of_death: Optional[str]

    @validator('date_of_death')
    def date_of_death_test(cls, v):
        if v == "":
            return None
        elif datetime.strptime(v, "%Y-%m-%d"):
            return v
        else:
            raise ValueError('invalid date format')

    validator('date_of_death')

    @validator('author_patronymic')
    def author_patronymic_test(cls, v):
        if v == "":
            return None
        elif len(v) < 2:
            raise ValueError('field length must be greater than 1')
        return v

    class Config:
        orm_mode = True
