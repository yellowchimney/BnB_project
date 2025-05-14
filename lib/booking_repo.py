from lib.booking import Booking

class UserRepository:
    
    def __init__(self, connection):
        self._connection = connection
    
    def get_booking_by_user_id(self, user_id):
        rows = self._connection.execute('SELECT * FROM bookings WHERE id = %s', [user_id])
        return [Booking(row.id, row.user_id, row.space_id, row.date, row.is_approved) for row in rows]

    def get_booking_by_space_id(self, space_id):
        rows = self._connection.execute('SELECT * FROM bookings WHERE id = %s', [space_id])
        return [Booking(row.id, row.user_id, row.space_id, row.date, row.is_approved) for row in rows]


    def approve_booking(self, booking_id):
        self._connection.execute('UPDATE bookings SET is_aproved = TRUE WHERE id = %s', [booking_id])
        

    def get_booking_by_id(self, booking_id):
            rows = self._connection.execute('SELECT * FROM bookings WHERE id = %s', [booking_id])
            row = rows[0]
            booking = Booking(row['id'], row['user_id'], row['space_id'], row['date'], row['is_approved'])

            return booking
    
    def create_booking(self, booking):
        rows = self._connection.execute('INSERT INTO bookings (user_id, space_id, date, is_approved) ' \
         'VALUES (%s,%s,%s,%s) RETURNING id', [booking.user_id, booking.space_id, booking.date, booking.is_approved])

        return self.get_booking_by_id(rows[0]['id'])