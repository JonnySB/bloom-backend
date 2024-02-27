class Plants:
    
    def __init__(self, id, commum_name, latin_name, photo, watering_frequency):
        self.id = id
        self.commum_name = commum_name
        self.latin_name = latin_name
        self.photo = photo
        self.watering_frequency = watering_frequency


    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __repr__(self):
        return f"Plants({self.id}, {self.commum_name}, {self.latin_name}, {self.photo}, {self.watering_frequency})"