import requests
from bs4 import BeautifulSoup
from database import (
    insert_team,
    insert_standing,
    insert_competition,
    insert_match,
    log_scrape,
    create_connection,
    initialise_database,
)
from datetime import date

request_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",  # cspell:ignore KHTML
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

MAX_RETRIES = 3
RETRY_DELAY = 2


def fetch_espn_page(url):
    """fetches a page from ESPN with retries and detailed error handling"""
    if not url:
        return None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url, headers=request_headers, timeout=10)
            response.raise_for_status()
            return response.text

        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response else "unknown"
            if status == 404:
                print(f"  page not found (404): {url}")
                return None
            elif status == 403:
                print(f"  access denied (403) — ESPN may be blocking scrapers")
                return None
            elif status == 429:
                print(f"  rate limited (429) — waiting before retry...")
                import time

                time.sleep(5)
            elif status >= 500:
                print(
                    f"  ESPN server error ({status}), attempt {attempt}/{MAX_RETRIES}"
                )
            else:
                print(f"  http error {status}: {e}")
                return None

        except requests.exceptions.ConnectionError:
            print(f"  no internet connection — attempt {attempt}/{MAX_RETRIES}")

        except requests.exceptions.Timeout:
            print(f"  request timed out — attempt {attempt}/{MAX_RETRIES}")

        except requests.exceptions.RequestException as e:
            print(f"  unexpected error: {e}")
            return None

        if attempt < MAX_RETRIES:
            import time

            time.sleep(RETRY_DELAY)

    print(f"  failed after {MAX_RETRIES} attempts: {url}")
    return None


def is_espn_reachable():
    """quick check if ESPN is reachable at all"""
    try:
        r = requests.get("https://www.espn.com", headers=request_headers, timeout=5)
        return r.status_code < 500
    except Exception:
        return False


def _find_stats_table(soup):
    tables = soup.find_all("table")
    for table in tables:
        classes = table.get("class") or []
        if "Table--align-right" in classes and "Table--fixed-left" not in classes:
            return table
    return None


def parse_standings(html):
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")
    standings = []

    left_table = soup.find("table", class_="Table--fixed-left")
    if not left_table:
        return []

    left_tbody = left_table.find("tbody")
    if not left_tbody:
        return []
    team_rows = left_tbody.find_all("tr")

    right_table = _find_stats_table(soup)
    if not right_table:
        return []

    right_tbody = right_table.find("tbody")
    if not right_tbody:
        return []
    stat_rows = right_tbody.find_all("tr")

    for i, (team_row, stat_row) in enumerate(zip(team_rows, stat_rows)):
        position_tag = team_row.find("span", class_="team-position")
        position = int(position_tag.text.strip()) if position_tag else i + 1

        name_tag = team_row.find("span", class_="hide-mobile")
        team_name = name_tag.text.strip() if name_tag else "unknown"

        stat_cells = stat_row.find_all("span", class_="stat-cell")
        if len(stat_cells) < 14:
            continue

        standings.append(
            {
                "position": position,
                "team_name": team_name,
                "played": int(stat_cells[0].text.strip()),
                "won": int(stat_cells[1].text.strip()),
                "drawn": int(stat_cells[2].text.strip()),
                "lost": int(stat_cells[3].text.strip()),
                "points_for": int(stat_cells[5].text.strip()),
                "points_against": int(stat_cells[6].text.strip()),
                "points_diff": stat_cells[12].text.strip(),
                "points": int(stat_cells[13].text.strip()),
            }
        )

    return standings


def scrape_and_save(competition_id, url, competition_name, competition_type, season):
    initialise_database()
    insert_competition(competition_name, competition_type, season)
    html = fetch_espn_page(url)
    standings = parse_standings(html)

    if not standings:
        log_scrape(0, "failed")
        return False

    for row in standings:
        insert_team(row["team_name"], None, None, None)

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT team_id FROM teams WHERE team_name = ?", (row["team_name"],)
        )
        result = cursor.fetchone()
        conn.close()

        if not result:
            continue

        insert_standing(
            result[0],
            competition_id,
            row["position"],
            row["played"],
            row["won"],
            row["drawn"],
            row["lost"],
            row["points_for"],
            row["points_against"],
            row["points_diff"],
            row["points"],
            date.today().isoformat(),
        )

    log_scrape(len(standings), "success")
    return True


