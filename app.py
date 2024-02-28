import os
from flask import Flask
from lib.database_connection import get_flask_database_connection

app = Flask(__name__)

# stuff goes here


if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5001)))
