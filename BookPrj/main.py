from flask import Flask
from Create_db import create_database
from models.Genres import Genres
from models.database import Session

app = Flask(__name__)


@app.route("/")
def hello(**dct):
    return "Main"

@app.get("/api/genres")
def get_people(db: Session = Session()):
    return db.query(Genres).all()


if __name__ == "__main__":
    create_database()
    app.run()
