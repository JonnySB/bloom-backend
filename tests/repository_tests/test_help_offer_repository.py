from lib.models.help_offer import HelpOffer
from lib.repositories.help_offer_repository import HelpOfferRepository


def test_create_offer_and_find_all(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repo = HelpOfferRepository(db_connection)
    offer_1 = HelpOffer(None, 1, 1, "willing to help", 3.75, "pending")
    offer_2 = HelpOffer(None, 2, 1, "willing to help for cheaper", 3.25, "pending")
    repo.create_offer(offer_1)
    repo.create_offer(offer_2)
    offers = repo.all()
    assert offers == [
        HelpOffer(
            1,
            2,
            6,
            "I can water your plants regularly during your vacation.",
            70.0,
            "pending",
        ),
        HelpOffer(
            2,
            3,
            7,
            "I am available to assist with your gardening needs.",
            85.0,
            "pending",
        ),
        HelpOffer(
            3,
            4,
            8,
            "I can provide immediate help with watering your plants.",
            60.0,
            "pending",
        ),
        HelpOffer(
            4,
            5,
            9,
            "I am experienced in caring for indoor plants and can help.",
            75.0,
            "pending",
        ),
        HelpOffer(
            5, 1, 10, "I can assist you with watering your garden.", 65.0, "pending"
        ),
        HelpOffer(
            6,
            2,
            1,
            "I am available to help with your garden maintenance.",
            80.0,
            "pending",
        ),
        HelpOffer(
            7,
            3,
            2,
            "I can provide assistance in caring for your indoor plants.",
            55.0,
            "pending",
        ),
        HelpOffer(
            8,
            4,
            3,
            "I have gardening experience and can help with your garden.",
            90.0,
            "pending",
        ),
        HelpOffer(
            9,
            5,
            4,
            "I am willing to assist with your gardening needs.",
            75.0,
            "pending",
        ),
        HelpOffer(
            10,
            1,
            5,
            "I can take care of your plants while you are on holiday.",
            70.0,
            "pending",
        ),
        HelpOffer(
            11,
            2,
            6,
            "I am available to assist with your gardening needs.",
            85.0,
            "pending",
        ),
        HelpOffer(
            12,
            3,
            7,
            "I can water your plants regularly during your vacation.",
            70.0,
            "pending",
        ),
        HelpOffer(
            13,
            4,
            8,
            "I am experienced in caring for indoor plants and can help.",
            75.0,
            "pending",
        ),
        HelpOffer(
            14, 5, 9, "I can assist you with watering your garden.", 65.0, "pending"
        ),
        HelpOffer(
            15,
            1,
            10,
            "I am available to help with your garden maintenance.",
            80.0,
            "pending",
        ),
        HelpOffer(
            16,
            2,
            1,
            "I can provide immediate help with watering your plants.",
            60.0,
            "pending",
        ),
        HelpOffer(
            17,
            3,
            2,
            "I am willing to assist with your gardening needs.",
            75.0,
            "pending",
        ),
        HelpOffer(
            18,
            4,
            3,
            "I have gardening experience and can help with your garden.",
            90.0,
            "pending",
        ),
        HelpOffer(
            19,
            5,
            4,
            "I can take care of your plants while you are on holiday.",
            70.0,
            "pending",
        ),
        HelpOffer(
            20,
            1,
            5,
            "I am available to assist with your gardening needs.",
            85.0,
            "pending",
        ),
        HelpOffer(21, 1, 1, "willing to help", 3.75, "pending"),
        HelpOffer(22, 2, 1, "willing to help for cheaper", 3.25, "pending"),
    ]


def test_find_by_id(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repo = HelpOfferRepository(db_connection)
    offer_1 = HelpOffer(None, 1, 1, "willing to help", 3.75, "pending")
    offer_2 = HelpOffer(None, 2, 1, "willing to help for cheaper", 3.25, "pending")
    repo.create_offer(offer_1)
    repo.create_offer(offer_2)
    offer = repo.find_offer(22)
    assert offer == HelpOffer(22, 2, 1, "willing to help for cheaper", 3.25, "pending")


def test_find_by_user(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repo = HelpOfferRepository(db_connection)
    offer_1 = HelpOffer(None, 1, 1, "willing to help", 3.75, "pending")
    offer_2 = HelpOffer(None, 2, 1, "willing to help for cheaper", 3.25, "pending")
    repo.create_offer(offer_1)
    repo.create_offer(offer_2)
    offers_by_user = repo.find_by_user(1)
    assert offers_by_user == [
        HelpOffer(
            5, 1, 10, "I can assist you with watering your garden.", 65.0, "pending"
        ),
        HelpOffer(
            10,
            1,
            5,
            "I can take care of your plants while you are on holiday.",
            70.0,
            "pending",
        ),
        HelpOffer(
            15,
            1,
            10,
            "I am available to help with your garden maintenance.",
            80.0,
            "pending",
        ),
        HelpOffer(
            20,
            1,
            5,
            "I am available to assist with your gardening needs.",
            85.0,
            "pending",
        ),
        HelpOffer(21, 1, 1, "willing to help", 3.75, "pending"),
    ]


def test_find_by_request_id(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repo = HelpOfferRepository(db_connection)
    offer_1 = HelpOffer(None, 1, 1, "willing to help", 3.75, "pending")
    offer_2 = HelpOffer(None, 2, 2, "willing to help for cheaper", 3.25, "pending")
    repo.create_offer(offer_1)
    repo.create_offer(offer_2)
    offers_for_request = repo.find_by_request_id(2)
    assert offers_for_request == [
        HelpOffer(
            7,
            3,
            2,
            "I can provide assistance in caring for your indoor plants.",
            55.0,
            "pending",
        ),
        HelpOffer(
            17,
            3,
            2,
            "I am willing to assist with your gardening needs.",
            75.0,
            "pending",
        ),
        HelpOffer(22, 2, 2, "willing to help for cheaper", 3.25, "pending"),
    ]


def test_delete_offer(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repo = HelpOfferRepository(db_connection)
    offer_1 = HelpOffer(None, 1, 1, "willing to help", 3.75, "pending")
    offer_2 = HelpOffer(None, 2, 1, "willing to help for cheaper", 3.25, "pending")
    repo.create_offer(offer_1)
    repo.create_offer(offer_2)
    offers = repo.all()

    assert offers == [
        HelpOffer(
            1,
            2,
            6,
            "I can water your plants regularly during your vacation.",
            70.0,
            "pending",
        ),
        HelpOffer(
            2,
            3,
            7,
            "I am available to assist with your gardening needs.",
            85.0,
            "pending",
        ),
        HelpOffer(
            3,
            4,
            8,
            "I can provide immediate help with watering your plants.",
            60.0,
            "pending",
        ),
        HelpOffer(
            4,
            5,
            9,
            "I am experienced in caring for indoor plants and can help.",
            75.0,
            "pending",
        ),
        HelpOffer(
            5, 1, 10, "I can assist you with watering your garden.", 65.0, "pending"
        ),
        HelpOffer(
            6,
            2,
            1,
            "I am available to help with your garden maintenance.",
            80.0,
            "pending",
        ),
        HelpOffer(
            7,
            3,
            2,
            "I can provide assistance in caring for your indoor plants.",
            55.0,
            "pending",
        ),
        HelpOffer(
            8,
            4,
            3,
            "I have gardening experience and can help with your garden.",
            90.0,
            "pending",
        ),
        HelpOffer(
            9,
            5,
            4,
            "I am willing to assist with your gardening needs.",
            75.0,
            "pending",
        ),
        HelpOffer(
            10,
            1,
            5,
            "I can take care of your plants while you are on holiday.",
            70.0,
            "pending",
        ),
        HelpOffer(
            11,
            2,
            6,
            "I am available to assist with your gardening needs.",
            85.0,
            "pending",
        ),
        HelpOffer(
            12,
            3,
            7,
            "I can water your plants regularly during your vacation.",
            70.0,
            "pending",
        ),
        HelpOffer(
            13,
            4,
            8,
            "I am experienced in caring for indoor plants and can help.",
            75.0,
            "pending",
        ),
        HelpOffer(
            14, 5, 9, "I can assist you with watering your garden.", 65.0, "pending"
        ),
        HelpOffer(
            15,
            1,
            10,
            "I am available to help with your garden maintenance.",
            80.0,
            "pending",
        ),
        HelpOffer(
            16,
            2,
            1,
            "I can provide immediate help with watering your plants.",
            60.0,
            "pending",
        ),
        HelpOffer(
            17,
            3,
            2,
            "I am willing to assist with your gardening needs.",
            75.0,
            "pending",
        ),
        HelpOffer(
            18,
            4,
            3,
            "I have gardening experience and can help with your garden.",
            90.0,
            "pending",
        ),
        HelpOffer(
            19,
            5,
            4,
            "I can take care of your plants while you are on holiday.",
            70.0,
            "pending",
        ),
        HelpOffer(
            20,
            1,
            5,
            "I am available to assist with your gardening needs.",
            85.0,
            "pending",
        ),
        HelpOffer(21, 1, 1, "willing to help", 3.75, "pending"),
        HelpOffer(22, 2, 1, "willing to help for cheaper", 3.25, "pending"),
    ]

    repo.delete_offer(2)
    offers = repo.all()

    assert offers == [
        HelpOffer(
            1,
            2,
            6,
            "I can water your plants regularly during your vacation.",
            70.0,
            "pending",
        ),
        HelpOffer(
            3,
            4,
            8,
            "I can provide immediate help with watering your plants.",
            60.0,
            "pending",
        ),
        HelpOffer(
            4,
            5,
            9,
            "I am experienced in caring for indoor plants and can help.",
            75.0,
            "pending",
        ),
        HelpOffer(
            5, 1, 10, "I can assist you with watering your garden.", 65.0, "pending"
        ),
        HelpOffer(
            6,
            2,
            1,
            "I am available to help with your garden maintenance.",
            80.0,
            "pending",
        ),
        HelpOffer(
            7,
            3,
            2,
            "I can provide assistance in caring for your indoor plants.",
            55.0,
            "pending",
        ),
        HelpOffer(
            8,
            4,
            3,
            "I have gardening experience and can help with your garden.",
            90.0,
            "pending",
        ),
        HelpOffer(
            9,
            5,
            4,
            "I am willing to assist with your gardening needs.",
            75.0,
            "pending",
        ),
        HelpOffer(
            10,
            1,
            5,
            "I can take care of your plants while you are on holiday.",
            70.0,
            "pending",
        ),
        HelpOffer(
            11,
            2,
            6,
            "I am available to assist with your gardening needs.",
            85.0,
            "pending",
        ),
        HelpOffer(
            12,
            3,
            7,
            "I can water your plants regularly during your vacation.",
            70.0,
            "pending",
        ),
        HelpOffer(
            13,
            4,
            8,
            "I am experienced in caring for indoor plants and can help.",
            75.0,
            "pending",
        ),
        HelpOffer(
            14, 5, 9, "I can assist you with watering your garden.", 65.0, "pending"
        ),
        HelpOffer(
            15,
            1,
            10,
            "I am available to help with your garden maintenance.",
            80.0,
            "pending",
        ),
        HelpOffer(
            16,
            2,
            1,
            "I can provide immediate help with watering your plants.",
            60.0,
            "pending",
        ),
        HelpOffer(
            17,
            3,
            2,
            "I am willing to assist with your gardening needs.",
            75.0,
            "pending",
        ),
        HelpOffer(
            18,
            4,
            3,
            "I have gardening experience and can help with your garden.",
            90.0,
            "pending",
        ),
        HelpOffer(
            19,
            5,
            4,
            "I can take care of your plants while you are on holiday.",
            70.0,
            "pending",
        ),
        HelpOffer(
            20,
            1,
            5,
            "I am available to assist with your gardening needs.",
            85.0,
            "pending",
        ),
        HelpOffer(21, 1, 1, "willing to help", 3.75, "pending"),
        HelpOffer(22, 2, 1, "willing to help for cheaper", 3.25, "pending"),
    ]


def test_get_associated_help_offer_ids(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repo = HelpOfferRepository(db_connection)
    associated_ids = repo.get_other_help_offer_ids_associated_with_request_id(2)

    assert associated_ids == [2, 12]


def test_accept_help_offer(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repo = HelpOfferRepository(db_connection)
    help_offer_before = repo.find_offer(2)

    assert help_offer_before == HelpOffer(
        2, 3, 7, "I am available to assist with your gardening needs.", 85.0, "pending"
    )

    repo.accept_help_offer(2)
    help_offer_after = repo.find_offer(2)

    assert help_offer_after == HelpOffer(
        2, 3, 7, "I am available to assist with your gardening needs.", 85.0, "accepted"
    )


def test_reject_help_offer(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repo = HelpOfferRepository(db_connection)
    help_offer_before = repo.find_offer(2)

    assert help_offer_before == HelpOffer(
        2, 3, 7, "I am available to assist with your gardening needs.", 85.0, "pending"
    )

    repo.reject_help_offer(2)
    help_offer_after = repo.find_offer(2)

    assert help_offer_after == HelpOffer(
        2, 3, 7, "I am available to assist with your gardening needs.", 85.0, "rejected"
    )


def test_rescind_help_offer(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repo = HelpOfferRepository(db_connection)
    help_offer_before = repo.find_offer(2)

    assert help_offer_before == HelpOffer(
        2, 3, 7, "I am available to assist with your gardening needs.", 85.0, "pending"
    )

    repo.rescind_help_offer(2)
    help_offer_after = repo.find_offer(2)

    assert help_offer_after == HelpOffer(
        2,
        3,
        7,
        "I am available to assist with your gardening needs.",
        85.0,
        "rescinded",
    )
