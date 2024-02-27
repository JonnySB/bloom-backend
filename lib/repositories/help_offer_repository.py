from lib.models.help_offer import HelpOffer

class HelpOfferRepository():
    def __init__(self, connection):
        self.connection = connection

    def all(self):
        rows = self.connection.execute("SELECT * FROM help_offers")
        help_offers = []
        for row in rows:
            help_offer = HelpOffer(row['id'], row['user_id'], row['message'], row['bid'], row['status'])
            help_offers.append(help_offer)
        return help_offers
    
    def create_offer(self, offer):
        self.connection.execute("INSERT INTO help_offers (user_id, message, bid, status) \
                                VALUES (%s, %s, %s, %s)",
                                [offer.user_id, offer.message, offer.bid, offer.status])