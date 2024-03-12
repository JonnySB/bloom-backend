from lib.models.extended_help_offer import ExtendedHelpOffer


class ExtendedHelpOfferRepository:
    def __init__(self, connection):
        self.connection = connection

    # gets all received offers for a particular user_id
    # UNTESTED
    def get_all_received_extended_help_offers(self, user_id):
        rows = self.connection.execute(
            """
            select
                help_requests.id as help_request_id, 
                help_requests.start_date as help_request_start_date, 
                help_requests.end_date as help_request_end_date,
                help_requests.title as help_request_name,
                help_requests.user_id as help_request_user_id,
                help_offers.id as help_offer_id,
                help_offers.message as help_offer_message,
                help_offers.status as help_offer_status,
                help_offers.user_id  as help_offer_user_id,
                help_offers.bid as help_offer_bid,
                user_offer.first_name as help_offer_first_name,
                user_offer.last_name as help_offer_last_name,
                user_offer.username as help_offer_username,
                user_offer.avatar_url_string as help_offer_avatar_url_string,
                user_receive.first_name as help_receive_first_name,
                user_receive.last_name as help_receive_last_name,
                user_receive.username as help_receive_username,
                user_receive.avatar_url_string as help_receive_avatar_url_string
            from help_requests
            join help_offers on help_requests.id = help_offers.request_id
            join users user_offer on help_offers.user_id = user_offer.id
            join users user_receive on help_requests.user_id = user_receive.id
            where help_requests.user_id = %s;
            """,
            [user_id],
        )

        extended_help_offer_list = []
        for row in rows:
            extended_help_offer = ExtendedHelpOffer(
                help_request_id=row["help_request_id"],
                help_request_start_date=row["help_request_start_date"],
                help_request_end_date=row["help_request_end_date"],
                help_request_name=row["help_request_name"],
                help_request_user_id=row["help_request_user_id"],
                help_offer_id=row["help_offer_id"],
                help_offer_message=row["help_offer_message"],
                help_offer_status=row["help_offer_status"],
                help_offer_user_id=row["help_offer_user_id"],
                help_offer_bid=row["help_offer_bid"],
                help_offer_first_name=row["help_offer_first_name"],
                help_offer_last_name=row["help_offer_last_name"],
                help_offer_username=row["help_offer_username"],
                help_offer_avatar_url_string=row["help_offer_avatar_url_string"],
                help_receive_first_name=row["help_receive_first_name"],
                help_receive_last_name=row["help_receive_last_name"],
                help_receive_username=row["help_receive_username"],
                help_receive_avatar_url_string=row["help_receive_avatar_url_string"],
            )
            extended_help_offer_list.append(extended_help_offer)

        return extended_help_offer_list

    # gets all outgoing help offers for a particular user_id
    # UNTESTED
    def get_all_outgoing_extended_help_offers(self, user_id):
        rows = self.connection.execute(
            """
            select
                help_requests.id as help_request_id, 
                help_requests.start_date as help_request_start_date, 
                help_requests.end_date as help_request_end_date,
                help_requests.title as help_request_name,
                help_requests.user_id as help_request_user_id,
                help_offers.id as help_offer_id,
                help_offers.message as help_offer_message,
                help_offers.status as help_offer_status,
                help_offers.user_id  as help_offer_user_id,
                help_offers.bid as help_offer_bid,
                user_offer.first_name as help_offer_first_name,
                user_offer.last_name as help_offer_last_name,
                user_offer.username as help_offer_username,
                user_offer.avatar_url_string as help_offer_avatar_url_string,
                user_receive.first_name as help_receive_first_name,
                user_receive.last_name as help_receive_last_name,
                user_receive.username as help_receive_username,
                user_receive.avatar_url_string as help_receive_avatar_url_string
            from help_requests
            join help_offers on help_requests.id = help_offers.request_id
            join users user_offer on help_offers.user_id = user_offer.id
            join users user_receive on help_requests.user_id = user_receive.id
            where help_offers.user_id = %s;
            """,
            [user_id],
        )

        extended_help_offer_list = []
        for row in rows:
            extended_help_offer = ExtendedHelpOffer(
                help_request_id=row["help_request_id"],
                help_request_start_date=row["help_request_start_date"],
                help_request_end_date=row["help_request_end_date"],
                help_request_name=row["help_request_name"],
                help_request_user_id=row["help_request_user_id"],
                help_offer_id=row["help_offer_id"],
                help_offer_message=row["help_offer_message"],
                help_offer_status=row["help_offer_status"],
                help_offer_user_id=row["help_offer_user_id"],
                help_offer_bid=row["help_offer_bid"],
                help_offer_first_name=row["help_offer_first_name"],
                help_offer_last_name=row["help_offer_last_name"],
                help_offer_username=row["help_offer_username"],
                help_offer_avatar_url_string=row["help_offer_avatar_url_string"],
                help_receive_first_name=row["help_receive_first_name"],
                help_receive_last_name=row["help_receive_last_name"],
                help_receive_username=row["help_receive_username"],
                help_receive_avatar_url_string=row["help_receive_avatar_url_string"],
            )
            extended_help_offer_list.append(extended_help_offer)

        return extended_help_offer_list
