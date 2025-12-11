from bike import Bike
from customer import Customer
from rental_manager import RentalManager

def main():
    # Initialize RentalManager
    manager = RentalManager()

    # DEBUG: show inventory and tickets after init
    print("RentalManager initialized")
    print("Current inventory:", manager.inventory)
    print("Current active tickets:", manager.active_tickets)

    # Add bikes (fresh start)
    bike1 = Bike(id=1, make="Trek", model="FX 3", hourly_rate=7)
    bike2 = Bike(id=2, make="Giant", model="Escape 2", hourly_rate=6)
    manager.add_bike(bike1)
    manager.add_bike(bike2)

    print("\nAvailable bikes after adding:")
    for b in manager.list_available_bikes():
        print(b)

    # Create a customer
    customer = Customer(id=1, name="Darian Porch", phone="555-1234")

    # Rent a bike
    ticket = manager.create_ticket(customer=customer, bike_id=1, hours=2)
    print("\nCreated ticket:")
    print(ticket)

    print("\nAvailable bikes after renting:")
    for b in manager.list_available_bikes():
        print(b)

    # Return the bike
    returned_ticket = manager.return_bike(ticket.id)
    print("\nReturned ticket:")
    print(returned_ticket)

    print("\nAvailable bikes after return:")
    for b in manager.list_available_bikes():
        print(b)

if __name__ == "__main__":
    main()