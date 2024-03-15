import os
from datetime import timedelta
import requests

import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, request
from flask.helpers import get_flashed_messages
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
# dependecies for livechat
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms

from werkzeug.utils import secure_filename

from lib.database_connection import get_flask_database_connection

from lib.models.extended_help_offer import ExtendedHelpOffer
from lib.models.help_offer import HelpOffer
from lib.models.help_request import HelpRequest
from lib.models.user import User
from lib.repositories.chat_repository import ChatRepository
from lib.repositories.extended_help_offer_repository import \
    ExtendedHelpOfferRepository
from lib.repositories.help_offer_repository import HelpOfferRepository
from lib.repositories.help_request_repository import HelpRequestRepository
from lib.repositories.plants_repository import PlantsRepository
from lib.repositories.plants_user_repository import PlantsUserRepository
from lib.repositories.user_repository import UserRepository

load_dotenv()


app = Flask(__name__)


# Token Setup
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
    days=1
)  # I JUST ADD THIS FOR NOW SO THE TOKEN DON"T KEEP EXIRING PLEASE REMOVE LATER.

CORS(app, origins=["http://localhost:5173"], supports_credentials=True) # also added this

socketio = SocketIO(
    app,
    cors_allowed_origins=["http://localhost:5173"],# added this instead of allowing all 
    logger=True,
    engineio_logger=True,
    async_mode="gevent",
)  # we are allowing all origings just for development
jwt = JWTManager(app)


# Takes username / email and password from POST request
# Returns authentication token if good match, otherwise 401
@app.route("/token", methods=["POST"])
@cross_origin()
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
    return jsonify({"token": access_token, "user_id": user_id}), 201


