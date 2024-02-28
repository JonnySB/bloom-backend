import os
from flask import Flask, jsonify, request
from lib.database_connection import get_flask_database_connection
from flask_jwt_extended import JWTManager, create_access_token
from dotenv import load_dotenv
from lib.repositories.plants_repository import PlantsRepository
from lib.models.plants import Plants

from lib.repositories.user_repository import UserRepository

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

### PLANTS ROUT ###

@app.route('/plants', methods=['GET'])
def get_plants():
    connection = get_flask_database_connection(app)
    repository = PlantsRepository(connection)
    plants = repository.all()
    data_json = [{
        "id" : plant.id,
        "common_name" : plant.common_name,
        "latin_name": plant.latin_name,
        "photo": plant.photo,
        "watering_frequency": plant.watering_frequency
        }
    for plant in plants
    ]
    return jsonify(data_json)


@app.route('/add_plant', methods=['POST'])
def create_new_plant(user_id):
    connection = get_flask_database_connection(app)
    repository = PlantsRepository(connection)
    plant = Plants(None, request.form["common_name"], request.form["latin_name"], request.form["photo"], int(request.form["watering_frequency"]))
    repository.create(plant)
    return redirect(f'/plants')


# @app.route('/plants/<user_id>', methods=['GET'])
# def get_plants():
#     connection = get_flask_database_connection(app)
#     repository = PlantsRepository(connection)
#     plants = repository.all(user_id)
#     data_json = [{
#         "id" : plant.id,
#         "common_name" : plant.common_name,
#         "latin_name": plant.latin_name,
#         "photo": plant.photo,
#         "watering_frequency": plant.watering_frequency
#         }
#     for plant in plants
#     ]
#     return jsonify(data_json)







if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5001)))
