from calendar_file import Calendar_file
from event_actions import EventActions
from location_actions import LocationActions
from datetime import datetime

class CalendarApp:
    def __init__(self, server, database):
        self.calendar = Calendar_file(server, database)
        self.event_actions = EventActions(self.calendar)
        self.location_actions = LocationActions(self.calendar)

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
                self.event_actions.add_event()
            elif choice == '2':
                self.event_actions.edit_event()
            elif choice == '3':
                self.event_actions.delete_event()
            elif choice == '4':
                self.event_actions.display_events_today()
            elif choice == '5':
                self.event_actions.display_monthly_calendar()
            elif choice == '6':
                self.event_actions.add_recurring_event()
            elif choice == '7':
                self.event_actions.filter_events()
            elif choice == '8':
                self.location_actions.add_location()
            elif choice == '9':
                self.location_actions.edit_location()
            elif choice == '10':
                self.location_actions.delete_location()
            elif choice == '11':
                self.location_actions.add_event_location()
            elif choice == '12':
                self.location_actions.remove_event_location()
            elif choice == '13':
                self.calendar.close_connection()
                break
            else:
                print("Invalid choice. Please try again.")
