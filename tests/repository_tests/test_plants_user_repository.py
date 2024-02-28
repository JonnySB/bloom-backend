from lib.repositories.plants_user_repository import PlantsUserRepository
from lib.models.plants_user import PlantsUser


def test_all(db_connection):
    db_connection.seed('seeds/bloom.sql')
    repository = PlantsUserRepository(db_connection)
    assert repository.all() == [
        PlantsUser(1, 1, 1, 3)
    ]



# def test_create(db_connection):
#     db_connection.seed('seeds/bloom.sql')
#     repository = PlantsUserRepository(db_connection)
#     plant_user = PlantsUser(None, 1, 2, 2)
#     repository.create(plant_user)
#     assert repository.all() == [
#         PlantsUser(1, 1, 1, 3),
#         PlantsUser(2, 1, 2, 2)
#     ]