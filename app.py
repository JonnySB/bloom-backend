import os
from flask import Flask, jsonify, request
from lib.database_connection import get_flask_database_connection
from flask_jwt_extended import JWTManager, create_access_token
from dotenv import load_dotenv

from lib.repositories.user_repository import UserRepository
from lib.repositories.help_offer_repository import HelpOfferRepository
from lib.models.help_offer import HelpOffer

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


#get all help offers made by a specific user
@app.route("/help_offers/<user_id>", methods=["GET"])
def find_offers_by_user_id(user_id):

    #connect to db and set up offer repository
    connection = get_flask_database_connection(app)
    offer_repository = HelpOfferRepository(connection)

    #returns array of HelpOffer object IDs made by user matching user_id
    offers_by_user = offer_repository.find_by_user(user_id)
    user_offer_ids = []
    for offer in offers_by_user:
        user_offer_ids.append(offer.id)

    return jsonify({"user_offer_ids": user_offer_ids})

#create a new help offer for a help request
@app.route("/help_offers/<help_request_id>", methods=["POST"])
def create_help_offer(help_request_id):

    #connect to db and set up offer repository
    connection = get_flask_database_connection(app)
    offer_repository = HelpOfferRepository(connection)

    #get data from request body and create help_offer in DB
    user_id = request.json.get("user_id", None)
    request_id = help_request_id
    message = request.json.get("message", None)
    bid = request.json.get("bid", None)
    status = request.json.get("status", None)

    new_offer = HelpOffer(None, user_id, request_id, message, bid, status)
    offer_repository.create_offer(new_offer)
    return 201

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5001)))
