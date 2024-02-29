import os
from flask import Flask, jsonify, request
from flask.helpers import get_flashed_messages
from lib.database_connection import get_flask_database_connection
from flask_jwt_extended import JWTManager, create_access_token
from dotenv import load_dotenv

from lib.models.user import User
from lib.repositories.user_repository import UserRepository

# load .env file variables see readme details
load_dotenv()

app = Flask(__name__)

# Token Setup
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)


# Takes username / email and password from POST request
# Returns authentication token if good match, otherwise 401
@app.route("/token", methods=["POST"])
def create_token():
    # get username or email and password
    username_email = request.json.get("username_email", None)
    password = request.json.get("password", None)

    # query db to ensure user exists:
    connection = get_flask_database_connection(app)
    user_repository = UserRepository(connection)

    # returns user_id if correct, otherwise false
    user_id = user_repository.check_username_or_email_and_password(
        username_email, password
    )

    # catch if username_email / password combination is not in db
    if not user_id:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=user_id)
    return jsonify({"token": access_token, "user_id": user_id})


# Takes user details from POST request
# creates user in database
# return 200 if okay, otherwise 401
@app.route("/user/signup", methods=["POST"])
def create_user():
    # NOTE - form validation must be handled on the front end to ensure that
    # appropriate fields are completed. e.g. first_name != "" etc.
    first_name = request.json.get("first_name")
    last_name = request.json.get("last_name")
    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")
    password_confirm = request.json.get("password_confirm")
    address = request.json.get("address")

    if password == password_confirm:
        try:
            user = User(None, first_name, last_name, username, email, password, address)

            connection = get_flask_database_connection(app)
            user_repository = UserRepository(connection)
            user_repository.add_user_to_db(user)

            return jsonify({"msg": "User created"}), 200
        except:
            return (
                jsonify(
                    {
                        "msg": "Bad request - user not created. This username or email could be taken."
                    }
                ),
                401,
            )

    return (
        jsonify({"msg": "Bad request - user not created. Passwords does not match."}),
        401,
    )


# Takes user_id and returns user_details
@app.route("/user_details/<id>")
def get_user_details(id):
    connection = get_flask_database_connection(app)
    user_repository = UserRepository(connection)
    user = user_repository.get_user_by_id(id)

    print(user)

    if user:
        return (
            jsonify(
                {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "username": user.username,
                    "email": user.email,
                    "avatar_url_string": user.avatar_url_string,
                    "address": user.address,
                }
            )
        ), 200
    return jsonify({"msg": "User not found"}), 400


##### MORE ROUTES GO HERE #####


if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5001)))
