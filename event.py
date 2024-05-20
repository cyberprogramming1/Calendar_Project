class Event:
    def __init__(self, id, title, description, event_date):
        self.id = id
        self.title = title
        self.description = description
        self.event_date = event_date

class RecurringEvent:
    def __init__(self, id, title, description, start_date, end_date, recurrence_pattern):
        self.id = id
        self.title = title
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.recurrence_pattern = recurrence_pattern
