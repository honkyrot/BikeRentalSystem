from datetime import datetime

class Ticket:
    def __init__(self, id, bike, customer, start_time, planned_hours, end_time=None, total_fee=0):
        self.id = id
        self.bike = bike
        self.customer = customer
        self.start_time = start_time
        self.planned_hours = planned_hours
        self.end_time = end_time
        self.total_fee = total_fee

    def __repr__(self):
        return (f"Ticket({self.id}, Bike {self.bike.id}, Customer {self.customer.id}, "
                f"Start: {self.start_time}, End: {self.end_time}, Fee: ${self.total_fee})")