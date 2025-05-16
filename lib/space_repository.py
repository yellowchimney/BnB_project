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

    def create_space(self, space):
        rows = self._connection.execute("INSERT INTO spaces (name, description, price_per_night, owner_id, url) VALUES(%s,%s,%s,%s,%s) RETURNING id",
                                 [space.name, space.description, space.price_per_night, space.owner_id, space.url])       
        return rows[0]["id"]
    

    def get_all_owner_spaces(self, owner_id):
        rows = self._connection.execute("SELECT * FROM spaces WHERE owner_id = %s", [owner_id])
        return [Space(row['id'], row['name'], row['description'], row['price_per_night'], row['owner_id'], row['url']) for row in rows]
    

    def delete_space(self, space_id):
        self._connection.execute("DELETE FROM spaces WHERE id = %s", [space_id])

