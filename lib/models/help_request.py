class HelpRequest:
    
    def __init__(self, id, user_id, timestamp, title, messsage, plant, date_range, max_price):
        self.id = id
        self.user_id = user_id
        self.timestamp = timestamp
        self.title = title
        self.message = messsage
        self.plant = plant
        self.date_range = date_range
        self.max_price = max_price

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __repr__(self):
        return f"HelpRequest({self.id}, {self.user_id}, {self.timestamp}, {self.title}, {self.message}, {self.plant}, {self.date_range}, {self.max_price})"