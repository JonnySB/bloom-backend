import datetime
from lib.repositories.help_request_repository import HelpRequestRepository
from lib.models.help_request import HelpRequest


def test_can_get_all_help_requests(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = HelpRequestRepository(db_connection)

    help_requests = repository.all_requests()
    
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
            )]
    
