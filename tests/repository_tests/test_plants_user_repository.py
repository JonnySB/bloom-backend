from lib.models.plants import Plants
from lib.models.plants_user import PlantsUser
from lib.repositories.plants_user_repository import PlantsUserRepository


def test_find_plants_by_user_id_one(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = PlantsUserRepository(db_connection)
    repository.assign_plant_to_user(3, 1, 5)  ## assigning 5 plants id 1 to user id 3.
    find = repository.find_plants_by_user_id(3)
    assert find == [
        {
            "plant": Plants(
                1,
                1,
                "African sheepbush",
                "Pentzia incana",
                "https://res.cloudinary.com/dououppib/image/upload/v1709740425/PLANTS/African_sheepbush_lyorlf.jpg",
                2,
            ),
            "quantity": 5,
        },
        {
            "plant": Plants(
                2,
                2,
                "Alder",
                "Alnus. Black alder",
                "https://res.cloudinary.com/dououppib/image/upload/v1709740428/PLANTS/Alder_jc4szc.jpg",
                1,
            ),
            "quantity": 3,
        },
        {
            "plant": Plants(
                5,
                5,
                "Barberry",
                "Berberis",
                "https://res.cloudinary.com/dououppib/image/upload/v1709740432/PLANTS/Barberry_copy_gseiuj.png",
                1,
            ),
            "quantity": 2,
        },
    ]


def test_find_plants_by_user_id_two(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = PlantsUserRepository(db_connection)
    repository.assign_plant_to_user(4, 1, 5)  ## assigning 5 plants id 1 to user id 4.
    repository.assign_plant_to_user(4, 3, 3)  ## assigning 3 plants id 3 to user id 4.
    find = repository.find_plants_by_user_id(4)
    assert find == [
        {
            "plant": Plants(
                1,
                1,
                "African sheepbush",
                "Pentzia incana",
                "https://res.cloudinary.com/dououppib/image/upload/v1709740425/PLANTS/African_sheepbush_lyorlf.jpg",
                2,
            ),
            "quantity": 5,
        },
        {
            "plant": Plants(
                2,
                2,
                "Alder",
                "Alnus. Black alder",
                "https://res.cloudinary.com/dououppib/image/upload/v1709740428/PLANTS/Alder_jc4szc.jpg",
                1,
            ),
            "quantity": 5,
        },
        {
            "plant": Plants(
                3,
                3,
                "Almond",
                "Prunus dulcis",
                "https://res.cloudinary.com/dououppib/image/upload/v1709740430/PLANTS/Almond_aikcyc.jpg",
                1,
            ),
            "quantity": 3,
        },
    ]


def test_update_plant_quantity(db_connection):
    repository = PlantsUserRepository(db_connection)
    repository.assign_plant_to_user(5, 1, 5)  ## assigning 5 plants id 1 to user id 5.
    repository.update_plants_quantity(5, 1, 3)  # updating the new quantity to 3
    find = repository.find_plants_by_user_id(5)
    assert find == [
        {
            "plant": Plants(
                1,
                1,
                "African sheepbush",
                "Pentzia incana",
                "https://res.cloudinary.com/dououppib/image/upload/v1709740425/PLANTS/African_sheepbush_lyorlf.jpg",
                2,
            ),
            "quantity": 3,
        },
        {
            "plant": Plants(
                4,
                4,
                "Bamboo",
                "Fargesia",
                "https://res.cloudinary.com/dououppib/image/upload/v1709740434/PLANTS/Bamboo_bkwm52.jpg",
                1,
            ),
            "quantity": 10,
        },
        {
            "plant": Plants(
                5,
                5,
                "Barberry",
                "Berberis",
                "https://res.cloudinary.com/dououppib/image/upload/v1709740432/PLANTS/Barberry_copy_gseiuj.png",
                1,
            ),
            "quantity": 2,
        },
    ]


def test_delete_plant_from_user(db_connection):
    repository = PlantsUserRepository(db_connection)
    repository.delete_plants_from_user(1, 1)  ## delete plant 1
    find = repository.find_plants_by_user_id(
        1
    )  ## return a single plant instead 2 after deleting
    assert find == [
        {
            "plant": Plants(
                2,
                2,
                "Alder",
                "Alnus. Black alder",
                "https://res.cloudinary.com/dououppib/image/upload/v1709740428/PLANTS/Alder_jc4szc.jpg",
                1,
            ),
            "quantity": 3,
        },
        {
            "plant": Plants(
                5,
                5,
                "Barberry",
                "Berberis",
                "https://res.cloudinary.com/dououppib/image/upload/v1709740432/PLANTS/Barberry_copy_gseiuj.png",
                1,
            ),
            "quantity": 2,
        },
    ]
