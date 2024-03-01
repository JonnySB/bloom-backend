from lib.repositories.plants_repository import PlantsRepository
from lib.models.plants import Plants


def test_all(db_connection):
    db_connection.seed('seeds/bloom.sql')
    repository = PlantsRepository(db_connection)
    assert repository.all() == [
        Plants(1, 'African sheepbush', 'Pentzia incana', 'plant_01.png', 2),
        Plants(2, 'Alder', 'Alnus. Black alder', 'plant_02.png', 1),
        Plants(3, 'Almond', 'Prunus dulcis', 'plant_03.png', 1)
    ]
        

def test_create(db_connection):
    db_connection.seed('seeds/bloom.sql')
    repository = PlantsRepository(db_connection)
    plant = Plants(None, 'Plant Name', 'Latin Plant Name', 'photo title', 1)
    repository.create(plant)
    assert repository.all() == [
        Plants(1, 'African sheepbush', 'Pentzia incana', 'plant_01.png', 2),
        Plants(2, 'Alder', 'Alnus. Black alder', 'plant_02.png', 1),
        Plants(3, 'Almond', 'Prunus dulcis', 'plant_03.png', 1),
        Plants(4, 'Plant Name', 'Latin Plant Name', 'photo title', 1)
    ]

def test_delete_last_one(db_connection):
    db_connection.seed('seeds/bloom.sql')
    repository = PlantsRepository(db_connection)
    repository.delete(3)
    assert repository.all() == [
        Plants(1, 'African sheepbush', 'Pentzia incana', 'plant_01.png', 2),
        Plants(2, 'Alder', 'Alnus. Black alder', 'plant_02.png', 1),
    ]

def test_delete_no_order(db_connection):
    db_connection.seed('seeds/bloom.sql')
    repository = PlantsRepository(db_connection)
    repository.delete(2)
    assert repository.all() == [
        Plants(1, 'African sheepbush', 'Pentzia incana', 'plant_01.png', 2),
        Plants(3, 'Almond', 'Prunus dulcis', 'plant_03.png', 1)
    ]


def test_find(db_connection):
    db_connection.seed('seeds/bloom.sql')
    repository = PlantsRepository(db_connection)
    plant = repository.find(2)
    assert plant == Plants(2, 'Alder', 'Alnus. Black alder', 'plant_02.png', 1)
    

def test_update(db_connection):
    db_connection.seed('seeds/bloom.sql')
    repository = PlantsRepository(db_connection)
    repository.update(1, {'common_name': 'New Name'})
    assert repository.all() == [
        Plants(2, 'Alder', 'Alnus. Black alder', 'plant_02.png', 1),
        Plants(3, 'Almond', 'Prunus dulcis', 'plant_03.png', 1),
        Plants(1, 'New Name', 'Pentzia incana', 'plant_01.png', 2)
    ]



