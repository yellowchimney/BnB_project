from lib.space import Space

class SpaceRepository:

    def __init__(self, connection):
        self._connection = connection

    def get_all(self):
        rows = self._connection.execute('SELECT * FROM spaces')
        return [Space(row['id'], row['name'], row['description'], row['price_per_night'], row['owner_id'], row['url']) for row in rows]
    
    def get_single_space(self, space_id):
        rows = self._connection.execute('SELECT * FROM spaces WHERE id = %s', [space_id])
        row = rows[0]
        return Space(row['id'], row['name'], row['description'], row['price_per_night'], row['owner_id'], row['url'])