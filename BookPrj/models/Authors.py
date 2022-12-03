from datetime import date
from typing import Optional
from pydantic import BaseModel
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

    def __str__(self):
        return f'ID: {self.id}, Author name: {self.author_name}, ' \
               f'Author surname: {self.author_surname}, Author patronymic: {self.author_patronymic}, ' \
               f'Date of birth: {self.date_of_birth}, Date of death: {self.date_of_death}.'


class AuthorsSchema(BaseModel):
    id: Optional[int]
    author_name: str
    author_surname: str
    author_patronymic: str
    date_of_birth: date
    date_of_death: date

    class Config:
        orm_mode = True
