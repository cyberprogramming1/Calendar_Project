from datetime import datetime, timedelta
from event import Event, RecurringEvent
from location import Location
from database import Database
import calendar

class Calendar_file:
    def __init__(self, server, database):
        self.db = Database(server, database)
        self.db.create_locations_table()
        self.db.create_event_locations_table()
        self.conn = self.db.conn  # Initialize conn attribute
        self.cursor = self.db.cursor  # Initialize cursor attribute
    
    def add_event_location(self, event_id, location_id):
        sql = "INSERT INTO event_locations (event_id, location_id) VALUES (?, ?)"
        self.db.cursor.execute(sql, (event_id, location_id))
        self.db.conn.commit()

    def remove_event_location(self, event_id, location_id):
        sql = "DELETE FROM event_locations WHERE event_id = ? AND location_id = ?"
        self.db.cursor.execute(sql, (event_id, location_id))
        self.db.conn.commit()

    def add_location(self, location):
        sql = "INSERT INTO locations (name, address) VALUES (?, ?)"
        self.db.cursor.execute(sql, (location.name, location.address))
        self.db.conn.commit()

    def edit_location(self, location_id, name, address):
        sql = "UPDATE locations SET name = ?, address = ? WHERE id = ?"
        self.db.cursor.execute(sql, (name, address, location_id))
        self.db.conn.commit()

    def delete_location(self, location_id):
        sql_delete_location = "DELETE FROM locations WHERE id = ?"
        self.db.cursor.execute(sql_delete_location, (location_id,))
        self.db.conn.commit() 

    def close_connection(self):
        self.db.conn.close()

    def filter_events(self, **kwargs):
        """
        Filter events based on provided criteria.

        Supported criteria:
        - date (datetime.date): Filter events on a specific date.
        - title (str): Filter events by title.
        - location_id (int): Filter events by location ID.
        """
        filters = []
        params = []

        if 'date' in kwargs:
            filters.append("event_date = ?")
            params.append(kwargs['date'])

        if 'title' in kwargs:
            filters.append("title LIKE ?")
            params.append('%' + kwargs['title'] + '%')

        if 'location_id' in kwargs:
            filters.append("location_id = ?")
            params.append(kwargs['location_id'])

        if filters:
            where_clause = "WHERE " + " AND ".join(filters)
        else:
            where_clause = ""

        sql = f"SELECT e.id, e.title, e.description, e.event_date FROM events e JOIN event_locations el ON e.id = el.event_id {where_clause}"
        self.db.cursor.execute(sql, params)
        rows = self.db.cursor.fetchall()
        events = [Event(row.id, row.title, row.description, row.event_date) for row in rows]
        return events

    def edit_event(self, event_id, title, description, event_date):
        """Edit an existing event in the database."""
        sql = "UPDATE events SET title = ?, description = ?, event_date = ? WHERE id = ?"
        self.cursor.execute(sql, (title, description, event_date, event_id))
        self.conn.commit()
        print(f"Event with ID {event_id} edited successfully.")
    
    def delete_event(self, event_id):
        """Delete an event from the database by its ID."""
        sql_delete_event = "DELETE FROM events WHERE id = ?"
        self.cursor.execute(sql_delete_event, (event_id,))
        self.conn.commit()
        print(f"Event with ID {event_id} deleted successfully.")


    def add_event(self, event, locations=None):
        sql = "INSERT INTO events (title, description, event_date) VALUES (?, ?, ?)"
        self.cursor.execute(sql, (event.title, event.description, event.event_date))
        self.conn.commit()
        event_id = self.cursor.execute("SELECT SCOPE_IDENTITY()").fetchone()[0]

        if locations:
            for location in locations:
                location_id = self._get_or_create_location(location)
                self._associate_event_with_location(event_id, location_id)

    def add_recurring_event(self, recurring_event):
        sql = "INSERT INTO recurring_events (title, description, start_date, end_date, recurrence_pattern) VALUES (?, ?, ?, ?, ?)"
        self.cursor.execute(sql, (recurring_event.title, recurring_event.description, recurring_event.start_date, recurring_event.end_date, recurring_event.recurrence_pattern))
        self.conn.commit()
        recurring_event_id = self.cursor.execute("SELECT SCOPE_IDENTITY()").fetchone()[0]
        print(f"Debug: Recurring Event ID {recurring_event_id} added.")
        self._generate_recurring_events(recurring_event)

    def _generate_recurring_events(self, recurring_event):
        current_date = recurring_event.start_date
        while current_date <= recurring_event.end_date:
            event = Event(None, recurring_event.title, recurring_event.description, current_date)
            self.add_event(event)
            if recurring_event.recurrence_pattern == 'daily':
                current_date += timedelta(days=1)
            elif recurring_event.recurrence_pattern == 'weekly':
                current_date += timedelta(weeks=1)
            elif recurring_event.recurrence_pattern == 'monthly':
                current_date = (current_date.replace(day=1) + timedelta(days=32)).replace(day=recurring_event.start_date.day)

    def _get_or_create_location(self, location):
        sql = "SELECT id FROM locations WHERE name = ? AND address = ?"
        result = self.cursor.execute(sql, (location.name, location.address)).fetchone()
        if result:
            return result[0]
        else:
            sql = "INSERT INTO locations (name, address) VALUES (?, ?)"
            self.cursor.execute(sql, (location.name, location.address))
            self.conn.commit()
            return self.cursor.execute("SELECT SCOPE_IDENTITY()").fetchone()[0]

    def _associate_event_with_location(self, event_id, location_id):
        sql = "INSERT INTO event_locations (event_id, location_id) VALUES (?, ?)"
        self.cursor.execute(sql, (event_id, location_id))
        self.conn.commit()

    def get_events(self, date):
        sql = "SELECT e.id, e.title, e.description, e.event_date FROM events e WHERE e.event_date = ?"
        self.cursor.execute(sql, (date,))
        rows = self.cursor.fetchall()
        events = [Event(row.id, row.title, row.description, row.event_date) for row in rows]
        return events

    def display_monthly_calendar(self, year, month):
        cal = calendar.monthcalendar(year, month)
        for week in cal:
            for day in week:
                if day == 0:
                    print("   ", end=' ')
                else:
                    events = self.get_events(datetime(year, month, day).date())
                    if events:
                        print(f"{day:2}*", end=' ')
                    else:
                        print(f"{day:2} ", end=' ')
            print()

    def close_connection(self):
        self.conn.close()

