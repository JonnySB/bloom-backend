from lib.models.plants import Plants

# id, commum_name, latin_name, photo, watering_frequency)


def test_construction():
    plant  = Plants(1, 'Plant Name', 'Latin Plant Name', 'photo title', 'Once a day')
    assert plant.id == 1
    assert plant.commum_name == 'Plant Name'
    assert plant.latin_name == 'Latin Plant Name'
    assert plant.photo == 'photo title'
    assert plant.watering_frequency == 'Once a day'
    
    


def test_compare():
    plant_1 = Plants(1, 'Plant Name', 'Latin Plant Name', 'photo title', 'Once a day')
    plant_2 = Plants(1, 'Plant Name', 'Latin Plant Name', 'photo title', 'Once a day')
    assert plant_1 == plant_2

def test_stringfying():
    plant = Plants(1, 'Plant Name', 'Latin Plant Name', 'photo title', 'Once a day')
    assert str(plant) == 'Plants(1, Plant Name, Latin Plant Name, photo title, Once a day)'