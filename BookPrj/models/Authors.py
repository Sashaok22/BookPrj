from models.database import Base
from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship

class Authors(Base):
    __tablename__ = 'authors'

    id = Column(Integer,primary_key = True)
    author_name = Column(String,nullable=False)
    author_surname = Column(String, nullable=False)
    author_patronymic = Column(String, nullable=True)