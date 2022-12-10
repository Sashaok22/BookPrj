from flask import request, abort, Blueprint, make_response
from pydantic import ValidationError
from spectree import Response
from SpecTree_config import spec
from alembic_BaseModels.Authors_BaseModels import AuthorsSchema
from alembic_BaseModels.Books_BaseModels import BooksSchema
from alembic_BaseModels.Genres_BaseModels import GenreSchema, GenresSchema
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
    """
        Get all genres

        Return all genres
    """
    genre = db.query(Genres).all()
    if not genre:
        abort(make_response(WebError(error_code=404, msg="Genres not found").dict(), 404))
    response = GenresSchema()
    response.genres = genre
    return response


@genres_blueprint.get("/api/genres_authors/<int:genre_id>")
@spec.validate(resp=Response(HTTP_404=(WebError, "Authors not found"),
                             HTTP_200=(AuthorsSchema, 'Successful operation')), tags=["Genres_request"])
def get_genres_authors(genre_id, db: Session = Session()):
    """
        Find all authors by genre

        Return all authors by genre
    """
    authors = db.query(Authors)\
        .join(Books.Books_Authors)\
        .join(Books.Books_Genres)\
        .filter(
        Genres.id == genre_id
    ).all()
    if not authors:
        abort(make_response(WebError(error_code=404, msg="Authors not found").dict(), 404))
    response = AuthorsSchema()
    response.authors = authors
    return response


@genres_blueprint.get("/api/genres_books/<int:genre_id>")
@spec.validate(resp=Response(HTTP_404=(WebError, "Books not found"),
                             HTTP_200=(BooksSchema, 'Successful operation')), tags=["Genres_request"])
def get_genres_books(genre_id, db: Session = Session()):
    """
        Find all books by genre

        Return all books by genre
    """
    books = db.query(Books)\
        .join(Books.Books_Genres)\
        .filter(
        Genres.id == genre_id
    ).all()
    if not books:
        abort(make_response(WebError(error_code=404, msg="Books not found").dict(), 404))
    response = BooksSchema()
    response.books = books
    return response


@genres_blueprint.get("/api/genres/<int:genre_id>")
@spec.validate(resp=Response(HTTP_404=(WebError, "Genre not found"),
                             HTTP_200=(GenreSchema, 'Successful operation')), tags=["Genres_request"])
def get_genre(genre_id, db: Session = Session()):
    """
        Find one genre by id

        Return one genre by id
    """
    genre = db.query(Genres).get(genre_id)
    if not genre:
        abort(make_response(WebError(error_code=404, msg="Genre not found").dict(), 404))
    _genre = GenreSchema.from_orm(genre)
    return _genre


@genres_blueprint.post("/api/genres")
@spec.validate(json=GenreSchema,
               resp=Response(HTTP_400=(WebError, "Request data error"),
                             HTTP_200=(GenreSchema, 'Successful operation')),
               tags=["Genres_request"])
def create_genre(db: Session = Session()):
    """
        Add new genre

        Return new genre
    """
    if not request:
        abort(make_response(WebError(error_code=400, msg="Request data error").dict(), 400))
    try:
        genre = GenreSchema(**request.json)
    except ValidationError as e:
        return "Exception" + e.json()
    _genre = Genres(**genre.dict())
    db.add(_genre)
    db.commit()
    db.refresh(_genre)
    genre = GenreSchema.from_orm(_genre)
    return genre


@genres_blueprint.put("/api/genres/<int:genre_id>")
@spec.validate(json=GenreSchema,
               resp=Response(HTTP_404=(WebError, "Genre not found"),
                             HTTP_400=(WebError, "Request data error"),
                             HTTP_200=(GenreSchema, 'Successful operation')),
               tags=["Genres_request"])
def update_genre(genre_id, db: Session = Session()):
    """
        Update genre

        Return updated genre
    """
    if not request:
        abort(make_response(WebError(error_code=400, msg="Request data error").dict(), 400))
    try:
        _genre = GenreSchema(**request.json)
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
    _genre = GenreSchema.from_orm(genre)
    return _genre


@genres_blueprint.delete("/api/genres/<int:genre_id>")
@spec.validate(resp=Response(HTTP_404=(WebError, "Genre not found"),
                             HTTP_200=(GenreSchema, 'Successful operation')),
               tags=["Genres_request"])
def delete_genre(genre_id, db: Session = Session()):
    """
        Delete genre

        Return delete message
    """
    genre = db.query(Genres).get(genre_id)
    if not genre:
        abort(make_response(WebError(error_code=404, msg="Genre not found").dict(), 404))
    db.delete(genre)
    db.commit()
    abort(make_response(WebError(error_code=200, msg="Genre deleted").dict(), 200))
    pass
