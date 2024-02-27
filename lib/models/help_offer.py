class HelpOffer():
    def __init__(self, id: int, user_id: int, message: str, bid: float, status: str):
        self.id = id
        self.user_id = user_id
        self.message = message
        self.bid = bid
        self.status = status

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __repr__(self):
        return f"HelpOffer({self.id}, {self.user_id}, {self.message}, {self.bid}, {self.status})"