# Takes user details from POST request
# creates user in database
# return 201 if okay, otherwise 401
@app.route("/user/signup", methods=["POST"])
@cross_origin()
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
            user = User(
                None, first_name, last_name, username, email, password, "", address
            )

            connection = get_flask_database_connection(app)
            user_repository = UserRepository(connection)
            user_repository.add_user_to_db(user)

            return jsonify({"msg": "User created"}), 201
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
@cross_origin()  # WE NEED TO PASS THE CORS ORIGIN IN ORDER TO ENABLE THE BROWSER TO MAKE REQUESTS FROM THE ORIGIN DOMAIN
def get_user_details(id):
    connection = get_flask_database_connection(app)
    user_repository = UserRepository(connection)
    user = user_repository.get_user_by_id(id)

    if user:
        return (
            jsonify(
                {
                    "id": user.id,
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


# Takes user_id and updates the user_details
@app.route("/edit_user_details/<int:id>", methods=["PUT", "OPTIONS"])
@jwt_required()
def edit_user_details(id):
    if request.method == "OPTIONS":
        response = make_response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Methods"] = "PUT, OPTIONS"
        return response

    # PUT request processing
    try:
        connection = get_flask_database_connection(app)
        user_repository = UserRepository(connection)
        first_name = request.json.get("first_name")
        last_name = request.json.get("last_name")
        username = request.json.get("username")
        email = request.json.get("email")
        address = request.json.get("address")

        user_repository.edit_user_details(
            id, first_name, last_name, username, email, address
        )
        response = make_response(jsonify({"msg": "User updated successful"}), 200)
        print(response)
        return response

    except Exception as e:
        print(f"Error processing PUT request: {e}")
        response = make_response(jsonify({"error": "Internal Server Error"}), 500)
        print(response)

    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)


@app.route("/edit_user_avatar/<int:id>", methods=["PUT"])
@jwt_required()
def edit_user_picture(id):
    if "avatar" not in request.files:
        return jsonify({"msg": "No avatar file part"}), 400
    file = request.files["avatar"]
    if file.filename == "":
        return jsonify({"msg": "No selected file"}), 400

    filename = secure_filename(file.filename)
    result = cloudinary.uploader.upload(file, folder="PLANTS/AVATARS")
    avatar_url = result.get("url")
    connection = get_flask_database_connection(app)
    user_repository = UserRepository(connection)
    user_repository.edit_user_avatar(id, avatar_url)
    return (
        jsonify({"msg": "Avatar updated successfully", "avatar_url": avatar_url}),
        200,
    )


# CONFLICTS WITH NEEDED ROUTE
# # get all help offers made by a specific "" @app.route("/help_offers/<user_id>", methods=["GET"])
# def find_offers_by_user_id(user_id):
#
#     # connect to db and set up offer repository
#     connection = get_flask_database_connection(app)
#     offer_repository = HelpOfferRepository(connection)
#
#     # returns array of HelpOffer object IDs made by user matching user_id
#     offers_by_user = offer_repository.find_by_user(user_id)
#     user_offers = []
#     for offer in offers_by_user:
#         offer_obj = {
#             "id": offer.id,
#             "user_id": offer.user_id,
#             "request_id": offer.request_id,
#             "message": offer.message,
#             "bid": offer.bid,
#             "status": offer.status,
#         }
#         user_offers.append(offer_obj)
#
#     return jsonify(user_offers), 200

# # get all help offers made by a specific user
# @app.route("/help_offers/<user_id>", methods=["GET"])
# def find_offers_by_user_id(user_id):
#
#     # connect to db and set up offer repository
#     connection = get_flask_database_connection(app)
#     offer_repository = HelpOfferRepository(connection)
#
#     # returns array of HelpOffer object IDs made by user matching user_id
#     offers_by_user = offer_repository.find_by_user(user_id)
#     user_offers = []
#     for offer in offers_by_user:
#         offer_obj = {
#             "id": offer.id,
#             "user_id": offer.user_id,
#             "request_id": offer.request_id,
#             "message": offer.message,
#             "bid": offer.bid,
#             "status": offer.status,
#         }
#         user_offers.append(offer_obj)
#
#     return jsonify(user_offers), 200


# create a new help offer for a help request
@app.route("/help_offers/<help_request_id>", methods=["POST"])
@cross_origin()
@jwt_required()
def create_help_offer(help_request_id):
    try:
        # connect to db and set up offer repository
        connection = get_flask_database_connection(app)
        offer_repository = HelpOfferRepository(connection)

        # get data from request body and create help_offer in DB
        user_id = request.json.get("user_id")
        request_id = help_request_id
        message = request.json.get("message")
        bid = request.json.get("bid")
        status = "pending"

        new_offer = HelpOffer(None, user_id, request_id, message, bid, status)

        if None in (user_id, request_id, message, bid, status):
            raise ValueError("All required fields must be filled")
        offer_repository.create_offer(new_offer)
        return jsonify({"msg": "Help Offer Created"}), 201
    except:
        return jsonify({"msg": "Help offer creation unsuccessful"}), 400


# return array of offers made to a particular user (user_id)
@app.route("/help_offers/help_requests/<user_id>")
@jwt_required()
@cross_origin()
def received_help_offers_by_user_id(user_id):
    connection = get_flask_database_connection(app)
    extended_help_offer_repostitory = ExtendedHelpOfferRepository(connection)
    extended_help_offer = (
        extended_help_offer_repostitory.get_all_received_extended_help_offers(user_id)
    )

    help_offered = []
    for offer in extended_help_offer:
        offer_obj = {
            "help_request_id": offer.help_request_id,
            "help_request_start_date": offer.help_request_start_date,
            "help_request_end_date": offer.help_request_end_date,
            "help_request_name": offer.help_request_name,
            "help_request_user_id": offer.help_request_user_id,
            "help_offer_id": offer.help_offer_id,
            "help_offer_message": offer.help_offer_message,
            "help_offer_status": offer.help_offer_status,
            "help_offer_user_id": offer.help_offer_user_id,
            "help_offer_bid": offer.help_offer_bid,
            "help_offer_first_name": offer.help_offer_first_name,
            "help_offer_last_name": offer.help_offer_last_name,
            "help_offer_avatar_url_string": offer.help_offer_avatar_url_string,
            "help_offer_username": offer.help_offer_username,
            "help_receive_first_name": offer.help_receive_first_name,
            "help_receive_last_name": offer.help_receive_last_name,
            "help_receive_avatar_url_string": offer.help_receive_avatar_url_string,
            "help_receive_username": offer.help_receive_username,
        }
        help_offered.append(offer_obj)
    return jsonify(help_offered)


# accept help offer
@app.route("/help_offers/accept_offer/<help_offer_id>", methods=["PUT"])
@jwt_required()
@cross_origin()
def accept_help_offer(help_offer_id):
    connection = get_flask_database_connection(app)
    help_offers_repository = HelpOfferRepository(connection)

    # get list of help_offer_ids associated with request (id to accept excluded)
    associated_help_offer_ids = (
        help_offers_repository.get_other_help_offer_ids_associated_with_request_id(
            help_offer_id
        )
    )
    associated_help_offer_ids.remove(int(help_offer_id))

    # Accept help_offer
    help_offers_repository.accept_help_offer(help_offer_id)

    # Reject other associated help offers
    for help_offer_id in associated_help_offer_ids:
        help_offers_repository.reject_help_offer(help_offer_id)

    return jsonify({"msg": "Help offer accepted"}), 200


# reject help offer
@app.route("/help_offers/reject_offer/<help_offer_id>", methods=["PUT"])
@jwt_required()
@cross_origin()
def reject_help_offer(help_offer_id):
    connection = get_flask_database_connection(app)
    help_offers_repository = HelpOfferRepository(connection)

    help_offers_repository.reject_help_offer(help_offer_id)

    return jsonify({"msg": "Help offer rejected"}), 200


# return array of offers made by a particular user (user_id)
@app.route("/help_offers/<user_id>")
@jwt_required()
@cross_origin()
def outgoing_help_offers_by_user_id(user_id):
    connection = get_flask_database_connection(app)
    extended_help_offer_repostitory = ExtendedHelpOfferRepository(connection)
    extended_help_offer = (
        extended_help_offer_repostitory.get_all_outgoing_extended_help_offers(user_id)
    )

    help_offered = []
    for offer in extended_help_offer:
        offer_obj = {
            "help_request_id": offer.help_request_id,
            "help_request_start_date": offer.help_request_start_date,
            "help_request_end_date": offer.help_request_end_date,
            "help_request_name": offer.help_request_name,
            "help_request_user_id": offer.help_request_user_id,
            "help_offer_id": offer.help_offer_id,
            "help_offer_message": offer.help_offer_message,
            "help_offer_status": offer.help_offer_status,
            "help_offer_user_id": offer.help_offer_user_id,
            "help_offer_bid": offer.help_offer_bid,
            "help_offer_first_name": offer.help_offer_first_name,
            "help_offer_last_name": offer.help_offer_last_name,
            "help_offer_avatar_url_string": offer.help_offer_avatar_url_string,
            "help_offer_username": offer.help_offer_username,
            "help_receive_first_name": offer.help_receive_first_name,
            "help_receive_last_name": offer.help_receive_last_name,
            "help_receive_avatar_url_string": offer.help_receive_avatar_url_string,
            "help_receive_username": offer.help_receive_username,
        }
        help_offered.append(offer_obj)
    return jsonify(help_offered)


# reject help offer
@app.route("/help_offers/rescind_offer/<help_offer_id>", methods=["PUT"])
@jwt_required()
@cross_origin()
def rescind_help_offer(help_offer_id):
    connection = get_flask_database_connection(app)
    help_offers_repository = HelpOfferRepository(connection)

    help_offers_repository.rescind_help_offer(help_offer_id)

    return jsonify({"msg": "Help offer rescinded"}), 200


# Help Request Routes
@app.route("/help_requests", methods=["GET"])
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
                "maxprice": request.maxprice,
            }
            for request in all_requests
        ]
        return jsonify(request_data), 200
    return jsonify({"message": "Unable to find all requests"}), 400


