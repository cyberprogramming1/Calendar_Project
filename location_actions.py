from location import Location

class LocationActions:
    def __init__(self, calendar):
        self.calendar = calendar

    def add_location(self):
        name = input("Enter location name: ")
        address = input("Enter location address: ")
        new_location = Location(None, name, address)
        self.calendar.add_location(new_location)
        print("Location added successfully.")

    def edit_location(self):
        location_id = input("Enter location ID: ")
        name = input("Enter new location name: ")
        address = input("Enter new location address: ")
        self.calendar.edit_location(int(location_id), name, address)
        print("Location edited successfully.")

    def delete_location(self):
        location_id = input("Enter location ID: ")
        self.calendar.delete_location(int(location_id))
        print("Location deleted successfully.")

    def add_event_location(self):
        event_id = input("Enter event ID: ")
        location_id = input("Enter location ID: ")
        self.calendar.add_event_location(int(event_id), int(location_id))
        print("Event location added successfully.")

    def remove_event_location(self):
        event_id = input("Enter event ID: ")
        location_id = input("Enter location ID: ")
        self.calendar.remove_event_location(int(event_id), int(location_id))
        print("Event location removed successfully.")
