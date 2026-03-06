import requests
from bs4 import BeautifulSoup

request_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",  # cspell:ignore KHTML
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}


def fetch_espn_page(url):
    try:
        response = requests.get(url, headers=request_headers, timeout=10)
        response.raise_for_status()
        print("page fetched successfully")
        return response.text
    except requests.exceptions.HTTPError as e:
        print(f"http error fetching {url}: {e}")
        return None
    except requests.exceptions.ConnectionError:
        print("connection error - are you online?")
        return None
    except requests.exceptions.Timeout:
        print(f"timed out fetching {url}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"something went wrong fetching {url}: {e}")
        return None


def _find_stats_table(soup):
    # ESPN somehow splits standings into two tables i need the one without fixed-left ngl idk why would they even do this in the first place but here i am trying to work around it
    tables = soup.find_all("table")
    for table in tables:
        classes = table.get("class") or []
        if "Table--align-right" in classes and "Table--fixed-left" not in classes:
            return table
    return None


def parse_standings(html):
    if not html:
        print("no html to parse")
        return []

    soup = BeautifulSoup(html, "html.parser")
    standings = []

    left_table = soup.find("table", class_="Table--fixed-left")
    if not left_table:
        print("couldn't find the team table - maybe ESPN changed their layout")
        return []

    left_tbody = left_table.find("tbody")
    if not left_tbody:
        return []
    team_rows = left_tbody.find_all("tr")

    right_table = _find_stats_table(soup)
    if not right_table:
        print("couldn't find the stats table")
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

        # order: GP W D L BYE F A TF TA TBP LBP BP PD P (this is like a note to myself cuz i couldnt remember it mb)
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
                "points": int(stat_cells[13].text.strip()),
            }
        )

    print(f"parsed {len(standings)} teams")
    return standings
