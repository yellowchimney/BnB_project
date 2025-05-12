from lib.user import User

def test_construct():
    user = User(1,"Georgey", "geo@geo.com", "complicatedpassword1", "07777423411", [1])
    assert user.id == 1
    assert user.username == "Georgey"
    assert user.email == "geo@geo.com"
    assert user.password == "complicatedpassword1"
    assert user.phone_number == "07777423411"
    assert user.space_ids == [1]
    
def test_equality():
     user1 = User(1,"Georgey", "geo@geo.com", "complicatedpassword1", "07777423411", [1])
     user2 = User(1,"Georgey", "geo@geo.com", "complicatedpassword1", "07777423411", [1])
     user3 = User(1,"Georgey2", "geo@g2eo.com", "complicatedpassword12", "07777423412", [2])

     assert user1 == user2
     assert user1 != user3


def test_format():
      user = User(1,"Georgey", "geo@geo.com", "complicatedpassword1", "07777423411", [1])
      assert str(user) == "User(1, Georgey, geo@geo.com, complicatedpassword1, 07777423411, [1])"

     

