from lib.models.plants import Plants

# id, commum_name, latin_name, photo, watering_frequency)


def test_construction():
    plant  = Plants(1, 'Plant Name', 'Latin Plant Name', 'photo title', 1)
    assert plant.id == 1
    assert plant.commum_name == 'Plant Name'
    assert plant.latin_name == 'Latin Plant Name'
    assert plant.photo == 'photo title'
    assert plant.watering_frequency == 1
    
    


def test_compare():
    plant_1 = Plants(1, 'Plant Name', 'Latin Plant Name', 'photo title', 1)
    plant_2 = Plants(1, 'Plant Name', 'Latin Plant Name', 'photo title', 1)
    assert plant_1 == plant_2

def test_stringfying():
    plant = Plants(1, 'Plant Name', 'Latin Plant Name', 'photo title', 1)
    assert str(plant) == 'Plants(1, Plant Name, Latin Plant Name, photo title, 1)'