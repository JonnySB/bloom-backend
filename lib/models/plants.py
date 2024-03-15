class Plants:

    def __init__(self, id, plant_id, common_name, latin_name, photo, watering_frequency):
        self.id = id
        self.plant_id = plant_id
        self.common_name = common_name
        self.latin_name = latin_name
        self.photo = photo
        self.watering_frequency = watering_frequency

    def __eq__(self, other):
        if not isinstance(other, Plants):
            return False
        return (
            self.id == other.id
            and self.plant_id == other.plant_id
            and self.common_name == other.common_name
            and self.latin_name == other.latin_name
            and self.photo == other.photo
            and self.watering_frequency == other.watering_frequency
        )

    def __repr__(self):
        return f"Plants({self.id}, {self.plant_id}, {self.common_name}, {self.latin_name}, {self.photo}, {self.watering_frequency})"
