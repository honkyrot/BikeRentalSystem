class Bike:
    def __init__(self, bike_id, make_model, status="available", hourly_rate=10):
        self.bike_id = bike_id
        self.make_model = make_model
        self.status = status
        self.hourly_rate = hourly_rate