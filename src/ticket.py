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

        # mark the bike rented
        self.bike.mark_rented()

    def __repr__(self):
        return (f"Ticket({self.id}, Bike {self.bike.id}, Customer {self.customer.id}, "
                f"Start: {self.start_time}, End: {self.end_time}, Fee: ${self.total_fee})")

    def to_dict(self):
        # convert Ticket object into a dictonary for JSON compatibility
        return {
            "id": self.id,
            "bike_id": self.bike.id,
            "customer_id": self.customer.id,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "planned_hours": self.planned_hours,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "total_fee": self.total_fee
        }
    
    def endRental(self):
        # get current time
        self.end_time = datetime.now()

        # get the difference between the start and end times
        durationSec = (self.start_time - self.end_time).total_seconds()
        duration = durationSec/3600

        # calculate and round the fee
        fee = (duration*self.bike.hourly_rate)
        self.total_fee = round(fee, 2)

        # mark the bike avaliable again
        self.bike.markAvaliable()

        return self.total_fee
    
    @classmethod
    def from_dict(cls, data, bikes, customers):
        # get info from dictionary to turn into a Ticket object with that info
        bike = bikes[data['bike_id']]
        customer = customers[data['customer_id']]
        start_time = datetime.fromisoformat(data['state_time']) if data['start_time'] else None
        end_time = datetime.fromisoformat(data['end_time']) if data['end_time'] else None

        return cls(id=data['id'], bike=bike, customer=customer, start_time=start_time, planned_hours=data['planned_hours'], end_time=end_time, total_fee=data['total_fee'])
