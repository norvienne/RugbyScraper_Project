import sqlite3
import os


# took me a while to figure this out but this gets the correct path to the database
def get_database_path():
    base_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_directory, "data", "rugby.db")


# simple connection function so i dont repeat this everywhere
def create_connection():
    connection = sqlite3.connect(get_database_path())
    return connection


# teams table stores (basic info about each rugby team)
def create_teams_table():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teams (
            team_id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_name TEXT NOT NULL,
            short_name TEXT,
            country TEXT,
            league TEXT
        )
    """)

    connection.commit()
    connection.close()
    print("Teams table created successfully")


# competitions table  (different rugby competitions)
def create_competitions_table():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS competitions (
            competition_id INTEGER PRIMARY KEY AUTOINCREMENT,
            competition_name TEXT NOT NULL,
            competition_type TEXT,
            season TEXT
        )
    """)

    connection.commit()
    connection.close()
    print("Competitions table created successfully")


create_teams_table()
create_competitions_table()
