from lib.user_repository import UserRepository
from lib.user import User


def test_single_user_by_username(db_connection):
    db_connection.seed("seeds/bnb_seeds.sql")
    repository = UserRepository(db_connection)

    user = repository.get_user_by_username('Gromit')

    assert user == User(1, 'Gromit', 'gromit@wallace.com', '$2b$12$odSf0B0I5gSqVFfddp92oeZudmdDj2gkNmlXT4do1S2roiT45N5tu', '07867564876')

def test_all_users_by(db_connection):
    db_connection.seed("seeds/bnb_seeds.sql")
    repository = UserRepository(db_connection)

    users = repository.get_all()

    assert users == [User(1, 'Gromit', 'gromit@wallace.com', '$2b$12$odSf0B0I5gSqVFfddp92oeZudmdDj2gkNmlXT4do1S2roiT45N5tu', '07867564876'), User(2, 'Wallace', 'wallace@wallace.com', '$2b$12$ol40SdrozS89ixcXk8mFHOSHTiTpo9raSD7u4fX86CR5mg1W7u18G', '07867564123'), User(3, 'Shawn', 'shawn@example.com', 'password_1', '123-456-7890'), User(4, 'Bilbo', 'bilbo@shiremail.com', 'password_2', '111-222-3333'), User(5, 'Sam', 'sam@hobbitmail.com', 'assword_3', '444-555-6666')]

def test_user_exists(db_connection):
    db_connection.seed("seeds/bnb_seeds.sql")
    repository = UserRepository(db_connection)

    assert repository.user_exists('Bilbo') == True

def test_get_user_by_id(db_connection):
    db_connection.seed("seeds/bnb_seeds.sql")
    repository = UserRepository(db_connection)

    user = repository.get_user_by_id(1)

    assert user == User(1, 'Gromit', 'gromit@wallace.com', '$2b$12$odSf0B0I5gSqVFfddp92oeZudmdDj2gkNmlXT4do1S2roiT45N5tu', '07867564876')

def test_create_user(db_connection):
    db_connection.seed("seeds/bnb_seeds.sql")
    repository = UserRepository(db_connection)
    new_user = User(None, 'Brian', 'Brian@Brian.com', 'PassWord', '3625')
    returned_user = repository.create_user(new_user)

    assert returned_user == User(6, 'Brian', 'Brian@Brian.com', 'PassWord', '3625')