@app.route("/help_requests2", methods=["GET"])
@cross_origin()
def get_all_help_requests_with_user_details():
    connection = get_flask_database_connection(app)
    request_repository = HelpRequestRepository(connection)
    help_requests_with_users = (
        request_repository.get_all_help_requests_with_user_first_name_and_last_name()
    )

    response_data = []
    for help_request, user_details in help_requests_with_users:
        response_data.append(
            {
                "id": help_request.id,
                "date": help_request.date.strftime("%Y-%m-%d %H:%M:%S"),
                "title": help_request.title,
                "message": help_request.message,
                "start_date": help_request.start_date.strftime("%Y-%m-%d"),
                "end_date": help_request.end_date.strftime("%Y-%m-%d"),
                "user_id": help_request.user_id,
                "maxprice": help_request.maxprice,
                "first_name": user_details["first_name"],
                "last_name": user_details["last_name"],
                "username": user_details["username"],
                "avatar_url_string": user_details["avatar_url_string"],
            }
        )

    return jsonify(response_data), 200


@app.route("/help_requests/<request_id>", methods=["GET"])
@cross_origin()
def get_one_help_request_by_id(request_id):
    connection = get_flask_database_connection(app)
    request_repository = HelpRequestRepository(connection)
    request_with_user_details = request_repository.find_request_by_id(request_id)

    if request_with_user_details:
        help_request, user_details = request_with_user_details
        response_data = {
            "id": help_request.id,
            "date": help_request.date.strftime("%Y-%m-%d %H:%M:%S"),
            "title": help_request.title,
            "message": help_request.message,
            "start_date": help_request.start_date.strftime("%Y-%m-%d"),
            "end_date": help_request.end_date.strftime("%Y-%m-%d"),
            "user_id": help_request.user_id,
            "maxprice": help_request.maxprice,
            "user_details": {
                "first_name": user_details["first_name"],
                "last_name": user_details["last_name"],
                "username": user_details["username"],
                "avatar_url_string": user_details["avatar_url_string"],
            },
        }
        return jsonify(response_data), 200
    return jsonify({"message": "Help Request not found"}), 400


