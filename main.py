from calendar_app import CalendarApp

def main():
    server_name = 'DESKTOP-NA23RM9'  
    database_name = 'Calendar'  

    app = CalendarApp(server_name, database_name)
    app.run()

if __name__ == "__main__":
    main()
