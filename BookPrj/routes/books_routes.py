from flask import request, abort, Blueprint, make_response
from pydantic import ValidationError
from spectree import Response
from SpecTree_config import spec
from alembic_BaseModels.Authors_BaseModels import AuthorSchema
from alembic_BaseModels.Books_BaseModels import BooksSchema, Book_content, BookSchema, Book_content_id
from alembic_BaseModels.Genres_BaseModels import GenresSchema
from alembic_BaseModels.Others_BaseModels import WebError
from models.Authors import Authors
from models.Books import Books
from models.Genres import Genres
from models.database import Session

books_blueprint = Blueprint(__name__.split(".")[-1], __name__)


@books_blueprint.get("/api/books")
@spec.validate(resp=Response(HTTP_404=(WebError, "Books not found"),
                             HTTP_200=(BooksSchema, 'Successful operation')), tags=["Books_request"])
def get_books(db: Session = Session()):
    """
        Get all books

        Return all books with all their authors and genres
    """
    book = db.query(Books)
    if not request.values:
        _book = book.all()
    else:
        reit = request.values['rating']
        _book = book.filter(Books.rating == reit).all()
    if not _book:
        abort(make_response(WebError(error_code=404, msg="Books not found").dict(), 404))
    all_books = []
    for b in _book:
        book = Book_content.from_orm(b)
        genres = b.Books_Genres
        book.genres = [GenresSchema.from_orm(g) for g in genres]
        authors = b.Books_Authors
        book.books = [AuthorSchema.from_orm(a) for a in authors]
        all_books.append(book)
    response = BooksSchema()
    response.books = all_books
    return response


@books_blueprint.get("/api/books/<int:book_id>")
@spec.validate(resp=Response(HTTP_404=(WebError, "Books not found"),
                             HTTP_200=(Book_content, 'Successful operation')), tags=["Books_request"])
def get_book(book_id, db: Session = Session()):
    """
        Find one book by id

        Return one book by id with all its authors and genres
    """
    book = db.query(Books).get(book_id)
    if book is None:
        abort(make_response(WebError(error_code=404, msg="Books not found").dict(), 404))
    _book = Book_content.from_orm(book)
    genres = book.Books_Genres
    _book.genres = [GenresSchema.from_orm(g) for g in genres]
    authors = book.Books_Authors
    _book.books = [AuthorSchema.from_orm(a) for a in authors]
    return _book


@books_blueprint.post("/api/books")
@spec.validate(json=Book_content_id,
               resp=Response(HTTP_400=(WebError, "Request data error"),
                             HTTP_404=(WebError, "Books not found"),
                             HTTP_200=(Book_content, 'Successful operation')), tags=["Books_request"])
def create_book(db: Session = Session()):
    """
        Add new book with all its authors and genres

        Return new book
    """
    if request is None:
        abort(make_response(WebError(error_code=400, msg="Request data error").dict(), 400))
    try:
        book = BookSchema(**request.json)
    except ValidationError as e:
        return "Exception" + e.json()
    _book = Books(**book.dict())
    db.add(_book)
    book = Book_content.from_orm(book)

    # adding genres to the created book
    genre_list = [db.query(Genres).get(gnr_id)
                  for gnr_id in request.json["genres_id"]
                  if db.query(Genres).get(gnr_id) is not None]
    if not genre_list:
        abort(make_response(WebError(error_code=404, msg="Genres not found").dict(), 404))
    [gnr.book.append(_book) for gnr in genre_list]

    # adding authors to the created book
    author_list = [db.query(Authors).get(author_id)
                   for author_id in request.json["authors_id"]
                   if db.query(Authors).get(author_id) is not None]
    if not author_list:
        abort(make_response(WebError(error_code=404, msg="Authors not found").dict(), 404))
    [author.book.append(_book) for author in author_list]

    db.commit()
    db.refresh(_book)
    book.genres = genre_list
    book.authors = author_list
    return book


@books_blueprint.put("/api/books/<int:book_id>")
@spec.validate(json=Book_content_id,
               resp=Response(HTTP_400=(WebError, "Request data error"),
                             HTTP_404=(WebError, "Books not found"),
                             HTTP_200=(Book_content, 'Successful operation')), tags=["Books_request"])
def update_book(book_id, db: Session = Session()):
    """
        Update book with all its authors and genres

        Return updated book
    """
    if request is None:
        abort(make_response(WebError(error_code=400, msg="Request data error").dict(), 400))
    try:
        BookSchema(**request.json)
    except ValidationError as e:
        return "Exception" + e.json()
    book = db.query(Books).get(book_id)
    if book is None:
        abort(make_response(WebError(error_code=404, msg="Book not found").dict(), 404))
    book.book_name = request.json['book_name']
    book.number_of_pages = request.json['number_of_pages']
    book.rating = request.json['rating']
    db.add(book)
    _book = Book_content.from_orm(book)

    [gnr.book.remove(book) for gnr in book.Books_Genres]
    genre_list = [db.query(Genres).get(gnr_id)
                  for gnr_id in request.json["genres_id"]
                  if db.query(Genres).get(gnr_id) is not None]
    if not genre_list:
        abort(make_response(WebError(error_code=404, msg="Genres not found").dict(), 404))
    [gnr.book.append(book) for gnr in genre_list]

    [author.book.remove(book) for author in book.Books_Authors]
    author_list = [db.query(Authors).get(author_id)
                   for author_id in request.json["authors_id"]
                   if db.query(Authors).get(author_id) is not None]
    if not author_list:
        abort(make_response(WebError(error_code=404, msg="Authors not found").dict(), 404))
    [author.book.append(book) for author in author_list]

    db.commit()
    db.refresh(book)
    _book.genres = genre_list
    _book.authors = author_list
    return _book


@books_blueprint.delete("/api/books/<int:book_id>")
@spec.validate(resp=Response(HTTP_404=(WebError, "Books not found"),
                             HTTP_200=(WebError, 'Successful operation')), tags=["Books_request"])
def delete_book(book_id, db: Session = Session()):
    """
        Delete book

        Return delete message
    """
    book = db.query(Books).get(book_id)
    if book is None:
        abort(make_response(WebError(error_code=404, msg="Books not found").dict(), 404))
    db.delete(book)
    db.commit()
    abort(make_response(WebError(error_code=200, msg="Book deleted").dict(), 200))
    pass
