from lib.repositories.plants_user_repository import PlantsUserRepository
from lib.models.plants_user import PlantsUser
from lib.models.plants import Plants


def test_find_plants_by_user_id_one(db_connection):
    db_connection.seed('seeds/bloom.sql')
    repository = PlantsUserRepository(db_connection)
    repository.assign_plan_to_user(3, 1, 5) ## assigning 5 plants id 1 to user id 3.
    find = repository.find_plants_by_user_id(3)
    assert find == [{
                'plant': Plants(1,"African sheepbush", "Pentzia incana", "plant_01.png", 2),
                'quantity': 5
                }]
    
def test_find_plants_by_user_id_two(db_connection):
    db_connection.seed('seeds/bloom.sql')
    repository = PlantsUserRepository(db_connection)
    repository.assign_plan_to_user(4, 1, 5) ## assigning 5 plants id 1 to user id 4.
    repository.assign_plan_to_user(4, 2, 1) ## assigning 1 plant id 2 to user id 4.
    repository.assign_plan_to_user(4, 3, 3) ## assigning 3 plants id 3 to user id 4.
    find = repository.find_plants_by_user_id(4)
    assert find == [
                {
                    'plant': Plants(1,"African sheepbush", "Pentzia incana", "plant_01.png", 2),
                    'quantity': 5
                },
                {
                    'plant': Plants(2,"Alder", "Alnus. Black alder", "plant_02.png", 1),
                    'quantity': 1
                },
                {
                    'plant': Plants(3,"Almond", "Prunus dulcis", "plant_03.png", 1),
                    'quantity': 3
                }]
    
def test_update_plant_quantity(db_connection):
    repository = PlantsUserRepository(db_connection)
    repository.assign_plan_to_user(5, 1, 5) ## assigning 5 plants id 1 to user id 5.
    repository.update_plants_quantity(5, 1, 3) #updating the new quantity to 3
    find = repository.find_plants_by_user_id(5)
    assert find == [{
                    'plant': Plants(1,"African sheepbush", "Pentzia incana", "plant_01.png", 2),
                    'quantity': 3
                }]
    
def test_delete_plant_from_user(db_connection):
    repository = PlantsUserRepository(db_connection)
    repository.assign_plan_to_user(6, 1, 1) ## assigning 1 plant id 1 to user id 6.
    repository.assign_plan_to_user(6, 2, 1) ## assigning a second plant. 1 plant id 2 to user id 6.
    repository.delete_plants_from_user(6, 1) ## delete plant 1
    find = repository.find_plants_by_user_id(6) ## return a single plant instead 2 after deleting 
    assert find == [{
                    'plant': Plants(2,"Alder", "Alnus. Black alder", "plant_02.png", 1),
                    'quantity': 1
                }]