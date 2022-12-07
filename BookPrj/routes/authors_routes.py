from flask import request, Blueprint
from pydantic import ValidationError
from spectree import SpecTree, Response
from models.Authors import Authors, WebError, AuthorSchema, AuthorsSchema, Author_content
from models.Books import Books, BooksSchema
from models.Genres import Genres, GenresSchema
from models.database import Session

authors_blueprint = Blueprint(__name__.split(".")[-1], __name__)
spec = SpecTree("flask")


@authors_blueprint.get("/api/authors")
@spec.validate(resp=Response(HTTP_404=(WebError, "Author not found"),
                             HTTP_200=(AuthorsSchema, 'Successful operation')), tags=["Authors_request"])
def get_authors(db: Session = Session()):
    """
        Get all authors.
    """
    authors = db.query(Authors) \
        .join(Books.Books_Authors) \
        .join(Books.Books_Genres).all()
    if not authors:
        return WebError(**{'error_code': 404, 'msg': "Authors not found"})
    all_authors = []
    for a in authors:
        _author = Author_content(**a.to_dict())
        genres = db.query(Genres).join(Books.Books_Authors).join(Books.Books_Genres).all()
        _author.genres = [GenresSchema(**g.to_dict()) for g in genres]
        books = a.book
        _author.books = [BooksSchema(**b.to_dict()) for b in books]
        all_authors.append(_author)
    response = AuthorsSchema()
    response.Authors = all_authors
    return response


@authors_blueprint.get("/api/authors/<int:author_id>")
@spec.validate(resp=Response(HTTP_404=(WebError, "Author not found"),
                             HTTP_200=(Author_content, 'Successful operation')), tags=["Authors_request"])
def get_author(author_id, db: Session = Session()):
    """
        Find author by id.
    """
    author = db.query(Authors) \
        .join(Books.Books_Authors) \
        .join(Books.Books_Genres) \
        .filter(Authors.id == author_id).all()
    if not author:
        return WebError(**{'error_code': 404, 'msg': "Author not found"})
    _author = Author_content(**author[0].to_dict())
    genres = db.query(Genres).join(Books.Books_Authors).join(Books.Books_Genres).all()
    _author.genres = [GenresSchema(**g.to_dict()) for g in genres]
    books = author[0].book
    _author.books = [BooksSchema(**b.to_dict()) for b in books]
    return _author


@authors_blueprint.post("/api/authors")
@spec.validate(json=AuthorSchema,
               resp=Response(HTTP_400=(WebError, "Invalid author data"),
                             HTTP_200=(AuthorSchema, 'Successful operation')),
               tags=["Authors_request"])
def create_author(db: Session = Session()):
    """
        Add new author.
    """
    if request.json is None:
        return WebError(**{'error_code': 400, 'msg': "Invalid author data"})
    try:
        author = AuthorSchema(**request.json)
    except ValidationError as e:
        return "Exception" + e.json()
    _author = Authors(**author.dict())
    db.add(_author)
    db.commit()
    db.refresh(_author)
    return author


@authors_blueprint.put("/api/authors/<int:author_id>")
@spec.validate(json=AuthorSchema,
               resp=Response(HTTP_400=(WebError, "Invalid author data"),
                             HTTP_404=(WebError, "Author not found"),
                             HTTP_200=(AuthorSchema, 'Successful operation')),
               tags=["Authors_request"])
def update_author(author_id, db: Session = Session()):
    """
        Update an existing author
    """
    if request is None:
        return WebError(**{'error_code': 400, 'msg': "Invalid author data"})
    try:
        author = AuthorSchema(**request.json)
    except ValidationError as e:
        return "Exception" + e.json()
    _author = db.query(Authors).get(author_id)
    if author is None:
        return WebError(**{'error_code': 404, 'msg': "Author not found"})
    _author = Authors(**author.dict())
    db.add(_author)
    db.commit()
    db.refresh(_author)
    return author


@authors_blueprint.delete("/api/authors/<int:author_id>")
@spec.validate(json=AuthorSchema,
               resp=Response(HTTP_404=(WebError, "Author not found"),
                             HTTP_200=(WebError, 'Successful operation')), tags=["Authors_request"])
def delete_author(author_id, db: Session = Session()):
    """
        Delete Author
    """
    author = db.query(Authors).get(author_id)
    if author is None:
        return WebError(**{'error_code': 404, 'msg': "Author not found"})
    db.delete(author)
    db.commit()
    return WebError(**{'error_code': 200, 'msg': "Author successful deleted"})
