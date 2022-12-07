from flask import Flask
from Create_db import create_database
from json_serializable import JSONSerializable
from routes.authors_routes import authors_blueprint, spec
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
    create_database()
    app.run()
