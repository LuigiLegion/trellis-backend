# Imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, drop_database, create_database

from secrets import (
    POSTGRESQL_URI,
    POSTGRESQL_USERNAME,
    POSTGRESQL_PASSWORD,
    POSTGRESQL_DATABASE,
)


# Initializations
# Initialize server
app = Flask(__name__)
# Configure database connection
DATABASE_URI = f"postgresql+psycopg2://{POSTGRESQL_USERNAME}:{POSTGRESQL_PASSWORD}@{POSTGRESQL_URI}/{POSTGRESQL_DATABASE}"
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Suppress deprecation warning
# Initialize database
db = SQLAlchemy(app)
# db.init_app(app)


@app.cli.command("resetdb")
def reset_db():
    """ Destroys and creates database and tables. """

    if database_exists(DATABASE_URI):
        print("Dropping database...")
        drop_database(DATABASE_URI)

    if not database_exists(DATABASE_URI):
        print("Creating database...")
        create_database(DATABASE_URI)

    print("Creating tables...")
    db.create_all()
    print("Tables created successfully!")


# Models
class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25), nullable=False, unique=True)


class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False, unique=True)


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)


# Run server
if __name__ == "__main__":
    app.run(debug=True)
