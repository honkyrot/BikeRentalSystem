class Bike:
    def __init__(self, id, make, model, status='available', hourly_rate=5.0):
        self.id = id
        self.make = make
        self.model = model
        self.status = status  # 'available' or 'rented'
        self.hourly_rate = hourly_rate

    def __repr__(self):
        return f"Bike({self.id}, {self.make}, {self.model}, {self.status}, ${self.hourly_rate}/hr)"