from datetime import date, datetime

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
    expected_help_request = HelpRequest(
        1,
        datetime(2023, 10, 19, 10, 23, 54),
        "title_01",
        "message requesting help",
        date(2023, 2, 1),
        date(2023, 3, 1),
        1,
        50.0,
    )
    expected_user_details = {
        "first_name": "user",
        "last_name": "1",
        "username": "user1",
        "avatar_url_string": "test_image1.png",
    }

    assert result[0] == expected_help_request
    assert result[1] == expected_user_details


def test_can_find_help_requests_by_user(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = HelpRequestRepository(db_connection)
    assert repository.find_requests_by_user_id(1) == [
        HelpRequest(
            1,
            datetime(2023, 10, 19, 10, 23, 54),
            "title_01",
            "message requesting help",
            date(2023, 2, 1),
            date(2023, 3, 1),
            1,
            50.0,
        ),
        HelpRequest(
            3,
            datetime(2023, 10, 19, 10, 23, 54),
            "t_03",
            "message requesting help 3",
            date(2023, 2, 1),
            date(2023, 3, 1),
            1,
            80.0,
        ),
    ]


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
            "title_01",
            "message requesting help",
            date(2023, 2, 1),
            date(2023, 3, 1),
            1,
            50.0,
        ),
        HelpRequest(
            2,
            datetime(2023, 10, 20, 10, 23, 54),
            "title_02",
            "message requesting help 2",
            date(2023, 2, 3),
            date(2023, 3, 3),
            2,
            60.0,
        ),
        HelpRequest(
            3,
            datetime(2023, 10, 19, 10, 23, 54),
            "t_03",
            "message requesting help 3",
            date(2023, 2, 1),
            date(2023, 3, 1),
            1,
            80.0,
        ),
        HelpRequest(
            4,
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

    repository.delete_request(1)
    assert repository.all_requests() == [
        HelpRequest(
            2,
            datetime(2023, 10, 20, 10, 23, 54),
            "title_02",
            "message requesting help 2",
            date(2023, 2, 3),
            date(2023, 3, 3),
            2,
            60.0,
        ),
        HelpRequest(
            3,
            datetime(2023, 10, 19, 10, 23, 54),
            "t_03",
            "message requesting help 3",
            date(2023, 2, 1),
            date(2023, 3, 1),
            1,
            80.0,
        ),
    ]


# def test_can_update_request_title(db_connection):
#     db_connection.seed("seeds/bloom.sql")
#     repository = HelpRequestRepository(db_connection)

#     repository.update_help_request_by_id(1, {"title" : "updated title"})
#     assert repository.all_requests() == [
#         HelpRequest(
#             1,
#             datetime(2023, 10, 19, 10, 23, 54),
#             "updated title",
#             "message requesting help",
#             date(2023, 2, 1),
#             date(2023, 3, 1),
#             1,
#             50.0
#         ),
#         HelpRequest(
#             2,
#             datetime(2023, 10, 20, 10, 23, 54),
#             "title_02",
#             "message requesting help 2",
#             date(2023, 2, 3),
#             date(2023, 3, 3),
#             2,
#             60.0
#         ),
#         HelpRequest(
#             3,
#             datetime(2023, 10, 19, 10, 23, 54),
#             "t_03",
#             "message requesting help 3",
#             date(2023, 2, 1),
#             date(2023, 3, 1),
#             1,
#             80.0
#         )
#     ]

# def test_can_update_request_start_and_end_date(db_connection):
#     db_connection.seed("seeds/bloom.sql")
#     repository = HelpRequestRepository(db_connection)

#     repository.update_help_request_by_id(1, {"start_date" : date(2024, 2, 28)})
#     repository.update_help_request_by_id(1, {"end_date" : date(2024, 3, 7)})
#     assert repository.all_requests() == [
#         HelpRequest(
#             1,
#             datetime(2023, 10, 19, 10, 23, 54),
#             "title_01",
#             "message requesting help",
#             date(2024, 2, 28),
#             date(2024, 3, 7),
#             1,
#             50.0
#         ),
#         HelpRequest(
#             2,
#             datetime(2023, 10, 20, 10, 23, 54),
#             "title_02",
#             "message requesting help 2",
#             date(2023, 2, 3),
#             date(2023, 3, 3),
#             2,
#             60.0
#         ),
#         HelpRequest(
#             3,
#             datetime(2023, 10, 19, 10, 23, 54),
#             "t_03",
#             "message requesting help 3",
#             date(2023, 2, 1),
#             date(2023, 3, 1),
#             1,
#             80.0
#         )
#     ]


def test_can_find_title_substring_from_requests(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = HelpRequestRepository(db_connection)

    assert repository.find_requests_by_title_substring("title") == [
        HelpRequest(
            1,
            datetime(2023, 10, 19, 10, 23, 54),
            "title_01",
            "message requesting help",
            date(2023, 2, 1),
            date(2023, 3, 1),
            1,
            50.0,
        ),
        HelpRequest(
            2,
            datetime(2023, 10, 20, 10, 23, 54),
            "title_02",
            "message requesting help 2",
            date(2023, 2, 3),
            date(2023, 3, 3),
            2,
            60.0,
        ),
    ]


def test_can_find_no_requests_from_given_substring(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = HelpRequestRepository(db_connection)

    assert repository.find_requests_by_title_substring("water") == []


def test_can_find_one_request_from_given_substring(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = HelpRequestRepository(db_connection)

    assert repository.find_requests_by_title_substring("02") == [
        HelpRequest(
            2,
            datetime(2023, 10, 20, 10, 23, 54),
            "title_02",
            "message requesting help 2",
            date(2023, 2, 3),
            date(2023, 3, 3),
            2,
            60.0,
        )
    ]


def test_can_find_all_help_requests_by_user_id(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = HelpRequestRepository(db_connection)

    help_request_4 = HelpRequest(
        None,
        datetime(2023, 10, 19, 10, 23, 54),
        "title_04",
        "message requesting help 4",
        date(2023, 2, 1),
        date(2023, 3, 1),
        1,
        60.0,
    )
    repository.create_request(help_request_4)
    requests_by_user = repository.find_requests_by_user_id(1)
    assert requests_by_user == [
        HelpRequest(
            1,
            datetime(2023, 10, 19, 10, 23, 54),
            "title_01",
            "message requesting help",
            date(2023, 2, 1),
            date(2023, 3, 1),
            1,
            50.0,
        ),
        HelpRequest(
            3,
            datetime(2023, 10, 19, 10, 23, 54),
            "t_03",
            "message requesting help 3",
            date(2023, 2, 1),
            date(2023, 3, 1),
            1,
            80.0,
        ),
        HelpRequest(
            4,
            datetime(2023, 10, 19, 10, 23, 54),
            "title_04",
            "message requesting help 4",
            date(2023, 2, 1),
            date(2023, 3, 1),
            1,
            60.0,
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
                "title_01",
                "message requesting help",
                date(2023, 2, 1),
                date(2023, 3, 1),
                1,
                50.0,
            ),
            {
                "first_name": "user",
                "last_name": "1",
                "username": "user1",
                "avatar_url_string": "test_image1.png",
            },
        ),
        (
            HelpRequest(
                2,
                datetime(2023, 10, 20, 10, 23, 54),
                "title_02",
                "message requesting help 2",
                date(2023, 2, 3),
                date(2023, 3, 3),
                2,
                60.0,
            ),
            {
                "first_name": "user",
                "last_name": "2",
                "username": "user2",
                "avatar_url_string": "test_image2.png",
            },
        ),
        (
            HelpRequest(
                3,
                datetime(2023, 10, 19, 10, 23, 54),
                "t_03",
                "message requesting help 3",
                date(2023, 2, 1),
                date(2023, 3, 1),
                1,
                80.0,
            ),
            {
                "first_name": "user",
                "last_name": "1",
                "username": "user1",
                "avatar_url_string": "test_image1.png",
            },
        ),
    ]

