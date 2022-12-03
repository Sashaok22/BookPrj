from flask import Flask, request, jsonify
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
    return jsonify(db.query(Genres).all())


@app.get("/api/genres/<int:genre_id>")
def get_genre(genre_id, db: Session = Session()):
    genre = db.query(Genres).filter(Genres.id == genre_id).first()
    return jsonify(genre)


@app.post("/api/genres")
def create_genre(db: Session = Session()):
    genre = GenresSchema(genre_name=request.form["genre_name"],
                         short_description=request.form["short_description"])
    _genre = Genres(**genre.dict())
    db.add(_genre)
    db.commit()
    db.refresh(_genre)
    return jsonify(_genre)


@app.delete("/api/genres/<int:genre_id>")
def delete_genre(genre_id, db: Session = Session()):
    genre = db.query(Genres).filter(Genres.id == genre_id).first()
    db.delete(genre)
    db.commit()
    return jsonify(db.query(Genres).all())


if __name__ == "__main__":
    create_database()
    app.run()
