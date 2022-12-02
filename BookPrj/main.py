from flask import Flask
from Create_db import create_database

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello world!"


if __name__ == "__main__":
    create_database()
    app.run()
