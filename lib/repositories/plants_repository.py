from lib.models.plants import Plants


class PlantsRepository:

    def __init__(self, connection):
        self.connection = connection

    def create(self, plant):
        self.connection.execute(
            "INSERT INTO plants (common_name, latin_name, photo, watering_frequency) VALUES (%s, %s, %s, %s)",
            [
                plant.common_name,
                plant.latin_name,
                plant.photo,
                plant.watering_frequency,
            ],
        )
        return None

    def all(self):
        rows = self.connection.execute("SELECT * from plants")
        plant_list = []
        for row in rows:
            item = Plants(
                row["id"],
                row["common_name"],
                row["latin_name"],
                row["photo"],
                row["watering_frequency"],
            )
            plant_list.append(item)
        return plant_list

    def delete(self, plant_id):
        self.connection.execute("DELETE FROM user_plants WHERE plant_id = %s", [plant_id])
        self.connection.execute("DELETE FROM plants WHERE id = %s", [plant_id])
        return None

    def find(self, plant_id):
        rows = self.connection.execute("SELECT * from plants WHERE id = %s", [plant_id])
        row = rows[0]
        return Plants(
            row["id"],
            row["common_name"],
            row["latin_name"],
            row["photo"],
            row["watering_frequency"],
        )

    def update(self, plant_id, new_value):
        plant = self.find(plant_id)
        if plant is None:
            return None

        for key, value in new_value.items():
            setattr(plant, key, value)

        change = ", ".join([f"{key} = %s" for key in new_value.keys()])

        query = f"UPDATE plants SET {change} WHERE id = %s"
        values = list(new_value.values()) + [plant_id]
        self.connection.execute(query, values)

        return None
