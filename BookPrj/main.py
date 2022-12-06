from flask import Flask, request, jsonify, abort, json, Blueprint
from pydantic import ValidationError
from sqlalchemy import and_, func
from Create_db import create_database
from json_serializable import JSONSerializable
from models.Authors import Authors, AuthorsSchema, books_authors
from models.Books import Books, BooksSchema
from models.Genres import Genres, GenresSchema, books_genres
from models.database import Session

app = Flask(__name__)
JSONSerializable(app)
app.config['SECRET_KEY'] = 'VERY VERY VERY SECRET KEY'
app.debug = True

bp1 = Blueprint(__name__.split(".")[-1], __name__)



@bp1.route("/qq")
def qq():
    return "Main"


@app.route("/")
def hello():
    return "Main"


@app.get("/api/genres")
def get_genres(db: Session = Session()):
    genre = db.query(Genres).all()
    if not genre:
        abort(404)
    return jsonify(genre)


@app.get("/api/genres_authors/<int:genre_id>")
def get_genres_authors(genre_id, db: Session = Session()):
    authors = db.query(Books).filter(and_(
        books_genres.c.book_id == Books.id,
        books_genres.c.genre_id == Genres.id,
        books_authors.c.book_id == Books.id,
        books_authors.c.author_id == Authors.id,
        Genres.id == genre_id
    )).all()
    if not authors:
        abort(404)
    return jsonify(authors)


@app.get("/api/genres_books/<int:genre_id>")
def get_genres_books(genre_id, db: Session = Session()):
    books = db.query(Books).filter(and_(
        books_genres.c.book_id == Books.id,
        books_genres.c.genre_id == Genres.id,
        Genres.id == genre_id
    )).all()
    if not books:
        abort(404)
    return jsonify(books)


@app.get("/api/genres/<int:genre_id>")
def get_genre(genre_id, db: Session = Session()):
    genre = db.query(Genres).get(genre_id)
    if not genre:
        abort(404)
    return jsonify(genre)


@app.post("/api/genres")
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


@app.put("/api/genres/<int:genre_id>")
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


@app.delete("/api/genres/<int:genre_id>")
def delete_genre(genre_id, db: Session = Session()):
    genre = db.query(Genres).get(genre_id)
    if not genre:
        abort(404)
    db.delete(genre)
    db.commit()
    return jsonify(True)


@app.get("/api/authors")
def get_authors(db: Session = Session()):
    author = db.query(Authors, Books, Genres).filter(and_(
        books_genres.c.book_id == Books.id,
        books_genres.c.genre_id == Genres.id,
        books_authors.c.book_id == Books.id,
        books_authors.c.author_id == Authors.id,
    )).all()
    if not author:
        abort(404)
    data = []
    for row in author:
        data.append([x for x in row])
    return jsonify(data)


@app.get("/api/authors/<int:author_id>")
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


@app.post("/api/authors")
def create_author(db: Session = Session()):
    if request == None:
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


@app.put("/api/authors/<int:author_id>")
def update_author(author_id, db: Session = Session()):
    if request == None:
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


@app.delete("/api/authors/<int:author_id>")
def delete_author(author_id, db: Session = Session()):
    author = db.query(Authors).get(author_id)
    if author is None:
        abort(404)
    db.delete(author)
    db.commit()
    return jsonify(True)


@app.get("/api/books")
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


@app.get("/api/books/<int:book_id>")
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


@app.post("/api/books")
def create_book(db: Session = Session()):
    if request == None:
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


@app.put("/api/books/<int:book_id>")
def update_book(book_id, db: Session = Session()):
    if request == None:
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


@app.delete("/api/books/<int:book_id>")
def delete_book(book_id, db: Session = Session()):
    book = db.query(Books).get(book_id)
    if book is None:
        abort(404)
    db.delete(book)
    db.commit()
    return jsonify(True)


if __name__ == "__main__":
    app.register_blueprint(bp1)
    create_database()
    app.run()
