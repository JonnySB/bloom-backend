from datetime import datetime
from lib.models.help_request import HelpRequest


# test help request object constructs - passes
def  test_constructs_help_request_with_fields():
    help_request = HelpRequest(1, datetime(2024, 2, 1, 10, 30, 45), "Need help with gardening", "Looking for someone to help with planting flowers.", "[2024-01-01, 2024-01-31]", 1, 100)

    assert help_request.id == 1
    assert help_request.date == datetime(2024, 2, 1, 10, 30, 45)
    assert help_request.title == "Need help with gardening"
    assert help_request.message == "Looking for someone to help with planting flowers."
    assert help_request.date_range == "[2024-01-01, 2024-01-31]"
    assert help_request.user_id == 1
    assert help_request.max_price == 100

# test two help request objects are equal - passes
def test_help_requests_are_equal():
    help_request_1 = HelpRequest(1, datetime(2024, 2, 1, 10, 30, 45), "Need help with gardening", "Looking for someone to help with planting flowers.", "[2024-01-01, 2024-01-31]", 1, 100)
    help_request_2 = HelpRequest(1, datetime(2024, 2, 1, 10, 30, 45), "Need help with gardening", "Looking for someone to help with planting flowers.", "[2024-01-01, 2024-01-31]", 1, 100)

    assert help_request_1 == help_request_2

# test help request object formats nicely with the data provided - fails
def test_help_request_formats_nicely():
    help_request = HelpRequest(1, datetime(2024, 2, 1, 10, 30, 45), "Need help with gardening", "Looking for someone to help with planting flowers.", "[2024-01-01, 2024-01-31]", 1, 100)
    assert str(help_request) == "HelpRequest(1, 2024-02-01 10:30:45, Need help with gardening, Looking for someone to help with planting flowers., [2024-01-01, 2024-01-31], 1, 100)"

