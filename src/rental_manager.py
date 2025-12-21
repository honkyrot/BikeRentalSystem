import json
from datetime import datetime
import json
import math
from bike import Bike
from customer import Customer
from ticket import Ticket

class RentalManager:

    def __init__(self):
        self.inventory = []  # list of Bike objects
        self.tickets = {}  # dict: ticket_id -> Ticket
        self.load_data()

        self.late_fee_rate = 1.0 # for PROD, this would be configurable

    # --------------------
    # JSON Persistence
    # --------------------
    def load_data(self, inventory_file='inventory.json', tickets_file='tickets.json') -> None:
        """Load bikes and tickets from JSON files."""
        # check and create files if they don't exist
        self.check_files_exist(inventory_file, tickets_file)

        # Load bikes
        try:
            with open(inventory_file, 'r') as file:
                bikes_data = json.loads(file.read())
                self.inventory = [Bike(**b) for b in bikes_data]
        except FileNotFoundError:
            self.inventory = []

        # Load tickets
        try:
            with open(tickets_file, 'r') as file:
                tickets_data = json.loads(file.read())
                self.tickets = {t['id']: Ticket(**t) for t in tickets_data}
        except FileNotFoundError:
            self.tickets = {}

    def save_data(self, inventory_file='inventory.json', tickets_file='tickets.json') -> None:
        """Save bikes and tickets to JSON files."""
        # check and create files if they don't exist
        self.check_files_exist(inventory_file, tickets_file)

        # save bikes
        with open(inventory_file, 'w') as file:
            json.dump([b.__dict__ for b in self.inventory], file, indent=4)
        with open(tickets_file, 'w') as file:
            json.dump([t.__dict__ for t in self.tickets.values()], file, indent=4)

    def check_files_exist(self, inventory_file='inventory.json', tickets_file='tickets.json') -> bool:
        """Check if the JSON files exist."""
        try:
            with open(inventory_file, 'r') as file:
                pass
            with open(tickets_file, 'r') as file:
                pass
            return True
        except FileNotFoundError:
            # create empty files
            with open(inventory_file, 'w') as file:
                json.dump([], file)

            with open(tickets_file, 'w') as file:
                json.dump([], file)
            return False

    # --------------------
    # Bike Inventory
    # --------------------
    def add_bike(self, bike: Bike) -> None:
        """Add a new bike to the inventory."""
        self.inventory.append(bike)
        self.save_data()

    def list_available_bikes(self) -> list[Bike]:
        """Return a list of bikes that are available for rental."""
        return [b for b in self.inventory if b.status == 'available']
    
    def list_rented_bikes(self) -> list[Bike]:
        """Return a list of bikes that are currently rented out."""
        return [b for b in self.inventory if b.status == 'rented']
    
    def list_any_bikes(self, status: str) -> list[Bike]:
        """Return a list of bikes filtered by status."""
        return [b for b in self.inventory if b.status == status]
    
    def list_inventory(self) -> list[Bike]:
        """Return the full bike inventory."""
        return self.inventory
    
    def set_bike_status(self, bike_id: int, status: str, new_value = None) -> Bike:
        """Set the status of a bike."""
        for bike in self.inventory:
            if bike.id == bike_id:
                bike.__setattr__(status, new_value)
                self.save_data()
                return bike
        raise ValueError("Bike not found")
    
    def remove_bike(self, bike_id: int) -> None:
        """Remove a bike from the inventory."""
        # DONT SHIFT THE IDS OF OTHER BIKES
        
        for i, bike in enumerate(self.inventory):
            if bike.id == bike_id:
                del self.inventory[i]
                self.save_data()
                return
            
        raise ValueError("Bike not found")

    # --------------------
    # Ticket Management
    # --------------------
    def create_ticket(self, customer: Customer, bike_id: int, hours: int, personal_notes='') -> Ticket:
        """Create a new rental ticket."""
        bike = next((b for b in self.inventory if b.id == bike_id and b.status == 'available'), None)
        if not bike:
            raise ValueError("Bike not available")
        
        # repack customer object into a dict
        
        if customer.id is None:
            # assign a new customer ID
            if self.tickets:
                max_customer_id = max(t.customer['id'] for t in self.tickets.values())
                customer.id = max_customer_id + 1
            else:
                customer.id = 1

        customer_str = {"id": customer.id, "name": customer.name, "phone": customer.phone}

        # repack bike
        bike_str = {"id": bike.id, "make": bike.make, "model": bike.model, "hourly_rate": bike.hourly_rate, "status": "rented"}

        if self.tickets:
            ticket_id = max(self.tickets.keys()) + 1
        else:
            ticket_id = 1

        start_time = datetime.now().isoformat() # store as ISO string

        # create ticket object
        ticket = Ticket(
            id=ticket_id,
            status='active',
            bike=bike_str,
            customer=customer_str,
            start_time=start_time,
            planned_hours=hours,
            end_time="",
            total_fee=0,
            system_notes='',
            personal_notes=personal_notes
        )

        # Mark bike as rented in inventory
        self.set_bike_status(bike.id, 'status', 'rented')
        self.set_bike_status(bike.id, 'rented_by', customer.name)

        self.tickets[ticket_id] = ticket
        
        self.save_data()
        return ticket

    def close_ticket(self, ticket_id: int) -> Ticket:
        """Close a ticket after bike return."""
        ticket = self.tickets.get(ticket_id)
        if not ticket:
            raise ValueError("Ticket not found")
        
        end_time = datetime.now().isoformat()

        # Calculate total fee
        hours_rented = (datetime.fromisoformat(end_time) - datetime.fromisoformat(ticket.start_time)).total_seconds() / 3600

        ticket.end_time = end_time
        ticket.bike['status'] = 'available'

        # Charge on hourly rate on the planned hours, round up hours
        total_fee = 0
        total_fee = math.ceil(ticket.planned_hours) * ticket.bike['hourly_rate']  # round up hours

        # if overdue, add late fee
        overdue_fee = 0
        overdue_hours = 0
        if hours_rented > ticket.planned_hours:
            late_hours = hours_rented - ticket.planned_hours
            late_fee = late_hours * ticket.bike['hourly_rate'] * self.late_fee_rate
            overdue_fee = late_fee
            overdue_hours = late_hours

        # total fee
        ticket.total_fee = total_fee + overdue_fee
        

        # Mark bike as available in inventory
        self.set_bike_status(ticket.bike['id'], 'status', 'available')
        self.set_bike_status(ticket.bike['id'], 'rented_by', None)

        # close the ticket
        ticket.status = 'closed'

        # note about overdue if any
        if overdue_fee > 0:
            ticket.system_notes = f"Overdue by {overdue_hours:.2f} hours. Original fee: ${total_fee:.2f}. Late fee applied: ${overdue_fee:.2f} = ({overdue_hours:.2f}hours * {ticket.bike['hourly_rate'] * self.late_fee_rate:.2f}rate)."
        else:
            ticket.system_notes = "Returned on time."

        # round total fee to 2 decimal places
        ticket.total_fee = round(ticket.total_fee, 2)

        # Remove ticket from active tickets
        # del self.active_tickets[ticket_id]
        # self.save_data()

        # From hong, we want to keep the ticket for records, so we won't delete it.
        # just mark the end_time and total_fee and leave the ticket alone.

        self.save_data()
        return ticket
    
    def find_active_tickets_by_customer(self, name, phone) -> list[Ticket]:
        """Find active tickets matching customer name and phone."""
        matches = []
        for ticket in self.tickets.values():
            # strict matching on phone, loose on name, must be active
            if (ticket.customer['name'] == name and 
                str(ticket.customer['phone']) == str(phone) and 
                ticket.end_time == ""):
                matches.append(ticket)
        return matches
    
    def get_ticket(self, ticket_id: int) -> None | Ticket:
        """Return the ticket object json for a given ticket ID."""
        return self.tickets.get(ticket_id)
        
    def active_tickets_list(self) -> list[Ticket]:
        """Return a list of all active tickets."""
        return list(self.tickets.values())
    
    def get_all_tickets(self) -> list[Ticket]:
        """Return all tickets."""
        return list(self.tickets.values())

    # --------------------
    # Simple Reports
    # --------------------
    def total_active_rentals(self) -> int:
        """Return the number of active rentals."""
        return len([t for t in self.tickets.values() if t.status == 'active'])

    def total_revenue(self) -> float:
        """Return total revenue from completed tickets."""
        # For simplicity, calculate from tickets that have end_time
        completed_tickets = [t for t in self.tickets.values() if t.end_time is not None]
        return sum(t.total_fee for t in completed_tickets)