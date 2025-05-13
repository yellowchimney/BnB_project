from lib.user_repository import UserRepository
from lib.user import User


def test_single_user_by_username(db_connection):
    db_connection.seed("seeds/bnb_seeds.sql")
    repository = UserRepository(db_connection)

    user = repository.get_user_by_username('Gromit')

    assert user == User(1, 'Gromit', 'gromit@wallace.com', 'passw0rd1', '07867564876')

def test_all_users_by(db_connection):
    db_connection.seed("seeds/bnb_seeds.sql")
    repository = UserRepository(db_connection)

    users = repository.get_all()

    assert users == [
        User(1, 'Gromit', 'gromit@wallace.com', 'passw0rd1', '07867564876'),
        User(2, 'Wallace', 'wallace@wallace.com', 'passw0rd2', '07867564123')
    ]