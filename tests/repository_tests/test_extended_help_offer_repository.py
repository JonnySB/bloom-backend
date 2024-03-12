from datetime import date

from lib.models.extended_help_offer import ExtendedHelpOffer
from lib.repositories.extended_help_offer_repository import ExtendedHelpOfferRepository


def test_get_all_received_extended_help_offers(db_connection):
    db_connection.seed("seeds/bloom.sql")
    extended_help_repo = ExtendedHelpOfferRepository(db_connection)
    help_offers = extended_help_repo.get_all_received_extended_help_offers(3)
    print(help_offers)

    assert help_offers == [
        ExtendedHelpOffer(
            8,
            date(2023, 9, 10),
            date(2023, 9, 15),
            "Plant care help needed urgently.",
            3,
            3,
            "I can provide immediate help with watering your plants.",
            "pending",
            4,
            60.0,
            "Barbra",
            "Banes",
            "barn-owl58",
            "https://res.cloudinary.com/dououppib/image/upload/v1709830406/PLANTS/person1_jdh4xm.jpg",
            "Jilly",
            "Smith",
            "sm1thi",
            "https://res.cloudinary.com/dououppib/image/upload/v1709830406/PLANTS/person2_jpuq5z.jpg",
        ),
        ExtendedHelpOffer(
            3,
            date(2023, 4, 15),
            date(2023, 4, 20),
            "Need assistance with gardening.",
            3,
            8,
            "I have gardening experience and can help with your garden.",
            "pending",
            4,
            90.0,
            "Barbra",
            "Banes",
            "barn-owl58",
            "https://res.cloudinary.com/dououppib/image/upload/v1709830406/PLANTS/person1_jdh4xm.jpg",
            "Jilly",
            "Smith",
            "sm1thi",
            "https://res.cloudinary.com/dououppib/image/upload/v1709830406/PLANTS/person2_jpuq5z.jpg",
        ),
        ExtendedHelpOffer(
            8,
            date(2023, 9, 10),
            date(2023, 9, 15),
            "Plant care help needed urgently.",
            3,
            13,
            "I am experienced in caring for indoor plants and can help.",
            "pending",
            4,
            75.0,
            "Barbra",
            "Banes",
            "barn-owl58",
            "https://res.cloudinary.com/dououppib/image/upload/v1709830406/PLANTS/person1_jdh4xm.jpg",
            "Jilly",
            "Smith",
            "sm1thi",
            "https://res.cloudinary.com/dououppib/image/upload/v1709830406/PLANTS/person2_jpuq5z.jpg",
        ),
        ExtendedHelpOffer(
            3,
            date(2023, 4, 15),
            date(2023, 4, 20),
            "Need assistance with gardening.",
            3,
            18,
            "I have gardening experience and can help with your garden.",
            "pending",
            4,
            90.0,
            "Barbra",
            "Banes",
            "barn-owl58",
            "https://res.cloudinary.com/dououppib/image/upload/v1709830406/PLANTS/person1_jdh4xm.jpg",
            "Jilly",
            "Smith",
            "sm1thi",
            "https://res.cloudinary.com/dououppib/image/upload/v1709830406/PLANTS/person2_jpuq5z.jpg",
        ),
    ]
