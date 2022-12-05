from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, validator, root_validator
from models.database import Base
from sqlalchemy import Integer, String, Column, Date, ForeignKey, Table
from sqlalchemy.orm import relationship


association_table = Table("association_table", Base.metadata,
                          Column('book_id', ForeignKey('books.id'), primary_key=True),
                          Column("author_id", ForeignKey('authors.id', ondelete='CASCADE'), primary_key=True),
                          )


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
    book = relationship('Authors', secondary=association_table, backref="Authors_Books")


class AuthorsSchema(BaseModel):
    id: Optional[int]
    author_name: str = Field(..., min_length=2)
    author_surname: str = Field(..., min_length=2)
    author_patronymic: Optional[str]
    date_of_birth: str
    date_of_death: Optional[str]

    @root_validator
    def date_validation(cls, v):
        if v['date_of_death'] == "":
            v['date_of_death'] = None
        if v['date_of_death'] != None:
            if datetime.strptime(v['date_of_death'] and v['date_of_birth'], "%Y-%m-%d"):
                v['date_of_death'] = datetime.strptime(v['date_of_death'], "%Y-%m-%d")
                v['date_of_birth'] = datetime.strptime(v['date_of_birth'], "%Y-%m-%d")
                if v['date_of_death'] > v['date_of_birth'] \
                        or (v['date_of_death'] > datetime.now() or v['date_of_birth'] > datetime.now()):
                    raise ValueError('the date of death must be before the date of birth '
                                     'and both dates must be before the current moment')
                return v
            else:
                raise ValueError('invalid date format')
        elif datetime.strptime(v['date_of_birth'], "%Y-%m-%d"):
            v['date_of_birth'] = datetime.strptime(v['date_of_birth'], "%Y-%m-%d")
            if v['date_of_birth'] > datetime.now():
                raise ValueError('the date of birth must be before the current moment')
            else:
                return v
        else:
            raise ValueError('invalid date format')

    @validator('author_patronymic')
    def author_patronymic_test(cls, v):
        if v == "":
            return None
        elif len(v) < 2:
            raise ValueError('field length must be greater than 1')
        return v

    class Config:
        orm_mode = True
