from lib.plants_repository import PlanstsRepository
from lib.plants import Plants

def test_all(db_connection):
    repository = PlanstsRepository(db_connection)
    assert repository.all() == [
    
    ]
