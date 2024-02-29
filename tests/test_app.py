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


'''
============================
help_offer route tests
============================
'''

def test_find_offers_by_user_id(
        db_connection, test_web_address
):
    db_connection.seed("seeds/bloom.sql")
    response = requests.get(f"http://{test_web_address}/help_offers/1")
    assert response.status_code == 200
    assert response.json() == [
    {
        "bid": 50.0,
        "id": 1,
        "message": "Offering help",
        "request_id": 1,
        "status": "pending",
        "user_id": 1
    }
    ]


def test_create_offer(
        db_connection, test_web_address
):
    db_connection.seed("seeds/bloom.sql")
    user_data = {"username_email": "user1", "password": "Password123!"}
    login_response = requests.post(f"http://{test_web_address}/token", json=user_data)
    token = login_response.json()["token"]
    offer_details = {
        "user_id": 1,
        "message": 'I can help',
        "bid": 10.0,
        "status": "pending"
    }
    response = requests.post(f"http://{test_web_address}/help_offers/1", json=offer_details, headers={"Authorization":f"Bearer {token}"})
    assert response.status_code == 201
    assert response.json() == {"msg":"Help Offer Created"}

def test_create_offer_missing_info(
        db_connection, test_web_address
):
    db_connection.seed("seeds/bloom.sql")
    user_data = {"username_email": "user1", "password": "Password123!"}
    login_response = requests.post(f"http://{test_web_address}/token", json=user_data)
    token = login_response.json()["token"]
    offer_details = {
        "user_id": 1,
        "message": None,
        "bid": 10.0,
        "status": "pending"
    }
    response = requests.post(f"http://{test_web_address}/help_offers/1", json=offer_details, headers={"Authorization":f"Bearer {token}"})
    assert response.status_code == 400
    assert response.json() == {"msg":"Help offer creation unsuccessful"}

def test_create_offer_no_auth(
        db_connection, test_web_address
):
    db_connection.seed("seeds/bloom.sql")
    offer_details = {
        "user_id": 1,
        "message": None,
        "bid": 10.0,
        "status": "pending"
    }
    response = requests.post(f"http://{test_web_address}/help_offers/1", json=offer_details)
    assert response.status_code == 401

def test_get_help_offered_to_user(
        db_connection, test_web_address
):
    db_connection.seed("seeds/bloom.sql")
    user_data = {"username_email": "user1", "password": "Password123!"}
    login_response = requests.post(f"http://{test_web_address}/token", json=user_data)
    token = login_response.json()["token"]
    response = requests.get(f"http://{test_web_address}/help_offers/help_requests/1", headers={"Authorization":f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == [
        {
            "bid": 50.0,
            "id": 1,
            "message": "Offering help",
            "request_id": 1,
            "status": "pending",
            "user_id": 1
        }
    ]

def test_get_help_offered_to_user_no_auth(
        db_connection, test_web_address
):
    db_connection.seed("seeds/bloom.sql")
    
    response = requests.get(f"http://{test_web_address}/help_offers/help_requests/1")
    assert response.status_code == 401