from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database


# database connection data
DATABASE_NAME = 'book_shop'
DATABASE_HOST = 'localhost'
DATABASE_PORT = '5432'
DATABASE_USERNAME = 'postgres'
DATABASE_PASSWORD = 'admin'
DATABASE_DIALECT = 'postgresql'
DATABASE_DRIVER = 'psycopg2'

# database connection
engine = create_engine(f'{DATABASE_DIALECT}+{DATABASE_DRIVER}://'
                       f'{DATABASE_USERNAME}:{DATABASE_PASSWORD}@'
                       f'{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')

# create session to manage data
Session = sessionmaker(bind=engine)

# create base model
Base = declarative_base()


# Create database method
def create_db():
    # Create new database if not exists
    if not database_exists(engine.url):
        create_database(engine.url)
    # Create all database entities
    Base.metadata.create_all(engine)
