from lib.booking import Booking

class BookingRepository:
    
    def __init__(self, connection):
        self._connection = connection
    
    def get_bookings_by_user_id(self, user_id):
        return self._connection.execute('SELECT bookings.id AS booking_id, bookings.user_id AS booker_id, bookings.space_id, bookings.date, bookings.is_approved, spaces.name FROM bookings JOIN spaces ON bookings.space_id = spaces.id WHERE bookings.id = %s', [user_id])


    def get_bookings_by_space_id(self, space_id):
        rows = self._connection.execute('SELECT * FROM bookings WHERE id = %s', [space_id])
        return [Booking(row['id'], row['user_id'], row['space_id'], row['date'], row['is_approved']) for row in rows]

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
    
    def get_booked_dates_for_space(self, space_id):
        rows = self._connection.execute("SELECT date FROM bookings WHERE space_id = %s AND is_approved = TRUE",
                (space_id,)
        )
        return [row['date'] for row in rows] 
    
    def get_all_bookings_by_owner_id(self, owner_id):
        return self._connection.execute("SELECT bookings.id AS booking_id, bookings.user_id AS booker_id, bookings.space_id, bookings.date, bookings.is_approved, spaces.owner_id, users.username FROM bookings JOIN spaces ON bookings.space_id = spaces.id JOIN users ON bookings.user_id = users.id WHERE spaces.owner_id = %s", [owner_id])