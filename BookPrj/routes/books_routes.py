from flask import request, jsonify, abort, Blueprint
from pydantic import ValidationError
from sqlalchemy import and_
from models.Authors import Authors, books_authors
from models.Books import Books, BooksSchema
from models.Genres import Genres, books_genres
from models.database import Session

books_blueprint = Blueprint(__name__.split(".")[-1], __name__)


@books_blueprint.get("/api/books")
def get_books(db: Session = Session()):
    book = db.query(Books)
    if not request.values:
        _book = book.all()
    else:
        reit = request.values['reiting']
        _book = book.filter(Books.reiting == reit).all()
    _book = [
        {
            "book": b,
            "authors": b.Books_Authors,
            "genres": b.Books_Genres
        }
        for b in _book
    ]
    if not _book:
        abort(404)
    return jsonify(_book)


@books_blueprint.get("/api/books/<int:book_id>")
def get_book(book_id, db: Session = Session()):
    book = db.query(Books, Genres, Authors).filter(and_(
        books_genres.c.book_id == Books.id,
        books_genres.c.genre_id == Genres.id,
        books_authors.c.book_id == Books.id,
        books_authors.c.author_id == Authors.id,
        Books.id == book_id
    )).all()
    if book is None:
        abort(404)
    data = []
    for row in book:
        data.append([x for x in row])
    return jsonify(data)


@books_blueprint.post("/api/books")
def create_book(db: Session = Session()):
    if request is None:
        abort(400)
    try:
        book = BooksSchema(**request.form)
    except ValidationError as e:
        return "Exception" + e.json()
    _book = Books(**book.dict())
    db.add(_book)

    # adding genres to the created book
    genres_list_id = request.form["genres_id"].split(',')
    genre_list = [db.query(Genres).get(gnr_id) for gnr_id in genres_list_id]
    [gnr.book.append(_book) for gnr in genre_list]

    # adding authors to the created book
    authors_list_id = request.form["authors_id"].split(',')
    author_list = [db.query(Authors).get(author_id) for author_id in authors_list_id]
    [author.book.append(_book) for author in author_list]

    db.commit()
    db.refresh(_book)
    return jsonify(_book)


@books_blueprint.put("/api/books/<int:book_id>")
def update_book(book_id, db: Session = Session()):
    if request is None:
        abort(400)
    try:
        BooksSchema(**request.form)
    except ValidationError as e:
        return "Exception" + e.json()
    book = db.query(Books).get(book_id)
    if book is None:
        abort(404)
    book.book_name = request.form['book_name']
    book.number_of_pages = request.form['number_of_pages']
    book.reiting = request.form['reiting']
    db.add(book)

    genre_list = db.query(Genres).filter(and_(
        books_genres.c.book_id == book.id,
        books_genres.c.genre_id == Genres.id
    )).all()
    [gnr.book.remove(book) for gnr in genre_list]
    genres_list_id = request.form["genres_id"].split(',')
    genre_list = [db.query(Genres).get(gnr_id) for gnr_id in genres_list_id]
    [gnr.book.append(book) for gnr in genre_list]

    author_list = db.query(Authors).filter(and_(
        books_authors.c.book_id == book.id,
        books_authors.c.author_id == Authors.id
    )).all()
    [author.book.remove(book) for author in author_list]
    authors_list_id = request.form["authors_id"].split(',')
    author_list = [db.query(Authors).get(author_id) for author_id in authors_list_id]
    [author.book.append(book) for author in author_list]

    db.commit()
    db.refresh(book)
    return jsonify(book)


@books_blueprint.delete("/api/books/<int:book_id>")
def delete_book(book_id, db: Session = Session()):
    book = db.query(Books).get(book_id)
    if book is None:
        abort(404)
    db.delete(book)
    db.commit()
    return jsonify(True)
