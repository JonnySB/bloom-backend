class HelpRequest:
    
    '''
        id, 
        date, 
        title, 
        message, 
        daterange, 
pc->    user_id, 
        maxprice
    '''
    def __init__(self, id, date, title, messsage, date_range, user_id, max_price):
        self.id = id
        self.date = date
        self.title = title
        self.message = messsage
        self.date_range = date_range
        self.user_id = user_id
        self.max_price = max_price

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __repr__(self):
        return f"HelpRequest({self.id}, {self.date}, {self.title}, {self.message}, {self.date_range}, {self.user_id}, {self.max_price})"