# test cases for our system
import json
import unittest
import rental_manager
import os

class TestRentalManager(unittest.TestCase):
    def setUp(self):
        self.manager = rental_manager.RentalManager()
        self.manager.inventory = []  # Reset inventory for each test
        self.manager.tickets = {}  # Reset tickets for each test

        self.debug_output = True

    def tearDown(self):
        if self.debug_output:
            # spit out data
            print("==================== DEBUG OUTPUT ====================")
            print("Inventory Data\n", json.dumps([b.__dict__ for b in self.manager.inventory], indent=4))
            print("Tickets Data\n", json.dumps([t.__dict__ for t in self.manager.tickets.values()], indent=4))

    def test_add_bike(self):
        """
        TEST: 1
        Test adding a bike to the inventory.
        """
        bike = rental_manager.Bike(id=1, make='test_brand_1', model='test_model_1')
        self.manager.add_bike(bike)

        self.assertIn(bike, self.manager.inventory) # Bike added
        self.assertEqual(len(self.manager.inventory), 1) # One bike in inventory

    def test_add_multiple_bikes(self):
        """
        TEST: 2
        Test adding multiple bikes to the inventory.
        """
        self.debug_output = False  # Disable debug save for this test

        for i in range(100):
            bike = rental_manager.Bike(id=i, make='test_brand_'+str(i), model='test_model_'+str(i))
            self.manager.add_bike(bike)

        self.assertEqual(len(self.manager.inventory), 100) # 100 bikes in inventory
    
    def test_remove_bike(self):
        """
        TEST: 3
        Test adding and removing a bike from the inventory.
        """
        bike = rental_manager.Bike(id=1, make='test_brand_3', model='test_model_3')
        self.manager.add_bike(bike)
        self.manager.remove_bike(bike_id=1)

        self.assertNotIn(bike, self.manager.inventory) # Bike removed
        self.assertEqual(len(self.manager.inventory), 0) # Inventory is empty

    def test_set_bike_status(self):
        """
        TEST: 4
        Test setting the status of a bike.
        """
        bike = rental_manager.Bike(id=1, make='test_brand_4', model='test_model_4')
        self.manager.add_bike(bike)
        updated_bike = self.manager.set_bike_status(bike_id=1, status='status', new_value='rented')

        self.assertEqual(updated_bike.status, 'rented') # Status updated

    def test_return_bike(self):
        """
        TEST: 5
        Test returning a rented bike.
        """
        bike = rental_manager.Bike(id=1, make='test_brand_5', model='test_model_5', status='rented')
        self.manager.add_bike(bike)
        updated_bike = self.manager.set_bike_status(bike_id=1, status='status', new_value='available')

        self.assertEqual(updated_bike.status, 'available') # Status updated

    def test_create_ticket(self):
        """
        TEST: 6
        Test creating a rental ticket.
        """
        bike = rental_manager.Bike(id=1, make='test_brand_6', model='test_model_6')
        self.manager.add_bike(bike)

        customer = rental_manager.Customer(id=1, name='test_customer_6 Multivitiman Gummies', phone='test_phone_123-456-7890')
        ticket = self.manager.create_ticket(customer=customer, bike_id=1, hours=3)

        self.assertIn(ticket.id, self.manager.tickets) # Ticket is active
        self.assertEqual(ticket.bike['status'], 'rented') # Bike status updated
        self.assertEqual(self.manager.inventory[0].status, 'rented') # Bike in inventory updated

    def test_create_ticket_unavailable_bike(self):
        """
        TEST: 7
        Test creating a rental ticket for an unavailable bike.
        """
        bike = rental_manager.Bike(id=1, make='test_brand_7', model='test_model_7', status='rented')
        self.manager.add_bike(bike)

        customer = rental_manager.Customer(id=1, name='test_customer_7 Multivitiman Gummies', phone='test_phone_123-456-7890')
        
        with self.assertRaises(ValueError) as context:
            self.manager.create_ticket(customer=customer, bike_id=1, hours=3)
        
        self.assertEqual(str(context.exception), "Bike not available") # Correct exception raised

    def test_create_multiple_tickets(self):
        """
        TEST: 8
        Test creating multiple rental tickets.
        """
        self.debug_output = False  # Disable debug save for this test

        for i in range(10):
            bike = rental_manager.Bike(id=i, make='test_brand_'+str(i), model='test_model_'+str(i))
            self.manager.add_bike(bike)

        for i in range(10):
            customer = rental_manager.Customer(id=i, name='test_customer_'+str(i), phone='test_phone_000-000-000'+str(i))
            ticket = self.manager.create_ticket(customer=customer, bike_id=i, hours=2)
            self.assertIn(ticket.id, self.manager.tickets) # Ticket is active
            self.assertEqual(ticket.bike['status'], 'rented') # Bike status updated

    def test_timely_return_ticket(self):
        """
        TEST: 9
        Test closing a ticket with timely return.
        """
        bike = rental_manager.Bike(id=1, make='test_brand_9_with_10_dollars_per_hour', model='test_model_9', hourly_rate=10.0)
        self.manager.add_bike(bike)

        customer = rental_manager.Customer(id=1, name='test_customer_9 Multivitiman Gummies', phone='test_phone_123-456-7890')
        ticket = self.manager.create_ticket(customer=customer, bike_id=1, hours=1)

        closed_ticket = self.manager.close_ticket(ticket_id=ticket.id)

        self.assertEqual(closed_ticket.status, 'closed') # Ticket closed
        self.assertEqual(closed_ticket.total_fee, 10.0) # No late fee
        self.assertEqual(self.manager.inventory[0].status, 'available') # Bike status updated

    def test_overdue_return_ticket(self):
        """
        TEST: 10
        Test closing a ticket with overdue return.
        Late fee is 2x for this test case.
        """
        bike = rental_manager.Bike(id=1, make='test_brand_10_with_10_dollars_per_hour', model='test_model_10', hourly_rate=10.0)
        self.manager.late_fee_rate = 2.0  # 2x
        self.manager.add_bike(bike)

        customer = rental_manager.Customer(id=1, name='test_customer_10 Multivitiman Gummies', phone='test_phone_123-456-7890')
        ticket = self.manager.create_ticket(customer=customer, bike_id=1, hours=1)

        # Manually adjust start_time to simulate overdue
        from datetime import datetime, timedelta
        ticket.start_time = (datetime.now() - timedelta(hours=3)).isoformat() # overdue by 2 hours so total 3 hours

        closed_ticket = self.manager.close_ticket(ticket_id=ticket.id)

        self.assertEqual(closed_ticket.status, 'closed') # Ticket closed
        self.assertEqual(closed_ticket.total_fee, 50.0) # Late fee applied
        self.assertIn('Overdue by', closed_ticket.system_notes) # Notes updated
        self.assertEqual(self.manager.inventory[0].status, 'available') # Bike status updated


# Run the tests
if __name__ == '__main__':
    unittest.main()