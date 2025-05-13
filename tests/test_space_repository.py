from lib.space_repository import SpaceRepository
from lib.space import Space

def test_all_spaces(db_connection):
    db_connection.seed("seeds/bnb_seeds.sql")
    repository = SpaceRepository(db_connection)

    spaces = repository.get_all()

    assert spaces == [
        Space(1, 'Flat', 'Lovely flat', 5, 2),
        Space(2, 'Kennel', 'The dog house', 1, 1)
    ]

def test_single_space(db_connection):
    db_connection.seed("seeds/bnb_seeds.sql")
    repository = SpaceRepository(db_connection)

    space = repository.get_single_space(2)

    assert space == Space(2, 'Kennel', 'The dog house', 1, 1)