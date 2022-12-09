from flask import request, Blueprint, abort, make_response
from pydantic import ValidationError
from spectree import Response
from SpecTree_config import spec
from alembic_BaseModels.Authors_BaseModels import AuthorsSchema, Author_content, AuthorSchema
from alembic_BaseModels.Books_BaseModels import BookSchema
from alembic_BaseModels.Genres_BaseModels import GenreSchema
from alembic_BaseModels.Others_BaseModels import WebError
from models.Authors import Authors
from models.Books import Books
from models.Genres import Genres
from models.database import Session

authors_blueprint = Blueprint(__name__.split(".")[-1], __name__)


@authors_blueprint.get("/api/authors")
@spec.validate(resp=Response(HTTP_404=(WebError, "Authors not found"),
                             HTTP_200=(AuthorsSchema, 'Successful operation')), tags=["Authors_request"])
def get_authors(db: Session = Session()):
    """
        Get all authors

        Return all authors with all their books and genres
    """
    authors = db.query(Authors).all()
    if not authors:
        abort(make_response(WebError(error_code=404, msg="Authors not found").dict(), 404))
    all_authors = []
    for a in authors:
        _author = Author_content.from_orm(a)
        genres = db.query(Genres).join(Books.Books_Authors).join(Books.Books_Genres).all()
        _author.genres = [GenreSchema.from_orm(g) for g in genres]
        books = a.book
        _author.books = [BookSchema.from_orm(b) for b in books]
        all_authors.append(_author)
    response = AuthorsSchema()
    response.authors = all_authors
    return response


@authors_blueprint.get("/api/authors/<int:author_id>")
@spec.validate(resp=Response(HTTP_404=(WebError, "Author not found"),
                             HTTP_200=(Author_content, 'Successful operation')), tags=["Authors_request"])
def get_author(author_id, db: Session = Session()):
    """
        Find author by id

        Return one author by id with all his books and genres
    """
    author = db.query(Authors).get(author_id)
    if author is None:
        abort(make_response(WebError(error_code=404, msg="Author not found").dict(), 404))
    _author = Author_content.from_orm(author)
    genres = db.query(Genres).join(Books.Books_Authors).join(Books.Books_Genres).all()
    _author.genres = [GenreSchema.from_orm(g) for g in genres]
    books = author.book
    _author.books = [BookSchema.from_orm(b) for b in books]
    return _author


@authors_blueprint.post("/api/authors")
@spec.validate(json=AuthorSchema,
               resp=Response(HTTP_400=(WebError, "Request data error"),
                             HTTP_200=(AuthorSchema, 'Successful operation')),
               tags=["Authors_request"])
def create_author(db: Session = Session()):
    """
        Add new author

        Return new author
    """
    if request is None:
        abort(make_response(WebError(error_code=400, msg="Request data error").dict(), 400))
    try:
        author = AuthorSchema(**request.json)
    except ValidationError as e:
        return "Exception" + e.json()
    _author = Authors(**author.dict())
    db.add(_author)
    db.commit()
    db.refresh(_author)
    author = AuthorSchema.from_orm(_author)
    return author


@authors_blueprint.put("/api/authors/<int:author_id>")
@spec.validate(json=AuthorSchema,
               resp=Response(HTTP_400=(WebError, "Request data error"),
                             HTTP_404=(WebError, "Author not found"),
                             HTTP_200=(AuthorSchema, 'Successful operation')),
               tags=["Authors_request"])
def update_author(author_id, db: Session = Session()):
    """
        Update an existing author

        Return updated author
    """
    if request is None:
        abort(make_response(WebError(error_code=400, msg="Request data error").dict(), 400))
    try:
        author = AuthorSchema(**request.json)
    except ValidationError as e:
        return "Exception" + e.json()
    _author = db.query(Authors).get(author_id)
    if _author is None:
        abort(make_response(WebError(error_code=404, msg="Author not found").dict(), 404))
    _author.author_name = author.author_name
    _author.author_surname = author.author_surname
    _author.author_patronymic = author.author_patronymic
    _author.date_of_birth = author.date_of_birth
    _author.date_of_death = author.date_of_death
    db.add(_author)
    db.commit()
    db.refresh(_author)
    author = AuthorSchema.from_orm(_author)
    return author


@authors_blueprint.delete("/api/authors/<int:author_id>")
@spec.validate(resp=Response(HTTP_404=(WebError, "Author not found"),
                             HTTP_200=(WebError, "Successful operation")), tags=["Authors_request"])
def delete_author(author_id, db: Session = Session()):
    """
        Delete Author with all his books

        Return delete message
    """
    author = db.query(Authors).get(author_id)
    if author is None:
        abort(make_response(WebError(error_code=404, msg="Author not found").dict(), 404))
    db.delete(author)
    db.commit()
    abort(make_response(WebError(error_code=200, msg="Author deleted").dict(), 200))
    pass
