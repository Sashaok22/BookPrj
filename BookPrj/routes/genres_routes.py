from flask import request, jsonify, abort, Blueprint
from pydantic import ValidationError

from alembic_BaseModels.Genres_BaseModels import GenresSchema
from models.Authors import Authors
from models.Books import Books
from models.Genres import Genres
from models.database import Session

genres_blueprint = Blueprint(__name__.split(".")[-1], __name__)


@genres_blueprint.get("/api/genres")
def get_genres(db: Session = Session()):
    genre = db.query(Genres).all()
    if not genre:
        abort(404)
    return jsonify(genre)


@genres_blueprint.get("/api/genres_authors/<int:genre_id>")
def get_genres_authors(genre_id, db: Session = Session()):
    authors = db.query(Authors)\
        .join(Books.Books_Authors)\
        .join(Books.Books_Genres)\
        .filter(
        Genres.id == genre_id
    ).all()
    if not authors:
        abort(404)
    return jsonify(authors)


@genres_blueprint.get("/api/genres_books/<int:genre_id>")
def get_genres_books(genre_id, db: Session = Session()):
    books = db.query(Books)\
        .join(Books.Books_Genres)\
        .filter(
        Genres.id == genre_id
    ).all()
    if not books:
        abort(404)
    return jsonify(books)


@genres_blueprint.get("/api/genres/<int:genre_id>")
def get_genre(genre_id, db: Session = Session()):
    genre = db.query(Genres).get(genre_id)
    if not genre:
        abort(404)
    return jsonify(GenresSchema(**genre.to_dict()).dict())


@genres_blueprint.post("/api/genres")
def create_genre(db: Session = Session()):
    if not request:
        abort(400)
    try:
        genre = GenresSchema(**request.form)
    except ValidationError as e:
        return "Exception" + e.json()
    _genre = Genres(**genre.dict())
    db.add(_genre)
    db.commit()
    db.refresh(_genre)
    return jsonify(_genre)


@genres_blueprint.put("/api/genres/<int:genre_id>")
def update_genre(genre_id, db: Session = Session()):
    if not request:
        abort(400)
    try:
        GenresSchema(**request.form)
    except ValidationError as e:
        return "Exception" + e.json()
    genre = db.query(Genres).get(genre_id)
    if not genre:
        abort(404)
    genre.genre_name = request.form['genre_name']
    genre.short_description = request.form['short_description']
    db.add(genre)
    db.commit()
    db.refresh(genre)
    return jsonify(genre)


@genres_blueprint.delete("/api/genres/<int:genre_id>")
def delete_genre(genre_id, db: Session = Session()):
    genre = db.query(Genres).get(genre_id)
    if not genre:
        abort(404)
    db.delete(genre)
    db.commit()
    return jsonify(True)
