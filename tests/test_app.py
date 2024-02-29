from app import *
import requests


def test_user_authentication_successful_via_username(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")
    user_data = {"username_email": "user1", "password": "Password123!"}
    response = requests.post(f"http://{test_web_address}/token", json=user_data)
    response.json()
    assert response.status_code == 200
    assert response != {"msg": "Bad username or password"}


def test_user_authentication_successful_via_email(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")
    user_data = {"username_email": "user1@email.com", "password": "Password123!"}
    response = requests.post(f"http://{test_web_address}/token", json=user_data)
    response.json()
    assert response.status_code == 200
    assert response != {"msg": "Bad username or password"}


def test_user_authentication_unsucessful_with_wrong_password(
    db_connection, test_web_address
):
    db_connection.seed("seeds/bloom.sql")
    user_data = {"username_email": "user1", "password": "Password123"}
    response = requests.post(f"http://{test_web_address}/token", json=user_data)
    assert response.status_code == 401
    assert response.json() == {"msg": "Bad username or password"}


def test_user_authentication_unsucessful_with_no_corresponding_email(
    db_connection, test_web_address
):
    db_connection.seed("seeds/bloom.sql")
    user_data = {"username_email": "user7@email.com", "password": "Password123!"}
    response = requests.post(f"http://{test_web_address}/token", json=user_data)
    assert response.status_code == 401
    assert response.json() == {"msg": "Bad username or password"}


def test_user_authentication_unsucessful_with_no_corresponding_username(
    db_connection, test_web_address
):
    db_connection.seed("seeds/bloom.sql")
    user_data = {"username_email": "user7", "password": "Password123!"}
    response = requests.post(f"http://{test_web_address}/token", json=user_data)
    assert response.status_code == 401
    assert response.json() == {"msg": "Bad username or password"}


def test_get_all_plants(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")
    response = requests.get(f"http://{test_web_address}/plants")
    assert response.status_code == 200
    except_plants = [
            {"id": 1, "common_name": "African sheepbush", "latin_name": "Pentzia incana", "photo": "plant_01.png", "watering_frequency": 2},
            {"id": 2, "common_name": "Alder", "latin_name": "Alnus. Black alder", "photo": "plant_02.png", "watering_frequency": 1},
            {"id": 3, "common_name": "Almond", "latin_name": "Prunus dulcis", "photo": "plant_03.png", "watering_frequency": 1},
    ]
    assert response.json() == except_plants
    

def test_get_plants_by_user_id(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")
    PlantsUserRepository(db_connection)
    
    login_data = {"username_email": "user1", "password": "Password123!"}
    login_response = requests.post(f"http://{test_web_address}/token", json=login_data)
    assert login_response.status_code == 200
    access_token = login_response.json()["token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"http://{test_web_address}/plants/user/1", headers=headers)
    
    assert response.status_code == 200
    
    except_plants = [
        {
            "id": 1,
            "common_name": "African sheepbush",
            "latin_name": "Pentzia incana",
            "photo": "plant_01.png",
            "watering_frequency": 2,
            "quantity": 2  
        }
    ]
    
    assert response.json() == except_plants