@app.route("/help_requests/user/<user_id>", methods=["GET"])
@jwt_required()
@cross_origin()
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
            "maxprice": request.maxprice,
        }
        formatted_requests.append(formatted_request)

    return jsonify(formatted_requests), 200


@app.route("/help_requests/create/<user_id>", methods=["POST"])
@jwt_required()
@cross_origin()
def create_help_request(user_id):
    try:
        connection = get_flask_database_connection(app)
        request_repository = HelpRequestRepository(connection)
        date = request.json.get("date")
        title = request.json.get("title")
        message = request.json.get("message")
        start_date = request.json.get("start_date")
        end_date = request.json.get("end_date")
        maxprice = request.json.get("maxprice")
        if None in (title, message, start_date, end_date, maxprice):
            raise ValueError("All required fields must be filled")
        request_repository.create_request(
            HelpRequest(
                None, date, title, message, start_date, end_date, user_id, maxprice
            )
        )
        return jsonify({"message": "Help request created successfully"}), 200
    except:
        return jsonify({"message": "Help request creation unsuccessful"}), 400


### PLANTS ROUT ###


# Show all plants in DB
@app.route("/plants", methods=["GET"])
@cross_origin()
def get_plants():
    connection = get_flask_database_connection(app)
    repository = PlantsRepository(connection)
    plants = repository.all()
    data_json = [
        {
            "id": plant.id,
            "common_name": plant.common_name,
            "latin_name": plant.latin_name,
            "photo": plant.photo,
            "watering_frequency": plant.watering_frequency,
        }
        for plant in plants
    ]
    return jsonify(data_json), 200


@app.route("/plants/create", methods=["POST"])
@cross_origin()
def add_new_plant():
    connection = get_flask_database_connection(app)
    repository = PlantsRepository(connection)
    user_id = request.json.get("user_id")
    plant_id = request.json.get("plant_id")
    common_name = request.json.get("common_name")
    latin_name = request.json.get("latin_name")
    photo = request.json.get("photo")
    water_frequency = 1
    repository.create(plant_id, common_name, latin_name, photo, water_frequency)
   
    # return jsonify(data_json), 200


# Show all plants by user
@app.route("/plants/user/<user_id>", methods=["GET"])
@cross_origin()
@jwt_required()
def get_plants_by_user(user_id):
    connection = get_flask_database_connection(app)
    repository = PlantsUserRepository(connection)
    plants_with_quantity = repository.find_plants_by_user_id(user_id)
    user_plants = []
    for plant_info in plants_with_quantity:
        plant = plant_info["plant"]
        quantity = plant_info["quantity"]
        plant_obj = {
            "id": plant.id,
            "common_name": plant.common_name,
            "latin_name": plant.latin_name,
            "photo": plant.photo,
            "watering_frequency": plant.watering_frequency,
            "quantity": quantity,
        }
        user_plants.append(plant_obj)

    return jsonify(user_plants), 200


@app.route("/plants/user/assign", methods=["POST"])
@cross_origin()
@jwt_required()
def assign_plant_to_user():
    user_id = request.json.get("user_id")
    plant_id = request.json.get("plant_id")
    quantity = request.json.get("quantity", 1)  # Default quantity to 1 if not specified
    connection = get_flask_database_connection(app)
    repository = PlantsUserRepository(connection)
    repository.assign_plant_to_user(user_id, plant_id, quantity)
    access_token = create_access_token(identity=user_id)

    return (
        jsonify({"message": "Plant assigned successfully", "token": access_token}),
        200,
    )

