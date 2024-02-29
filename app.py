import os
from flask import Flask, jsonify, request
from flask.helpers import get_flashed_messages
from lib.database_connection import get_flask_database_connection
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from dotenv import load_dotenv

from lib.models.user import User
from lib.repositories.user_repository import UserRepository
from lib.models.help_request import HelpRequest
from lib.repositories.help_request_repository import HelpRequestRepository

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

# Help Request Routes
@app.route('/help_requests', methods=['GET'])
def get_all_help_requests():
    connection = get_flask_database_connection(app)
    request_repository = HelpRequestRepository(connection)

    all_requests = request_repository.all_requests()
    if all_requests:
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
        return jsonify(request_data), 200
    return jsonify({"message" : "Unable to find all requests"}), 400

@app.route('/help_requests/<id>', methods=['GET'])
def get_one_help_request_by_id(id):
    connection = get_flask_database_connection(app)
    request_repository = HelpRequestRepository(connection)
    request = request_repository.find_request_by_id(id)
    if request:
        return jsonify({
            "id": request.id,
            "date": request.date.strftime("%Y-%m-%d %H:%M:%S"),
            "title": request.title,
            "message": request.message,
            "start_date": request.start_date.strftime("%Y-%m-%d"),
            "end_date": request.end_date.strftime("%Y-%m-%d"),
            "user_id": request.user_id,
            "maxprice": request.maxprice
        }), 200
    return jsonify({"message" : "Help Request not found"}), 400

@app.route('/help_requests/user/<user_id>', methods=['GET'])
@jwt_required()
def get_all_requests_made_by_one_user(user_id):
    connection = get_flask_database_connection(app)
    request_repository = HelpRequestRepository(connection)
    requests_by_user = request_repository.find_requests_by_user_id(user_id)

    formatted_requests = []
    for request in requests_by_user:
        formatted_request = {
            "id": request.id,
            "date": request.date.strftime("%Y-%m-%d %H:%M:%S"),
            "title": request.title,
            "message": request.message,
            "start_date": request.start_date.strftime("%Y-%m-%d"),
            "end_date": request.end_date.strftime("%Y-%m-%d"),
            "user_id": request.user_id,
            "maxprice": request.maxprice
        }
        formatted_requests.append(formatted_request)
        
    if formatted_requests: 
        return jsonify(formatted_requests), 200
    else:
        return jsonify({"message": "Help requests for current user not found"}), 400


@app.route("/help_requests/create/<user_id>", methods=['POST'])
@jwt_required()
def create_help_request(user_id):
    try:
        connection = get_flask_database_connection(app)
        request_repository = HelpRequestRepository(connection)
        date = request.json.get('date')
        title = request.json.get('title')
        message = request.json.get('message')
        start_date = request.json.get('start_date')
        end_date = request.json.get("end_date")
        maxprice = request.json.get("maxprice")
        if None in (date, title, message, start_date, end_date, maxprice):
            raise ValueError("All required fields must be filled")
        request_repository.create_request(HelpRequest(None, date, title, message, start_date, end_date, user_id, maxprice))
        return jsonify({"message" : "Help request created successfully"}), 200
    except:
        return jsonify({"message" : "Help request creation unsuccessful"}), 400

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5001)))
