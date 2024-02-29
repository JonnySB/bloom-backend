from lib.repositories.plants_user_repository import PlantsUserRepository
from lib.models.plants_user import PlantsUser
from lib.models.plants import Plants


# def test_find_plants_by_user_id(db_connection):
#     db_connection.seed('seeds/bloom.sql')
#     repository = PlantsUserRepository(db_connection)
#     repository.assign_plan_to_user(1, 1, 5)
    


# def test_find_plants_by_user_id_1(db_connection):
#     db_connection.seed('seeds/bloom.sql')
#     repository = PlantsUserRepository(db_connection)
#     find = repository.find_plants_by_user_id(1)
#     assert find == [{
#         'plant': Plants(1,"African sheepbush", "Pentzia incana", "plant_01.png", 2),
#         'quantity': 2
#         }]
    
# def test_find_plants_by_user_id_2(db_connection):
#     db_connection.seed('seeds/bloom.sql')
#     repository = PlantsUserRepository(db_connection)
#     find = repository.find_plants_by_user_id(2)
#     assert find == [{
#         'plant': Plants(2, 'Alder', 'Alnus. Black alder', 'plant_02.png', 1),
#         'quantity': 2
#         }]
        
