class Bike:
    def __init__(self, bike_id, make_model, status="available", hourly_rate=10):
        self.bike_id = bike_id
        self.make_model = make_model
        self.status = status
        self.hourly_rate = hourly_rate

    def __repr__(self):
        return f"Bike({self.bike_id}, {self.make_model}, {self.model}, {self.status}, ${self.hourly_rate}/hr)"

    def markRented(self):
        self.status = 'rented'

    def markAvaliable(self):
        self.status = 'available'
16dee08a1aaa6fc94d8c99a06125b5d65e5fe6bb