# API REQUEST 
@app.route('/api/plants')
@cross_origin()
@jwt_required()
def get_plant():
    token = "-y-wxiT1X3z5emjJ1u1h7Flnpe65UO82CUGHkisnVJY"
    response = requests.get(f"https://trefle.io/api/v1/plants?token={token}&page=1")
    if response.ok:
        plant_data = response.json()
        my_plants = []
        for item in plant_data['data']:
            plant_info = {"common_name": item['common_name'],"plant_id": item['id'], 'latin_name': item['scientific_name'], 'photo': item['image_url'],  }
            my_plants.append(plant_info)
        return jsonify(my_plants)
    else:
        return jsonify({"error": "Failed to fetch data from Trefle API"}), response.status_code






@app.route("/plants/user/update", methods=["POST"])
@cross_origin()
@jwt_required()
def update_plants_quantity():
    user_id = request.json.get("user_id")
    plant_id = request.json.get("plant_id")
    new_quantity = request.json.get("new_quantity")
    connection = get_flask_database_connection(app)
    repository = PlantsUserRepository(connection)
    repository.update_plants_quantity(user_id, plant_id, new_quantity)
    access_token = create_access_token(identity=user_id)

    return (
        jsonify(
            {"message": "Plant quantity updated successfully", "token": access_token}
        ),
        200,
    )


@app.route("/plants/user/delete", methods=["DELETE"])
@jwt_required()
def delete_plants_from_user():
    user_id = request.json.get("user_id")
    plant_id = request.json.get("plant_id")

    connection = get_flask_database_connection(app)
    repository = PlantsUserRepository(connection)
    repository.delete_plants_from_user(user_id, plant_id)

    return jsonify({"message": "Plant deleted successfully"}), 200


# Show all chats by user
@app.route("/messages/user/<user_id>", methods=["GET"])
@jwt_required()
def get_chats_by_user_id(user_id):
    connection = get_flask_database_connection(app)
    repository = ChatRepository(connection)
    messages = repository.find_messages_by_userid(user_id)
    all_messages = []
    for message_info in messages:
        receiver_username = message_info["receiver_username"]
        sender_username = message_info["sender_username"]
        message = message_info["message"]
        message_obj = {
            "id": message.id,
            "recipient_id": message.recipient_id,
            "message": message.message,
            "start_date": message.start_date,
            "end_date": message.end_date,
            "sender_id": message.sender_id,
            "receiver_username": receiver_username,
            "sender_username": sender_username,
        }
        all_messages.append(message_obj)

    return jsonify(all_messages), 200


@app.route("/messages", methods=["POST"])
@jwt_required()
def post_messages():
    connection = get_flask_database_connection(app)
    repository = ChatRepository(connection)
    get_message = request.json.get("content")
    receiver_id = request.json.get("receiverId")
    receiver_username = request.json.get("receiver_username")
    sender_username = request.json.get("sender_username")
    user_id = request.json.get("userId")
    repository.create(user_id, receiver_id, get_message, receiver_username, sender_username)

    return jsonify({"message": "Message sent successfully"}), 200


room_memberships = {}

@socketio.on('join')
def on_join(data):
    room = data['room']
    sid = request.sid
    join_room(room)
    
    if room not in room_memberships:
        room_memberships[room] = []
    if sid not in room_memberships[room]:
        room_memberships[room].append(sid)
    
    print(f"Current sockets in room {room}: {room_memberships[room]}")
    socketio.emit('joined_room', {'message': f"Joined room {room}"}, to=sid)
    

@socketio.on('message')
def handle_message(data):
    room = data['room']
    socketio.emit('new_messages', {'sender': data['sender'], 'message': data['message']}, room=room, include_self=False)
    

@socketio.on('leave')
def on_leave(data):
    room = data['room']
    sid = request.sid
    leave_room(room)
    if room in room_memberships and sid in room_memberships[room]:
        room_memberships[room].remove(sid)
        print(f"Socket {sid} left room {room}. Current sockets in room: {room_memberships.get(room, [])}")

@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    for room, members in room_memberships.items():
        if sid in members:
            members.remove(sid)
            print(f"Socket {sid} removed from room {room} upon disconnect.")
            socketio.emit('user_left', {'sid': sid, 'room': room}, room=room)
            
            


@app.route("/messages/<chat_id>", methods=["GET"])
@jwt_required()
def get_chats_by_chat_id(chat_id):
    connection = get_flask_database_connection(app)
    repository = ChatRepository(connection)
    messages = repository.find_message_by_chat_id(chat_id)
    return jsonify(messages), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    print(f" * Running on http://127.0.0.1:{port}")
    socketio.run(app, debug=True, port=port, use_reloader=False)
