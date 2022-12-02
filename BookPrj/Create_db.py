from models.database import create_db
from models.Books import Books
from models.Authors import Authors
from models.Authors_Books import Authors_Books
from models.Genres import Genres
from models.Books_Geners import Books_Genres

def create_database():
    create_db()