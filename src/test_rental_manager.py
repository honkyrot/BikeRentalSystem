import unittest
from bike import Bike
from customer import Customer
from rental_manager import RentalManager

class TestRentalManager(unittest.TestCase):

    def setUp(self):
        # This runs before each test
        self.manager = RentalManager()
        # Clear inventory and tickets for testing
        self.manager.inventory = []
        self.manager.active_tickets = []
        self.manager.closed_tickets = []
        self.manager.bike_lookup = {}
        self.manager.ticket_lookup = {}

        # Add sample bikes
        self.bike1 = Bike("B1", ("Trek", "FX1"), "available", 10)
        self.bike2 = Bike("B2", ("Giant", "Escape 3"), "available", 15)
        self.manager.add_bike(self.bike1)
        self.manager.add_bike(self.bike2)

        # Add a sample customer
        self.customer = Customer("C1", "John Doe", "1234567890")

    def test_create_ticket(self):
        ticket = self.manager.create_ticket("T1", "B1", self.customer, planned_hours=2)
        self.assertEqual(ticket.ticket_id, "T1")
        self.assertEqual(ticket.bike.bike_id, "B1")
        self.assertEqual(ticket.customer.name, "John Doe")
        self.assertEqual(ticket.bike.status, "rented")

    def test_return_bike(self):
        self.manager.create_ticket("T1", "B1", self.customer, planned_hours=2)
        fee = self.manager.return_bike("T1")
        self.assertEqual(fee, 20)
        self.assertEqual(self.bike1.status, "available")
        self.assertEqual(len(self.manager.active_tickets), 0)
        self.assertEqual(len(self.manager.closed_tickets), 1)

    def test_get_available_bikes(self):
        available = self.manager.get_available_bikes()
        self.assertIn(self.bike1, available)
        self.assertIn(self.bike2, available)
        self.manager.create_ticket("T1", "B1", self.customer, planned_hours=1)
        available_after = self.manager.get_available_bikes()
        self.assertNotIn(self.bike1, available_after)
        self.assertIn(self.bike2, available_after)

if __name__ == "__main__":
    unittest.main()
