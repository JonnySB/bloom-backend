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
    
    def find(self, offer_id):
        rows = self._connection.execute(
            'SELECT * from help_offers WHERE id = %s', [offer_id])
        row = rows[0]
        return HelpOffer(row["id"], row["user_id"], row["message"], row["bid"], row["status"])
    
    def create_offer(self, offer):
        self.connection.execute("INSERT INTO help_offers (user_id, message, bid, status) \
                                VALUES (%s, %s, %s, %s)",
                                [offer.user_id, offer.message, offer.bid, offer.status])
        
    def delete_offer(self, offer_id):
        self.connection.execute("DELETE FROM help_offers WHERE id = %s", [offer_id])
        return None