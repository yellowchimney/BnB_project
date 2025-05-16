from lib.booking import Booking
from lib.booking_repo import BookingRepository

def test_get_booking_by_user_id(db_connection):
    db_connection.seed("seeds/bnb_seeds.sql")
    repository = BookingRepository(db_connection)

    bookings = repository.get_bookings_by_user_id(1)

    assert bookings == [{'booking_id': 1, 'booker_id': 1, 'space_id': 3, 'date': '2025-06-01', 'is_approved': False, 'name': 'The Toadstool Den', 'price_per_night': 50, 'url': 'https://www.bpmcdn.com/f/files/mission/import/2022-04/28932492_web1_220504-PWN-HobbitHouse_1.jpg;w=960;h=640;bgcolor=000000'}]

def test_get_bookings_by_space_id(db_connection):
    db_connection.seed("seeds/bnb_seeds.sql")
    repository = BookingRepository(db_connection)

    bookings = repository.get_bookings_by_space_id(1)

    assert bookings == [Booking(1, 1, 3, '2025-06-01', False)]

def test_approve_booking(db_connection):
    db_connection.seed("seeds/bnb_seeds.sql")
    repository = BookingRepository(db_connection)

    repository.approve_booking(1)

    booking = repository.get_booking_by_id(1)

    assert str(booking) == 'Booking(1, 1, 3, 2025-06-01, True)'

def test_decline_booking(db_connection):
    db_connection.seed("seeds/bnb_seeds.sql")
    repository = BookingRepository(db_connection)

    repository.decline_booking(1)

    booking = repository.get_bookings_by_space_id(3)

    assert booking == [Booking(3, 2, 1, '2025-07-04', False)]

def test_get_booking_by_id(db_connection):
    db_connection.seed("seeds/bnb_seeds.sql")
    repository = BookingRepository(db_connection)

    booking = repository.get_booking_by_id(1)

    assert str(booking) == 'Booking(1, 1, 3, 2025-06-01, False)'

def test_create_booking(db_connection):
    db_connection.seed("seeds/bnb_seeds.sql")
    repository = BookingRepository(db_connection)
    booking = Booking(None, 1, 1, '2025-07-04', False)
    new_booking = repository.create_booking(booking)
    assert str(new_booking) == 'Booking(6, 1, 1, 2025-07-04, False)'

def test_get_booked_dates_for_space(db_connection):
    db_connection.seed("seeds/bnb_seeds.sql")
    repository = BookingRepository(db_connection)

    bookings = repository.get_booked_dates_for_space(2)

    assert bookings == ['2025-08-09']

def test_get_all_bookings_by_owner_id(db_connection):
    db_connection.seed("seeds/bnb_seeds.sql")
    repository = BookingRepository(db_connection)

    booking_list = repository.get_all_bookings_by_owner_id(1)

    assert booking_list == [
        {'booker_id': 4,
        'booking_id': 2,
        'date': '2025-06-15',
        'is_approved': False,
        'owner_id': 1,
        'space_id': 6,
        'username': 'Bilbo'
        },
        {
        'booker_id': 2,
        'booking_id': 3,
        'date': '2025-07-04',
        'is_approved': False,
        'owner_id': 1,
        'space_id': 1,
        'username': 'Wallace',
         }]