import os
from flask import Flask, jsonify, request
from lib.database_connection import get_flask_database_connection
from flask_jwt_extended import JWTManager, create_access_token
from dotenv import load_dotenv

from lib.repositories.user_repository import UserRepository
from lib.repositories.help_request_repository import HelpRequestRepository

# load .env file variables see readme details
load_dotenv()

app = Flask(__name__)

# Token Setup
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)


# get token - login
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


##### MORE ROUTES GO HERE #####

# Help Request Routes
@app.route('/help_requests', methods=['GET'])
def get_all_help_requests():
    connection = get_flask_database_connection(app)
    request_repository = HelpRequestRepository(connection)

    all_requests = request_repository.all_requests()
    request_data = [
        {
            "id": request.id,
            "date": request.date.strftime("%Y-%m-%d %H:%M:%S"),
            "title": request.title,
            "message": request.message,
            "start_date": request.start_date.strftime("%Y-%m-%d"),
            "end_date": request.end_date.strftime("%Y-%m-%d"),
            "user_id": request.user_id,
            "maxprice": request.maxprice
        }
        for request in all_requests
    ]
    return jsonify(request_data)


if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5001)))
