from datetime import datetime, date
from lib.repositories.help_request_repository import HelpRequestRepository
from lib.models.help_request import HelpRequest
from lib.models.user import User

def test_can_get_all_help_requests(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = HelpRequestRepository(db_connection)

    help_requests = repository.all_requests()

    assert help_requests == [
        HelpRequest(
            1, 
            datetime(2023, 10, 19, 10, 23, 54), 
            "title_01", 
            "message requesting help", 
            date(2023, 2, 1), 
            date(2023, 3, 1), 
            1, 
            50.0
        ),
        HelpRequest(
            2, 
            datetime(2023, 10, 20, 10, 23, 54), 
            "title_02", 
            "message requesting help 2", 
            date(2023, 2, 3), 
            date(2023, 3, 3), 
            2, 
            60.0
        ),
        HelpRequest(
            3, 
            datetime(2023, 10, 19, 10, 23, 54), 
            "t_03", 
            "message requesting help 3", 
            date(2023, 2, 1), 
            date(2023, 3, 1), 
            1, 
            80.0
        )
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
        50.0
    )
    expected_user_details = {
        "first_name": "user",
        "last_name": "1",
        "username": "user1",
        "avatar_url_string": "test_image1.png"
    }


    
    assert result[0] == expected_help_request
    assert result[1] == expected_user_details
    
def test_can_find_help_requests_by_user(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = HelpRequestRepository(db_connection)
    assert repository.find_requests_by_user_id(1) == [
        HelpRequest(1, datetime(2023, 10, 19, 10, 23, 54),
            'title_01',
            'message requesting help',
            date(2023, 2, 1),
            date(2023, 3, 1),
            1,
            50.0
        ),
        HelpRequest(
            3, 
            datetime(2023, 10, 19, 10, 23, 54), 
            "t_03", 
            "message requesting help 3", 
            date(2023, 2, 1), 
            date(2023, 3, 1), 
            1, 
            80.0
        )
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
            60.0
        ))
    
    assert repository.all_requests() == [
        HelpRequest(
            1, 
            datetime(2023, 10, 19, 10, 23, 54), 
            "title_01", 
            "message requesting help", 
            date(2023, 2, 1), 
            date(2023, 3, 1), 
            1, 
            50.0
        ),
        HelpRequest(
            2, 
            datetime(2023, 10, 20, 10, 23, 54), 
            "title_02", 
            "message requesting help 2", 
            date(2023, 2, 3), 
            date(2023, 3, 3), 
            2, 
            60.0
        ),
        HelpRequest(
            3, 
            datetime(2023, 10, 19, 10, 23, 54), 
            "t_03", 
            "message requesting help 3", 
            date(2023, 2, 1), 
            date(2023, 3, 1), 
            1, 
            80.0
        ),
        HelpRequest(
            4, 
            datetime(2024, 2, 27, 14, 30, 50), 
            "new title", 
            "need help watering plant", 
            date(2024, 2, 29), 
            date(2023, 3, 7), 
            1, 
            60.0
        )
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
            60.0
        ),
        HelpRequest(
            3, 
            datetime(2023, 10, 19, 10, 23, 54), 
            "t_03", 
            "message requesting help 3", 
            date(2023, 2, 1), 
            date(2023, 3, 1), 
            1, 
            80.0
        )
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
            50.0
        ),
        HelpRequest(
            2, 
            datetime(2023, 10, 20, 10, 23, 54), 
            "title_02", 
            "message requesting help 2", 
            date(2023, 2, 3), 
            date(2023, 3, 3), 
            2, 
            60.0
        )
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
            60.0
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
        60.0
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
            50.0
        ),
        HelpRequest(
            3, 
            datetime(2023, 10, 19, 10, 23, 54), 
            "t_03", 
            "message requesting help 3", 
            date(2023, 2, 1), 
            date(2023, 3, 1), 
            1, 
            80.0
        ),
        HelpRequest(
            4, 
            datetime(2023, 10, 19, 10, 23, 54), 
            "title_04", 
            "message requesting help 4", 
            date(2023, 2, 1), 
            date(2023, 3, 1), 
            1, 
            60.0
        )
    ]

def test_get_all_help_requests_with_user_details(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = HelpRequestRepository(db_connection)

    help_requests_with_users = repository.get_all_help_requests_with_user_first_name_and_last_name()

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
                50.0
            ),
            {"first_name": "user", "last_name": "1", "username": "user1", "avatar_url_string": "test_image1.png"}  
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
                60.0
            ),
            {"first_name": "user", "last_name": "2", "username": "user2", "avatar_url_string": "test_image2.png"}  
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
                80.0
            ),
            {"first_name": "user", "last_name": "1", "username": "user1", "avatar_url_string": "test_image1.png"} 
        )
    ]