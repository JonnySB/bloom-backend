from datetime import datetime


class HelpRequest:

    def __init__(
        self, id, date, title, messsage, start_date, end_date, user_id, maxprice
    ):
        self.id = id
        self.date = date if date else datetime.now()
        self.title = title
        self.message = messsage
        self.start_date = start_date
        self.end_date = end_date
        self.user_id = user_id
        self.maxprice = maxprice

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"HelpRequest({self.id}, {self.date}, {self.title}, {self.message}, {self.start_date}, {self.end_date}, {self.user_id}, {self.maxprice})"
