from lib.repositories.plants_repository import PlantsRepository
from lib.models.plants import Plants


def test_all(db_connection):
    repository = PlantsRepository(db_connection)
    assert repository.all() == [
        Plants('African sheepbush', 'Pentzia incana', 'plant_01.png', 2),
        Plants('Alder', 'Alnus. Black alder', 'plant_02.png', 1),
        Plants('Almond', 'Prunus dulcis', 'plant_03.png', 1)
    ]
        

