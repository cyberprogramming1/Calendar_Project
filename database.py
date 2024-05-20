import pyodbc

class Database:
    def __init__(self, server, database):
        self.conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;')
        self.cursor = self.conn.cursor()

    def create_locations_table(self):
        """Create the locations table if it does not exist."""
        sql = """
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'locations')
            BEGIN
                CREATE TABLE locations (
                    id INT PRIMARY KEY IDENTITY(1,1),
                    name NVARCHAR(100),
                    address NVARCHAR(255)
                );
            END
        """
        self.cursor.execute(sql)
        self.conn.commit()
        print("Locations table created or already exists.")
    
    def create_event_locations_table(self):
        """Create the event_locations table if it does not exist."""
        sql = """
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'event_locations')
            BEGIN
                CREATE TABLE event_locations (
                    event_id INT,
                    location_id INT,
                    PRIMARY KEY (event_id, location_id),
                    FOREIGN KEY (event_id) REFERENCES events(id),
                    FOREIGN KEY (location_id) REFERENCES locations(id)
                );
            END
        """
        self.cursor.execute(sql)
        self.conn.commit()
        print("Event_locations table created or already exists.")
    
    
