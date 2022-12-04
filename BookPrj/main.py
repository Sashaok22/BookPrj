from flask import Flask, request, jsonify, abort
from pydantic import ValidationError

from Create_db import create_database
from json_serializable import JSONSerializable
from models.Genres import Genres, GenresSchema
from models.database import Session

app = Flask(__name__)
JSONSerializable(app)
app.config['SECRET_KEY'] = 'VERY VERY VERY SECRET KEY'


@app.route("/")
def hello():
    return "Main"


@app.get("/api/genres")
def get_genres(db: Session = Session()):
    genre = db.query(Genres).all()
    if genre is None:
        abort(404)
    return jsonify(genre)


@app.get("/api/genres/<int:genre_id>")
def get_genre(genre_id, db: Session = Session()):
    genre = db.query(Genres).get(genre_id)
    if genre is None:
        abort(404)
    return jsonify(genre)


@app.post("/api/genres")
def create_genre(db: Session = Session()):
    if request == None:
        abort(400)

    try:
        genre = GenresSchema(genre_name=request.form["genre_name"],
                             short_description=request.form["short_description"])
    except ValidationError as e:
        return "Exception" + e.json()
    _genre = Genres(**genre.dict())
    db.add(_genre)
    db.commit()
    db.refresh(_genre)
    return jsonify(_genre)


@app.put("/api/genres/<int:genre_id>")
def update_genre(genre_id, db: Session = Session()):
    if request == None:
        abort(400)
    try:
        genre = GenresSchema(genre_name=request.form["genre_name"],
                             short_description=request.form["short_description"])
    except ValidationError as e:
        return "Exception" + e.json()
    genre = db.query(Genres).get(genre_id)
    if genre is None:
        abort(404)
    genre.genre_name = request.form["genre_name"]
    genre.short_description = request.form["short_description"]
    db.add(genre)
    db.commit()
    db.refresh(genre)
    return jsonify(genre)


@app.delete("/api/genres/<int:genre_id>")
def delete_genre(genre_id, db: Session = Session()):
    genre = db.query(Genres).get(genre_id)
    if genre is None:
        abort(404)
    db.delete(genre)
    db.commit()
    return jsonify(True)


if __name__ == "__main__":
    create_database()
    app.run()
