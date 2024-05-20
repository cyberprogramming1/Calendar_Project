from calendar_file import Calendar_file
from event import Event, RecurringEvent
from datetime import datetime, timedelta
from location import Location

class CalendarApp:
    def __init__(self, server, database):
        self.calendar = Calendar_file(server, database)

    def run(self):
         while True:
            print("\n1. Add Event")
            print("2. Edit Event")
            print("3. Delete Event")
            print("4. Display Events for Today")
            print("5. Display Monthly Calendar")
            print("6. Add Recurring Event")
            print("7. Filter Events")
            print("8. Add Location")
            print("9. Edit Location")
            print("10. Delete Location")
            print("11. Add Event Location")
            print("12. Remove Event Location")
            print("13. Exit")

            choice = input("\nEnter your choice: ")

            if choice == '1':
                self.add_event()
            elif choice == '2':
                self.edit_event()
            elif choice == '3':
                self.delete_event()
            elif choice == '4':
                self.display_events_today()
            elif choice == '5':
                self.display_monthly_calendar()
            elif choice == '6':
                self.add_recurring_event()
            elif choice == '7':
                self.filter_events()
            elif choice == '8':
                self.add_location()
            elif choice == '9':
                self.edit_location()
            elif choice == '10':
                self.delete_location()
            elif choice == '11':
                self.add_event_location()
            elif choice == '12':
                self.remove_event_location()
            elif choice == '13':
                self.calendar.close_connection()
                break
            else:
                print("Invalid choice. Please try again.")

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
    
    def filter_events(self):
        criteria = {}
        date = input("Enter event date (YYYY-MM-DD): ")
        if date:
            criteria['date'] = date
        title = input("Enter event title: ")
        if title:
            criteria['title'] = title
        location_id = input("Enter location ID: ")
        if location_id:
            criteria['location_id'] = int(location_id)
        
        filtered_events = self.calendar.filter_events(**criteria)
        if filtered_events:
            print("Filtered Events:")
            for event in filtered_events:
                print(f"ID: {event.id}, Title: {event.title}, Description: {event.description}, Date: {event.event_date}")
        else:
            print("No events found matching the criteria.")

    def add_event(self):
        title = input("Enter event title: ")
        description = input("Enter event description: ")
        event_date = input("Enter event date (YYYY-MM-DD): ")
        new_event = Event(None, title, description, datetime.strptime(event_date, "%Y-%m-%d").date())
        self.calendar.add_event(new_event)
        print("Event added successfully.")

    def add_recurring_event(self):
        title = input("Enter recurring event title: ")
        description = input("Enter recurring event description: ")
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")

        valid_patterns = ['daily', 'weekly', 'monthly']
        while True:
            recurrence_pattern = input("Enter recurrence pattern (daily, weekly, monthly): ").lower()
            if recurrence_pattern in valid_patterns:
                break
            else:
                print("Invalid recurrence pattern. Please enter 'daily', 'weekly', or 'monthly'.")

        new_recurring_event = RecurringEvent(None, title, description, datetime.strptime(start_date, "%Y-%m-%d").date(), datetime.strptime(end_date, "%Y-%m-%d").date(), recurrence_pattern)
        self.calendar.add_recurring_event(new_recurring_event)
        print("Recurring event added successfully.")

    def edit_event(self):
        event_id = input("Enter event id: ")
        title = input("Enter new event title: ")
        description = input("Enter new event description: ")
        event_date = input("Enter new event date (YYYY-MM-DD): ")
        self.calendar.edit_event(int(event_id), title, description, datetime.strptime(event_date, "%Y-%m-%d").date())
        print("Event edited successfully.")

    def delete_event(self):
        event_id = input("Enter event id: ")
        self.calendar.delete_event(int(event_id))
        print("Event deleted successfully.")

    def display_events_today(self):
        today_date = datetime.now().date()
        print(f"Debug: Displaying events for today: {today_date}")
        today_events = self.calendar.get_events(today_date)
        if not today_events:
            print("No events for today.")
        for event in today_events:
            print(f"{event.event_date}: {event.title} - {event.description}")

    def display_monthly_calendar(self):
        year = datetime.now().year
        month = datetime.now().month
        self.calendar.display_monthly_calendar(year, month)

