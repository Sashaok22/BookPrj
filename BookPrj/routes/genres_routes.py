from flask import request, jsonify, abort, Blueprint, make_response
from pydantic import ValidationError
from spectree import Response
from SpecTree_config import spec
from alembic_BaseModels.Authors_BaseModels import AuthorSchema
from alembic_BaseModels.Books_BaseModels import BooksSchema
from alembic_BaseModels.Genres_BaseModels import GenresSchema
from alembic_BaseModels.Others_BaseModels import WebError
from models.Authors import Authors
from models.Books import Books
from models.Genres import Genres
from models.database import Session

genres_blueprint = Blueprint(__name__.split(".")[-1], __name__)


@genres_blueprint.get("/api/genres")
@spec.validate(resp=Response(HTTP_404=(WebError, "Genres not found"),
                             HTTP_200=(GenresSchema, 'Successful operation')), tags=["Genres_request"])
def get_genres(db: Session = Session()):
    genre = db.query(Genres).all()
    if not genre:
        abort(make_response(WebError(error_code=404, msg="Genres not found").dict(), 404))
    _genre = GenresSchema.from_orm(genre)
    return jsonify(_genre)


@genres_blueprint.get("/api/genres_authors/<int:genre_id>")
@spec.validate(resp=Response(HTTP_404=(WebError, "Authors not found"),
                             HTTP_200=(AuthorSchema, 'Successful operation')), tags=["Genres_request"])
def get_genres_authors(genre_id, db: Session = Session()):
    authors = db.query(Authors)\
        .join(Books.Books_Authors)\
        .join(Books.Books_Genres)\
        .filter(
        Genres.id == genre_id
    ).all()
    if not authors:
        abort(make_response(WebError(error_code=404, msg="Authors not found").dict(), 404))
    _authors = AuthorSchema.from_orm(authors)
    return _authors


@genres_blueprint.get("/api/genres_books/<int:genre_id>")
@spec.validate(resp=Response(HTTP_404=(WebError, "Books not found"),
                             HTTP_200=(BooksSchema, 'Successful operation')), tags=["Genres_request"])
def get_genres_books(genre_id, db: Session = Session()):
    books = db.query(Books)\
        .join(Books.Books_Genres)\
        .filter(
        Genres.id == genre_id
    ).all()
    if not books:
        abort(make_response(WebError(error_code=404, msg="Books not found").dict(), 404))
    _books = BooksSchema.from_orm(books)
    return _books


@genres_blueprint.get("/api/genres/<int:genre_id>")
@spec.validate(resp=Response(HTTP_404=(WebError, "Genre not found"),
                             HTTP_200=(GenresSchema, 'Successful operation')), tags=["Genres_request"])
def get_genre(genre_id, db: Session = Session()):
    genre = db.query(Genres).get(genre_id)
    if not genre:
        abort(make_response(WebError(error_code=404, msg="Genre not found").dict(), 404))
    _genre = GenresSchema.from_orm(genre)
    return _genre


@genres_blueprint.post("/api/genres")
@spec.validate(json=GenresSchema,
               resp=Response(HTTP_400=(WebError, "Request data error"),
                             HTTP_200=(GenresSchema, 'Successful operation')),
               tags=["Genres_request"])
def create_genre(db: Session = Session()):
    if not request:
        abort(make_response(WebError(error_code=400, msg="Request data error").dict(), 400))
    try:
        genre = GenresSchema(**request.json)
    except ValidationError as e:
        return "Exception" + e.json()
    _genre = Genres(**genre.dict())
    db.add(_genre)
    db.commit()
    db.refresh(_genre)
    genre = GenresSchema.from_orm(_genre)
    return genre


@genres_blueprint.put("/api/genres/<int:genre_id>")
@spec.validate(json=GenresSchema,
               resp=Response(HTTP_404=(WebError, "Genre not found"),
                             HTTP_400=(WebError, "Request data error"),
                             HTTP_200=(GenresSchema, 'Successful operation')),
               tags=["Genres_request"])
def update_genre(genre_id, db: Session = Session()):
    if not request:
        abort(make_response(WebError(error_code=400, msg="Request data error").dict(), 400))
    try:
        _genre = GenresSchema(**request.json)
    except ValidationError as e:
        return "Exception" + e.json()
    genre = db.query(Genres).get(genre_id)
    if not genre:
        abort(make_response(WebError(error_code=404, msg="Genre not found").dict(), 404))
    genre.genre_name = _genre.genre_name
    genre.short_description = _genre.short_description
    db.add(genre)
    db.commit()
    db.refresh(genre)
    _genre = GenresSchema.from_orm(genre)
    return _genre


@genres_blueprint.delete("/api/genres/<int:genre_id>")
@spec.validate(resp=Response(HTTP_404=(WebError, "Genre not found"),
                             HTTP_200=(GenresSchema, 'Successful operation')),
               tags=["Genres_request"])
def delete_genre(genre_id, db: Session = Session()):
    genre = db.query(Genres).get(genre_id)
    if not genre:
        abort(make_response(WebError(error_code=404, msg="Genre not found").dict(), 404))
    db.delete(genre)
    db.commit()
    abort(make_response(WebError(error_code=200, msg="Genre deleted").dict(), 200))
    pass
