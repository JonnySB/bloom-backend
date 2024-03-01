from lib.models.plants_user import PlantsUser



def test_construction():
    plant_user = PlantsUser(1, 1, 1, 1)
    assert plant_user.id == 1
    assert plant_user.user_id == 1
    assert plant_user.plant_id == 1
    assert plant_user.quantity == 1


def test_compare():
    plant_user_1 = PlantsUser(1, 1, 1, 1)
    plant_user_2 = PlantsUser(1, 1, 1, 1)
    assert plant_user_1 == plant_user_2


def test_stringfying():
    plant_user = PlantsUser(1, 1, 1, 1)
    assert str(plant_user) == "PlantsUser(1, 1, 1, 1)"
