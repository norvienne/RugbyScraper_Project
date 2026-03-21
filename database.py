import sqlite3
import os
from datetime import datetime


def get_database_path():
    base_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_directory, "data", "rugby.db")


def create_connection():
    connection = sqlite3.connect(get_database_path())
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_teams_table():
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS teams (
                team_id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_name TEXT NOT NULL UNIQUE,
                short_name TEXT,
                country TEXT,
                league TEXT
            )
        """)
        connection.commit()
    except sqlite3.Error as e:
        print(f"error creating teams table: {e}")
    finally:
        connection.close()


def create_competitions_table():
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS competitions (
                competition_id INTEGER PRIMARY KEY AUTOINCREMENT,
                competition_name TEXT NOT NULL,
                competition_type TEXT,
                season TEXT
            )
        """)
        connection.commit()
    except sqlite3.Error as e:
        print(f"error creating competitions table: {e}")
    finally:
        connection.close()


def create_standings_table():
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS standings (
                standing_id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id INTEGER NOT NULL,
                competition_id INTEGER NOT NULL,
                position INTEGER,
                played INTEGER,
                won INTEGER,
                drawn INTEGER,
                lost INTEGER,
                points_for INTEGER,
                points_against INTEGER,
                points_diff TEXT,
                points INTEGER,
                scraped_date TEXT,
                FOREIGN KEY (team_id) REFERENCES teams (team_id),
                FOREIGN KEY (competition_id) REFERENCES competitions (competition_id),
                UNIQUE (team_id, competition_id, scraped_date)
            )
        """)
        connection.commit()
    except sqlite3.Error as e:
        print(f"error creating standings table: {e}")
    finally:
        connection.close()


def create_matches_table():
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS matches (
                match_id INTEGER PRIMARY KEY AUTOINCREMENT,
                competition_id INTEGER NOT NULL,
                home_team TEXT NOT NULL,
                away_team TEXT NOT NULL,
                home_score INTEGER,
                away_score INTEGER,
                match_date TEXT,
                FOREIGN KEY (competition_id) REFERENCES competitions (competition_id),
                UNIQUE (competition_id, home_team, away_team, match_date)
            )
        """)
        connection.commit()
    except sqlite3.Error as e:
        print(f"error creating matches table: {e}")
    finally:
        connection.close()


def create_scrape_log_table():
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scrape_log (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                scraped_at TEXT NOT NULL,
                records_found INTEGER,
                status TEXT
            )
        """)
        connection.commit()
    except sqlite3.Error as e:
        print(f"error creating scrape_log table: {e}")
    finally:
        connection.close()


def insert_team(team_name, short_name, country, league):
    if not team_name:
        return
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            INSERT OR IGNORE INTO teams (team_name, short_name, country, league)
            VALUES (?, ?, ?, ?)
        """,
            (team_name, short_name, country, league),
        )
        connection.commit()
    except sqlite3.Error as e:
        print(f"error inserting team {team_name}: {e}")
    finally:
        connection.close()


def insert_competition(competition_name, competition_type, season):
    if not competition_name:
        return
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            INSERT OR IGNORE INTO competitions (competition_name, competition_type, season)
            VALUES (?, ?, ?)
        """,
            (competition_name, competition_type, season),
        )
        connection.commit()
    except sqlite3.Error as e:
        print(f"error inserting competition {competition_name}: {e}")
    finally:
        connection.close()


def insert_standing(
    team_id,
    competition_id,
    position,
    played,
    won,
    drawn,
    lost,
    points_for,
    points_against,
    points_diff,
    points,
    scraped_date,
):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            INSERT OR IGNORE INTO standings 
            (team_id, competition_id, position, played, won, drawn, lost,
             points_for, points_against, points_diff, points, scraped_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                team_id,
                competition_id,
                position,
                played,
                won,
                drawn,
                lost,
                points_for,
                points_against,
                points_diff,
                points,
                scraped_date,
            ),
        )
        connection.commit()
    except sqlite3.Error as e:
        print(f"error inserting standing: {e}")
    finally:
        connection.close()


def insert_match(
    competition_id, home_team, away_team, home_score, away_score, match_date
):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            INSERT OR IGNORE INTO matches 
            (competition_id, home_team, away_team, home_score, away_score, match_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (competition_id, home_team, away_team, home_score, away_score, match_date),
        )
        connection.commit()
    except sqlite3.Error as e:
        print(f"error inserting match {home_team} vs {away_team}: {e}")
    finally:
        connection.close()


def log_scrape(records_found, status):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO scrape_log (scraped_at, records_found, status)
            VALUES (?, ?, ?)
        """,
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), records_found, status),
        )
        connection.commit()
    except sqlite3.Error as e:
        print(f"error logging scrape: {e}")
    finally:
        connection.close()


def get_known_match_ids(competition_id):
    """returns a set of match identifiers already in the database"""
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT home_team, away_team, match_date
            FROM matches
            WHERE competition_id = ?
            """,
            (competition_id,),
        )
        rows = cursor.fetchall()
        return {(r[0], r[1], r[2]) for r in rows}
    except sqlite3.Error as e:
        print(f"error fetching known matches: {e}")
        return set()
    finally:
        connection.close()


def initialise_database():
    create_teams_table()
    create_competitions_table()
    create_standings_table()
    create_matches_table()
    create_scrape_log_table()


if __name__ == "__main__":
    initialise_database()
    print("database ready!")
