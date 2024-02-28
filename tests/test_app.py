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

# Help Request route tests:

def test_get_all_help_requests_from_database(test_web_address, db_connection):
    db_connection.seed("seeds/bloom.sql")
    HelpRequestRepository(db_connection)

    response = requests.get(f"http://{test_web_address}/help_requests")
    assert response.status_code == 200

    expected_data = [
        {
            "id": 1,
            "date": "2023-10-19 10:23:54",
            "title": "title_01",
            "message": "message requesting help",
            "start_date": "2023-02-01",
            "end_date": "2023-03-01",
            "user_id": 1,
            "maxprice": 50.0
        },
        {
            "id": 2,
            "date": "2023-10-20 10:23:54",
            "title": "title_02",
            "message": "message requesting help 2",
            "start_date": "2023-02-03",
            "end_date": "2023-03-03",
            "user_id": 2,
            "maxprice": 60.0
        }
    ]

    assert response.json() == expected_data

def test_get_one_help_request_from_db(test_web_address, db_connection):
    db_connection.seed("seeds/bloom.sql")
    HelpRequestRepository(db_connection)

    response = requests.get(f"http://{test_web_address}/help_requests/2")
    
    assert response.status_code == 200
    expected_data = {
            "id": 2,
            "date": "2023-10-20 10:23:54",
            "title": "title_02",
            "message": "message requesting help 2",
            "start_date": "2023-02-03",
            "end_date": "2023-03-03",
            "user_id": 2,
            "maxprice": 60.0
        }
    assert response.json() == expected_data