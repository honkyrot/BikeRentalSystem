import json
from datetime import datetime
from ticket import Ticket

class RentalManager:

    def __init__(self):
        self.inventory = []
        self.active_tickets = []
        self.closed_tickets = []
        self.bike_lookup = {}
        self.ticket_lookup = {}
        self.load_inventory()
        self.load_tickets()

    # ------------------------------
    # INVENTORY MANAGEMENT
    # ------------------------------
    def add_bike(self, bike):
        self.inventory.append(bike)
        self.bike_lookup[bike.bike_id] = bike
        self.save_inventory()

    def get_available_bikes(self):
        return [bike for bike in self.inventory if bike.status == "available"]

    # ------------------------------
    # TICKET MANAGEMENT
    # ------------------------------
    def create_ticket(self, ticket_id, bike_id, customer, planned_hours):
        bike = self.bike_lookup.get(bike_id)
        if not bike or bike.status != "available":
            print(f"Bike {bike_id} is not available.")
            return None

        ticket = Ticket(
            ticket_id=ticket_id,
            bike=bike,
            customer=customer,
            start_time=datetime.now(),
            planned_hours=planned_hours
        )
        bike.status = "rented"
        self.active_tickets.append(ticket)
        self.ticket_lookup[ticket_id] = ticket

        self.save_inventory()
        self.save_tickets()

        print(f"Ticket created successfully:\n Ticket ID: {ticket.ticket_id}\n Bike rented: {bike.bike_id}\n Customer: {customer.name}\n Start time: {ticket.start_time}")
        return ticket

    def return_bike(self, ticket_id):
        ticket = self.ticket_lookup.get(ticket_id)
        if not ticket:
            print(f"No active ticket found for {ticket_id}")
            return None

        ticket.bike.status = "available"
        if ticket in self.active_tickets:
            self.active_tickets.remove(ticket)
        self.closed_tickets.append(ticket)

        self.save_inventory()
        self.save_tickets()

        total_fee = ticket.bike.hourly_rate * ticket.planned_hours
        print(f"Bike returned. Total fee: ${total_fee}")
        return total_fee

    # ------------------------------
    # JSON PERSISTENCE
    # ------------------------------
    def save_inventory(self):
        data = []
        for bike in self.inventory:
            data.append({
                "bike_id": bike.bike_id,
                "make_model": bike.make_model,
                "status": bike.status,
                "hourly_rate": bike.hourly_rate
            })
        with open("inventory.json", "w") as f:
            json.dump(data, f, indent=4)

    def load_inventory(self):
        try:
            with open("inventory.json", "r") as f:
                data = json.load(f)
                for b in data:
                    from bike import Bike
                    bike = Bike(
                        bike_id=b["bike_id"],
                        make_model=tuple(b["make_model"]),
                        status=b["status"],
                        hourly_rate=b["hourly_rate"]
                    )
                    self.inventory.append(bike)
                    self.bike_lookup[bike.bike_id] = bike
        except FileNotFoundError:
            pass

    def save_tickets(self):
        data = []
        for ticket in self.active_tickets + self.closed_tickets:
            data.append({
                "ticket_id": ticket.ticket_id,
                "bike_id": ticket.bike.bike_id,
                "customer_name": ticket.customer.name,
                "start_time": ticket.start_time.isoformat(),
                "planned_hours": ticket.planned_hours
            })
        with open("tickets.json", "w") as f:
            json.dump(data, f, indent=4)

    def load_tickets(self):
        try:
            with open("tickets.json", "r") as f:
                data = json.load(f)
                from bike import Bike
                from customer import Customer
                for t in data:
                    bike = self.bike_lookup.get(t["bike_id"])
                    customer = Customer(name=t["customer_name"], customer_id="C1", phone="")
                    ticket = Ticket(
                        ticket_id=t["ticket_id"],
                        bike=bike,
                        customer=customer,
                        start_time=datetime.fromisoformat(t["start_time"]),
                        planned_hours=t.get("planned_hours", 1)
                    )
                    if bike.status == "rented":
                        self.active_tickets.append(ticket)
                    else:
                        self.closed_tickets.append(ticket)
                    self.ticket_lookup[ticket.ticket_id] = ticket
        except FileNotFoundError:
            pass
