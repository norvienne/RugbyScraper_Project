import csv
import os
from datetime import date
from database import create_connection


def export_standings_to_csv(competition_id, competition_name):
    # pulls standings from db and writes to a csv file in data/exports/
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT t.team_name, s.position, s.played, s.won, s.drawn, s.lost,
               s.points_for, s.points_against, s.points_diff, s.points, s.scraped_date
        FROM standings s
        JOIN teams t ON s.team_id = t.team_id
        WHERE s.competition_id = ?
        AND s.scraped_date = (
            SELECT MAX(scraped_date) FROM standings
            WHERE competition_id = ?
        )
        ORDER BY s.position
        """,
        (competition_id, competition_id),
    )
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print(f"no standings found for {competition_name}")
        return None

    # make sure exports folder exists
    base_dir = os.path.dirname(os.path.abspath(__file__))
    exports_dir = os.path.join(base_dir, "data", "exports")
    os.makedirs(exports_dir, exist_ok=True)

    filename = (
        f"{competition_name.lower().replace(' ', '_')}_{date.today().isoformat()}.csv"
    )
    filepath = os.path.join(exports_dir, filename)

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["Team", "Position", "GP", "W", "D", "L", "PF", "PA", "PD", "Pts", "Date"]
        )
        writer.writerows(rows)

    return filepath
