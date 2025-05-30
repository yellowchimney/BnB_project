class Space:
    def __init__(self,id, name, description, price_per_night, owner_id, url):
        self.id = id 
        self.name = name
        self.description = description
        self.price_per_night = price_per_night
        self.owner_id = owner_id
        self.url = url
        
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"Space({self.id}, {self.name}, {self.description}, {self.price_per_night}, {self.owner_id}, {self.url})"