from bike import Bike
from customer import Customer
from ticket import Ticket
from datetime import datetime
import json

class RentalManager:
    def __init__(self):
        self.inventory = []  # list of Bike objects
        self.active_tickets = {}  # dict: ticket_id -> Ticket
        self.load_data()

    # --------------------
    # JSON Persistence
    # --------------------
    def load_data(self, inventory_file='inventory.json', tickets_file='tickets.json'):
        """Load bikes and tickets from JSON files."""
        # Load bikes
        try:
            with open(inventory_file, 'r') as f:
                bikes_data = json.load(f)
                self.inventory = [Bike(**b) for b in bikes_data]
        except FileNotFoundError:
            self.inventory = []

        # Load tickets
        try:
            with open(tickets_file, 'r') as f:
                tickets_data = json.load(f)
                self.active_tickets = {t['id']: Ticket(**t) for t in tickets_data}
        except FileNotFoundError:
            self.active_tickets = {}

    def save_data(self, inventory_file='inventory.json', tickets_file='tickets.json'):
        """Save bikes and tickets to JSON files."""
        with open(inventory_file, 'w') as f:
            json.dump([b.__dict__ for b in self.inventory], f, indent=4)
        with open(tickets_file, 'w') as f:
            json.dump([t.__dict__ for t in self.active_tickets.values()], f, indent=4)

    # --------------------
    # Bike Inventory
    # --------------------
    def add_bike(self, bike: Bike):
        """Add a new bike to the inventory."""
        self.inventory.append(bike)
        self.save_data()

    def list_available_bikes(self):
        """Return a list of bikes that are available for rental."""
        return [b for b in self.inventory if b.status == 'available']

    # --------------------
    # Ticket Management
    # --------------------
    def create_ticket(self, customer: Customer, bike_id: int, hours: int):
        """Create a new rental ticket."""
        bike = next((b for b in self.inventory if b.id == bike_id and b.status == 'available'), None)
        if not bike:
            raise ValueError("Bike not available")

        ticket_id = len(self.active_tickets) + 1
        start_time = datetime.now()
        ticket = Ticket(
            id=ticket_id,
            bike=bike,
            customer=customer,
            start_time=start_time,
            planned_hours=hours,
            end_time=None,
            total_fee=0
        )
        self.active_tickets[ticket_id] = ticket
        bike.status = 'rented'
        self.save_data()
        return ticket

    def return_bike(self, ticket_id: int):
        """Return a bike and calculate total fee."""
        ticket = self.active_tickets.get(ticket_id)
        if not ticket:
            raise ValueError("Ticket not found")
        
        end_time = datetime.now()
        hours_rented = (end_time - ticket.start_time).total_seconds() / 3600
        ticket.end_time = end_time
        ticket.total_fee = round(hours_rented * ticket.bike.hourly_rate, 2)
        ticket.bike.status = 'available'

        # Remove ticket from active tickets
        del self.active_tickets[ticket_id]
        self.save_data()
        return ticket

    # --------------------
    # Simple Reports
    # --------------------
    def total_active_rentals(self):
        """Return the number of active rentals."""
        return len(self.active_tickets)

    def total_revenue(self):
        """Return total revenue from completed tickets."""
        # For simplicity, calculate from tickets that have end_time
        completed_tickets = [t for t in self.active_tickets.values() if t.end_time is not None]
        return sum(t.total_fee for t in completed_tickets)