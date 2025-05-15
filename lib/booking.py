

class Booking():

    def __init__(self, id, user_id, space_id, date, is_approved=False):
        self.id = id
        self.user_id = user_id
        self.space_id = space_id
        self.date = date
        self.is_approved = False

    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__


    def __repr__(self):

        return f"Booking({self.id}, {self.user_id}, {self.space_id}, {self.date}, {self.is_approved})"
