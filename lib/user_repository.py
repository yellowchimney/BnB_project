from lib.user import User

class UserRepository:
    
    def __init__(self, connection):
        self._connection = connection

    def get_user_by_username(self, username):
        rows = self._connection.execute('SELECT * FROM users WHERE username = %s', [username])

        user = User()
