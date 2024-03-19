from datetime import date, datetime
import pytest
from lib.models.help_request import HelpRequest
from lib.models.user import User
from lib.repositories.help_request_repository import HelpRequestRepository


def test_can_get_all_help_requests(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = HelpRequestRepository(db_connection)

    help_requests = repository.all_requests()

    assert help_requests == [
        HelpRequest(
            1,
            datetime(2023, 10, 19, 10, 23, 54),
            "Help needed whilst on holiday.",
            "I am going on holiday for all of February - would love some help!",
            date(2023, 2, 1),
            date(2023, 2, 28),
            1,
            75.0,
        ),
        HelpRequest(
            2,
            datetime(2023, 11, 12, 8, 45, 21),
            "Help required with plant care.",
            "Looking for someone to water my plants while I am away.",
            date(2023, 3, 5),
            date(2023, 3, 10),
            2,
            100.0,
        ),
        HelpRequest(
            3,
            datetime(2023, 11, 28, 14, 30, 9),
            "Need assistance with gardening.",
            "Seeking help in maintaining my garden during my absence.",
            date(2023, 4, 15),
            date(2023, 4, 20),
            3,
            90.0,
        ),
        HelpRequest(
            4,
            datetime(2023, 12, 7, 11, 20, 35),
            "Help wanted for plant care.",
            "Require someone to water my indoor plants while I am out of town.",
            date(2023, 5, 3),
            date(2023, 5, 8),
            4,
            80.0,
        ),
        HelpRequest(
            5,
            datetime(2023, 12, 20, 9, 55, 47),
            "Assistance needed with garden maintenance.",
            "Looking for a reliable person to care for my garden while I am away.",
            date(2023, 6, 12),
            date(2023, 6, 18),
            5,
            70.0,
        ),
        HelpRequest(
            6,
            datetime(2024, 1, 5, 16, 10, 2),
            "Plant watering help required.",
            "Seeking someone to water my plants regularly during my vacation.",
            date(2023, 7, 2),
            date(2023, 7, 7),
            1,
            85.0,
        ),
        HelpRequest(
            7,
            datetime(2024, 1, 15, 13, 40, 19),
            "Gardening assistance wanted.",
            "Require help in maintaining my backyard garden for a few weeks.",
            date(2023, 8, 20),
            date(2023, 8, 25),
            2,
            95.0,
        ),
        HelpRequest(
            8,
            datetime(2024, 2, 2, 10, 5, 38),
            "Plant care help needed urgently.",
            "Looking for immediate assistance in watering my plants.",
            date(2023, 9, 10),
            date(2023, 9, 15),
            3,
            65.0,
        ),
        HelpRequest(
            9,
            datetime(2024, 2, 14, 7, 30, 55),
            "Help needed with indoor plants.",
            "Seeking someone to take care of my indoor plants for a short duration.",
            date(2023, 10, 5),
            date(2023, 10, 10),
            4,
            75.0,
        ),
        HelpRequest(
            10,
            datetime(2024, 2, 28, 15, 20, 10),
            "Garden watering assistance required.",
            "Require help in watering my garden while I am away.",
            date(2023, 11, 22),
            date(2023, 11, 27),
            5,
            60.0,
        ),
    ]


def test_can_find_help_request_by_id(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = HelpRequestRepository(db_connection)

    result = repository.find_request_by_id(1)

    assert result[0] == HelpRequest(
        1,
        datetime(2023, 10, 19, 10, 23, 54),
        "Help needed whilst on holiday.",
        "I am going on holiday for all of February - would love some help!",
        date(2023, 2, 1),
        date(2023, 2, 28),
        1,
        75.0,
    )
    assert result[1] == {
        "first_name": "Tom",
        "last_name": "Jones",
        "username": "tee-jay",
        "avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1708633707/MY_UPLOADS/aibxzxdpk6gl4u5xjgjg.jpg",
    }


def test_can_find_help_requests_by_user(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = HelpRequestRepository(db_connection)
    actual_results = repository.find_requests_by_user_id(1)

    assert len(actual_results) == 2  
    help_request_1 = actual_results[0]['help_request']
    assert help_request_1.id == 1  
    assert help_request_1.title == 'Help needed whilst on holiday.'
 

    plant_photos_1 = actual_results[0]['plant_photos']
    expected_plant_photos_1 = [
        'https://res.cloudinary.com/dououppib/image/upload/v1709740432/PLANTS/Barberry_copy_gseiuj.png',
        'https://res.cloudinary.com/dououppib/image/upload/v1709740425/PLANTS/African_sheepbush_lyorlf.jpg',
        'https://res.cloudinary.com/dououppib/image/upload/v1709740428/PLANTS/Alder_jc4szc.jpg'
    ]
    assert set(plant_photos_1) == set(expected_plant_photos_1) 





def test_create_new_help_request_with_fields(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = HelpRequestRepository(db_connection)

    repository.create_request(
        HelpRequest(
            None,
            datetime(2024, 2, 27, 14, 30, 50),
            "new title",
            "need help watering plant",
            date(2024, 2, 29),
            date(2023, 3, 7),
            1,
            60.0,
        )
    )

    assert repository.all_requests() == [
        HelpRequest(
            1,
            datetime(2023, 10, 19, 10, 23, 54),
            "Help needed whilst on holiday.",
            "I am going on holiday for all of February - would love some help!",
            date(2023, 2, 1),
            date(2023, 2, 28),
            1,
            75.0,
        ),
        HelpRequest(
            2,
            datetime(2023, 11, 12, 8, 45, 21),
            "Help required with plant care.",
            "Looking for someone to water my plants while I am away.",
            date(2023, 3, 5),
            date(2023, 3, 10),
            2,
            100.0,
        ),
        HelpRequest(
            3,
            datetime(2023, 11, 28, 14, 30, 9),
            "Need assistance with gardening.",
            "Seeking help in maintaining my garden during my absence.",
            date(2023, 4, 15),
            date(2023, 4, 20),
            3,
            90.0,
        ),
        HelpRequest(
            4,
            datetime(2023, 12, 7, 11, 20, 35),
            "Help wanted for plant care.",
            "Require someone to water my indoor plants while I am out of town.",
            date(2023, 5, 3),
            date(2023, 5, 8),
            4,
            80.0,
        ),
        HelpRequest(
            5,
            datetime(2023, 12, 20, 9, 55, 47),
            "Assistance needed with garden maintenance.",
            "Looking for a reliable person to care for my garden while I am away.",
            date(2023, 6, 12),
            date(2023, 6, 18),
            5,
            70.0,
        ),
        HelpRequest(
            6,
            datetime(2024, 1, 5, 16, 10, 2),
            "Plant watering help required.",
            "Seeking someone to water my plants regularly during my vacation.",
            date(2023, 7, 2),
            date(2023, 7, 7),
            1,
            85.0,
        ),
        HelpRequest(
            7,
            datetime(2024, 1, 15, 13, 40, 19),
            "Gardening assistance wanted.",
            "Require help in maintaining my backyard garden for a few weeks.",
            date(2023, 8, 20),
            date(2023, 8, 25),
            2,
            95.0,
        ),
        HelpRequest(
            8,
            datetime(2024, 2, 2, 10, 5, 38),
            "Plant care help needed urgently.",
            "Looking for immediate assistance in watering my plants.",
            date(2023, 9, 10),
            date(2023, 9, 15),
            3,
            65.0,
        ),
        HelpRequest(
            9,
            datetime(2024, 2, 14, 7, 30, 55),
            "Help needed with indoor plants.",
            "Seeking someone to take care of my indoor plants for a short duration.",
            date(2023, 10, 5),
            date(2023, 10, 10),
            4,
            75.0,
        ),
        HelpRequest(
            10,
            datetime(2024, 2, 28, 15, 20, 10),
            "Garden watering assistance required.",
            "Require help in watering my garden while I am away.",
            date(2023, 11, 22),
            date(2023, 11, 27),
            5,
            60.0,
        ),
        HelpRequest(
            11,
            datetime(2024, 2, 27, 14, 30, 50),
            "new title",
            "need help watering plant",
            date(2024, 2, 29),
            date(2023, 3, 7),
            1,
            60.0,
        ),
    ]


def test_can_delete_request(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = HelpRequestRepository(db_connection)

    repository.delete_request(1, 1)
    assert repository.all_requests() == [
        HelpRequest(
            2,
            datetime(2023, 11, 12, 8, 45, 21),
            "Help required with plant care.",
            "Looking for someone to water my plants while I am away.",
            date(2023, 3, 5),
            date(2023, 3, 10),
            2,
            100.0,
        ),
        HelpRequest(
            3,
            datetime(2023, 11, 28, 14, 30, 9),
            "Need assistance with gardening.",
            "Seeking help in maintaining my garden during my absence.",
            date(2023, 4, 15),
            date(2023, 4, 20),
            3,
            90.0,
        ),
        HelpRequest(
            4,
            datetime(2023, 12, 7, 11, 20, 35),
            "Help wanted for plant care.",
            "Require someone to water my indoor plants while I am out of town.",
            date(2023, 5, 3),
            date(2023, 5, 8),
            4,
            80.0,
        ),
        HelpRequest(
            5,
            datetime(2023, 12, 20, 9, 55, 47),
            "Assistance needed with garden maintenance.",
            "Looking for a reliable person to care for my garden while I am away.",
            date(2023, 6, 12),
            date(2023, 6, 18),
            5,
            70.0,
        ),
        HelpRequest(
            6,
            datetime(2024, 1, 5, 16, 10, 2),
            "Plant watering help required.",
            "Seeking someone to water my plants regularly during my vacation.",
            date(2023, 7, 2),
            date(2023, 7, 7),
            1,
            85.0,
        ),
        HelpRequest(
            7,
            datetime(2024, 1, 15, 13, 40, 19),
            "Gardening assistance wanted.",
            "Require help in maintaining my backyard garden for a few weeks.",
            date(2023, 8, 20),
            date(2023, 8, 25),
            2,
            95.0,
        ),
        HelpRequest(
            8,
            datetime(2024, 2, 2, 10, 5, 38),
            "Plant care help needed urgently.",
            "Looking for immediate assistance in watering my plants.",
            date(2023, 9, 10),
            date(2023, 9, 15),
            3,
            65.0,
        ),
        HelpRequest(
            9,
            datetime(2024, 2, 14, 7, 30, 55),
            "Help needed with indoor plants.",
            "Seeking someone to take care of my indoor plants for a short duration.",
            date(2023, 10, 5),
            date(2023, 10, 10),
            4,
            75.0,
        ),
        HelpRequest(
            10,
            datetime(2024, 2, 28, 15, 20, 10),
            "Garden watering assistance required.",
            "Require help in watering my garden while I am away.",
            date(2023, 11, 22),
            date(2023, 11, 27),
            5,
            60.0,
        ),
    ]


def test_can_find_title_substring_from_requests(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = HelpRequestRepository(db_connection)

    assert repository.find_requests_by_title_substring("Help needed whilst") == [
        HelpRequest(
            1,
            datetime(2023, 10, 19, 10, 23, 54),
            "Help needed whilst on holiday.",
            "I am going on holiday for all of February - would love some help!",
            date(2023, 2, 1),
            date(2023, 2, 28),
            1,
            75.0,
        ),
    ]


def test_can_find_no_requests_from_given_substring(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = HelpRequestRepository(db_connection)

    assert repository.find_requests_by_title_substring("elephant") == []


def test_can_find_one_request_from_given_substring(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = HelpRequestRepository(db_connection)

    assert repository.find_requests_by_title_substring("maintenance") == [
        HelpRequest(
            5,
            datetime(2023, 12, 20, 9, 55, 47),
            "Assistance needed with garden maintenance.",
            "Looking for a reliable person to care for my garden while I am away.",
            date(2023, 6, 12),
            date(2023, 6, 18),
            5,
            70.0,
        ),
    ]



def test_get_all_help_requests_with_user_details(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = HelpRequestRepository(db_connection)

    help_requests_with_users = (
        repository.get_all_help_requests_with_user_first_name_and_last_name()
    )

    assert help_requests_with_users == [
        (
            HelpRequest(
                1,
                datetime(2023, 10, 19, 10, 23, 54),
                "Help needed whilst on holiday.",
                "I am going on holiday for all of February - would love some help!",
                date(2023, 2, 1),
                date(2023, 2, 28),
                1,
                75.0,
            ),
            {
                "avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1708633707/MY_UPLOADS/aibxzxdpk6gl4u5xjgjg.jpg",
                "first_name": "Tom",
                "last_name": "Jones",
                "username": "tee-jay",
            },
        ),
        (
            HelpRequest(
                2,
                datetime(2023, 11, 12, 8, 45, 21),
                "Help required with plant care.",
                "Looking for someone to water my plants while I am away.",
                date(2023, 3, 5),
                date(2023, 3, 10),
                2,
                100.0,
            ),
            {
                "avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1709830407/PLANTS/person4_kqdufy.jpg",
                "first_name": "Jane",
                "last_name": "Smith",
                "username": "jane95",
            },
        ),
        (
            HelpRequest(
                3,
                datetime(2023, 11, 28, 14, 30, 9),
                "Need assistance with gardening.",
                "Seeking help in maintaining my garden during my absence.",
                date(2023, 4, 15),
                date(2023, 4, 20),
                3,
                90.0,
            ),
            {
                "avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1709830406/PLANTS/person2_jpuq5z.jpg",
                "first_name": "Jilly",
                "last_name": "Smith",
                "username": "sm1thi",
            },
        ),
        (
            HelpRequest(
                4,
                datetime(2023, 12, 7, 11, 20, 35),
                "Help wanted for plant care.",
                "Require someone to water my indoor plants while I am out of town.",
                date(2023, 5, 3),
                date(2023, 5, 8),
                4,
                80.0,
            ),
            {
                "avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1709830406/PLANTS/person1_jdh4xm.jpg",
                "first_name": "Barbra",
                "last_name": "Banes",
                "username": "barn-owl58",
            },
        ),
        (
            HelpRequest(
                5,
                datetime(2023, 12, 20, 9, 55, 47),
                "Assistance needed with garden maintenance.",
                "Looking for a reliable person to care for my garden while I am away.",
                date(2023, 6, 12),
                date(2023, 6, 18),
                5,
                70.0,
            ),
            {
                "avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1709830407/PLANTS/person3_itrqub.jpg",
                "first_name": "Alice",
                "last_name": "Lane",
                "username": "laney",
            },
        ),
        (
            HelpRequest(
                6,
                datetime(2024, 1, 5, 16, 10, 2),
                "Plant watering help required.",
                "Seeking someone to water my plants regularly during my vacation.",
                date(2023, 7, 2),
                date(2023, 7, 7),
                1,
                85.0,
            ),
            {
                "avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1708633707/MY_UPLOADS/aibxzxdpk6gl4u5xjgjg.jpg",
                "first_name": "Tom",
                "last_name": "Jones",
                "username": "tee-jay",
            },
        ),
        (
            HelpRequest(
                7,
                datetime(2024, 1, 15, 13, 40, 19),
                "Gardening assistance wanted.",
                "Require help in maintaining my backyard garden for a few weeks.",
                date(2023, 8, 20),
                date(2023, 8, 25),
                2,
                95.0,
            ),
            {
                "avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1709830407/PLANTS/person4_kqdufy.jpg",
                "first_name": "Jane",
                "last_name": "Smith",
                "username": "jane95",
            },
        ),
        (
            HelpRequest(
                8,
                datetime(2024, 2, 2, 10, 5, 38),
                "Plant care help needed urgently.",
                "Looking for immediate assistance in watering my plants.",
                date(2023, 9, 10),
                date(2023, 9, 15),
                3,
                65.0,
            ),
            {
                "avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1709830406/PLANTS/person2_jpuq5z.jpg",
                "first_name": "Jilly",
                "last_name": "Smith",
                "username": "sm1thi",
            },
        ),
        (
            HelpRequest(
                9,
                datetime(2024, 2, 14, 7, 30, 55),
                "Help needed with indoor plants.",
                "Seeking someone to take care of my indoor plants for a short duration.",
                date(2023, 10, 5),
                date(2023, 10, 10),
                4,
                75.0,
            ),
            {
                "avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1709830406/PLANTS/person1_jdh4xm.jpg",
                "first_name": "Barbra",
                "last_name": "Banes",
                "username": "barn-owl58",
            },
        ),
        (
            HelpRequest(
                10,
                datetime(2024, 2, 28, 15, 20, 10),
                "Garden watering assistance required.",
                "Require help in watering my garden while I am away.",
                date(2023, 11, 22),
                date(2023, 11, 27),
                5,
                60.0,
            ),
            {
                "avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1709830407/PLANTS/person3_itrqub.jpg",
                "first_name": "Alice",
                "last_name": "Lane",
                "username": "laney",
            },
        ),
    ]

@pytest.mark.skip
def test_get_all_help_requests_with_user_details_and_plant_photo(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = HelpRequestRepository(db_connection)

    help_requests_with_users = (
        repository.get_plant_photo_with_user_details_for_help_request()
    )

    assert help_requests_with_users == [
        (
            HelpRequest(
                1,
                datetime(2023, 10, 19, 10, 23, 54),
                "Help needed whilst on holiday.",
                "I am going on holiday for all of February - would love some help!",
                date(2023, 2, 1),
                date(2023, 2, 28),
                1,
                75.0,
            ),
            {
                "avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1708633707/MY_UPLOADS/aibxzxdpk6gl4u5xjgjg.jpg",
                "first_name": "Tom",
                "last_name": "Jones",
                "username": "tee-jay",
            },
        ),
        (
            HelpRequest(
                2,
                datetime(2023, 11, 12, 8, 45, 21),
                "Help required with plant care.",
                "Looking for someone to water my plants while I am away.",
                date(2023, 3, 5),
                date(2023, 3, 10),
                2,
                100.0,
            ),
            {
                "avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1709830407/PLANTS/person4_kqdufy.jpg",
                "first_name": "Jane",
                "last_name": "Smith",
                "username": "jane95",
            },
        ),
        (
            HelpRequest(
                3,
                datetime(2023, 11, 28, 14, 30, 9),
                "Need assistance with gardening.",
                "Seeking help in maintaining my garden during my absence.",
                date(2023, 4, 15),
                date(2023, 4, 20),
                3,
                90.0,
            ),
            {
                "avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1709830406/PLANTS/person2_jpuq5z.jpg",
                "first_name": "Jilly",
                "last_name": "Smith",
                "username": "sm1thi",
            },
        ),
        (
            HelpRequest(
                4,
                datetime(2023, 12, 7, 11, 20, 35),
                "Help wanted for plant care.",
                "Require someone to water my indoor plants while I am out of town.",
                date(2023, 5, 3),
                date(2023, 5, 8),
                4,
                80.0,
            ),
            {
                "avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1709830406/PLANTS/person1_jdh4xm.jpg",
                "first_name": "Barbra",
                "last_name": "Banes",
                "username": "barn-owl58",
            },
        ),
        (
            HelpRequest(
                5,
                datetime(2023, 12, 20, 9, 55, 47),
                "Assistance needed with garden maintenance.",
                "Looking for a reliable person to care for my garden while I am away.",
                date(2023, 6, 12),
                date(2023, 6, 18),
                5,
                70.0,
            ),
            {
                "avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1709830407/PLANTS/person3_itrqub.jpg",
                "first_name": "Alice",
                "last_name": "Lane",
                "username": "laney",
            },
             'https://res.cloudinary.com/dououppib/image/upload/v1709740432/PLANTS/Barberry_copy_gseiuj.png'
        ),
        (
            HelpRequest(
                6,
                datetime(2024, 1, 5, 16, 10, 2),
                "Plant watering help required.",
                "Seeking someone to water my plants regularly during my vacation.",
                date(2023, 7, 2),
                date(2023, 7, 7),
                1,
                85.0,
            ),
            {
                "avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1708633707/MY_UPLOADS/aibxzxdpk6gl4u5xjgjg.jpg",
                "first_name": "Tom",
                "last_name": "Jones",
                "username": "tee-jay",
            },
        ),
        (
            HelpRequest(
                7,
                datetime(2024, 1, 15, 13, 40, 19),
                "Gardening assistance wanted.",
                "Require help in maintaining my backyard garden for a few weeks.",
                date(2023, 8, 20),
                date(2023, 8, 25),
                2,
                95.0,
            ),
            {
                "avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1709830407/PLANTS/person4_kqdufy.jpg",
                "first_name": "Jane",
                "last_name": "Smith",
                "username": "jane95",
            },
        ),
        (
            HelpRequest(
                8,
                datetime(2024, 2, 2, 10, 5, 38),
                "Plant care help needed urgently.",
                "Looking for immediate assistance in watering my plants.",
                date(2023, 9, 10),
                date(2023, 9, 15),
                3,
                65.0,
            ),
            {
                "avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1709830406/PLANTS/person2_jpuq5z.jpg",
                "first_name": "Jilly",
                "last_name": "Smith",
                "username": "sm1thi",
            },
        ),
        (
            HelpRequest(
                9,
                datetime(2024, 2, 14, 7, 30, 55),
                "Help needed with indoor plants.",
                "Seeking someone to take care of my indoor plants for a short duration.",
                date(2023, 10, 5),
                date(2023, 10, 10),
                4,
                75.0,
            ),
            {
                "avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1709830406/PLANTS/person1_jdh4xm.jpg",
                "first_name": "Barbra",
                "last_name": "Banes",
                "username": "barn-owl58",
            },
        ),
        (
            HelpRequest(
                10,
                datetime(2024, 2, 28, 15, 20, 10),
                "Garden watering assistance required.",
                "Require help in watering my garden while I am away.",
                date(2023, 11, 22),
                date(2023, 11, 27),
                5,
                60.0,
            ),
            {
                "avatar_url_string": "https://res.cloudinary.com/dououppib/image/upload/v1709830407/PLANTS/person3_itrqub.jpg",
                "first_name": "Alice",
                "last_name": "Lane",
                "username": "laney",
            },
        ),
    ]

