import sqlite3


DATABASE = "globetrotter.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db():
    connection = get_db_connection()

    connection.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            cover_photo TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
                REFERENCES users (id)
                ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS cities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            country TEXT NOT NULL,
            region TEXT,
            cost_index REAL DEFAULT 0,
            popularity REAL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS trip_stops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trip_id INTEGER NOT NULL,
            city_id INTEGER NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            stop_order INTEGER NOT NULL,

            FOREIGN KEY (trip_id)
                REFERENCES trips (id)
                ON DELETE CASCADE,

            FOREIGN KEY (city_id)
                REFERENCES cities (id)
        );

        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            activity_type TEXT,
            cost REAL DEFAULT 0,
            duration REAL DEFAULT 0,

            FOREIGN KEY (city_id)
                REFERENCES cities (id)
        );

        CREATE TABLE IF NOT EXISTS trip_activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trip_stop_id INTEGER NOT NULL,
            activity_id INTEGER NOT NULL,
            activity_date TEXT NOT NULL,
            start_time TEXT,
            cost REAL DEFAULT 0,

            FOREIGN KEY (trip_stop_id)
                REFERENCES trip_stops (id)
                ON DELETE CASCADE,

            FOREIGN KEY (activity_id)
                REFERENCES activities (id)
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trip_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            amount REAL NOT NULL,

            FOREIGN KEY (trip_id)
                REFERENCES trips (id)
                ON DELETE CASCADE
        );
    """)

    connection.commit()
    connection.close()