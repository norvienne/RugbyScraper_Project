import os
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.spinner import Spinner

console = Console()

LOGO = """
██████╗ ██╗   ██╗ ██████╗ ██████╗ ██╗   ██╗
██╔══██╗██║   ██║██╔════╝ ██╔══██╗╚██╗ ██╔╝
██████╔╝██║   ██║██║  ███╗██████╔╝ ╚████╔╝ 
██╔══██╗██║   ██║██║   ██║██╔══██╗  ╚██╔╝  
██║  ██║╚██████╔╝╚██████╔╝██████╔╝   ██║   
╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═════╝   ╚═╝   
███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗ 
██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝
╚════██║██║     ██╔══██╗██╔══██╗██╔═══╝ ██╔══╝  ██╔══██╗
███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║
╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
"""

TAGLINE = "                                        by norvienne 🏉"

COMPETITIONS = [
    ("1", "[EU]", "Six Nations"),
    ("2", "[GB]", "Premiership"),
    ("3", "[FR]", "Top 14"),
    ("4", "[WR]", "United Rugby Championship"),
    ("5", "[EU]", "Champions Cup"),
    ("6", "[WR]", "Rugby Championship"),
    ("7", "[WR]", "Rugby World Cup 2027  [soon]"),
]


def clear_screen():
    os.system("clear")


def animate_logo():
    clear_screen()
    for line in LOGO.splitlines():
        console.print(line, style="bold green")
        time.sleep(0.1)
    console.print(TAGLINE, style="dim green")
    time.sleep(1.2)
    clear_screen()


def flicker():
    for _ in range(4):
        clear_screen()
        time.sleep(0.05)
        console.print("█" * 50, style="bold green")
        time.sleep(0.05)
    clear_screen()


def animate_menu():
    flicker()
    time.sleep(0.1)

    menu_lines = []
    for key, flag, name in COMPETITIONS:
        menu_lines.append(f"  {key}.  {flag}  {name}")
    menu_lines.append("")
    menu_lines.append("  q.  Quit")

    printed = []
    for line in menu_lines:
        printed.append(line)
        clear_screen()
        console.print(
            Panel(
                "\n".join(printed),
                title="[bold green]Select Competition[/bold green]",
                border_style="green",
                padding=(1, 2),
                width=60,
            )
        )
        time.sleep(0.07)

    return console.input("\n[bold green]  >[/bold green] ")


def get_row_style(position, total_teams):
    # colour for positions
    if position == 1:
        return "bold yellow"  # gold
    elif position <= 3:
        return "bold green"  # green
    elif position >= total_teams:
        return "bold red"  # red
    else:
        return "white"  # white


def show_standings(competition_name, standings):
    # makes the table look nice and adds a note of what the meaning of each column is at the bottom
    clear_screen()

    table = Table(
        title=f"[bold green]{competition_name}[/bold green]",
        border_style="green",
        header_style="bold green",
        show_lines=False,
    )

    table.add_column("Pos", justify="center", width=5)
    table.add_column("Team", width=20)
    table.add_column("GP", justify="center", width=5)
    table.add_column("W", justify="center", width=5)
    table.add_column("D", justify="center", width=5)
    table.add_column("L", justify="center", width=5)
    table.add_column("Pts", justify="center", width=5)

    total = len(standings)
    for row in standings:
        style = get_row_style(row["position"], total)
        table.add_row(
            str(row["position"]),
            row["team_name"],
            str(row["played"]),
            str(row["won"]),
            str(row["drawn"]),
            str(row["lost"]),
            str(row["points"]),
            style=style,
        )

    console.print(table)
    console.print(
        Panel(
            "[dim]GP[/dim]  Games Played\n"
            "[dim]W[/dim]   Won\n"
            "[dim]D[/dim]   Drawn\n"
            "[dim]L[/dim]   Lost\n"
            "[dim]Pts[/dim] Points",
            title="[dim]Note[/dim]",
            border_style="dim",
            width=30,
            padding=(0, 2),
        )
    )
    console.input("\n[dim]  press enter to go back...[/dim]")


def show_loading_spinner(message="fetching data..."):
    # shows a spinner while fetching
    with Live(Spinner("dots", text=f"[green]{message}[/green]"), refresh_per_second=10):
        time.sleep(2)


if __name__ == "__main__":
    animate_logo()
    choice = animate_menu()
    if choice == "1":
        show_loading_spinner("fetching six nations standings...")
        # hardcoded test data for now it is like just to show the display, will replace with real data later
        test_data = [
            {
                "position": 1,
                "team_name": "France",
                "played": 3,
                "won": 3,
                "drawn": 0,
                "lost": 0,
                "points": 15,
            },
            {
                "position": 2,
                "team_name": "Scotland",
                "played": 3,
                "won": 2,
                "drawn": 0,
                "lost": 1,
                "points": 11,
            },
            {
                "position": 3,
                "team_name": "Ireland",
                "played": 3,
                "won": 2,
                "drawn": 0,
                "lost": 1,
                "points": 9,
            },
            {
                "position": 4,
                "team_name": "England",
                "played": 3,
                "won": 1,
                "drawn": 0,
                "lost": 2,
                "points": 5,
            },
            {
                "position": 5,
                "team_name": "Italy",
                "played": 3,
                "won": 1,
                "drawn": 0,
                "lost": 2,
                "points": 5,
            },
            {
                "position": 6,
                "team_name": "Wales",
                "played": 3,
                "won": 0,
                "drawn": 0,
                "lost": 3,
                "points": 1,
            },
        ]
        show_standings("Six Nations 2026", test_data)
