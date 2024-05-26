from event import Event, RecurringEvent
from datetime import datetime
from tabulate import tabulate

class EventActions:
    def __init__(self, calendar):
        self.calendar = calendar

    def add_event(self):
        title = input("Enter event title: ")
        description = input("Enter event description: ")
        event_date = input("Enter event date (YYYY-MM-DD): ")
        new_event = Event(None, title, description, datetime.strptime(event_date, "%Y-%m-%d").date())
        self.calendar.add_event(new_event)
        print("Event added successfully.")

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
        print(f"Events for today: {today_date}")
        today_events = self.calendar.get_events(today_date)
        if not today_events:
            print("No events for today.")
        else:
            try:
                event_data = [(event.event_date, event.title, event.description) for event in today_events]
                headers = ["Date", "Title", "Description"]
                print(tabulate(event_data, headers=headers, tablefmt="grid"))
            except ImportError:
                print("Table display unavailable. Here are the events:")
                for event in today_events:
                    print(f"{event.event_date}: {event.title} - {event.description}")

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
            try:
                event_data = [(event.id, event.title, event.description, event.event_date) for event in filtered_events]
                headers = ["ID", "Title", "Description", "Date"]
                print(tabulate(event_data, headers=headers, tablefmt="grid"))
            except ImportError:
                for event in filtered_events:
                    print(f"ID: {event.id}, Title: {event.title}, Description: {event.description}, Date: {event.event_date}")
        else:
            print("No events found matching the criteria.")

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

    def display_monthly_calendar(self):
        year = datetime.now().year
        month = datetime.now().month
        self.calendar.display_monthly_calendar(year, month)
