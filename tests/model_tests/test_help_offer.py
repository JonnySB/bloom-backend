from lib.models.help_offer import HelpOffer

"""
When initiated with user_id, message, bid, and status
Has attributes for each of those values
"""
def test_initial_attributes():
    offer = HelpOffer(1, 1, 1, 'Willing to help', 3.75, 'Pending')
    assert offer.id == 1
    assert offer.user_id == 1
    assert offer.request_id == 1
    assert offer.message == "Willing to help"
    assert offer.bid == 3.75
    assert offer.status == "Pending"

"""
When two posts with same information are created
They are equal
"""
def test_equality():
    offer_1 = HelpOffer(1, 1, 1, 'Willing to help', 3.75, 'Pending')
    offer_2 = HelpOffer(1, 1, 1, 'Willing to help', 3.75, 'Pending')
    assert offer_1 == offer_2

"""
When formatted into a string
Shows easy-to-read string
"""
def test_str_formatting():
    offer = HelpOffer(1, 1, 1, 'Willing to help', 3.75, 'Pending')
    assert str(offer) == "HelpOffer(1, 1, 1, Willing to help, 3.75, Pending)"