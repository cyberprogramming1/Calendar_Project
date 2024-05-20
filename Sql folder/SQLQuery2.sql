
create database Calendar;

-- Create the events table
CREATE TABLE events (
    id INT IDENTITY(1,1) PRIMARY KEY,
    title NVARCHAR(255) NOT NULL,
    description NVARCHAR(MAX),
    event_date DATE NOT NULL
);

CREATE TABLE locations (
    id INT PRIMARY KEY IDENTITY(1,1),
    name NVARCHAR(100),
    address NVARCHAR(255)
);

CREATE TABLE event_locations (
    event_id INT,
    location_id INT,
    PRIMARY KEY (event_id, location_id),
    FOREIGN KEY (event_id) REFERENCES events(id),
    FOREIGN KEY (location_id) REFERENCES locations(id)
);

CREATE TABLE recurring_events (
    id INT PRIMARY KEY IDENTITY(1,1),
    title NVARCHAR(100),
    description NVARCHAR(255),
    start_date DATE,
    end_date DATE,
    recurrence_pattern NVARCHAR(50)
);

select * from event_locations;
select * from recurring_events;
select* from events;
select * from locations;

delete event_locations;
delete events;
delete locations;
delete recurring_events;

DBCC CHECKIDENT ('events', RESEED, 0);
DBCC CHECKIDENT ('locations', RESEED, 0);
DBCC CHECKIDENT ('recurring_events', RESEED, 0);

SELECT * FROM events WHERE event_date = '2024-05-14';