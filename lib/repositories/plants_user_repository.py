from lib.models.plants import Plants

class PlantsUserRepository:
    def __init__(self, connection):
        self.connection = connection

    # we will be using this function to assign which user has each plants. 
    def assign_plan_to_user(self, user_id, plant_id, quantity):
        self.connection.execute('INSERT INTO user_plants (user_id, plant_id, quantity) VALUES (%s, %s, %s)', [
            user_id, plant_id , quantity
        ])
        
    # using this function we can retrive the plant's information and the user's information
    def find_plants_by_user_id(self, user_id):
        query = """SELECT p.*, up.quantity FROM plants p JOIN user_plants up ON p.id = up.plant_id WHERE up.user_id = %s"""
        rows = self.connection.execute(query, [user_id])
        plants_by_user = []
        for row in rows:
            plant_with_quantity = {
                "plant": Plants(row["id"], row["common_name"], row["latin_name"], row["photo"], row["watering_frequency"]),
                "quantity": row["quantity"]
            }
            plants_by_user.append(plant_with_quantity)
        return plants_by_user
    
    def update_plants_quantity(self, user_id, plant_id, new_quantity):
        self.connection.execute('UPDATE user_plants SET quantity = %s WHERE user_id = %s AND plant_id = %s', [new_quantity, user_id, plant_id])
        
    def delete_plants_from_user(self, user_id, plant_id):
        self.connection.execute('DELETE FROM user_plants WHERE user_id = %s AND plant_id = %s', [user_id, plant_id])
        
        
        
