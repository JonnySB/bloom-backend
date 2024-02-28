from lib.models.plants_user import PlantsUser

class PlantsUserRepository:

    def __init__(self, connection):
        self.connection = connection

    def create(self, plantUser):
        self.connection.execute('INSERT INTO user_plants (user_id, plant_id, quantity) VALUES (%s, %s, %s)', [
            plantUser.user_id,
            plantUser.plant_id,
            plantUser.quantity
            ])
        return None
    

    def all(self):
        rows = self.connection.execute('SELECT * from user_plants')
        plant_user_list = []
        for row in rows:
            item = PlantsUser(row["id"], row["user_id"], row["plant_id"], row["quantity"])
            plant_user_list.append(item)
        return plant_user_list
    
    # def find(self, id):
    #     rows = self.connection.execute(
    #         'SELECT * from plants WHERE user_id = %s', [id])
    #     row = rows[0]
    #     return PlantsUser(row["id"], row["user_id"], row["plant_id"], row["quantity"])
    
