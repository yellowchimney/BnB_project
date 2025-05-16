from lib.booking import Booking

def test_construct():
    booking = Booking(1, 2, 3, '2025-06-11', True)
    assert booking.id == 1
    assert booking.user_id == 2
    assert booking.space_id == 3
    assert booking.date == '2025-06-11'
    assert booking.is_approved == True
    
    
def test_equality():
     booking1 = Booking(1, 2, 3, '2025-06-11', False)
     booking2 = Booking(1, 2, 3, '2025-06-11', False)
     booking3 = Booking(3, 1, 2, '2025-06-13', True)

     assert booking1 == booking2
     assert booking1 != booking3


def test_format():
      booking = Booking(1, 2, 3, '2025-06-11', True)
      assert str(booking) == "Booking(1, 2, 3, 2025-06-11, True)"

     

