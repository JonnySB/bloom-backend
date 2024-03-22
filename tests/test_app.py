import datetime
import io
from unittest.mock import MagicMock, patch

import pytest
import requests
from werkzeug.datastructures import FileStorage

from app import *

#########################
###### test /token ######
#########################


def test_user_authentication_successful_via_username(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")
    user_data = {"username_email": "tee-jay", "password": "Password123!"}
    response = requests.post(f"http://{test_web_address}/token", json=user_data)
    response.json()
    assert response.status_code == 201
    assert response != {"msg": "Bad username or password"}


def test_user_authentication_successful_via_email(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")
    user_data = {"username_email": "tjones@email.com", "password": "Password123!"}
    response = requests.post(f"http://{test_web_address}/token", json=user_data)
    response.json()
    assert response.status_code == 201
    assert response != {"msg": "Bad username or password"}


def test_user_authentication_unsucessful_with_wrong_password(
    db_connection, test_web_address
):
    db_connection.seed("seeds/bloom.sql")
    user_data = {"username_email": "tee-jay", "password": "Password123"}
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
        {
            "common_name": "African sheepbush",
            "id": 1,
            "latin_name": "Pentzia incana",
            "photo": "https://res.cloudinary.com/dououppib/image/upload/v1709740425/PLANTS/African_sheepbush_lyorlf.jpg",
            "watering_frequency": 2,
        },
        {
            "common_name": "Alder",
            "id": 2,
            "latin_name": "Alnus. Black alder",
            "photo": "https://res.cloudinary.com/dououppib/image/upload/v1709740428/PLANTS/Alder_jc4szc.jpg",
            "watering_frequency": 1,
        },
        {
            "common_name": "Almond",
            "id": 3,
            "latin_name": "Prunus dulcis",
            "photo": "https://res.cloudinary.com/dououppib/image/upload/v1709740430/PLANTS/Almond_aikcyc.jpg",
            "watering_frequency": 1,
        },
        {
            "common_name": "Bamboo",
            "id": 4,
            "latin_name": "Fargesia",
            "photo": "https://res.cloudinary.com/dououppib/image/upload/v1709740434/PLANTS/Bamboo_bkwm52.jpg",
            "watering_frequency": 1,
        },
        {
            "common_name": "Barberry",
            "id": 5,
            "latin_name": "Berberis",
            "photo": "https://res.cloudinary.com/dououppib/image/upload/v1709740432/PLANTS/Barberry_copy_gseiuj.png",
            "watering_frequency": 1,
        },
        {
            "common_name": "Bergamot",
            "id": 6,
            "latin_name": "Monarda",
            "photo": "https://res.cloudinary.com/dououppib/image/upload/v1709740426/PLANTS/Bergamot_k7ympf.jpg",
            "watering_frequency": 1,
        },
    ]
    assert response.json() == except_plants


# Plants Request route tests:
def test_get_plants_by_user_id(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")
    PlantsUserRepository(db_connection)

    login_data = {"username_email": "tee-jay", "password": "Password123!"}
    login_response = requests.post(f"http://{test_web_address}/token", json=login_data)
    assert login_response.status_code == 201
    access_token = login_response.json()["token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"http://{test_web_address}/plants/user/1", headers=headers)

    assert response.status_code == 200

    except_plants = [
        {
            "common_name": "African sheepbush",
            "id": 1,
            "latin_name": "Pentzia incana",
            "photo": "https://res.cloudinary.com/dououppib/image/upload/v1709740425/PLANTS/African_sheepbush_lyorlf.jpg",
            "plant_id": 1,
            "quantity": 3,
            "watering_frequency": 2,
        },
        {
            "common_name": "Alder",
            "id": 2,
            "latin_name": "Alnus. Black alder",
            "photo": "https://res.cloudinary.com/dououppib/image/upload/v1709740428/PLANTS/Alder_jc4szc.jpg",
            "plant_id": 2,
            "quantity": 3,
            "watering_frequency": 1,
        },
        {
            "common_name": "Barberry",
            "id": 5,
            "latin_name": "Berberis",
            "photo": "https://res.cloudinary.com/dououppib/image/upload/v1709740432/PLANTS/Barberry_copy_gseiuj.png",
            "plant_id": 5,
            "quantity": 2,
            "watering_frequency": 1,
        },
    ]

    assert response.json() == except_plants


def test_assign_plant_to_user(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")
    login_data = {"username_email": "tee-jay", "password": "Password123!"}
    login_response = requests.post(f"http://{test_web_address}/token", json=login_data)
    assert login_response.status_code == 201
    access_token = login_response.json()["token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    assign_data = {"user_id": 1, "plant_id": 6, "quantity": 3}
    response = requests.post(
        f"http://{test_web_address}/plants/user/assign",
        json=assign_data,
        headers=headers,
    )

    assert response.status_code == 200
    assert response.ok


def test_update_plant_quantity_for_user(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")
    login_data = {"username_email": "tee-jay", "password": "Password123!"}
    login_response = requests.post(f"http://{test_web_address}/token", json=login_data)
    assert login_response.status_code == 201
    access_token = login_response.json()["token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    update_data = {"user_id": 1, "plant_id": 2, "new_quantity": 5}
    response = requests.post(
        f"http://{test_web_address}/plants/user/update",
        json=update_data,
        headers=headers,
    )

    assert response.status_code == 200
    assert response.ok


def test_delete_plant_from_user(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")
    login_data = {"username_email": "tee-jay", "password": "Password123!"}
    login_response = requests.post(f"http://{test_web_address}/token", json=login_data)
    assert login_response.status_code == 201
    access_token = login_response.json()["token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    delete_data = {"user_id": 1, "plant_id": 2}
    response = requests.delete(
        f"http://{test_web_address}/plants/user/delete",
        json=delete_data,
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Plant deleted successfully"}


# Help Request route tests:


def test_get_all_help_requests_with_user_details(test_web_address, db_connection):
    db_connection.seed("seeds/bloom.sql")

    response = requests.get(f"http://{test_web_address}/help_requests2")
    assert response.status_code == 200

    expected_data = [
        {
            "avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1708633707/MY_UPLOADS/aibxzxdpk6gl4u5xjgjg.jpg",
            "date": "2023-10-19 10:23:54",
            "end_date": "2023-02-28",
            "first_name": "Tom",
            "id": 1,
            "last_name": "Jones",
            "maxprice": 75.0,
            "message": "I am going on holiday for all of February - would love some help!",
            "start_date": "2023-02-01",
            "title": "Help needed whilst on holiday.",
            "user_id": 1,
            "username": "tee-jay",
        },
        {
            "avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1709830407/PLANTS/person4_kqdufy.jpg",
            "date": "2023-11-12 08:45:21",
            "end_date": "2023-03-10",
            "first_name": "Jane",
            "id": 2,
            "last_name": "Smith",
            "maxprice": 100.0,
            "message": "Looking for someone to water my plants while I am away.",
            "start_date": "2023-03-05",
            "title": "Help required with plant care.",
            "user_id": 2,
            "username": "jane95",
        },
        {
            "avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1709830406/PLANTS/person2_jpuq5z.jpg",
            "date": "2023-11-28 14:30:09",
            "end_date": "2023-04-20",
            "first_name": "Jilly",
            "id": 3,
            "last_name": "Smith",
            "maxprice": 90.0,
            "message": "Seeking help in maintaining my garden during my absence.",
            "start_date": "2023-04-15",
            "title": "Need assistance with gardening.",
            "user_id": 3,
            "username": "sm1thi",
        },
        {
            "avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1709830406/PLANTS/person1_jdh4xm.jpg",
            "date": "2023-12-07 11:20:35",
            "end_date": "2023-05-08",
            "first_name": "Barbra",
            "id": 4,
            "last_name": "Banes",
            "maxprice": 80.0,
            "message": "Require someone to water my indoor plants while I am out of town.",
            "start_date": "2023-05-03",
            "title": "Help wanted for plant care.",
            "user_id": 4,
            "username": "barn-owl58",
        },
        {
            "avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1709830407/PLANTS/person3_itrqub.jpg",
            "date": "2023-12-20 09:55:47",
            "end_date": "2023-06-18",
            "first_name": "Alice",
            "id": 5,
            "last_name": "Lane",
            "maxprice": 70.0,
            "message": "Looking for a reliable person to care for my garden while I am away.",
            "start_date": "2023-06-12",
            "title": "Assistance needed with garden maintenance.",
            "user_id": 5,
            "username": "laney",
        },
        {
            "avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1708633707/MY_UPLOADS/aibxzxdpk6gl4u5xjgjg.jpg",
            "date": "2024-01-05 16:10:02",
            "end_date": "2023-07-07",
            "first_name": "Tom",
            "id": 6,
            "last_name": "Jones",
            "maxprice": 85.0,
            "message": "Seeking someone to water my plants regularly during my vacation.",
            "start_date": "2023-07-02",
            "title": "Plant watering help required.",
            "user_id": 1,
            "username": "tee-jay",
        },
        {
            "avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1709830407/PLANTS/person4_kqdufy.jpg",
            "date": "2024-01-15 13:40:19",
            "end_date": "2023-08-25",
            "first_name": "Jane",
            "id": 7,
            "last_name": "Smith",
            "maxprice": 95.0,
            "message": "Require help in maintaining my backyard garden for a few weeks.",
            "start_date": "2023-08-20",
            "title": "Gardening assistance wanted.",
            "user_id": 2,
            "username": "jane95",
        },
        {
            "avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1709830406/PLANTS/person2_jpuq5z.jpg",
            "date": "2024-02-02 10:05:38",
            "end_date": "2023-09-15",
            "first_name": "Jilly",
            "id": 8,
            "last_name": "Smith",
            "maxprice": 65.0,
            "message": "Looking for immediate assistance in watering my plants.",
            "start_date": "2023-09-10",
            "title": "Plant care help needed urgently.",
            "user_id": 3,
            "username": "sm1thi",
        },
        {
            "avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1709830406/PLANTS/person1_jdh4xm.jpg",
            "date": "2024-02-14 07:30:55",
            "end_date": "2023-10-10",
            "first_name": "Barbra",
            "id": 9,
            "last_name": "Banes",
            "maxprice": 75.0,
            "message": "Seeking someone to take care of my indoor plants for a short "
            "duration.",
            "start_date": "2023-10-05",
            "title": "Help needed with indoor plants.",
            "user_id": 4,
            "username": "barn-owl58",
        },
        {
            "avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1709830407/PLANTS/person3_itrqub.jpg",
            "date": "2024-02-28 15:20:10",
            "end_date": "2023-11-27",
            "first_name": "Alice",
            "id": 10,
            "last_name": "Lane",
            "maxprice": 60.0,
            "message": "Require help in watering my garden while I am away.",
            "start_date": "2023-11-22",
            "title": "Garden watering assistance required.",
            "user_id": 5,
            "username": "laney",
        },
    ]

    assert response.json() == expected_data


def test_get_all_help_requests_from_database(test_web_address, db_connection):
    db_connection.seed("seeds/bloom.sql")

    response = requests.get(f"http://{test_web_address}/help_requests")
    assert response.status_code == 200

    expected_data = [
        {
            "date": "2023-10-19 10:23:54",
            "end_date": "2023-02-28",
            "id": 1,
            "maxprice": 75.0,
            "message": "I am going on holiday for all of February - would love some help!",
            "start_date": "2023-02-01",
            "title": "Help needed whilst on holiday.",
            "user_id": 1,
        },
        {
            "date": "2023-11-12 08:45:21",
            "end_date": "2023-03-10",
            "id": 2,
            "maxprice": 100.0,
            "message": "Looking for someone to water my plants while I am away.",
            "start_date": "2023-03-05",
            "title": "Help required with plant care.",
            "user_id": 2,
        },
        {
            "date": "2023-11-28 14:30:09",
            "end_date": "2023-04-20",
            "id": 3,
            "maxprice": 90.0,
            "message": "Seeking help in maintaining my garden during my absence.",
            "start_date": "2023-04-15",
            "title": "Need assistance with gardening.",
            "user_id": 3,
        },
        {
            "date": "2023-12-07 11:20:35",
            "end_date": "2023-05-08",
            "id": 4,
            "maxprice": 80.0,
            "message": "Require someone to water my indoor plants while I am out of town.",
            "start_date": "2023-05-03",
            "title": "Help wanted for plant care.",
            "user_id": 4,
        },
        {
            "date": "2023-12-20 09:55:47",
            "end_date": "2023-06-18",
            "id": 5,
            "maxprice": 70.0,
            "message": "Looking for a reliable person to care for my garden while I am away.",
            "start_date": "2023-06-12",
            "title": "Assistance needed with garden maintenance.",
            "user_id": 5,
        },
        {
            "date": "2024-01-05 16:10:02",
            "end_date": "2023-07-07",
            "id": 6,
            "maxprice": 85.0,
            "message": "Seeking someone to water my plants regularly during my vacation.",
            "start_date": "2023-07-02",
            "title": "Plant watering help required.",
            "user_id": 1,
        },
        {
            "date": "2024-01-15 13:40:19",
            "end_date": "2023-08-25",
            "id": 7,
            "maxprice": 95.0,
            "message": "Require help in maintaining my backyard garden for a few weeks.",
            "start_date": "2023-08-20",
            "title": "Gardening assistance wanted.",
            "user_id": 2,
        },
        {
            "date": "2024-02-02 10:05:38",
            "end_date": "2023-09-15",
            "id": 8,
            "maxprice": 65.0,
            "message": "Looking for immediate assistance in watering my plants.",
            "start_date": "2023-09-10",
            "title": "Plant care help needed urgently.",
            "user_id": 3,
        },
        {
            "date": "2024-02-14 07:30:55",
            "end_date": "2023-10-10",
            "id": 9,
            "maxprice": 75.0,
            "message": "Seeking someone to take care of my indoor plants for a short "
            "duration.",
            "start_date": "2023-10-05",
            "title": "Help needed with indoor plants.",
            "user_id": 4,
        },
        {
            "date": "2024-02-28 15:20:10",
            "end_date": "2023-11-27",
            "id": 10,
            "maxprice": 60.0,
            "message": "Require help in watering my garden while I am away.",
            "start_date": "2023-11-22",
            "title": "Garden watering assistance required.",
            "user_id": 5,
        },
    ]

    assert response.json() == expected_data


def test_get_one_help_request_from_db(test_web_address, db_connection):
    db_connection.seed("seeds/bloom.sql")

    response = requests.get(f"http://{test_web_address}/help_requests/2")

    assert response.status_code == 200
    expected_data = {
        "date": "2023-11-12 08:45:21",
        "end_date": "2023-03-10",
        "id": 2,
        "maxprice": 100.0,
        "message": "Looking for someone to water my plants while I am away.",
        "start_date": "2023-03-05",
        "title": "Help required with plant care.",
        "user_details": {
            "avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1709830407/PLANTS/person4_kqdufy.jpg",
            "first_name": "Jane",
            "last_name": "Smith",
            "username": "jane95",
        },
        "user_id": 2,
        'plant_photo': 'https://res.cloudinary.com/dououppib/image/upload/v1709740432/PLANTS/Barberry_copy_gseiuj.png'
    }
    assert response.json() == expected_data


def test_get_all_requests_by_one_user(test_web_address, db_connection):
    db_connection.seed("seeds/bloom.sql")

    login_data = {"username_email": "tee-jay", "password": "Password123!"}
    login_response = requests.post(f"http://{test_web_address}/token", json=login_data)
    assert login_response.status_code == 201
    access_token = login_response.json()["token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(
        f"http://{test_web_address}/help_requests/user/1", headers=headers
    )

    assert response.status_code == 200
    expected_data = [
        {
            "date": "2023-10-19 10:23:54",
            "end_date": "2023-02-28",
            "id": 1,
            "maxprice": 75.0,
            "message": "I am going on holiday for all of February - would love some help!",
            "start_date": "2023-02-01",
            "title": "Help needed whilst on holiday.",
            "user_id": 1,
            "plant_photos": [
                "https://res.cloudinary.com/dououppib/image/upload/v1709740425/PLANTS/African_sheepbush_lyorlf.jpg",
                "https://res.cloudinary.com/dououppib/image/upload/v1709740432/PLANTS/Barberry_copy_gseiuj.png",
                "https://res.cloudinary.com/dououppib/image/upload/v1709740428/PLANTS/Alder_jc4szc.jpg",
            ],
        },
        {
            "date": "2024-01-05 16:10:02",
            "end_date": "2023-07-07",
            "id": 6,
            "maxprice": 85.0,
            "message": "Seeking someone to water my plants regularly during my vacation.",
            "start_date": "2023-07-02",
            "title": "Plant watering help required.",
            "user_id": 1,
            "plant_photos": [
                "https://res.cloudinary.com/dououppib/image/upload/v1709740425/PLANTS/African_sheepbush_lyorlf.jpg",
                "https://res.cloudinary.com/dououppib/image/upload/v1709740432/PLANTS/Barberry_copy_gseiuj.png",
                "https://res.cloudinary.com/dououppib/image/upload/v1709740428/PLANTS/Alder_jc4szc.jpg",
            ],
        },
    ]

    actual_data = response.json()
    assert len(actual_data) == len(expected_data), "Number of help requests does not match expected"
    for actual, expected in zip(actual_data, expected_data):
        assert actual['id'] == expected['id'], f"ID mismatch for help request {expected['id']}"
        assert actual['date'] == expected['date'], f"Date mismatch for help request {expected['id']}"
        assert set(actual['plant_photos']) == set(expected['plant_photos']), f"Plant photo URLs mismatch for help request {expected['id']}"


def test_create_help_request(test_web_address, db_connection):
    db_connection.seed("seeds/bloom.sql")

    login_data = {"username_email": "tee-jay", "password": "Password123!"}
    login_response = requests.post(f"http://{test_web_address}/token", json=login_data)
    assert login_response.status_code == 201
    access_token = login_response.json()["token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    new_request = {
        "date": "2024-03-12 13:14:15",
        "title": "title_03",
        "message": "message requesting help 3",
        "start_date": "2024-03-15",
        "end_date": "2024-03-18",
        "maxprice": 40.0,
    }
    # response = requests.post(f"http://{test_web_address}/help_requests/create/1", json=new_request)
    response = requests.post(
        f"http://{test_web_address}/help_requests/create/1",
        json=new_request,
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Help request created successfully"}


def test_unsuccessful_create_help_request_without_maxprice(
    test_web_address, db_connection
):
    db_connection.seed("seeds/bloom.sql")

    login_data = {"username_email": "tee-jay", "password": "Password123!"}
    login_response = requests.post(f"http://{test_web_address}/token", json=login_data)
    assert login_response.status_code == 201
    access_token = login_response.json()["token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    new_request = {
        "date": "2024-03-12 13:14:15",
        "title": "title_03",
        "message": "message requesting help 3",
        "start_date": "2024-03-15",
        "end_date": "2024-03-18",
    }
    # response = requests.post(f"http://{test_web_address}/help_requests/create/1", json=new_request)
    response = requests.post(
        f"http://{test_web_address}/help_requests/create/1",
        json=new_request,
        headers=headers,
    )
    assert response.status_code == 400
    assert response.json() == {"message": "Help request creation unsuccessful"}


###############################
###### test /user/signup ######
###############################


def test_user_created_with_correct_details_with_address(
    db_connection, test_web_address
):
    db_connection.seed("seeds/bloom.sql")
    user_data = {
        "first_name": "Tony",
        "last_name": "Smith",
        "username": "TS",
        "email": "tony_smith@email.com",
        "password": "Password123!",
        "password_confirm": "Password123!",
        "address": "An address!",
    }

    response = requests.post(f"http://{test_web_address}/user/signup", json=user_data)

    assert response.status_code == 201
    assert response.json() == {"message": "User created"}


def test_user_created_with_correct_details_with_blank_address(
    db_connection, test_web_address
):
    db_connection.seed("seeds/bloom.sql")
    user_data = {
        "first_name": "Tony",
        "last_name": "Smith",
        "username": "TS",
        "email": "tony_smith@email.com",
        "password": "Password123!",
        "password_confirm": "Password123!",
        "address": "",
    }

    response = requests.post(f"http://{test_web_address}/user/signup", json=user_data)

    assert response.status_code == 201
    assert response.json() == {"message": "User created"}


def test_user_not_created_when_duplicate_username(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")
    user_data = {
        "first_name": "Tony",
        "last_name": "Smith",
        "username": "TS",
        "email": "tony_smith@email.com",
        "password": "Password123!",
        "password_confirm": "Password123!",
        "address": "",
    }

    response = requests.post(f"http://{test_web_address}/user/signup", json=user_data)
    assert response.status_code == 201

    response = requests.post(f"http://{test_web_address}/user/signup", json=user_data)

    assert response.status_code == 401
    assert response.json() == {
        "message": "Bad request - user not created. This username has already been taken."
    }


def test_user_not_created_when_duplicate_email(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")
    user_data = {
        "first_name": "Tony",
        "last_name": "Smith",
        "username": "TS",
        "email": "tony_smith@email.com",
        "password": "Password123!",
        "password_confirm": "Password123!",
        "address": "",
    }

    response = requests.post(f"http://{test_web_address}/user/signup", json=user_data)
    assert response.status_code == 201

    response = requests.post(f"http://{test_web_address}/user/signup", json=user_data)

    assert response.status_code == 401
    assert response.json() == {
        "message": "Bad request - user not created. This username has already been taken."
    }





#####################################
###### test /user_details/<id> ######
#####################################


def test_get_user_details_for_valid_user_id(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")
    response = requests.get(f"http://{test_web_address}/user_details/1")

    assert response.status_code == 200
    assert response.json() == {
        "address": "test_address1",
        "avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1708633707/MY_UPLOADS/aibxzxdpk6gl4u5xjgjg.jpg",
        "email": "tjones@email.com",
        "first_name": "Tom",
        "id": 1,
        "last_name": "Jones",
        "username": "tee-jay",
    }


def test_return_user_not_found_for_invalid_user_id(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")
    response = requests.get(f"http://{test_web_address}/user_details/7")

    assert response.status_code == 400
    assert response.json() == {"msg": "User not found"}


####################################
###### help_offer route tests ######
####################################


def test_find_offers_by_user_id(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")

    user_data = {"username_email": "tee-jay", "password": "Password123!"}
    login_response = requests.post(f"http://{test_web_address}/token", json=user_data)
    token = login_response.json()["token"]

    response = requests.get(
        f"http://{test_web_address}/help_offers/1",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "help_offer_avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1708633707/MY_UPLOADS/aibxzxdpk6gl4u5xjgjg.jpg",
            "help_offer_bid": 65.0,
            "help_offer_first_name": "Tom",
            "help_offer_id": 5,
            "help_offer_last_name": "Jones",
            "help_offer_message": "I can assist you with watering your garden.",
            "help_offer_status": "pending",
            "help_offer_user_id": 1,
            "help_offer_username": "tee-jay",
            "help_receive_avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1709830407/PLANTS/person3_itrqub.jpg",
            "help_receive_first_name": "Alice",
            "help_receive_last_name": "Lane",
            "help_receive_username": "laney",
            "help_request_end_date": "Mon, 27 Nov 2023 00:00:00 GMT",
            "help_request_id": 10,
            "help_request_name": "Garden watering assistance required.",
            "help_request_start_date": "Wed, 22 Nov 2023 00:00:00 GMT",
            "help_request_user_id": 5,
        },
        {
            "help_offer_avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1708633707/MY_UPLOADS/aibxzxdpk6gl4u5xjgjg.jpg",
            "help_offer_bid": 70.0,
            "help_offer_first_name": "Tom",
            "help_offer_id": 10,
            "help_offer_last_name": "Jones",
            "help_offer_message": "I can take care of your plants while you are on holiday.",
            "help_offer_status": "pending",
            "help_offer_user_id": 1,
            "help_offer_username": "tee-jay",
            "help_receive_avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1709830407/PLANTS/person3_itrqub.jpg",
            "help_receive_first_name": "Alice",
            "help_receive_last_name": "Lane",
            "help_receive_username": "laney",
            "help_request_end_date": "Sun, 18 Jun 2023 00:00:00 GMT",
            "help_request_id": 5,
            "help_request_name": "Assistance needed with garden maintenance.",
            "help_request_start_date": "Mon, 12 Jun 2023 00:00:00 GMT",
            "help_request_user_id": 5,
        },
        {
            "help_offer_avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1708633707/MY_UPLOADS/aibxzxdpk6gl4u5xjgjg.jpg",
            "help_offer_bid": 80.0,
            "help_offer_first_name": "Tom",
            "help_offer_id": 15,
            "help_offer_last_name": "Jones",
            "help_offer_message": "I am available to help with your garden maintenance.",
            "help_offer_status": "pending",
            "help_offer_user_id": 1,
            "help_offer_username": "tee-jay",
            "help_receive_avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1709830407/PLANTS/person3_itrqub.jpg",
            "help_receive_first_name": "Alice",
            "help_receive_last_name": "Lane",
            "help_receive_username": "laney",
            "help_request_end_date": "Mon, 27 Nov 2023 00:00:00 GMT",
            "help_request_id": 10,
            "help_request_name": "Garden watering assistance required.",
            "help_request_start_date": "Wed, 22 Nov 2023 00:00:00 GMT",
            "help_request_user_id": 5,
        },
        {
            "help_offer_avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1708633707/MY_UPLOADS/aibxzxdpk6gl4u5xjgjg.jpg",
            "help_offer_bid": 85.0,
            "help_offer_first_name": "Tom",
            "help_offer_id": 20,
            "help_offer_last_name": "Jones",
            "help_offer_message": "I am available to assist with your gardening needs.",
            "help_offer_status": "pending",
            "help_offer_user_id": 1,
            "help_offer_username": "tee-jay",
            "help_receive_avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1709830407/PLANTS/person3_itrqub.jpg",
            "help_receive_first_name": "Alice",
            "help_receive_last_name": "Lane",
            "help_receive_username": "laney",
            "help_request_end_date": "Sun, 18 Jun 2023 00:00:00 GMT",
            "help_request_id": 5,
            "help_request_name": "Assistance needed with garden maintenance.",
            "help_request_start_date": "Mon, 12 Jun 2023 00:00:00 GMT",
            "help_request_user_id": 5,
        },
    ]


def test_create_offer(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")
    user_data = {"username_email": "tee-jay", "password": "Password123!"}
    login_response = requests.post(f"http://{test_web_address}/token", json=user_data)
    token = login_response.json()["token"]
    offer_details = {
        "user_id": 1,
        "message": "I can help",
        "bid": 10.0,
        "status": "pending",
    }
    response = requests.post(
        f"http://{test_web_address}/help_offers/1",
        json=offer_details,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    assert response.json() == {"msg": "Help Offer Created"}


def test_create_offer_missing_info(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")
    user_data = {"username_email": "tee-jay", "password": "Password123!"}
    login_response = requests.post(f"http://{test_web_address}/token", json=user_data)
    token = login_response.json()["token"]
    offer_details = {"user_id": 1, "message": None, "bid": 10.0, "status": "pending"}
    response = requests.post(
        f"http://{test_web_address}/help_offers/1",
        json=offer_details,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400
    assert response.json() == {"msg": "Help offer creation unsuccessful"}


def test_create_offer_no_auth(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")
    offer_details = {"user_id": 1, "message": None, "bid": 10.0, "status": "pending"}
    response = requests.post(
        f"http://{test_web_address}/help_offers/1", json=offer_details
    )
    assert response.status_code == 401


def test_get_help_offered_to_user(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")
    user_data = {"username_email": "tee-jay", "password": "Password123!"}
    login_response = requests.post(f"http://{test_web_address}/token", json=user_data)
    token = login_response.json()["token"]
    response = requests.get(
        f"http://{test_web_address}/help_offers/help_requests/1",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "help_offer_avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1709830407/PLANTS/person4_kqdufy.jpg",
            "help_offer_bid": 70.0,
            "help_offer_first_name": "Jane",
            "help_offer_id": 1,
            "help_offer_last_name": "Smith",
            "help_offer_message": "I can water your plants regularly during your vacation.",
            "help_offer_status": "pending",
            "help_offer_user_id": 2,
            "help_offer_username": "jane95",
            "help_receive_avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1708633707/MY_UPLOADS/aibxzxdpk6gl4u5xjgjg.jpg",
            "help_receive_first_name": "Tom",
            "help_receive_last_name": "Jones",
            "help_receive_username": "tee-jay",
            "help_request_end_date": "Fri, 07 Jul 2023 00:00:00 GMT",
            "help_request_id": 6,
            "help_request_name": "Plant watering help required.",
            "help_request_start_date": "Sun, 02 Jul 2023 00:00:00 GMT",
            "help_request_user_id": 1,
        },
        {
            "help_offer_avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1709830407/PLANTS/person4_kqdufy.jpg",
            "help_offer_bid": 80.0,
            "help_offer_first_name": "Jane",
            "help_offer_id": 6,
            "help_offer_last_name": "Smith",
            "help_offer_message": "I am available to help with your garden maintenance.",
            "help_offer_status": "pending",
            "help_offer_user_id": 2,
            "help_offer_username": "jane95",
            "help_receive_avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1708633707/MY_UPLOADS/aibxzxdpk6gl4u5xjgjg.jpg",
            "help_receive_first_name": "Tom",
            "help_receive_last_name": "Jones",
            "help_receive_username": "tee-jay",
            "help_request_end_date": "Tue, 28 Feb 2023 00:00:00 GMT",
            "help_request_id": 1,
            "help_request_name": "Help needed whilst on holiday.",
            "help_request_start_date": "Wed, 01 Feb 2023 00:00:00 GMT",
            "help_request_user_id": 1,
        },
        {
            "help_offer_avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1709830407/PLANTS/person4_kqdufy.jpg",
            "help_offer_bid": 85.0,
            "help_offer_first_name": "Jane",
            "help_offer_id": 11,
            "help_offer_last_name": "Smith",
            "help_offer_message": "I am available to assist with your gardening needs.",
            "help_offer_status": "pending",
            "help_offer_user_id": 2,
            "help_offer_username": "jane95",
            "help_receive_avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1708633707/MY_UPLOADS/aibxzxdpk6gl4u5xjgjg.jpg",
            "help_receive_first_name": "Tom",
            "help_receive_last_name": "Jones",
            "help_receive_username": "tee-jay",
            "help_request_end_date": "Fri, 07 Jul 2023 00:00:00 GMT",
            "help_request_id": 6,
            "help_request_name": "Plant watering help required.",
            "help_request_start_date": "Sun, 02 Jul 2023 00:00:00 GMT",
            "help_request_user_id": 1,
        },
        {
            "help_offer_avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1709830407/PLANTS/person4_kqdufy.jpg",
            "help_offer_bid": 60.0,
            "help_offer_first_name": "Jane",
            "help_offer_id": 16,
            "help_offer_last_name": "Smith",
            "help_offer_message": "I can provide immediate help with watering your plants.",
            "help_offer_status": "pending",
            "help_offer_user_id": 2,
            "help_offer_username": "jane95",
            "help_receive_avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1708633707/MY_UPLOADS/aibxzxdpk6gl4u5xjgjg.jpg",
            "help_receive_first_name": "Tom",
            "help_receive_last_name": "Jones",
            "help_receive_username": "tee-jay",
            "help_request_end_date": "Tue, 28 Feb 2023 00:00:00 GMT",
            "help_request_id": 1,
            "help_request_name": "Help needed whilst on holiday.",
            "help_request_start_date": "Wed, 01 Feb 2023 00:00:00 GMT",
            "help_request_user_id": 1,
        },
    ]

def test_accept_offer(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")

    user_data = {"username_email": "tee-jay", "password": "Password123!"}
    login_response = requests.post(f"http://{test_web_address}/token", json=user_data)
    token = login_response.json()["token"]

    response = requests.put(
        f"http://{test_web_address}/help_offers/accept_offer/2",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json() == {"msg": "Help offer accepted"}


def test_reject_offer(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")

    user_data = {"username_email": "tee-jay", "password": "Password123!"}
    login_response = requests.post(f"http://{test_web_address}/token", json=user_data)
    token = login_response.json()["token"]

    response = requests.put(
        f"http://{test_web_address}/help_offers/reject_offer/2",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json() == {"msg": "Help offer rejected"}

def test_rescind_offer(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")

    user_data = {"username_email": "tee-jay", "password": "Password123!"}
    login_response = requests.post(f"http://{test_web_address}/token", json=user_data)
    token = login_response.json()["token"]

    response = requests.put(
        f"http://{test_web_address}/help_offers/rescind_offer/2",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json() == {"msg": "Help offer rescinded"}

def test_get_help_offered_to_user_no_auth(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")

    response = requests.get(
        f"http://{test_web_address}/help_offers/help_requests/1",
    )
    assert response.status_code == 401


# TEST FOR MESSAGES


def test_get_messages_by_user_id(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")
    ChatRepository(db_connection)
    login_data = {"username_email": "tee-jay", "password": "Password123!"}
    login_response = requests.post(f"http://{test_web_address}/token", json=login_data)
    assert login_response.status_code == 201
    access_token = login_response.json()["token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(
        f"http://{test_web_address}/messages/user/1", headers=headers
    )

    assert response.status_code == 200

    chats = [
        {
            "end_date": "Fri, 01 Mar 2024 00:00:00 GMT",
            "id": 1,
            "message": [
                '{"sender": "jane95", "message": "Hello tee-jay, how are you?"}',
            ],
            "receiver_username": "tee-jay",
            "recipient_id": 1,
            "sender_id": 2,
            "sender_username": "jane95",
            "start_date": "Wed, 31 Jan 2024 00:00:00 GMT",
        },
    ]
    assert response.json() == chats


def test_create_messages(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")
    login_data = {"username_email": "tee-jay", "password": "Password123!"}
    login_response = requests.post(f"http://{test_web_address}/token", json=login_data)
    assert login_response.status_code == 201
    access_token = login_response.json()["token"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    message_payload = {
        "userId": 1,
        "receiverId": 2,
        "content": '{"sender": "tee-jay", "message": "Hello user two"}',
        "receiver_username": "user2",
        "sender_username": "tee-jay",
    }
    response = requests.post(
        f"http://{test_web_address}/messages", json=message_payload, headers=headers
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Message sent successfully"}


def test_select_chat_by_id(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")
    login_data = {"username_email": "tee-jay", "password": "Password123!"}
    login_response = requests.post(f"http://{test_web_address}/token", json=login_data)
    assert login_response.status_code == 201
    access_token = login_response.json()["token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"http://{test_web_address}/messages/1", headers=headers)
    assert response.status_code == 200
    chat = [
        {
            "end_date": "Fri, 01 Mar 2024 00:00:00 GMT",
            "id": 1,
            "message": [
                '{"sender": "jane95", "message": "Hello tee-jay, how are you?"}',
            ],
            "receiver_username": "tee-jay",
            "recipient_id": 1,
            "sender_id": 2,
            "sender_username": "jane95",
            "start_date": "Wed, 31 Jan 2024 00:00:00 GMT",
        },
    ]
    assert response.json() == chat


def test_edit_user_details(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")
    login_data = {"username_email": "tee-jay", "password": "Password123!"}
    login_response = requests.post(f"http://{test_web_address}/token", json=login_data)
    assert login_response.status_code == 201
    access_token = login_response.json()["token"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    edit_details_payload = {
        "first_name": "UpdatedFirstName",
        "last_name": "UpdatedLastName",
        "username": "UpdatedUsername",
        "email": "updated@email.com",
        "address": "Updated Address",
    }
    response = requests.put(
        f"http://{test_web_address}/edit_user_details/1",
        json=edit_details_payload,
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json() == {"msg": "User updated successful"}

    updated_user_response = requests.get(
        f"http://{test_web_address}/user_details/1", headers=headers
    )
    assert updated_user_response.status_code == 200
    updated_user_details = updated_user_response.json()
    assert updated_user_details["first_name"] == "UpdatedFirstName"
    assert updated_user_details["last_name"] == "UpdatedLastName"
    assert updated_user_details["username"] == "UpdatedUsername"
    assert updated_user_details["email"] == "updated@email.com"
    assert updated_user_details["address"] == "Updated Address"


@pytest.mark.skip  # THIS TEST PASS BUT IT DOES NOT PASS ON CI, REQUIRES Cloudinary KEYS
def test_edit_user_avatar(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")
    login_data = {"username_email": "tee-jay", "password": "Password123!"}
    login_response = requests.post(f"http://{test_web_address}/token", json=login_data)
    assert login_response.status_code == 201
    access_token = login_response.json()["token"]

    app.testing = True
    client = app.test_client()
    data = io.BytesIO(b"mock image data")
    data.name = "test_avatar.png"

    mock_cloudinary_response = {"url": "http://cloudinary.com/someimageurl"}

    with patch("cloudinary.uploader.upload", return_value=mock_cloudinary_response):
        response = client.put(
            f"/edit_user_avatar/1",
            content_type="multipart/form-data",
            data={"avatar": (data, "test_avatar.png")},
            headers={"Authorization": f"Bearer {access_token}"},
        )

    assert response.status_code == 200
    assert response.get_json() == {
        "msg": "Avatar updated successfully",
        "avatar_url": "http://cloudinary.com/someimageurl",
    }




@pytest.mark.skip  # THIS TEST PASS LOCAL BUT IT DOES NOT PASS ON CI, REQUIRES API KEYS
def test_search_plants_by_name(test_web_address, db_connection):
    db_connection.seed("seeds/bloom.sql")
    login_data = {"username_email": "tee-jay", "password": "Password123!"}
    login_response = requests.post(f"http://{test_web_address}/token", json=login_data)
    assert login_response.status_code == 201
    access_token = login_response.json()["token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.post(
        f"http://{test_web_address}/api/plants/name",
        json={"name": "Rose"},
        headers=headers
    )

    assert response.status_code == 200
    expected_plant_data = {
        "common_name": "Field rose",
        "plant_id": 265580,
        "latin_name": "Rosa arvensis",
        "photo": "https://bs.plantnet.org/image/o/afc9f4d7ce137f04746413f629330948b73e79d3"
    }
    plant_data = response.json()[0]  
    assert plant_data == expected_plant_data
