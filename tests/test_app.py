from app import *
import requests

#########################
###### test /token ######
#########################


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


###############################
###### test /user/signup ######
###############################


def test_user_created_with_correct_details_with_address(
    db_connection, test_web_address
):
    db_connection.seed("seeds/bloom.sql")
    user_data = {
        "first_name": "Tom",
        "last_name": "Jones",
        "username": "TJ",
        "email": "tjones@email.com",
        "password": "Password123!",
        "password_confirm": "Password123!",
        "address": "An address!",
    }

    response = requests.post(f"http://{test_web_address}/user/signup", json=user_data)

    assert response.status_code == 200
    assert response.json() == {"msg": "User created"}


def test_user_created_with_correct_details_with_blank_address(
    db_connection, test_web_address
):
    db_connection.seed("seeds/bloom.sql")
    user_data = {
        "first_name": "Tom",
        "last_name": "Jones",
        "username": "TJ",
        "email": "tjones@email.com",
        "password": "Password123!",
        "password_confirm": "Password123!",
        "address": "",
    }

    response = requests.post(f"http://{test_web_address}/user/signup", json=user_data)

    assert response.status_code == 200
    assert response.json() == {"msg": "User created"}


def test_user_not_created_when_duplicate_username(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")
    user_data1 = {
        "first_name": "Tom",
        "last_name": "Jones",
        "username": "TJ",
        "email": "tjones@email.com",
        "password": "Password123!",
        "password_confirm": "Password123!",
        "address": "",
    }

    response = requests.post(f"http://{test_web_address}/user/signup", json=user_data1)

    user_data2 = {
        "first_name": "Tony",
        "last_name": "Jonesy",
        "username": "TJ",
        "email": "tjonesy@email.com",
        "password": "Password123!",
        "password_confirm": "Password123!",
        "address": "",
    }
    response = requests.post(f"http://{test_web_address}/user/signup", json=user_data2)

    assert response.status_code == 401
    assert response.json() == {
        "msg": "Bad request - user not created. This username or email could be taken."
    }


def test_user_not_created_when_duplicate_email(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")
    user_data1 = {
        "first_name": "Tom",
        "last_name": "Jones",
        "username": "TJ",
        "email": "tjones@email.com",
        "password": "Password123!",
        "password_confirm": "Password123!",
        "address": "",
    }

    response = requests.post(f"http://{test_web_address}/user/signup", json=user_data1)

    user_data2 = {
        "first_name": "Tony",
        "last_name": "Jonesy",
        "username": "JT",
        "email": "tjones@email.com",
        "password": "Password123!",
        "password_confirm": "Password123!",
        "address": "",
    }
    response = requests.post(f"http://{test_web_address}/user/signup", json=user_data2)

    assert response.status_code == 401
    assert response.json() == {
        "msg": "Bad request - user not created. This username or email could be taken."
    }


def test_user_not_created_when_information_passwords_do_not_match(
    db_connection, test_web_address
):
    db_connection.seed("seeds/bloom.sql")
    user_data1 = {
        "first_name": "Tom",
        "last_name": "Jones",
        "username": "TJ",
        "email": "tjones@email.com",
        "password": "Password123!",
        "password_confirm": "Password456!",
        "address": "",
    }

    response = requests.post(f"http://{test_web_address}/user/signup", json=user_data1)

    assert response.status_code == 401
    assert response.json() == {
        "msg": "Bad request - user not created. Passwords does not match."
    }


#####################################
###### test /user_details/<id> ######
#####################################


def test_get_user_details_for_valid_user_id(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")
    response = requests.get(f"http://{test_web_address}/user_details/1")

    assert response.status_code == 200
    assert response.json() == {
        "first_name": "user",
        "last_name": "1",
        "username": "user1",
        "email": "user1@email.com",
        "avatar_url_string": "test_image1.png",
        "address": "test_address1",
    }


def test_return_user_not_found_for_invalid_user_id(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")
    response = requests.get(f"http://{test_web_address}/user_details/7")

    assert response.status_code == 400
    assert response.json() == {"msg": "User not found"}
