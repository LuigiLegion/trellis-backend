# Imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# Initializations
# Initialize server
app = Flask(__name__)


# Run server
if __name__ == "__main__":
    app.run(debug=True)
