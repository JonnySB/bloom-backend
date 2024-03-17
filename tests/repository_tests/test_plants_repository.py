from lib.models.plants import Plants
from lib.repositories.plants_repository import PlantsRepository


def test_all(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = PlantsRepository(db_connection)
    assert repository.all() == [
        Plants(
            1,
            1,
            "African sheepbush",
            "Pentzia incana",
            "https://res.cloudinary.com/dououppib/image/upload/v1709740425/PLANTS/African_sheepbush_lyorlf.jpg",
            2,
        ),
        Plants(
            2,
            2,
            "Alder",
            "Alnus. Black alder",
            "https://res.cloudinary.com/dououppib/image/upload/v1709740428/PLANTS/Alder_jc4szc.jpg",
            1,
        ),
        Plants(
            3,
            3,
            "Almond",
            "Prunus dulcis",
            "https://res.cloudinary.com/dououppib/image/upload/v1709740430/PLANTS/Almond_aikcyc.jpg",
            1,
        ),
        Plants(
            4,
            4,
            "Bamboo",
            "Fargesia",
            "https://res.cloudinary.com/dououppib/image/upload/v1709740434/PLANTS/Bamboo_bkwm52.jpg",
            1,
        ),
        Plants(
            5,
            5,
            "Barberry",
            "Berberis",
            "https://res.cloudinary.com/dououppib/image/upload/v1709740432/PLANTS/Barberry_copy_gseiuj.png",
            1,
        ),
        Plants(
            6,
            6,
            "Bergamot",
            "Monarda",
            "https://res.cloudinary.com/dououppib/image/upload/v1709740426/PLANTS/Bergamot_k7ympf.jpg",
            1,
        ),
    ]


def test_delete_last_one(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = PlantsRepository(db_connection)
    repository.delete(6)
    assert repository.all() == [
        Plants(
            1,
            1,
            "African sheepbush",
            "Pentzia incana",
            "https://res.cloudinary.com/dououppib/image/upload/v1709740425/PLANTS/African_sheepbush_lyorlf.jpg",
            2,
        ),
        Plants(
            2,
            2,
            "Alder",
            "Alnus. Black alder",
            "https://res.cloudinary.com/dououppib/image/upload/v1709740428/PLANTS/Alder_jc4szc.jpg",
            1,
        ),
        Plants(
            3,
            3,
            "Almond",
            "Prunus dulcis",
            "https://res.cloudinary.com/dououppib/image/upload/v1709740430/PLANTS/Almond_aikcyc.jpg",
            1,
        ),
        Plants(
            4,
            4,
            "Bamboo",
            "Fargesia",
            "https://res.cloudinary.com/dououppib/image/upload/v1709740434/PLANTS/Bamboo_bkwm52.jpg",
            1,
        ),
        Plants(
            5,
            5,
            "Barberry",
            "Berberis",
            "https://res.cloudinary.com/dououppib/image/upload/v1709740432/PLANTS/Barberry_copy_gseiuj.png",
            1,
        ),
    ]


def test_delete_no_order(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = PlantsRepository(db_connection)
    repository.delete(2)
    assert repository.all() == [
        Plants(
            1,
            1,
            "African sheepbush",
            "Pentzia incana",
            "https://res.cloudinary.com/dououppib/image/upload/v1709740425/PLANTS/African_sheepbush_lyorlf.jpg",
            2,
        ),
        Plants(
            3,
            3,
            "Almond",
            "Prunus dulcis",
            "https://res.cloudinary.com/dououppib/image/upload/v1709740430/PLANTS/Almond_aikcyc.jpg",
            1,
        ),
        Plants(
            4,
            4,
            "Bamboo",
            "Fargesia",
            "https://res.cloudinary.com/dououppib/image/upload/v1709740434/PLANTS/Bamboo_bkwm52.jpg",
            1,
        ),
        Plants(
            5,
            5,
            "Barberry",
            "Berberis",
            "https://res.cloudinary.com/dououppib/image/upload/v1709740432/PLANTS/Barberry_copy_gseiuj.png",
            1,
        ),
        Plants(
            6,
            6,
            "Bergamot",
            "Monarda",
            "https://res.cloudinary.com/dououppib/image/upload/v1709740426/PLANTS/Bergamot_k7ympf.jpg",
            1,
        ),
    ]


def test_find(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = PlantsRepository(db_connection)
    plant = repository.find(2)
    assert plant == Plants(
        2,
        2,
        "Alder",
        "Alnus. Black alder",
        "https://res.cloudinary.com/dououppib/image/upload/v1709740428/PLANTS/Alder_jc4szc.jpg",
        1,
    )


def test_update(db_connection):
    db_connection.seed("seeds/bloom.sql")
    repository = PlantsRepository(db_connection)
    repository.update(1, {"common_name": "New Name"})
    assert repository.all() == [
        Plants(
            2,
            2,
            "Alder",
            "Alnus. Black alder",
            "https://res.cloudinary.com/dououppib/image/upload/v1709740428/PLANTS/Alder_jc4szc.jpg",
            1,
        ),
        Plants(
            3,
            3,
            "Almond",
            "Prunus dulcis",
            "https://res.cloudinary.com/dououppib/image/upload/v1709740430/PLANTS/Almond_aikcyc.jpg",
            1,
        ),
        Plants(
            4,
            4,
            "Bamboo",
            "Fargesia",
            "https://res.cloudinary.com/dououppib/image/upload/v1709740434/PLANTS/Bamboo_bkwm52.jpg",
            1,
        ),
        Plants(
            5,
            5,
            "Barberry",
            "Berberis",
            "https://res.cloudinary.com/dououppib/image/upload/v1709740432/PLANTS/Barberry_copy_gseiuj.png",
            1,
        ),
        Plants(
            6,
            6,
            "Bergamot",
            "Monarda",
            "https://res.cloudinary.com/dououppib/image/upload/v1709740426/PLANTS/Bergamot_k7ympf.jpg",
            1,
        ),
        Plants(
            1,
            1,
            "New Name",
            "Pentzia incana",
            "https://res.cloudinary.com/dououppib/image/upload/v1709740425/PLANTS/African_sheepbush_lyorlf.jpg",
            2,
        ),
    ]
