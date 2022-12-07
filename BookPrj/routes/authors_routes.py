from flask import request, jsonify, abort, Blueprint
from pydantic import ValidationError
from models.Authors import Authors, AuthorsSchema
from models.Books import Books
from models.Genres import Genres
from models.database import Session

authors_blueprint = Blueprint(__name__.split(".")[-1], __name__)


@authors_blueprint.get("/api/authors")
def get_authors(db: Session = Session()):
    author = db.query(Authors) \
        .join(Books.Books_Authors) \
        .join(Books.Books_Genres).all()
    if not author:
        abort(404)
    author = [
        {
            "author": a,
            "books": a.book,
            "genres": db.query(Genres)
            .join(Books.Books_Authors)
            .join(Books.Books_Genres)
            .filter(Authors.id == a.id).all()
        }
        for a in author
    ]
    return jsonify(author)


@authors_blueprint.get("/api/authors/<int:author_id>")
def get_author(author_id, db: Session = Session()):
    author = db.query(Authors) \
        .join(Books.Books_Authors) \
        .join(Books.Books_Genres)\
        .filter(Authors.id == author_id).all()
    if not author:
        abort(404)
    author = [
        {
            "author": author[0],
            "books": author[0].book,
            "genres": db.query(Genres)
            .join(Books.Books_Authors)
            .join(Books.Books_Genres)
            .filter(Authors.id == author[0].id).all()
        }
    ]
    return jsonify(author)


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
