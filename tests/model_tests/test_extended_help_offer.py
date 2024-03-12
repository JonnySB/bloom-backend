from lib.models.extended_help_offer import ExtendedHelpOffer


def test_constructs():
    extended_help_offer = ExtendedHelpOffer(
        1,
        "2024-12-02",
        "2024-12-15",
        "help request name",
        1,
        1,
        "I can help!",
        "pending",
        2,
        50,
        "Tom",
        "Smith",
        "tsmith",
        "avatar_string_tsmith",
        "Joe",
        "Dune",
        "jdune",
        "avatar_string_jdune",
    )

    assert extended_help_offer.help_request_id == 1
    assert extended_help_offer.help_request_start_date == "2024-12-02"
    assert extended_help_offer.help_request_end_date == "2024-12-15"
    assert extended_help_offer.help_request_name == "help request name"
    assert extended_help_offer.help_request_user_id == 1
    assert extended_help_offer.help_offer_id == 1
    assert extended_help_offer.help_offer_message == "I can help!"
    assert extended_help_offer.help_offer_status == "pending"
    assert extended_help_offer.help_offer_user_id == 2
    assert extended_help_offer.help_offer_bid == 50
    assert extended_help_offer.help_offer_first_name == "Tom"
    assert extended_help_offer.help_offer_last_name == "Smith"
    assert extended_help_offer.help_offer_username == "tsmith"
    assert extended_help_offer.help_offer_avatar_url_string == "avatar_string_tsmith"
    assert extended_help_offer.help_receive_first_name == "Joe"
    assert extended_help_offer.help_receive_last_name == "Dune"
    assert extended_help_offer.help_receive_username == "jdune"
    assert extended_help_offer.help_receive_avatar_url_string == "avatar_string_jdune"


def test_equal():
    extended_help_offer1 = ExtendedHelpOffer(
        1,
        "2024-12-02",
        "2024-12-15",
        "help request name",
        1,
        1,
        "I can help!",
        "pending",
        2,
        50,
        "Tom",
        "Smith",
        "tsmith",
        "avatar_string_tsmith",
        "Joe",
        "Dune",
        "jdune",
        "avatar_string_jdune",
    )

    extended_help_offer2 = ExtendedHelpOffer(
        1,
        "2024-12-02",
        "2024-12-15",
        "help request name",
        1,
        1,
        "I can help!",
        "pending",
        2,
        50,
        "Tom",
        "Smith",
        "tsmith",
        "avatar_string_tsmith",
        "Joe",
        "Dune",
        "jdune",
        "avatar_string_jdune",
    )

    assert extended_help_offer1 == extended_help_offer2


def test_repr():
    extended_help_offer = ExtendedHelpOffer(
        1,
        "2024-12-02",
        "2024-12-15",
        "help request name",
        1,
        1,
        "I can help!",
        "pending",
        2,
        50,
        "Tom",
        "Smith",
        "tsmith",
        "avatar_string_tsmith",
        "Joe",
        "Dune",
        "jdune",
        "avatar_string_jdune",
    )

    assert (
        str(extended_help_offer)
        == "ExtendedHelpOffer: 1, 2024-12-02, 2024-12-15, help request name, 1, 1, I can help!, pending, 2, 50, Tom, Smith, tsmith, avatar_string_tsmith, Joe, Dune, jdune, avatar_string_jdune"
    )
