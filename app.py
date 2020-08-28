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
def reset_database():
    """ Drops and recreates database and tables. """

    if database_exists(DATABASE_URI):
        print("Dropping database...")
        drop_database(DATABASE_URI)

    if not database_exists(DATABASE_URI):
        print("Creating database...")
        create_database(DATABASE_URI)

    print("Creating tables...")

    db.create_all()

    print("Database reset successfully!")


@app.cli.command("seeddb")
def seed_database():
    """ Seeds database with dummy data. """

    def seed_table(table, data):
        """ Seeds table with dummy data. """

        print(f"Seeding {table} table...")

        for datum in data:
            db.session.add(datum)

        db.session.commit()

    boards = [Board(title="Projects")]
    seed_table("Board", boards)

    lists = [
        List(title="Backlog", board_id=1),
        List(title="Ongoing", board_id=1),
        List(title="Completed", board_id=1),
    ]
    seed_table("List", lists)

    cards = [
        Card(title="Go project", list_id=1),
        Card(title="Python project", list_id=2),
        Card(title="TypeScript project", list_id=2),
        Card(title="JavaScript project", list_id=3),
    ]
    seed_table("Card", cards)

    print("Database seeded successfully!")


# Models
class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25), nullable=False, unique=True)

    lists = db.relationship("List", backref="lists_board")


class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False, unique=True)
    board_id = db.Column(db.Integer, db.ForeignKey("board.id"), nullable=False)

    lists = db.relationship("Card", backref="cards_list")


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey("list.id"), nullable=False)


# Run server
if __name__ == "__main__":
    app.run(debug=True)
