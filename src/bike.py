class Bike:
    def __init__(self, id, make, model, status='available', rented_by=None, hourly_rate=5.0):
        self.id = id
        self.make = make
        self.model = model
        # self.make_model = make + model
        self.status = status  # 'available' or 'rented'
        self.rented_by = rented_by
        self.hourly_rate = hourly_rate

    def __repr__(self):
        return f"Bike({self.id}, {self.make}, {self.model}, {self.status}, {self.rented_by}, ${self.hourly_rate}/hr)"
        # return f"Bike({self.id}, {self.make_model}, {self.model}, {self.status}, ${self.hourly_rate}/hr)"
        
    def markRented(self):
        self.status = 'rented'

    def markAvaliable(self):
        self.status = 'available'