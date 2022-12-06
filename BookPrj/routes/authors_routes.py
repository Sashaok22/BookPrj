from flask import request, jsonify, abort, Blueprint
from pydantic import ValidationError
from sqlalchemy import and_
from models.Authors import Authors, books_authors, AuthorsSchema
from models.Books import Books
from models.Genres import Genres, books_genres
from models.database import Session

authors_blueprint = Blueprint(__name__.split(".")[-1], __name__)


@authors_blueprint.get("/api/authors")
def get_authors(db: Session = Session()):
    author = db.query(Authors)\
        .join(Books.Books_Authors)\
        .join(Books.Books_Genres).all()
    if not author:
        abort(404)
    [print(a) for a in author]
    author = [
        {
            "author": a,
            "books": a.book,
            "genres": a.book.Books_Genres
        }
        for a in author

    ]
    return jsonify(author)


@authors_blueprint.get("/api/authors/<int:author_id>")
def get_author(author_id, db: Session = Session()):
    author = db.query(Authors, Books, Genres).filter(and_(
        books_genres.c.book_id == Books.id,
        books_genres.c.genre_id == Genres.id,
        books_authors.c.book_id == Books.id,
        books_authors.c.author_id == Authors.id,
        Authors.id == author_id
    )).all()
    if not author:
        abort(404)
    data = []
    for row in author:
        data.append([x for x in row])
    return jsonify(data)


@authors_blueprint.post("/api/authors")
def create_author(db: Session = Session()):
    if request is None:
        abort(400)
    try:
        author = AuthorsSchema(**request.form)
    except ValidationError as e:
        return "Exception" + e.json()
    _author = Authors(**author.dict())
    db.add(_author)
    db.commit()
    db.refresh(_author)
    return jsonify(_author)


@authors_blueprint.put("/api/authors/<int:author_id>")
def update_author(author_id, db: Session = Session()):
    if request is None:
        abort(400)
    try:
        AuthorsSchema(**request.form)
    except ValidationError as e:
        return "Exception" + e.json()
    author = db.query(Authors).get(author_id)
    if author is None:
        abort(404)
    author.author_name = request.form['author_name']
    author.author_surname = request.form['author_surname']
    author.author_patronymic = request.form['author_patronymic']
    author.date_of_birth = request.form['date_of_birth']
    author.date_of_death = request.form['date_of_death']
    db.add(author)
    db.commit()
    db.refresh(author)
    return jsonify(author)


@authors_blueprint.delete("/api/authors/<int:author_id>")
def delete_author(author_id, db: Session = Session()):
    author = db.query(Authors).get(author_id)
    if author is None:
        abort(404)
    db.delete(author)
    db.commit()
    return jsonify(True)
