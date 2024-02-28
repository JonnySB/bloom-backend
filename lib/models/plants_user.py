class PlantsUser:


    def __init__(self, id, user_id, plant_id, quantity):
        self.id = id
        self.user_id = user_id
        self.plant_id = plant_id
        self.quantity = quantity


    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __repr__(self):
        return f"PlantsUser({self.id}, {self.user_id}, {self.plant_id}, {self.quantity})"