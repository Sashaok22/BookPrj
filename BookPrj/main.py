from flask import Flask
from SpecTree_config import spec
from json_serializable import JSONSerializable
from models.database import create_db
from routes.authors_routes import authors_blueprint
from routes.books_routes import books_blueprint
from routes.genres_routes import genres_blueprint

app = Flask(__name__)
JSONSerializable(app)
app.config['SECRET_KEY'] = 'VERY VERY VERY SECRET KEY'


if __name__ == "__main__":
    spec.register(app)
    app.register_blueprint(books_blueprint)
    app.register_blueprint(authors_blueprint)
    app.register_blueprint(genres_blueprint)
    create_db()
    app.run()
