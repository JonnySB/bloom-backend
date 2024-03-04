from lib.models.help_offer import HelpOffer

class HelpOfferRepository():
    def __init__(self, connection):
        self.connection = connection

    # returns all help offers from DB in an array.
    def all(self):
        rows = self.connection.execute("SELECT * FROM help_offers")
        help_offers = []
        for row in rows:
            help_offer = HelpOffer(row['id'], row['user_id'], row['request_id'], row['message'], row['bid'], row['status'])
            help_offers.append(help_offer)
        return help_offers
    
    # returns help offer matching offer_id from DB.
    def find_offer(self, offer_id):
        rows = self.connection.execute(
            'SELECT * from help_offers WHERE id = %s', [offer_id])
        row = rows[0]
        return HelpOffer(row["id"], row["user_id"], row["request_id"], row["message"], row["bid"], row["status"])
    
    # returns help offers made by a user matching user_id from DB.
    def find_by_user(self, user_id):
        rows = self.connection.execute("SELECT * FROM help_offers WHERE user_id = %s", [user_id])
        offers_by_user = []
        for row in rows:
            help_offer = HelpOffer(row['id'], row['user_id'], row["request_id"], row['message'], row['bid'], row['status'])
            offers_by_user.append(help_offer)
        return offers_by_user
    
    # returns help offers matching request_id from DB.
    def find_by_request_id(self, request_id):
        rows = self.connection.execute("SELECT * FROM help_offers WHERE request_id = %s", [request_id])
        offers_for_request = []
        for row in rows:
            help_offer = HelpOffer(row['id'], row['user_id'], row["request_id"], row['message'], row['bid'], row['status'])
            offers_for_request.append(help_offer)
        return offers_for_request

    
    # inserts offer into help_offers table in DB.
    def create_offer(self, offer):
        self.connection.execute("INSERT INTO help_offers (user_id, request_id, message, bid, status) \
                                VALUES (%s, %s, %s, %s, %s)",
                                [offer.user_id, offer.request_id, offer.message, offer.bid, offer.status])
        
    # deletes offer matching offer_id from DB.
    def delete_offer(self, offer_id):
        self.connection.execute("DELETE FROM help_offers WHERE id = %s", [offer_id])
        return None


