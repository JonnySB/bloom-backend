from lib.models.received_offer import ReceivedOffer


class ReceivedOffersRepository:
    def __init__(self, connection):
        self.connection = connection

    # gets all received offers for a particular user_id
    # UNTESTED
    def get_all_received_offers_for_user(self, user_id):
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
                users.first_name as help_offer_first_name,
                users.last_name as help_offer_last_name,
                users.username as help_offer_username,
                users.avatar_url_string as help_offer_avatar_url_string
            from help_requests
            join help_offers on help_requests.id = help_offers.request_id
            join users on help_offers.user_id = users.id
            where help_requests.user_id = %s;
            """,
            [user_id],
        )

        received_offers = []
        for row in rows:
            received_offer = ReceivedOffer(
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
            )
            received_offers.append(received_offer)

        return received_offers
