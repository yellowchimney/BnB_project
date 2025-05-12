from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, email, password, phone_number, space_ids):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.space_ids = space_ids
    


    def __eq__(self, other):
        return self.__dict__ == other.__dict__


    def __repr__(self):
        return f"User({self.id}, {self.username}, {self.email}, {self.password}, {self.phone_number}, {self.space_ids})"