from datetime import datetime

class Ticket:
    def __init__(self, id, status, bike, customer, start_time, planned_hours, end_time="", total_fee=0, system_notes='', personal_notes=''):
        self.id = id
        self.status = status
        self.bike = bike
        self.customer = customer
        self.start_time = start_time
        self.planned_hours = planned_hours
        self.end_time = end_time
        self.total_fee = total_fee
        self.system_notes = system_notes
        self.personal_notes = personal_notes

    def __repr__(self):
        return (f"Ticket({self.id}, Bike {self.bike}, Customer {self.customer}, "
                f"Start: {self.start_time}, End: {self.end_time}, Fee: ${self.total_fee})")