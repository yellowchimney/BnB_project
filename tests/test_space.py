from lib.space import Space

def test_construct():
    space = Space(1, "Georgey", "lovely flat", 800)
    assert space.id == 1
    assert space.name == "Georgey"
    assert space.description == "lovely flat"
    assert space.price_per_night == 800
    
    
def test_equality():
    space2 = Space(1, "Georgey", "lovely flat", 800)
    space3 = Space(1, "Georgey", "lovely flat", 800)

    assert space2 == space2



def test_format():
    space = Space(1, "Georgey", "lovely flat", 800)
    assert str(space) == "Space(1, Georgey, lovely flat, 800)"