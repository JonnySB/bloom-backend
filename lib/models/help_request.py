from datetime import datetime


class HelpRequest:
    def __init__(self, id, date, title, message, start_date, end_date, user_id, maxprice, plant_photos=None):
        self.id = id
        self.date = date
        self.title = title
        self.message = message
        self.start_date = start_date
        self.end_date = end_date
        self.user_id = user_id
        self.maxprice = maxprice
        self.plant_photos = plant_photos if plant_photos is not None else []

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"HelpRequest({self.id}, {self.date}, {self.title}, {self.message}, {self.start_date}, {self.end_date}, {self.user_id}, {self.maxprice})"
