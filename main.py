import os
import time

os.environ["TERM"] = "xterm"

from display import (
    animate_logo,
    animate_menu,
    show_standings,
    show_results,
    show_fixtures,
    show_loading_spinner,
    show_about,
    show_team_picker,
    show_team_graph,
    show_new_results_notification,
    clear_screen,
    animate_exit,
)
from scraper import (
    fetch_espn_page,
    parse_standings,
    parse_results,
    parse_fixtures,
    scrape_and_save,
    is_espn_reachable,
    auto_scrape_all,
)
from competitions import COMPETITIONS
from database import initialise_database, get_known_match_ids, create_connection
from exporter import export_standings_to_csv
from stats import get_team_history, build_form_data
from rich.console import Console

console = Console()


def _get_score(competition_id, home, away, match_date, side):
    """fetches a single score from the database for notification display"""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT home_score, away_score FROM matches
        WHERE competition_id = ? AND home_team = ? AND away_team = ? AND match_date = ?
        """,
        (competition_id, home, away, match_date),
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        return row[0] if side == "home" else row[1]
    return 0


def handle_choice(choice):
    if choice not in COMPETITIONS:
        console.print("[red]  invalid choice, try again[/red]")
        return

    comp = COMPETITIONS[choice]

    if comp["url"] is None:
        clear_screen()
        console.print(f"\n[yellow]  {comp['name']} is coming soon![/yellow]")
        console.input("\n[dim]  press enter to go back...[/dim]")
        return

    show_loading_spinner(f"fetching {comp['name']} standings...")
    html = fetch_espn_page(comp["url"])
    standings = parse_standings(html)

    if not standings:
        console.print("[red]  couldn't load standings, try again later[/red]")
        console.input("\n[dim]  press enter to go back...[/dim]")
        return

    scrape_and_save(
        int(choice), comp["url"], comp["name"], comp["type"], comp["season"]
    )

    form_data = {}
    results = []
    if comp["results_url"]:
        show_loading_spinner(f"fetching {comp['name']} form...")
        results_html = fetch_espn_page(comp["results_url"])
        results = parse_results(results_html)
        form_data = build_form_data(standings, results)

    result = show_standings(
        f"{comp['name']} {comp['season']}", standings, choice, form_data
    )

    if result == "e":
        path = export_standings_to_csv(int(choice), comp["name"])
        if path:
            console.print(f"\n[green]  exported to {path}[/green]")
        else:
            console.print("\n[red]  nothing to export yet[/red]")
        console.input("\n[dim]  press enter to go back...[/dim]")

    elif result == "r":
        if comp["results_url"] is None:
            clear_screen()
            console.print(
                f"\n[yellow]  no results available for {comp['name']} yet[/yellow]"
            )
            console.input("\n[dim]  press enter to go back...[/dim]")
            return
        if not results:
            show_loading_spinner(f"fetching {comp['name']} results...")
            results_html = fetch_espn_page(comp["results_url"])
            results = parse_results(results_html)
        show_results(f"{comp['name']} {comp['season']}", results, choice)

    elif result == "f":
        if comp["results_url"] is None:
            clear_screen()
            console.print(
                f"\n[yellow]  no fixtures available for {comp['name']} yet[/yellow]"
            )
            console.input("\n[dim]  press enter to go back...[/dim]")
            return
        show_loading_spinner(f"fetching {comp['name']} fixtures...")
        fixtures_html = fetch_espn_page(comp["results_url"])
        fixtures = parse_fixtures(fixtures_html)
        show_fixtures(f"{comp['name']} {comp['season']}", fixtures, choice)

    elif result == "t":
        team_name = show_team_picker(standings)
        if team_name:
            show_loading_spinner(f"loading {team_name} stats...")
            history = get_team_history(team_name, int(choice))
            show_team_graph(team_name, history, standings)


def main():
    animate_logo()
    initialise_database()

    console.print("[dim]  checking connection...[/dim]")
    if not is_espn_reachable():
        console.print(
            "[red]  warning: ESPN appears to be unreachable. data may be outdated.[/red]"
        )
        time.sleep(2)
    else:
        console.print("[dim green]  auto-scraping all competitions...[/dim green]")

        # snapshot known matches before scraping
        known_before = {}
        for key, comp in COMPETITIONS.items():
            if comp["results_url"]:
                known_before[key] = get_known_match_ids(int(key))

        scrape_results = auto_scrape_all(COMPETITIONS)
        success_count = sum(1 for v in scrape_results.values() if v.get("success"))
        console.print(
            f"[dim green]  scraped {success_count} competitions successfully[/dim green]"
        )

        # find new results by comparing before and after
        new_results = []
        for key, comp in COMPETITIONS.items():
            if comp["results_url"] is None:
                continue
            known_after = get_known_match_ids(int(key))
            known_prev = known_before.get(key, set())
            for match_key in known_after - known_prev:
                home, away, match_date = match_key
                new_results.append(
                    {
                        "competition": comp["name"],
                        "home": home,
                        "away": away,
                        "home_score": _get_score(
                            int(key), home, away, match_date, "home"
                        ),
                        "away_score": _get_score(
                            int(key), home, away, match_date, "away"
                        ),
                    }
                )

        if new_results:
            show_new_results_notification(new_results)

    while True:
        choice = animate_menu()
        if choice == "q":
            animate_exit()
            break
        elif choice == "a":
            show_about()
        else:
            handle_choice(choice)


if __name__ == "__main__":
    main()
