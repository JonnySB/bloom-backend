import os
from flask import Flask, jsonify, request
from lib.database_connection import get_flask_database_connection
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from dotenv import load_dotenv
from lib.repositories.plants_repository import PlantsRepository
from lib.repositories.plants_user_repository import PlantsUserRepository
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

# Show all plants in DB
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
    return jsonify(data_json), 200


# #Show all plants by user
@app.route('/plants/<user_id>', methods=['GET'])
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
            "quantity": quantity
        }
        user_plants.append(plant_obj)

    return jsonify(user_plants), 200





if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5001)))
