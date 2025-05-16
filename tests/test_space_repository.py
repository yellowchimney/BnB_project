from lib.space_repository import SpaceRepository
from lib.space import Space

def test_all_spaces(db_connection):
    db_connection.seed("seeds/bnb_seeds.sql")
    repository = SpaceRepository(db_connection)

    spaces = repository.get_all()

    assert len(spaces) == 8

def test_single_space(db_connection):
    db_connection.seed("seeds/bnb_seeds.sql")
    repository = SpaceRepository(db_connection)

    space = repository.get_single_space(2)

    assert str(space) == "Space(2, Mossy Hollow, A quaint hideaway with moss-covered walls and a fireplace that never goes out., 65, 2, https://news.airbnb.com/wp-content/uploads/sites/4/2022/04/Second-Breakfast-Hideaway-1-Kootenay-Boundary-E-BC-1.jpeg)"

def test_create_space(db_connection):
    db_connection.seed("seeds/bnb_seeds.sql")
    repository = SpaceRepository(db_connection)
    new_space = Space(None, 'Minas Tirith', 'Overblown city', 1256, 1, 'This_url')
    new_space_id = repository.create_space(new_space)

    created_space = repository.get_single_space(new_space_id)

    assert created_space == Space(9, 'Minas Tirith', 'Overblown city', 1256, 1, 'This_url')

