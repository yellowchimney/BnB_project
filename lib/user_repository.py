from lib.user import User

class UserRepository:
    
    def __init__(self, connection):
        self._connection = connection

    def get_user_by_username(self, username):
        rows = self._connection.execute('SELECT * FROM users WHERE username = %s', [username])
        row = rows[0]
        user = User(row['id'], row['username'], row['email'], row['password'], row['phone_number'])

        return user
    
    def get_all(self):
        rows = self._connection.execute('SELECT * FROM users')
        return [User(row['id'], row['username'], row['email'], row['password'], row['phone_number']) for row in rows]

    def user_exists(self, username):
         rows = self._connection.execute('SELECT * FROM users WHERE username = %s', [username])
         if rows:
             return True
         else:
             return False
         
    def get_user_by_id(self, user_id):
            rows = self._connection.execute('SELECT * FROM users WHERE id = %s', [user_id])
            row = rows[0]
            user = User(row['id'], row['username'], row['password'])

            return user