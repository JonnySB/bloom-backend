class ExtendedHelpOffer:
    # UNTESTED
    def __init__(
        self,
        help_request_id,
        help_request_start_date,
        help_request_end_date,
        help_request_name,
        help_request_user_id,
        help_offer_id,
        help_offer_message,
        help_offer_status,
        help_offer_user_id,
        help_offer_bid,
        help_offer_first_name,
        help_offer_last_name,
        help_offer_username,
        help_offer_avatar_url_string,
        help_receive_first_name,
        help_receive_last_name,
        help_receive_username,
        help_receive_avatar_url_string,
    ):
        self.help_request_id = help_request_id
        self.help_request_start_date = help_request_start_date
        self.help_request_end_date = help_request_end_date
        self.help_request_name = help_request_name
        self.help_request_user_id = help_request_user_id
        self.help_offer_id = help_offer_id
        self.help_offer_message = help_offer_message
        self.help_offer_status = help_offer_status
        self.help_offer_user_id = help_offer_user_id
        self.help_offer_bid = help_offer_bid
        self.help_offer_first_name = help_offer_first_name
        self.help_offer_last_name = help_offer_last_name
        self.help_offer_username = help_offer_username
        self.help_offer_avatar_url_string = help_offer_avatar_url_string
        self.help_receive_first_name = help_receive_first_name
        self.help_receive_last_name = help_receive_last_name
        self.help_receive_username = help_receive_username
        self.help_receive_avatar_url_string = help_receive_avatar_url_string

    # UNTESTED
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    # UNTESTED
    def __repr__(self):
        return f"ExtendedHelpOffer: {self.help_request_id}, {self.help_request_start_date}, {self.help_request_end_date}, {self.help_request_name}, {self.help_request_user_id}, {self.help_offer_id}, {self.help_offer_message}, {self.help_offer_status}, {self.help_offer_user_id}, {self.help_offer_bid}, {self.help_offer_first_name}, {self.help_offer_last_name}, {self.help_offer_username}, {self.help_offer_avatar_url_string}, {self.help_receive_first_name}, {self.help_receive_last_name}, {self.help_receive_username}, {self.help_receive_avatar_url_string}"
