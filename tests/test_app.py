from app import *
import requests
import datetime

#########################
###### test /token ######
#########################


def test_user_authentication_successful_via_username(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")
    user_data = {"username_email": "user1", "password": "Password123!"}
    response = requests.post(f"http://{test_web_address}/token", json=user_data)
    response.json()
    assert response.status_code == 201
    assert response != {"msg": "Bad username or password"}


def test_user_authentication_successful_via_email(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")
    user_data = {"username_email": "user1@email.com", "password": "Password123!"}
    response = requests.post(f"http://{test_web_address}/token", json=user_data)
    response.json()
    assert response.status_code == 201
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
    
# Plants Request route tests:
def test_get_plants_by_user_id(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")
    PlantsUserRepository(db_connection)
    
    login_data = {"username_email": "user1", "password": "Password123!"}
    login_response = requests.post(f"http://{test_web_address}/token", json=login_data)
    assert login_response.status_code == 201
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
    
def test_assign_plant_to_user(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")
    login_data = {"username_email": "user1", "password": "Password123!"}
    login_response = requests.post(f"http://{test_web_address}/token", json=login_data)
    assert login_response.status_code == 201
    access_token = login_response.json()["token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    assign_data = {"user_id": 1, "plant_id": 2, "quantity": 3}
    response = requests.post(f"http://{test_web_address}/plants/user/assign", json=assign_data, headers=headers)

    assert response.status_code == 200
    assert response.json() == {"message": "Plant assigned successfully"}
    
    
def test_update_plant_quantity_for_user(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")
    login_data = {"username_email": "user1", "password": "Password123!"}
    login_response = requests.post(f"http://{test_web_address}/token", json=login_data)
    assert login_response.status_code == 201
    access_token = login_response.json()["token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    update_data = {"user_id": 1, "plant_id": 2, "new_quantity": 5}
    response = requests.post(f"http://{test_web_address}/plants/user/update", json=update_data, headers=headers)

    assert response.status_code == 200
    assert response.json() == {"message": "Plant quantity updated successfully"}
    

def test_delete_plant_from_user(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")
    login_data = {"username_email": "user1", "password": "Password123!"}
    login_response = requests.post(f"http://{test_web_address}/token", json=login_data)
    assert login_response.status_code == 201
    access_token = login_response.json()["token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    delete_data = {"user_id": 1, "plant_id": 2}
    response = requests.delete(f"http://{test_web_address}/plants/user/delete", json=delete_data, headers=headers)

    assert response.status_code == 200
    assert response.json() == {"message": "Plant deleted successfully"}

# Help Request route tests:


def test_get_all_help_requests_from_database(test_web_address, db_connection):
    db_connection.seed("seeds/bloom.sql")

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
            "maxprice": 50.0,
        },
        {
            "id": 2,
            "date": "2023-10-20 10:23:54",
            "title": "title_02",
            "message": "message requesting help 2",
            "start_date": "2023-02-03",
            "end_date": "2023-03-03",
            "user_id": 2,
            "maxprice": 60.0,
        },
        {
            "id": 3,
            "date": "2023-10-19 10:23:54",
            "title": "t_03",
            "message": "message requesting help 3",
            "start_date": "2023-02-01",
            "end_date": "2023-03-01",
            "user_id": 1,
            "maxprice": 80.0,
        },
    ]

    assert response.json() == expected_data


def test_get_one_help_request_from_db(test_web_address, db_connection):
    db_connection.seed("seeds/bloom.sql")

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
        "maxprice": 60.0,
    }
    assert response.json() == expected_data


def test_get_all_requests_by_one_user(test_web_address, db_connection):
    db_connection.seed("seeds/bloom.sql")

    login_data = {"username_email": "user1", "password": "Password123!"}
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
            "id": 1,
            "date": "2023-10-19 10:23:54",
            "title": "title_01",
            "message": "message requesting help",
            "start_date": "2023-02-01",
            "end_date": "2023-03-01",
            "user_id": 1,
            "maxprice": 50.0,
        },
        {
            "id": 3,
            "date": "2023-10-19 10:23:54",
            "title": "t_03",
            "message": "message requesting help 3",
            "start_date": "2023-02-01",
            "end_date": "2023-03-01",
            "user_id": 1,
            "maxprice": 80.0,
        },
    ]

    assert response.json() == expected_data


def test_create_help_request(test_web_address, db_connection):
    db_connection.seed("seeds/bloom.sql")

    login_data = {"username_email": "user1", "password": "Password123!"}
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

    login_data = {"username_email": "user1", "password": "Password123!"}
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
        "first_name": "Tom",
        "last_name": "Jones",
        "username": "TJ",
        "email": "tjones@email.com",
        "password": "Password123!",
        "password_confirm": "Password123!",
        "address": "An address!",
    }

    response = requests.post(f"http://{test_web_address}/user/signup", json=user_data)

    assert response.status_code == 201
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

    assert response.status_code == 201
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
        "id" : 1,
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


"""
============================
help_offer route tests
============================
"""


def test_find_offers_by_user_id(db_connection, test_web_address):
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
            "user_id": 1,
        }
    ]


def test_create_offer(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")
    user_data = {"username_email": "user1", "password": "Password123!"}
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
    user_data = {"username_email": "user1", "password": "Password123!"}
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
    user_data = {"username_email": "user1", "password": "Password123!"}
    login_response = requests.post(f"http://{test_web_address}/token", json=user_data)
    token = login_response.json()["token"]
    response = requests.get(
        f"http://{test_web_address}/help_offers/help_requests/1",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "bid": 50.0,
            "id": 1,
            "message": "Offering help",
            "request_id": 1,
            "status": "pending",
            "user_id": 1,
        }
    ]


def test_get_help_offered_to_user_no_auth(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")

    response = requests.get(f"http://{test_web_address}/help_offers/help_requests/1")
    assert response.status_code == 401
    
    
# TEST FOR MESSAGES 

    
def test_get_messages_by_user_id(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")
    ChatRepository(db_connection)
    login_data = {"username_email": "user1", "password": "Password123!"}
    login_response = requests.post(f"http://{test_web_address}/token", json=login_data)
    assert login_response.status_code == 201
    access_token = login_response.json()["token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"http://{test_web_address}/messages/user/1", headers=headers)

    assert response.status_code == 200
    
    chats = [{
            "id": 1,
            "recipient_id": 2,
            "message": [
                '{"sender": "user1", "message": "Hello user two"}'
            ],
            "receiver_username": "user2",
            "sender_username": "user1",
            "start_date": "Wed, 31 Jan 2024 00:00:00 GMT",
            "end_date": "Fri, 01 Mar 2024 00:00:00 GMT",
            "sender_id": 1,
        }]
    assert response.json() == chats
    


def test_create_messages(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")
    login_data = {"username_email": "user1", "password": "Password123!"}
    login_response = requests.post(f"http://{test_web_address}/token", json=login_data)
    assert login_response.status_code == 201 
    access_token = login_response.json()["token"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    message_payload = {
        "userId": 1, 
        "receiverId": 2, 
        "content": '{"sender": "user1", "message": "Hello user two"}',
        "receiver_username": "user2",
        "sender_username": "user1"
    }
    response = requests.post(f"http://{test_web_address}/messages", json=message_payload, headers=headers)
    

    assert response.status_code == 200
    assert response.json() == {"message": "Message sent successfully"}
    
    
    
def test_select_chat_by_id(db_connection, test_web_address):
    db_connection.seed("seeds/bloom.sql")
    login_data = {"username_email": "user1", "password": "Password123!"}
    login_response = requests.post(f"http://{test_web_address}/token", json=login_data)
    assert login_response.status_code == 201 
    access_token = login_response.json()["token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"http://{test_web_address}/messages/1", headers=headers)
    assert response.status_code == 200
    chat = [{
            "id": 1,
            "recipient_id": 2,
            "message": [
                '{"sender": "user1", "message": "Hello user two"}'
            ],
            "receiver_username": "user2",
            "sender_username": "user1",
            "start_date": "Wed, 31 Jan 2024 00:00:00 GMT",
            "end_date": "Fri, 01 Mar 2024 00:00:00 GMT",
            "sender_id": 1,
        }]
    assert response.json() == chat