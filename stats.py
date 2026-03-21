from database import create_connection


def get_team_history(team_name, competition_id):
    """fetches all historical standings for a team in a competition"""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT s.position, s.points, s.scraped_date
        FROM standings s
        JOIN teams t ON s.team_id = t.team_id
        WHERE t.team_name = ?
        AND s.competition_id = ?
        ORDER BY s.scraped_date ASC
        """,
        (team_name, competition_id),
    )
    rows = cursor.fetchall()
    conn.close()

    return [{"position": row[0], "points": row[1], "date": row[2]} for row in rows]


def get_team_form(team_name, results):
    """works out W/L/D form for a team from a results list, last 5 games"""
    form = []
    for r in results:
        if r["home"] == team_name:
            try:
                hs = int(r["home_score"])
                as_ = int(r["away_score"])
                if hs > as_:
                    form.append("W")
                elif hs < as_:
                    form.append("L")
                else:
                    form.append("D")
            except ValueError:
                continue
        elif r["away"] == team_name:
            try:
                hs = int(r["home_score"])
                as_ = int(r["away_score"])
                if as_ > hs:
                    form.append("W")
                elif as_ < hs:
                    form.append("L")
                else:
                    form.append("D")
            except ValueError:
                continue
    return form[-5:]


def build_form_data(standings, results):
    """builds a dict of team_name -> form list for all teams in standings"""
    form_data = {}
    for row in standings:
        form_data[row["team_name"]] = get_team_form(row["team_name"], results)
    return form_data
