from lib.models.help_offer import HelpOffer
from lib.repositories.help_offer_repository import HelpOfferRepository


def test_create_offer_and_find_all(db_connection):
    db_connection.seed('seeds/bloom.sql')
    repo = HelpOfferRepository(db_connection)
    offer_1 = HelpOffer(None, 1, 1, 'willing to help', 3.75, 'pending')
    offer_2 = HelpOffer(None, 2, 1, 'willing to help for cheaper', 3.25, 'pending')
    repo.create_offer(offer_1)
    repo.create_offer(offer_2)
    offers = repo.all()
    assert offers == [
        HelpOffer(1, 1, 1, 'Offering help', 50.0, 'pending'),
        HelpOffer(2, 1, 1, 'willing to help', 3.75, 'pending'),
        HelpOffer(3, 2, 1, 'willing to help for cheaper', 3.25, 'pending')
    ]

def test_find_by_id(db_connection):
    db_connection.seed('seeds/bloom.sql')
    repo = HelpOfferRepository(db_connection)
    offer_1 = HelpOffer(None, 1, 1, 'willing to help', 3.75, 'pending')
    offer_2 = HelpOffer(None, 2, 1, 'willing to help for cheaper', 3.25, 'pending')
    repo.create_offer(offer_1)
    repo.create_offer(offer_2)
    offer = repo.find_offer(3)
    assert offer == HelpOffer(3, 2, 1, 'willing to help for cheaper', 3.25, 'pending')

def test_find_by_user(db_connection):
    db_connection.seed('seeds/bloom.sql')
    repo = HelpOfferRepository(db_connection)
    offer_1 = HelpOffer(None, 1, 1, 'willing to help', 3.75, 'pending')
    offer_2 = HelpOffer(None, 2, 1, 'willing to help for cheaper', 3.25, 'pending')
    repo.create_offer(offer_1)
    repo.create_offer(offer_2)
    offers_by_user = repo.find_by_user(1)
    assert offers_by_user == [
        HelpOffer(1, 1, 1, 'Offering help', 50.0, 'pending'),
        HelpOffer(2, 1, 1, 'willing to help', 3.75, 'pending'),
    ]

def test_delete_offer(db_connection):
    db_connection.seed('seeds/bloom.sql')
    repo = HelpOfferRepository(db_connection)
    offer_1 = HelpOffer(None, 1, 1, 'willing to help', 3.75, 'pending')
    offer_2 = HelpOffer(None, 2, 1, 'willing to help for cheaper', 3.25, 'pending')
    repo.create_offer(offer_1)
    repo.create_offer(offer_2)
    offers = repo.all()

    assert offers == [
        HelpOffer(1, 1, 1, 'Offering help', 50.0, 'pending'),
        HelpOffer(2, 1, 1, 'willing to help', 3.75, 'pending'),
        HelpOffer(3, 2, 1, 'willing to help for cheaper', 3.25, 'pending')
    ]

    repo.delete_offer(2)
    offers = repo.all()

    assert offers == [
        HelpOffer(1, 1, 1, 'Offering help', 50.0, 'pending'),
        HelpOffer(3, 2, 1, 'willing to help for cheaper', 3.25, 'pending')
    ]