def parse_results(html):
    """parses completed match results from ESPN scoreboard page"""
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")
    results = []

    matches = soup.find_all("section", class_="Scoreboard")

    for match in matches:
        try:
            teams = match.find_all("li", class_="ScoreboardScoreCell__Item")
            if len(teams) < 2:
                continue

            home_li = None
            away_li = None
            for t in teams:
                classes = t.get("class") or []
                if "ScoreboardScoreCell__Item--home" in classes:
                    home_li = t
                elif "ScoreboardScoreCell__Item--away" in classes:
                    away_li = t

            if home_li is None or away_li is None:
                continue

            home_name = home_li.find("div", class_="ScoreCell__TeamName")
            away_name = away_li.find("div", class_="ScoreCell__TeamName")
            home_score = home_li.find("div", class_="ScoreCell__Score")
            away_score = away_li.find("div", class_="ScoreCell__Score")

            if home_name is None or away_name is None:
                continue
            if home_score is None or away_score is None:
                continue

            home_score_text = home_score.text.strip()
            away_score_text = away_score.text.strip()
            if not home_score_text.isdigit() or not away_score_text.isdigit():
                continue

            date_tag = match.find("div", class_="ScoreCell__Time")
            if not date_tag:
                date_tag = match.find("span", class_="ScoreboardScoreCell__Date")
            match_date = (
                date_tag.text.strip()
                if date_tag and date_tag.text.strip()
                else date.today().isoformat()
            )

            results.append(
                {
                    "home": home_name.text.strip(),
                    "away": away_name.text.strip(),
                    "home_score": home_score_text,
                    "away_score": away_score_text,
                    "date": match_date,
                    "is_fixture": False,
                }
            )
        except Exception:
            continue

    return results


def parse_fixtures(html):
    """parses upcoming fixtures from ESPN scoreboard page"""
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")
    fixtures = []

    matches = soup.find_all("section", class_="Scoreboard")

    for match in matches:
        try:
            teams = match.find_all("li", class_="ScoreboardScoreCell__Item")
            if len(teams) < 2:
                continue

            home_li = None
            away_li = None
            for t in teams:
                classes = t.get("class") or []
                if "ScoreboardScoreCell__Item--home" in classes:
                    home_li = t
                elif "ScoreboardScoreCell__Item--away" in classes:
                    away_li = t

            if home_li is None or away_li is None:
                continue

            home_name = home_li.find("div", class_="ScoreCell__TeamName")
            away_name = away_li.find("div", class_="ScoreCell__TeamName")
            home_score = home_li.find("div", class_="ScoreCell__Score")
            away_score = away_li.find("div", class_="ScoreCell__Score")

            if home_name is None or away_name is None:
                continue

            home_score_text = home_score.text.strip() if home_score else ""
            away_score_text = away_score.text.strip() if away_score else ""
            if home_score_text.isdigit() and away_score_text.isdigit():
                continue

            date_tag = match.find("div", class_="ScoreCell__Time")
            if not date_tag:
                date_tag = match.find("div", class_="ScoreboardScoreCell__Time")
            match_date = (
                date_tag.text.strip() if date_tag and date_tag.text.strip() else "TBC"
            )

            home_form_tag = home_li.find("span", class_="clr-gray-04")
            away_form_tag = away_li.find("span", class_="clr-gray-04")
            home_form = home_form_tag.text.strip().strip("()") if home_form_tag else ""
            away_form = away_form_tag.text.strip().strip("()") if away_form_tag else ""

            fixtures.append(
                {
                    "home": home_name.text.strip(),
                    "away": away_name.text.strip(),
                    "date": match_date,
                    "home_form": home_form,
                    "away_form": away_form,
                    "is_fixture": True,
                }
            )
        except Exception:
            continue

    return fixtures


def save_results(competition_id, results):
    """saves match results to the database"""
    if not results:
        return

    for r in results:
        try:
            home_score = int(r["home_score"])
            away_score = int(r["away_score"])
        except ValueError:
            continue

        insert_match(
            competition_id,
            r["home"],
            r["away"],
            home_score,
            away_score,
            r.get("date", date.today().isoformat()),
        )


def auto_scrape_all(competitions):
    """scrapes all competitions with available URLs at startup"""
    results = {}
    for key, comp in competitions.items():
        if comp["url"] is None:
            results[key] = {"success": False, "reason": "coming soon"}
            continue

        success = scrape_and_save(
            int(key),
            comp["url"],
            comp["name"],
            comp["type"],
            comp["season"],
        )
        results[key] = {"success": success, "name": comp["name"]}

        if comp["results_url"]:
            html = fetch_espn_page(comp["results_url"])
            if html:
                matches = parse_results(html)
                save_results(int(key), matches)

    return results


if __name__ == "__main__":
    html = fetch_espn_page("https://www.espn.com/rugby/scoreboard/_/league/180659")
    if html:
        with open("test_results.html", "w") as f:
            f.write(html)
        results = parse_results(html)
        print(f"found {len(results)} matches")
        for r in results:
            print(f"  {r['home']} {r['home_score']} - {r['away_score']} {r['away']}")
    else:
        print("failed to fetch")
