from lib.models.plants import Plants

# self, id, commum_name, latin_name, photo, watering_frequency

class PlantsRepository:

    def __init__(self, connection):
        self.connection = connection

    def create(self, plant):
        self.connection.execute('INSERT INTO plants (commum_name, latin_name, photo, watering_frequency) VALUES (%s, %s, %s, %s)', [
            plant.commun_name,
            plant.latin_name,
            plant. photo,
            plant.watering_frequency
            ])
        return None
    

    def all(self):
        rows = self._connection.execute('SELECT * from plants')
        plant_list = []
        for row in rows:
            item = Plants(row["id"], row["commum_name"], row["latin_name"], row["photo"], row["watering_frequency"])
            plant_list.append(item)
        return plant_list
    

    def delete(self, plant_id):
            self._connection.execute(
                'DELETE FROM plants WHERE id = %s', [plant_id])
            return None
    
    def find(self, plant_id):
        rows = self._connection.execute(
            'SELECT * from plants WHERE id = %s', [plant_id])
        row = rows[0]
        return Plants (row["id"], row["commum_name"], row["latin_name"], row["photo"], row["watering_frequency"])