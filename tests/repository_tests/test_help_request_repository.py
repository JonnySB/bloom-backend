import datetime
from lib.repositories.help_request_repository import HelpRequestRepository
from lib.models.help_request import HelpRequest


def test_can_get_all_help_requests(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = HelpRequestRepository(db_connection)

    help_requests = repository.all_requests()
    # ('2023-10-20 10:23:54', 'title_02', 'message requesting help 2', '2023-02-03', '2023-03-03', 2, 60);
    assert help_requests == [
        HelpRequest(
            1, 
            datetime.datetime(2023, 10, 19, 10, 23, 54), 
            "title_01", 
            "message requesting help", 
            datetime.date(2023, 2, 1), 
            datetime.date(2023, 3, 1), 
            1, 
            50.0
        ),
        HelpRequest(
            2, 
            datetime.datetime(2023, 10, 20, 10, 23, 54), 
            "title_02", 
            "message requesting help 2", 
            datetime.date(2023, 2, 3), 
            datetime.date(2023, 3, 3), 
            2, 
            60.0
        )
    ]

def test_can_find_help_request_by_id(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = HelpRequestRepository(db_connection)

    assert repository.find_request_by_id(1) == HelpRequest(
            1, 
            datetime.datetime(2023, 10, 19, 10, 23, 54), 
            "title_01", 
            "message requesting help", 
            datetime.date(2023, 2, 1), 
            datetime.date(2023, 3, 1), 
            1, 
            50.0
        )
    
def test_create_new_help_request_with_fields(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = HelpRequestRepository(db_connection)

    repository.create_request(
        HelpRequest(
            None, 
            datetime.datetime(2024, 2, 27, 14, 30, 50), 
            "new title", 
            "need help watering plant", 
            datetime.date(2024, 2, 29), 
            datetime.date(2023, 3, 7), 
            1, 
            60.0
        ))
    
    assert repository.all_requests() == [
        HelpRequest(
            1, 
            datetime.datetime(2023, 10, 19, 10, 23, 54), 
            "title_01", 
            "message requesting help", 
            datetime.date(2023, 2, 1), 
            datetime.date(2023, 3, 1), 
            1, 
            50.0
        ),
        HelpRequest(
            2, 
            datetime.datetime(2023, 10, 20, 10, 23, 54), 
            "title_02", 
            "message requesting help 2", 
            datetime.date(2023, 2, 3), 
            datetime.date(2023, 3, 3), 
            2, 
            60.0
        ),
        HelpRequest(
            3, 
            datetime.datetime(2024, 2, 27, 14, 30, 50), 
            "new title", 
            "need help watering plant", 
            datetime.date(2024, 2, 29), 
            datetime.date(2023, 3, 7), 
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
            datetime.datetime(2023, 10, 20, 10, 23, 54), 
            "title_02", 
            "message requesting help 2", 
            datetime.date(2023, 2, 3), 
            datetime.date(2023, 3, 3), 
            2, 
            60.0
        )
    ]

def test_can_update_request_title(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = HelpRequestRepository(db_connection)

    repository.update_help_request_by_id(1, {"title" : "updated title"})
    assert repository.all_requests() == [
        HelpRequest(
            1, 
            datetime.datetime(2023, 10, 19, 10, 23, 54), 
            "updated title", 
            "message requesting help", 
            datetime.date(2023, 2, 1), 
            datetime.date(2023, 3, 1), 
            1, 
            50.0
        ),
        HelpRequest(
            2, 
            datetime.datetime(2023, 10, 20, 10, 23, 54), 
            "title_02", 
            "message requesting help 2", 
            datetime.date(2023, 2, 3), 
            datetime.date(2023, 3, 3), 
            2, 
            60.0
        )
    ]

def test_can_update_request_maxprice(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = HelpRequestRepository(db_connection)

    repository.update_help_request_by_id(2, {"maxprice" : 70})
    assert repository.all_requests() == [
        HelpRequest(
            1, 
            datetime.datetime(2023, 10, 19, 10, 23, 54), 
            "title_01", 
            "message requesting help", 
            datetime.date(2023, 2, 1), 
            datetime.date(2023, 3, 1), 
            1, 
            50.0
        ),
        HelpRequest(
            2, 
            datetime.datetime(2023, 10, 20, 10, 23, 54), 
            "title_02", 
            "message requesting help 2", 
            datetime.date(2023, 2, 3), 
            datetime.date(2023, 3, 3), 
            2, 
            70.0
        )
    ]

def test_can_update_request_start_date(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = HelpRequestRepository(db_connection)

    repository.update_help_request_by_id(1, {"start_date" : datetime.date(2024, 2, 28)})
    assert repository.all_requests() == [
        HelpRequest(
            1, 
            datetime.datetime(2023, 10, 19, 10, 23, 54), 
            "title_01", 
            "message requesting help", 
            datetime.date(2024, 2, 28), 
            datetime.date(2023, 3, 1), 
            1, 
            50.0
        ),
        HelpRequest(
            2, 
            datetime.datetime(2023, 10, 20, 10, 23, 54), 
            "title_02", 
            "message requesting help 2", 
            datetime.date(2023, 2, 3), 
            datetime.date(2023, 3, 3), 
            2, 
            60.0
        )
    ]

def test_can_update_request_start_and_end_date(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = HelpRequestRepository(db_connection)

    repository.update_help_request_by_id(1, {"start_date" : datetime.date(2024, 2, 28)})
    repository.update_help_request_by_id(1, {"end_date" : datetime.date(2024, 3, 7)})
    assert repository.all_requests() == [
        HelpRequest(
            1, 
            datetime.datetime(2023, 10, 19, 10, 23, 54), 
            "title_01", 
            "message requesting help", 
            datetime.date(2024, 2, 28), 
            datetime.date(2024, 3, 7), 
            1, 
            50.0
        ),
        HelpRequest(
            2, 
            datetime.datetime(2023, 10, 20, 10, 23, 54), 
            "title_02", 
            "message requesting help 2", 
            datetime.date(2023, 2, 3), 
            datetime.date(2023, 3, 3), 
            2, 
            60.0
        )
    ]

def test_can_find_title_substring_from_requests(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = HelpRequestRepository(db_connection)

    assert repository.find_requests_by_title_substring("title") == [
        HelpRequest(
            1, 
            datetime.datetime(2023, 10, 19, 10, 23, 54), 
            "title_01", 
            "message requesting help", 
            datetime.date(2023, 2, 1), 
            datetime.date(2023, 3, 1), 
            1, 
            50.0
        ),
        HelpRequest(
            2, 
            datetime.datetime(2023, 10, 20, 10, 23, 54), 
            "title_02", 
            "message requesting help 2", 
            datetime.date(2023, 2, 3), 
            datetime.date(2023, 3, 3), 
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
            datetime.datetime(2023, 10, 20, 10, 23, 54), 
            "title_02", 
            "message requesting help 2", 
            datetime.date(2023, 2, 3), 
            datetime.date(2023, 3, 3), 
            2, 
            60.0
        )
    ]

def test_can_find_all_help_requests_by_user_id(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = HelpRequestRepository(db_connection)

    help_request_3 = HelpRequest(
        None, 
        datetime.datetime(2023, 10, 19, 10, 23, 54), 
        "title_03", 
        "message requesting help 3", 
        datetime.date(2023, 2, 1), 
        datetime.date(2023, 3, 1), 
        1, 
        60.0
    )
    help_request_4 = HelpRequest(
        None, 
        datetime.datetime(2023, 10, 19, 10, 23, 54), 
        "title_04", 
        "message requesting help 4", 
        datetime.date(2023, 2, 1), 
        datetime.date(2023, 3, 1), 
        1, 
        70.0
    )
    repository.create_request(help_request_3)
    repository.create_request(help_request_4)
    requests_by_user = repository.find_requests_by_user(1)
    assert requests_by_user == [
        HelpRequest(
            1, 
            datetime.datetime(2023, 10, 19, 10, 23, 54), 
            "title_01", 
            "message requesting help", 
            datetime.date(2023, 2, 1), 
            datetime.date(2023, 3, 1), 
            1, 
            50.0
        ),
        HelpRequest(
            3, 
            datetime.datetime(2023, 10, 19, 10, 23, 54), 
            "title_03", 
            "message requesting help 3", 
            datetime.date(2023, 2, 1), 
            datetime.date(2023, 3, 1), 
            1, 
            60.0
        ),
        HelpRequest(
            4, 
            datetime.datetime(2023, 10, 19, 10, 23, 54), 
            "title_04", 
            "message requesting help 4", 
            datetime.date(2023, 2, 1), 
            datetime.date(2023, 3, 1), 
            1, 
            70.0
        )
    ]
