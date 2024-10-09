# db_setup.py
import sqlite3

def initialize_db():
    conn = sqlite3.connect('db/vehicle_management.db')
    cursor = conn.cursor()

    # Create Vehicles table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Vehicles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        make TEXT NOT NULL,
        model TEXT NOT NULL,
        year INTEGER,
        license_plate TEXT UNIQUE NOT NULL
    )
    ''')

    # Create Expenses table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicle_id INTEGER,
        description TEXT,
        amount REAL,
        date TEXT,
        FOREIGN KEY(vehicle_id) REFERENCES Vehicles(id)
    )
    ''')

    # Create Maintenance Logs table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS MaintenanceLogs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicle_id INTEGER,
        maintenance_type TEXT,
        date TEXT,
        mileage INTEGER,
        cost REAL,
        next_maintenance_date TEXT,
        FOREIGN KEY(vehicle_id) REFERENCES Vehicles(id)
    )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    initialize_db()
