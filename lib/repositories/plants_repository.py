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
    
    def delete_by_name(self, plant_name):
            self._connection.execute(
                'DELETE FROM plants WHERE commum_name = %s', [plant_name])
            return None
    
    def find_by_name(self, plant_name):
        rows = self._connection.execute(
            'SELECT * from plants WHERE commum_name = %s', [plant_name])
        row = rows[0]
        return Plants (row["id"], row["commum_name"], row["latin_name"], row["photo"], row["watering_frequency"])