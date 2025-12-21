# interacts with the backend of the bycycle app
# this is the frontend of the bycycle app

# 5 different pages:
# Main page: Buttons for New Ticket, Return Bike, Inventory, Reports
# New Ticket form: Enter customer info, select bike, enter planned rental hours
# Return Bike form: Enter ticket ID to close ticket and calculate fees
# Inventory: Add or edit bikes
# Reports: Show total active rentals and revenue


from datetime import datetime
from tkinter import messagebox
from tkinter import ttk

import random
import tkinter
import re
import sv_ttk
import rental_manager
import customer
import bike
import math

class BikeRentalApp:
    def __init__(self, root):
        self.root = root
        
        # variables
        self.delete_clicks = 0
        
        # initialize the rental manager
        self.rental_backend = rental_manager.RentalManager()

        # title
        self.root.title("Bluegrass Bicycle Company - Bike Rental Ticket System")

        # window size
        APP_WIDTH = 1280
        APP_HEIGHT = 720

        self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.root.minsize(APP_WIDTH, APP_HEIGHT)

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        self.left_frame = ttk.Frame(self.root, width=640, height=620)
        self.left_frame.pack(side="left", fill="y", expand=True)

        # for GUI responses
        self.response_frame = ttk.Frame(self.root, width=2, height=80)
        self.response_frame.pack(side="bottom", fill="x", expand=True)

        self.invisible_text = ttk.Label(self.response_frame, text="", anchor="center")
        self.invisible_text.pack(pady=10)

        self.right_frame = ttk.Frame(self.root, width=640, height=620)
        self.right_frame.pack(side="right", fill="y", expand=True)

        # Setup the initial view
        self.main_page()

    # helper functions

    def create_label(self, parent, text, **pack_kwargs):
        """Creates, packs, and returns a Label."""
        label = ttk.Label(parent, text=text)
        label.pack(**pack_kwargs)
        return label

    def create_entry(self, parent, width=64, **pack_kwargs):
        """Creates, packs, and returns an Entry."""
        entry = ttk.Entry(parent, width=width)
        entry.pack(**pack_kwargs)
        return entry

    # main page
    def main_page(self):
        """
        Home page to navigate to other pages.
        """
        self.clear_response()

        # create a frame for the main page
        main_frame = ttk.Frame(self.left_frame)
        main_frame.pack(fill="both", expand=True)
        self.root["bg"] = "#1e1e1e"
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        company_label = ttk.Label(main_frame, text="Bluegrass Bicycle Company", font=("Helvetica", 16))
        company_label.pack(pady=10)

        application_label = ttk.Label(main_frame, text="Bike Rental Ticket System", font=("Helvetica", 14))
        application_label.pack(pady=10)

        # create buttons for the main page
        new_ticket_button = ttk.Button(main_frame, text="New Ticket", command=lambda: self.clear_right_frame() or self.new_ticket_form(), width=32)
        new_ticket_button.pack(pady=10)

        return_bike_button = ttk.Button(main_frame, text="Return Bike", command=lambda: self.clear_right_frame() or self.return_bike_form(), width=32)
        return_bike_button.pack(pady=10)

        inventory_button = ttk.Button(main_frame, text="Inventory", command=lambda: self.clear_right_frame() or self.inventory_form(), width=32)
        inventory_button.pack(pady=10)

        reports_button = ttk.Button(main_frame, text="Reports", command=lambda: self.clear_right_frame() or self.reports_form(), width=32)
        reports_button.pack(pady=10)

        # prompt user to select a page

        txt_frame = ttk.Label(self.right_frame, text="Bike Rental Ticket System")
        txt_frame.pack(pady=10)

        txt_label = ttk.Label(txt_frame, text="Select a page to navigate to first.", width=64, anchor="center")
        txt_label.pack(pady=10)


    def get_available_bike_list(self):
        """
        Get the list of bikes from the backend.
        """
        # call the backend API to get the list of bikes
        bike_list = self.rental_backend.list_available_bikes()
        return bike_list

    # new ticket form
    def new_ticket_form(self):
        """
        Create a new ticket form for consumers, select bike and enter planned rental hours.
        """
        self.clear_response()

        # create a frame for the new ticket form
        new_ticket_frame = ttk.Frame(self.right_frame)
        new_ticket_frame.pack(fill="both", expand=True)

        txt_label = ttk.Label(new_ticket_frame, text="New Ticket Form", width=64, anchor="center")
        txt_label.pack(pady=10)

        # create labels and entry fields for the new ticket form
        customer_name_label = ttk.Label(new_ticket_frame, text="Customer Name")
        customer_name_label.pack(pady=5)

        customer_name_entry = ttk.Entry(new_ticket_frame, width=64)
        customer_name_entry.pack(pady=5)

        customer_phone_label = ttk.Label(new_ticket_frame, text="Customer Phone")
        customer_phone_label.pack(pady=5)

        customer_phone_entry = ttk.Entry(new_ticket_frame, width=64)
        customer_phone_entry.pack(pady=5)

        bike_selection_label = ttk.Label(new_ticket_frame, text="Select Bike")
        bike_selection_label.pack(pady=5)

        # dropdown for bike selection
        bike_list = self.get_available_bike_list()
        bike_options = [f"ID: {bike.id}, {bike.make} {bike.model}, Rate: ${bike.hourly_rate}/hr" for bike in bike_list]
        bike_selection_var = tkinter.StringVar()
        bike_selection_dropdown = ttk.Combobox(new_ticket_frame, textvariable=bike_selection_var, values=bike_options, width=62, state="readonly")
        bike_selection_dropdown.pack(pady=5)

        rental_hours_label = ttk.Label(new_ticket_frame, text="Planned Rental Hours")
        rental_hours_label.pack(pady=5)

        rental_hours_entry = ttk.Entry(new_ticket_frame, width=64)
        rental_hours_entry.pack(pady=5)

        personal_notes_label = ttk.Label(new_ticket_frame, text="Personal Notes (Optional)")
        personal_notes_label.pack(pady=5)

        personal_notes_entry = ttk.Entry(new_ticket_frame, width=64)
        personal_notes_entry.pack(pady=5)

        # create a button to submit the new ticket form
        submit_button = ttk.Button(new_ticket_frame, text="Submit", command=lambda: self.submit_new_ticket(customer_name_entry, customer_phone_entry, bike_selection_var, rental_hours_entry, personal_notes_entry))
        submit_button.pack(pady=10)

        # clear fields button
        clear_fields = ttk.Button(new_ticket_frame, text="Clear Fields", command=lambda: customer_name_entry.delete(0, 'end') or customer_phone_entry.delete(0, 'end') or rental_hours_entry.delete(0, 'end'))
        clear_fields.pack(pady=10)

    # return bike form
    def return_bike_form(self):
        """
        Return a bike form to close the ticket and calculate fees.
        """
        self.clear_response()

        # create a frame for the return bike form
        return_bike_frame = ttk.Frame(self.right_frame)
        return_bike_frame.pack(fill="both", expand=True)

        txt_label = ttk.Label(return_bike_frame, text="Return Bike Form", width=64, anchor="center")
        txt_label.pack(pady=10)

        txt_label_1 = ttk.Label(return_bike_frame, text="Enter Ticket ID to return bike", width=64, anchor="center")
        txt_label_1.pack(pady=10)

        # create labels and entry fields for the return bike form
        ticket_id_label = ttk.Label(return_bike_frame, text="Ticket ID")
        ticket_id_label.pack(pady=5)

        ticket_id_entry = ttk.Entry(return_bike_frame, width=64)
        ticket_id_entry.pack(pady=5)

        # alternative return fields could be customer name and phone number

        txt_label_2 = ttk.Label(return_bike_frame, text="OR Enter Customer Information", width=64, anchor="center")
        txt_label_2.pack(pady=10)

        customer_name_label = ttk.Label(return_bike_frame, text="Customer Name")
        customer_name_label.pack(pady=5)

        customer_name_entry = ttk.Entry(return_bike_frame, width=64)
        customer_name_entry.pack(pady=5)

        customer_phone_label = ttk.Label(return_bike_frame, text="Customer Phone")
        customer_phone_label.pack(pady=5)

        customer_phone_entry = ttk.Entry(return_bike_frame, width=64)
        customer_phone_entry.pack(pady=5)

        # create a button to submit the return bike form
        submit_button = ttk.Button(return_bike_frame, text="Submit", command=lambda: self.submit_return_bike(ticket_id_entry, customer_name_entry, customer_phone_entry))
        submit_button.pack(pady=10)

        # clear fields button
        clear_fields = ttk.Button(return_bike_frame, text="Clear Fields", command=lambda: ticket_id_entry.delete(0, 'end') or customer_name_entry.delete(0, 'end') or customer_phone_entry.delete(0, 'end'))
        clear_fields.pack(pady=10)

    # inventory form
    def inventory_form(self):
        """
        Inventory form to add or edit bikes.
        """
        self.clear_response()

        # create a frame for the inventory form
        inventory_frame = ttk.Frame(self.right_frame)
        inventory_frame.pack(fill="both", expand=True)

        txt_label = ttk.Label(inventory_frame, text="Inventory Form", width=64, anchor="center")
        txt_label.pack(pady=10)

        # view inventory button
        view_inventory_button = ttk.Button(inventory_frame, text="View Inventory", command=self.submit_view_inventory)
        view_inventory_button.pack(pady=10)

        # add bike button
        add_bike_button = ttk.Button(inventory_frame, text="Add Bike", command=self.submit_add_bike)
        add_bike_button.pack(pady=10)

        # edit bike button
        edit_bike_button = ttk.Button(inventory_frame, text="Edit Bike", command=self.submit_edit_bike)
        edit_bike_button.pack(pady=10)

    # reports form
    def reports_form(self):
        """
        Reports form to show total active rentals and revenue.
        """

        # create a frame for the reports form
        reports_frame = ttk.Frame(self.right_frame)
        reports_frame.pack(fill="both", expand=True)

        txt_label = ttk.Label(reports_frame, text="Reports Form", width=64, anchor="center")
        txt_label.pack(pady=10)

        # click to get reports
        submit_button = ttk.Button(reports_frame, text="Get Reports", command=self.submit_reports)
        submit_button.pack(pady=10)

        submit_full_reports = ttk.Button(reports_frame, text="Full Reports", command=lambda: self.submit_reports(all_reports=True))
        submit_full_reports.pack(pady=10)

    # submit functions
    def submit_new_ticket(self, customer_name_entry, customer_phone_entry, bike_selection_var, rental_hours_entry, personal_notes_entry):
        """
        Submit the new ticket form.
        """
        # validate inputs
        if not customer_name_entry.get() or not customer_phone_entry.get() or not bike_selection_var.get() or not rental_hours_entry.get():
            self.raise_error("All fields are required.")
            return
        
        # validate types
        try:
            int(rental_hours_entry.get())
        except ValueError:
            self.raise_error("Planned rental hours must be an integer.")
            return
        
        # make customer object
        customer_name = customer_name_entry.get()
        customer_phone = customer_phone_entry.get()

        # simple regex for phone: allows digits, dashes, spaces, parens
        phone_pattern = re.compile(r"^[\d\-\(\)\s]+$")
        if not phone_pattern.match(customer_phone_entry.get()):
            self.raise_error("Invalid phone number format.")
            return

        customer_obj = customer.Customer(id=None, name=customer_name, phone=customer_phone)

        # repack values
        customer_name = customer_name_entry.get() 
        bike_id = int(bike_selection_var.get().split(",")[0].split(":")[1].strip())
        rental_hours = int(rental_hours_entry.get())
        personal_notes = personal_notes_entry.get()

        try:
            ticket = self.rental_backend.create_ticket(customer_obj, bike_id, rental_hours, personal_notes)
            print("New ticket created:", ticket)
            self.raise_response(f"Ticket ID {ticket.id} created successfully for {customer_name}.")
        except ValueError as e:
            print("Error creating ticket:", e)
            self.raise_error(str(e))

    def submit_return_bike(self, ticket_id_entry, customer_name_entry, customer_phone_entry):
        """
        Submit the return bike form.
        """
        self.clear_response()

        # check if ticket is blank
        if not ticket_id_entry.get() == "":
            print("ticket id provided")
            # ticket is provided
            try:
                ticket_id = int(ticket_id_entry.get())

                # check if ticket exists
                ticket = self.rental_backend.get_ticket(ticket_id)
                if not ticket:
                    self.raise_error("Ticket ID not found.")
                    return
                
                if ticket.end_time != "":
                    self.raise_response(f"Bike ID {ticket.bike['id']} has already been returned on {self.iso_to_datetime(ticket.end_time)}.")
                    return
                
                returned_ticket = self.rental_backend.close_ticket(ticket_id)

                response_txt_label = f"Bike ID {returned_ticket.bike['id']} returned successfully.\n"\
                                     f"Total Fee: ${returned_ticket.total_fee} for {math.ceil((datetime.fromisoformat(returned_ticket.end_time) - datetime.fromisoformat(returned_ticket.start_time)).total_seconds() / 3600)} hours rented."
                print("Bike returned:", returned_ticket)
                self.raise_response(response_txt_label)

            except ValueError as e:
                print("Error returning bike:", e)
                self.raise_error(str(e))
        
        else:
            if not customer_name_entry.get() or not customer_phone_entry.get():
                self.raise_error("Either Ticket ID or Customer Information is required.")
                return
            
            print("customer info provided")
            
            # find ticket by customer info
            customer_name = str(customer_name_entry.get())
            customer_phone = str(customer_phone_entry.get())

            # find active tickets by customer info
            tickets = self.rental_backend.find_active_tickets_by_customer(customer_name, customer_phone)

            # output to user in case of multiple matches or no matches
            if len(tickets) == 0:
                self.raise_error("No active tickets found for the provided customer information. Please return with a Ticket ID.")
                return
            elif len(tickets) > 1:
                ticket_ids = [str(ticket.id) for ticket in tickets]
                self.raise_response(f"Multiple active tickets found for the provided customer information. Please return with a Ticket ID. Matching Ticket IDs: {', '.join(ticket_ids)}")

                # display matched tickets
                scrollable_content = self.create_scrollable_frame(self.right_frame)

                txt = ""

                for ticket in tickets:
                    txt += f"Ticket ID: {ticket.id}, Bike ID: {ticket.bike['id']}, \nRented by {ticket.customer['name']} with phone {ticket.customer['phone']}, \nStart Time: {self.iso_to_datetime(ticket.start_time)}, Planned Hours: {ticket.planned_hours}\n\n"

                tickets_label = ttk.Label(scrollable_content, text=txt, justify="left")
                tickets_label.pack(pady=10)
            else:
                # proceed to return the matched ticket
                try:
                    ticket_to_return = tickets[0]
                    returned_ticket = self.rental_backend.close_ticket(ticket_to_return.id)
                    response_txt_label = f"Bike ID {returned_ticket.bike['id']} returned successfully.\n"\
                                        f"Total Fee: ${returned_ticket.total_fee} for {math.ceil((datetime.fromisoformat(returned_ticket.end_time) - datetime.fromisoformat(returned_ticket.start_time)).total_seconds() / 3600)} hours rented."
                    print("Bike returned:", returned_ticket)    

                    self.raise_response(response_txt_label)
                except ValueError as e:
                    print("Error returning bike:", e)
                    self.raise_error(str(e))

    def submit_reports(self, all_reports=False):
        """
        Submit the reports form with search functionality.
        """
        # clear frame
        self.clear_right_frame()
        
        # store the current mode (active only vs all history) so the search knows what to filter
        self.report_mode_all = all_reports
        mode_title = "Full History" if all_reports else "Active Rentals"

        txt_label = ttk.Label(self.right_frame, text=f"Reports: {mode_title}", width=64, anchor="center")
        txt_label.pack(pady=10)

        total_rentals = self.rental_backend.total_active_rentals()
        total_rentals_revenue = self.rental_backend.total_revenue()

        stats_frame = ttk.Frame(self.right_frame)
        stats_frame.pack(pady=5)
        
        ttk.Label(stats_frame, text=f"Total Active Rentals: {total_rentals} | Total Revenue: ${total_rentals_revenue}").pack()

        # search controls
        search_frame = ttk.Frame(self.right_frame)
        search_frame.pack(pady=10)

        ttk.Label(search_frame, text="Search Customer:").pack(side="left", padx=5)
        
        report_search_entry = ttk.Entry(search_frame, width=30)
        report_search_entry.pack(side="left", padx=5)
        
        search_button = ttk.Button(search_frame, text="Filter", command=lambda: self.perform_report_search(report_search_entry.get()))
        search_button.pack(side="left", padx=5)

        reset_button = ttk.Button(search_frame, text="Show All", command=lambda: report_search_entry.delete(0, 'end') or self.perform_report_search(""))
        reset_button.pack(side="left", padx=5)

        ttk.Label(self.right_frame, text="Ticket List:", width=64, anchor="center").pack(pady=5)

        # create scrollable frame for results
        self.report_scroll_content = self.create_scrollable_frame(self.right_frame)
        
        # label to hold the list text
        self.report_list_label = ttk.Label(self.report_scroll_content, text="", justify="left")
        self.report_list_label.pack(pady=10)

        # perform initial empty search to load the list
        self.perform_report_search("")

    def perform_report_search(self, query):
        """
        Filters reports based on query and current mode (Active/All).
        """
        active_tickets = self.rental_backend.get_all_tickets()
        reports_str = ""
        
        query = query.lower()

        # iterate through tickets
        matches_found = False
        for ticket in active_tickets:
            # 1. filter by Mode (Active vs All)
            if not self.report_mode_all and ticket.end_time != "":
                continue

            # 2. filter by Search Query
            # check if query matches Customer Name OR Ticket ID
            if query:
                if (query not in ticket.customer['name'].lower()) and (query not in str(ticket.id)):
                    continue

            matches_found = True
            
            # 3. calculate time logic
            hours_passed = 0
            if ticket.end_time == "":
                passed_time = datetime.now() - datetime.fromisoformat(ticket.start_time)
                hours_passed = passed_time.total_seconds() / 3600
            else:
                passed_time = datetime.fromisoformat(ticket.end_time) - datetime.fromisoformat(ticket.start_time)
                hours_passed = passed_time.total_seconds() / 3600

            # 4. build string
            reports_str += f"\nBike ID: {ticket.bike['id']}, {ticket.bike['make']} {ticket.bike['model']}, Rate: ${ticket.bike['hourly_rate']}/hr\n"\
                        f"Rented by {ticket.customer['name']} (Phone: {ticket.customer['phone']})\n"\
                        f"Ticket ID: {ticket.id}, Start Time: {self.iso_to_datetime(ticket.start_time)}\n"\
                        f"Planned Hours: {ticket.planned_hours}, Actual Hours: {math.ceil(hours_passed)}\n"\
                        f"System Notes: {ticket.system_notes}\n"\
                        f"Personal Notes: {ticket.personal_notes}\n"
            
            if ticket.end_time != "":
                reports_str += f"Returned at: {self.iso_to_datetime(ticket.end_time)}, Total Fee: ${ticket.total_fee}\n\n"
            else:
                reports_str += "Currently Rented Out\n\n"

        if not matches_found:
            reports_str = "No tickets found matching your criteria."

        self.report_list_label.config(text=reports_str)

    def submit_view_inventory(self):
        """
        Submit the view inventory form with search functionality.
        """
        self.clear_response()
        self.clear_right_frame()

        title_label = ttk.Label(self.right_frame, text="Bike Inventory", width=64, anchor="center")
        title_label.pack(pady=10)

        # searching controls
        search_frame = ttk.Frame(self.right_frame)
        search_frame.pack(pady=5)

        ttk.Label(search_frame, text="Search:").pack(side="left", padx=5)
        
        search_entry = ttk.Entry(search_frame, width=30)
        search_entry.pack(side="left", padx=5)
        
        search_button = ttk.Button(search_frame, text="Filter", command=lambda: self.perform_inventory_search(search_entry.get()))
        search_button.pack(side="left", padx=5)

        # reset
        reset_button = ttk.Button(search_frame, text="Show All", command=lambda: search_entry.delete(0, 'end') or self.perform_inventory_search(""))
        reset_button.pack(side="left", padx=5)

        self.inventory_subtitle = ttk.Label(self.right_frame, text="Viewing All Bikes", width=64, anchor="center")
        self.inventory_subtitle.pack(pady=5)

        # create a scrollable frame for the inventory list
        # we store the scrollable frame in self so we can reference it if needed, 
        # though strictly we just need to update the label inside it.
        self.inventory_scroll_content = self.create_scrollable_frame(self.right_frame)

        # create the label that will hold the text. We keep a reference (self.inventory_list_label)
        # so the search function can update its text config later.
        self.inventory_list_label = ttk.Label(self.inventory_scroll_content, text="", justify="left")
        self.inventory_list_label.pack(pady=10)

        # populate initially with all bikes
        self.perform_inventory_search("")

        # return to inventory form button
        back_button = ttk.Button(self.right_frame, text="Back to Inventory Menu", command=lambda: self.clear_right_frame() or self.inventory_form())
        back_button.pack(pady=10)

    def perform_inventory_search(self, query):
        """
        Filters inventory list based on query and updates the display label.
        """
        # get full list from backend
        all_bikes = self.rental_backend.list_inventory()
        
        # filter Logic
        if not query:
            filtered_bikes = all_bikes
            self.inventory_subtitle.config(text="Viewing All Bikes")
        else:
            query = query.lower()
            # search by ID, Make, or Model
            filtered_bikes = [
                b for b in all_bikes 
                if query in str(b.id).lower() or 
                   query in b.make.lower() or 
                   query in b.model.lower()
            ]
            self.inventory_subtitle.config(text=f"Search Results for '{query}'")

        # build the display string
        inventory_str = ""
        if not filtered_bikes:
            inventory_str = "No bikes found matching your criteria."
        else:
            for bike in filtered_bikes:
                inventory_str += f"Bike ID: {bike.id}, \n{bike.make} {bike.model}, \nRate: ${bike.hourly_rate}/hr, \nStatus: {bike.status}\n\n"

        # Update the UI
        self.inventory_list_label.config(text=inventory_str)

    def submit_add_bike(self):
        """
        Submit the add bike form.
        """
        self.clear_response()
        self.clear_right_frame()

        title_label = ttk.Label(self.right_frame, text="Add New Bike", width=64, anchor="center")
        title_label.pack(pady=10)

        # create labels and entry fields for adding a new bike
        make_label = ttk.Label(self.right_frame, text="Bike Make")
        make_label.pack(pady=5)

        make_entry = ttk.Entry(self.right_frame, width=64)
        make_entry.pack(pady=5)

        model_label = ttk.Label(self.right_frame, text="Bike Model")
        model_label.pack(pady=5)

        model_entry = ttk.Entry(self.right_frame, width=64)
        model_entry.pack(pady=5)

        # hourly rate
        hourly_rate_label = ttk.Label(self.right_frame, text="Hourly Rate ($)")
        hourly_rate_label.pack(pady=5)

        hourly_rate_entry = ttk.Entry(self.right_frame, width=64)
        hourly_rate_entry.pack(pady=5)

        # create a button to submit the new bike form
        submit_button = ttk.Button(self.right_frame, text="Submit", command=lambda: self.add_bike(make_entry, model_entry, hourly_rate_entry))
        submit_button.pack(pady=10)

        # return to inventory form button
        back_button = ttk.Button(self.right_frame, text="Back to Inventory", command=lambda: self.clear_right_frame() or self.inventory_form())
        back_button.pack(pady=10)

    def add_bike(self, make_entry, model_entry, hourly_rate_entry):
        """
        Add a new bike to the inventory.
        """
        self.clear_response()

        # validate inputs
        if not make_entry.get() or not model_entry.get() or not hourly_rate_entry.get():
            self.raise_error("All fields are required.")
            return
        
        # validate types
        try:
            float(hourly_rate_entry.get())
        except ValueError:
            self.raise_error("Hourly rate must be a number.")
            return

        # create bike object
        bike_make = make_entry.get()
        bike_model = model_entry.get()
        bike_hourly_rate = float(hourly_rate_entry.get())

        bike_id = len(self.rental_backend.inventory) + 1
        new_bike = bike.Bike(id=bike_id, make=bike_make, model=bike_model, rented_by=None, hourly_rate=bike_hourly_rate)

        # add bike to backend
        try:
            self.rental_backend.add_bike(new_bike)
            print("New bike added:", new_bike)
            self.raise_response(f"Bike ID {new_bike.id} - {new_bike.make} {new_bike.model} added successfully to inventory.")
        except ValueError as e:
            print("Error adding bike:", e)
            self.raise_error(str(e))

    def submit_edit_bike(self):
        """
        Submit the edit bike form.
        """
        self.clear_response()
        self.clear_right_frame()

        title_label = ttk.Label(self.right_frame, text="Edit Bikes", width=64, anchor="center")
        title_label.pack(pady=10)

        scrollable_content = self.create_scrollable_frame(self.right_frame)

        for bike in self.rental_backend.inventory:
            bike_frame = ttk.Frame(scrollable_content)
            bike_frame.pack(pady=10, fill="x", expand=True)

            edit_button = ttk.Button(bike_frame, text="Edit", command=lambda b=bike: self.edit_bike_form(b))
            edit_button.pack(side="left", padx=5)

            bike_info_label = ttk.Label(bike_frame, text=f"Bike ID: {bike.id}, {bike.make} {bike.model}\n Rate: ${bike.hourly_rate}/hr, Status: {bike.status}", width=64, anchor="w")
            bike_info_label.pack(side="left", padx=5)

        # return to inventory form button
        back_button = ttk.Button(self.right_frame, text="Back to Inventory", command=lambda: self.clear_right_frame() or self.inventory_form())
        back_button.pack(pady=10)
        
    def edit_bike_form(self, bike):
        """
        Menu to edit a bike's information.
        """
        self.clear_response()
        self.clear_right_frame()

        title_label = ttk.Label(self.right_frame, text=f"Editing", width=64, anchor="center")
        title_label.pack(pady=10)

        bike_label = ttk.Label(self.right_frame, text=f"{bike.make} {bike.model}", font=("Helvetica", 14))
        bike_label.pack(pady=10)

        id_label = ttk.Label(self.right_frame, text=f"Bike ID: {bike.id}")
        id_label.pack(pady=5)

        make_label = ttk.Label(self.right_frame, text="Bike Make")
        make_label.pack(pady=5)

        make_entry = ttk.Entry(self.right_frame, width=64)
        make_entry.insert(0, bike.make)
        make_entry.pack(pady=5)

        model_label = ttk.Label(self.right_frame, text="Bike Model")
        model_label.pack(pady=5)

        model_entry = ttk.Entry(self.right_frame, width=64)
        model_entry.insert(0, bike.model)
        model_entry.pack(pady=5)
        
        # hourly rate
        hourly_rate_label = ttk.Label(self.right_frame, text="Hourly Rate ($)")
        hourly_rate_label.pack(pady=5)

        hourly_rate_entry = ttk.Entry(self.right_frame, width=64)
        hourly_rate_entry.insert(0, str(bike.hourly_rate))
        hourly_rate_entry.pack(pady=5)

        # status
        status_label = ttk.Label(self.right_frame, text=f"Status")
        status_label.pack(pady=5)

        status_options = ['available', 'rented', 'maintenance', 'unavailable', 'missing']

        status_dropdown = ttk.Combobox(self.right_frame, values=status_options, width=64, state="readonly")
        status_dropdown.set(bike.status)
        status_dropdown.pack(pady=5)

        # create a button to submit the edit bike form
        submit_button = ttk.Button(self.right_frame, text="Submit", command=lambda: self.save_edited_bike(bike, bike.id, make_entry, model_entry, hourly_rate_entry, status_dropdown))
        submit_button.pack(pady=10)

        # delete bike button
        delete_button = ttk.Button(self.right_frame, text="Delete Bike", command=lambda: self.delete_bike(bike.id))
        delete_button.pack(pady=10)

        # return to inventory form button
        back_button = ttk.Button(self.right_frame, text="Back to Inventory", command=lambda: self.clear_right_frame() or self.inventory_form())
        back_button.pack(pady=10)

        back_to_list_button = ttk.Button(self.right_frame, text="Back to Bike List", command=lambda: self.clear_right_frame() or self.submit_edit_bike())
        back_to_list_button.pack(pady=10)

    def save_edited_bike(self, bike, bike_id, make_entry, model_entry, hourly_rate_entry, status_dropdown):
        """
        Save the edited bike information.
        """

        self.clear_response()

        # validate inputs
        if not make_entry.get() or not model_entry.get() or not status_dropdown.get() or not hourly_rate_entry.get():
            self.raise_error("All fields are required.")
            return
        
        # validate types
        try:
            float(hourly_rate_entry.get())
        except ValueError:
            self.raise_error("Hourly rate must be a number.")
            return

        # update bike in backend
        try:
            old_val = f"Bike ID {bike.id} - {bike.make} {bike.model}"
            bike = self.rental_backend.set_bike_status(bike_id, 'make', make_entry.get())
            bike = self.rental_backend.set_bike_status(bike_id, 'model', model_entry.get())
            bike = self.rental_backend.set_bike_status(bike_id, 'status', status_dropdown.get())
            bike = self.rental_backend.set_bike_status(bike_id, 'hourly_rate', float(hourly_rate_entry.get()))
            
            print("Bike updated:", bike)
            
            # refresh the inventory form
            self.clear_right_frame()
            self.inventory_form()
            new_str = f"Changed\n{old_val} to\nBike ID {bike.id} - {bike.make} {bike.model} successfully."
            self.raise_response(new_str)
        except ValueError as e:
            print("Error updating bike:", e)
            self.raise_error(str(e))

    def delete_bike(self, bike_id):
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Bike {bike_id}?")
        if confirm:
            try:
                self.rental_backend.remove_bike(bike_id)
                self.clear_right_frame()
                self.inventory_form()
                self.raise_response(f"Bike {bike_id} deleted.")
            except ValueError as e:
                self.raise_error(str(e))

    def clear_right_frame(self):
        """
        Clear the right frame to navigate to a new page.
        """
        for widget in self.right_frame.winfo_children():
            widget.destroy()

    def raise_response(self, message):
        """
        Raise a response message in the response frame.
        """
        for widget in self.response_frame.winfo_children():
            widget.destroy()
        txt_label = ttk.Label(self.response_frame, text=message, foreground="white")
        txt_label.pack(pady=10)

    def raise_error(self, message):
        """
        Raise an error message in the response frame.
        """
        for widget in self.response_frame.winfo_children():
            widget.destroy()
        txt_label = ttk.Label(self.response_frame, text=f"Error: {message}", foreground="red")
        txt_label.pack(pady=10)
        
    def clear_response(self):
        """
        Clear the response frame.
        """
        for widget in self.response_frame.winfo_children():
            widget.destroy()

    def iso_to_datetime(self, iso_str):
        """
        Convert ISO string to readable datetime.
        """
        return datetime.fromisoformat(iso_str).strftime("%Y-%m-%d %H:%M:%S")

    def create_scrollable_frame(self, parent):
        """
        Create a scrollable frame and return the container and content frame.
        """
        scrollable_frame = ttk.Frame(parent)
        scrollable_frame.pack(fill="both", expand=True)

        canvas = tkinter.Canvas(scrollable_frame, height=500)
        scrollbar = ttk.Scrollbar(scrollable_frame, orient="vertical", command=canvas.yview)

        scrollable_content = ttk.Frame(canvas)
        scrollable_content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_content, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return scrollable_content

# launch the app
if __name__ == "__main__":
    root = tkinter.Tk()
    sv_ttk.use_dark_theme(root)
    app = BikeRentalApp(root)
    root.mainloop()