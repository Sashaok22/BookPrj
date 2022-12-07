from flask import request, jsonify, abort, Blueprint
from pydantic import ValidationError
from spectree import SpecTree, Response

from models.Authors import Authors, AuthorSchema, WebError, AuthorSchema, AuthorsSchema
from models.Books import Books, BooksSchema
from models.Genres import Genres, GenresSchema
from models.database import Session

authors_blueprint = Blueprint(__name__.split(".")[-1], __name__)
spec = SpecTree("flask")


@authors_blueprint.get("/api/authors")
def get_authors(db: Session = Session()):
    """
        Get all authors.
    """
    authors = db.query(Authors) \
        .join(Books.Books_Authors) \
        .join(Books.Books_Genres).all()
    if not authors:
        return WebError({'error_code': 404, 'msg': "Authors not found"})
    all_authors = []
    for a in authors:
        _author = AuthorSchema(**a.to_dict())
        genres = db.query(Genres).join(Books.Books_Authors).join(Books.Books_Genres).all()
        _author.genres = [GenresSchema(**g.to_dict()) for g in genres]
        books = a.book
        _author.books = [BooksSchema(**b.to_dict()) for b in books]
        all_authors.append(_author)
    response = AuthorsSchema()
    response.Authors = all_authors
    return response.dict()


@authors_blueprint.get("/api/authors/<int:author_id>")
@spec.validate(resp=Response(HTTP_404=(WebError, "Author not found"), HTTP_200=AuthorSchema), tags=["Authors_request"])
def get_author(author_id, db: Session = Session()):
    """
        Find author by id.
    """
    author = db.query(Authors) \
        .join(Books.Books_Authors) \
        .join(Books.Books_Genres) \
        .filter(Authors.id == author_id).all()
    if not author:
        return WebError({'error_code': 404, 'msg': "Author not found"})
    _author = AuthorSchema(**author[0].to_dict())
    genres = db.query(Genres).join(Books.Books_Authors).join(Books.Books_Genres).all()
    _author.genres = [GenresSchema(**g.to_dict()) for g in genres]
    books = author[0].book
    _author.books = [BooksSchema(**b.to_dict()) for b in books]
    return _author


@authors_blueprint.post("/api/authors")
@spec.validate(json=AuthorSchema, resp=Response('HTTP_400', HTTP_200=AuthorSchema), tags=["Authors_request"])
def create_author(db: Session = Session()):
    if request is None:
        abort(400)
    try:
        author = AuthorSchema(**request.json)
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
        AuthorSchema(**request.form)
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
