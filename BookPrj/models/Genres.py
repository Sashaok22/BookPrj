from models.database import Base
from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship

class Authors(Base):
    __tablename__ = 'genres'

    id = Column(Integer,primary_key = True)
    genre_name = Column(String,nullable=False)
    short_description = Column(String, nullable=False)