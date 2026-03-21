import os
import time
import random
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.live import Live
from rich.spinner import Spinner
from rich.text import Text

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

TAGLINE = "                                        by HlibSamodin 🏉"

ABOUT_TEXT = """
╔════════════════════════════════════════════════════════╗
║                  ABOUT RUGBYSCRAPER                    ║
╚════════════════════════════════════════════════════════╝

  Built by HlibSamodin — a 15 year old rugby fan who read
  Clean Code by Robert C. Martin and wanted to build
  something real to practice better coding.

  Rugby is my favourite sport so I built something I
  actually care about. This project scrapes live rugby
  data from ESPN and displays it in a clean terminal UI.

  github.com/HlibSamodin11
"""

COMPETITIONS = [
    ("1", "[EU]", "Six Nations"),
    ("2", "[GB]", "Premiership"),
    ("3", "[FR]", "Top 14"),
    ("4", "[WR]", "United Rugby Championship"),
    ("5", "[EU]", "Champions Cup"),
    ("6", "[WR]", "Rugby Championship"),
    ("7", "[WR]", "Rugby World Cup 2027"),
]

COMPETITION_DESCRIPTIONS = {
    "1": "Annual competition between England, France, Ireland, Italy, Scotland and Wales.\nOne of rugby's oldest tournaments, founded in 1883.",
    "2": "Top tier of English club rugby. The best clubs in England\ncompete across the season for the Premiership title.",
    "3": "The top professional rugby league in France, featuring\n14 clubs competing for the Bouclier de Brennus since 1892.",
    "4": "Cross-border competition featuring clubs from Ireland, Italy,\nScotland, South Africa, Wales and Argentina. Formed in 2021.",
    "5": "Elite European club rugby competition. The top clubs from\nacross Europe compete for the most prestigious club trophy.",
    "6": "Annual southern hemisphere international competition between\nArgentina, Australia, New Zealand and South Africa. Since 1996.",
    "7": "The biggest event in rugby union, held every 4 years.\nThe 2027 edition will be hosted in Australia.",
}

COMPETITION_COLOURS = {
    "1": "bold cyan",
    "2": "bold red",
    "3": "bold blue",
    "4": "bold magenta",
    "5": "bold yellow",
    "6": "bold green",
    "7": "bold white",
}

COMPETITION_BANNERS = {
    "1": [
        "╔════════════════════════════════════════════════════════╗",
        "║             ★ ★ ★   SIX NATIONS   ★ ★ ★                ║",
        "║                EUROPE  •  SINCE 1883                   ║",
        "╚════════════════════════════════════════════════════════╝",
    ],
    "2": [
        "╔════════════════════════════════════════════════════════╗",
        "║                   PREMIERSHIP RUGBY                    ║",
        "║                   ENGLAND  •  TIER 1                   ║",
        "╚════════════════════════════════════════════════════════╝",
    ],
    "3": [
        "╔════════════════════════════════════════════════════════╗",
        "║                         TOP 14                         ║",
        "║                    FRANCE  •  TIER 1                   ║",
        "╚════════════════════════════════════════════════════════╝",
    ],
    "4": [
        "╔════════════════════════════════════════════════════════╗",
        "║                UNITED RUGBY CHAMPIONSHIP               ║",
        "║                EUROPE & AFRICA  •  TIER 1              ║",
        "╚════════════════════════════════════════════════════════╝",
    ],
    "5": [
        "╔════════════════════════════════════════════════════════╗",
        "║                 ★   CHAMPIONS CUP   ★                  ║",
        "║                   EUROPE  •  ELITE                     ║",
        "╚════════════════════════════════════════════════════════╝",
    ],
    "6": [
        "╔════════════════════════════════════════════════════════╗",
        "║                 RUGBY CHAMPIONSHIP                     ║",
        "║             S.HEMISPHERE  •  SINCE 1996                ║",
        "╚════════════════════════════════════════════════════════╝",
    ],
    "7": [
        "╔════════════════════════════════════════════════════════╗",
        "║              ★   RUGBY WORLD CUP 2027   ★              ║",
        "║               AUSTRALIA  •  COMING SOON                ║",
        "╚════════════════════════════════════════════════════════╝",
    ],
}

GLITCH_CHARS = "▓▒░█▄▀■□▪▫╔╗╚╝║═╠╣╦╩╬░▒▓"


def clear_screen():
    os.system("clear")


def get_terminal_width():
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80


def is_narrow():
    return get_terminal_width() < 100


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


def animate_exit():
    clear_screen()
    console.print("\n\n  [bold green]Thanks for visiting RugbyScraper 🏉[/bold green]")
    console.print("  [dim green]See you next time, HlibSamodin![/dim green]\n")
    time.sleep(1.0)

    for _ in range(10):
        clear_screen()
        lines = []
        for _ in range(12):
            line = "".join(random.choice(GLITCH_CHARS) for _ in range(56))
            lines.append(line)
        console.print(
            "\n".join(lines),
            style=f"bold {'green' if random.random() > 0.3 else 'red'}",
        )
        time.sleep(0.07)

    logo_lines = [line for line in LOGO.splitlines() if line.strip()]
    for i in range(6):
        clear_screen()
        for j, line in enumerate(logo_lines):
            if random.random() > 0.4:
                glitched = "".join(
                    c if random.random() > 0.3 else random.choice(GLITCH_CHARS)
                    for c in line
                )
                console.print(glitched, style="bold green")
            else:
                console.print(" " * len(line))
        time.sleep(0.1)

    clear_screen()
    for line in LOGO.splitlines():
        console.print(line, style="bold green")
    console.print(TAGLINE, style="dim green")
    time.sleep(0.5)

    logo_lines_full = LOGO.splitlines()
    for i in range(len(logo_lines_full)):
        clear_screen()
        for j, line in enumerate(logo_lines_full):
            if j < len(logo_lines_full) - i:
                console.print(line, style="dim green")
        time.sleep(0.04)

    clear_screen()


def animate_menu():
    flicker()
    time.sleep(0.1)

    menu_lines = []
    for key, flag, name in COMPETITIONS:
        menu_lines.append(f"  {key}.  {flag}  {name}")
    menu_lines.append("")
    menu_lines.append("  a.  About")
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

    print("\n  > ", end="", flush=True)
    return input()


def get_row_style(position, total_teams):
    if position == 1:
        return "bold yellow"
    elif position <= 3:
        return "bold green"
    elif position >= total_teams:
        return "bold red"
    else:
        return "white"


def format_form(form_list):
    """turns a list like ['W','W','L','D','W'] into coloured dots"""
    symbols = {
        "W": "[bold green]●[/bold green]",
        "L": "[bold red]●[/bold red]",
        "D": "[bold yellow]●[/bold yellow]",
    }
    return " ".join(symbols.get(r, "[dim]·[/dim]") for r in form_list)


def format_position_cell(position, total_teams):
    """adds trophy to 1st, down arrow to last"""
    if position == 1:
        return f"🏆 {position}"
    elif position == total_teams:
        return f"⬇  {position}"
    return str(position)


def animate_banner(competition_key):
    if competition_key not in COMPETITION_BANNERS:
        return
    colour = COMPETITION_COLOURS.get(competition_key, "bold white")
    for line in COMPETITION_BANNERS[competition_key]:
        console.print(line, style=colour)
        time.sleep(0.08)


def show_about():
    clear_screen()
    for line in ABOUT_TEXT.splitlines():
        console.print(line, style="bold green")
        time.sleep(0.05)
    console.input("\n[dim]  press enter to go back...[/dim]")


def show_standings(competition_name, standings, competition_key=None, form_data=None):
    clear_screen()
    narrow = is_narrow()

    if competition_key:
        animate_banner(competition_key)
        time.sleep(0.2)

    if competition_key and competition_key in COMPETITION_DESCRIPTIONS:
        desc = COMPETITION_DESCRIPTIONS[competition_key]
        console.print(
            Panel(
                desc,
                border_style="dim",
                padding=(0, 2),
                width=min(get_terminal_width() - 4, 62),
            )
        )
        time.sleep(0.1)

    table = Table(
        title=f"[bold green]{competition_name}[/bold green]",
        border_style="green",
        header_style="bold green",
        show_lines=False,
    )

    table.add_column("Pos", justify="center", width=6)
    table.add_column("Team", width=22)
    table.add_column("GP", justify="center", width=4)
    table.add_column("W", justify="center", width=4)
    table.add_column("D", justify="center", width=4)
    table.add_column("L", justify="center", width=4)

    if not narrow:
        table.add_column("PF", justify="center", width=5)
        table.add_column("PA", justify="center", width=5)
        table.add_column("PD", justify="center", width=6)

    table.add_column("Pts", justify="center", width=5)

    if form_data:
        table.add_column("Form", justify="left", width=16)

    total = len(standings)
    for row in standings:
        style = get_row_style(row["position"], total)
        pos_cell = format_position_cell(row["position"], total)

        pd_val = row.get("points_diff", "0")
        if str(pd_val).startswith("+"):
            pd_display = f"[bold green]{pd_val}[/bold green]"
        elif str(pd_val).startswith("-"):
            pd_display = f"[bold red]{pd_val}[/bold red]"
        else:
            pd_display = str(pd_val)

        cells = [
            pos_cell,
            row["team_name"],
            str(row["played"]),
            str(row["won"]),
            str(row["drawn"]),
            str(row["lost"]),
        ]

        if not narrow:
            cells += [
                str(row.get("points_for", "")),
                str(row.get("points_against", "")),
                pd_display,
            ]

        cells.append(str(row["points"]))

        if form_data:
            team_form = form_data.get(row["team_name"], [])
            cells.append(format_form(team_form))

        table.add_row(*cells, style=style)

    console.print(table)

    if narrow:
        key_text = "[dim]GP[/dim] Played  [dim]W[/dim] Won  [dim]D[/dim] Drawn  [dim]L[/dim] Lost  [dim]Pts[/dim] Points"
    else:
        key_text = (
            "[dim]GP[/dim] Played    [dim]PF[/dim] Points For\n"
            "[dim]W[/dim]  Won       [dim]PA[/dim] Points Against\n"
            "[dim]D[/dim]  Drawn     [dim]PD[/dim] Points Difference\n"
            "[dim]L[/dim]  Lost      [dim]Pts[/dim] League Points"
        )
    if form_data:
        key_text += "\n[bold green]●[/bold green] Win  [bold red]●[/bold red] Loss  [bold yellow]●[/bold yellow] Draw"

    console.print(
        Panel(
            key_text,
            title="[dim]Key[/dim]",
            border_style="dim",
            width=50,
            padding=(0, 2),
        )
    )

    timestamp = time.strftime("%H:%M:%S")
    console.print(f"[dim]  last updated: {timestamp}[/dim]")

    print(
        "\n  enter to go back / e export / r results / f fixtures / t team stats > ",
        end="",
        flush=True,
    )
    return input()


def show_team_picker(standings):
    """lets user pick a team from the current standings"""
    clear_screen()
    console.print("\n[bold green]  Select a team:[/bold green]\n")
    for i, row in enumerate(standings, 1):
        console.print(f"  [dim]{i}.[/dim]  {row['team_name']}")
    console.print("\n  [dim]0.  Cancel[/dim]")
    print("\n  > ", end="", flush=True)
    choice = input()
    try:
        idx = int(choice)
        if idx == 0:
            return None
        if 1 <= idx <= len(standings):
            return standings[idx - 1]["team_name"]
    except ValueError:
        pass
    return None


def show_team_graph(team_name, history, standings):
    """shows an animated impressive stats screen for a team"""
    clear_screen()

    team_data = next((r for r in standings if r["team_name"] == team_name), None)
    if not team_data:
        console.print("[red]  team not found[/red]")
        input("\n  press enter to go back...")
        return

    # animated header
    header = f"  ★  {team_name.upper()}  ★"
    border = "  " + "═" * (len(header) - 2)
    for char in border:
        console.print(char, style="bold yellow", end="")
        time.sleep(0.01)
    console.print()
    for char in header:
        console.print(char, style="bold yellow", end="")
        time.sleep(0.02)
    console.print()
    for char in border:
        console.print(char, style="bold yellow", end="")
        time.sleep(0.01)
    console.print("\n")
    time.sleep(0.2)

    # animated stats card
    pd_val = team_data.get("points_diff", "0")
    pd_colour = "bold green" if str(pd_val).startswith("+") else "bold red"

    stats = [
        ("  Position", f"[bold yellow]{team_data['position']}[/bold yellow]", ""),
        ("  Played  ", f"{team_data['played']}", ""),
        (
            "  Won     ",
            f"[bold green]{team_data['won']}[/bold green]",
            "█" * team_data["won"],
        ),
        (
            "  Drawn   ",
            f"[bold yellow]{team_data['drawn']}[/bold yellow]",
            "█" * team_data["drawn"],
        ),
        (
            "  Lost    ",
            f"[bold red]{team_data['lost']}[/bold red]",
            "█" * team_data["lost"],
        ),
        ("  PF      ", f"{team_data.get('points_for', 'N/A')}", ""),
        ("  PA      ", f"{team_data.get('points_against', 'N/A')}", ""),
        ("  PD      ", f"[{pd_colour}]{pd_val}[/{pd_colour}]", ""),
        ("  Points  ", f"[bold yellow]{team_data['points']}[/bold yellow]", ""),
    ]

    for label, value, bar in stats:
        console.print(f"[dim]{label}[/dim]  :  {value}  [green]{bar}[/green]")
        time.sleep(0.08)

    time.sleep(0.3)

    # animated bar chart
    console.print("\n  [dim]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/dim]")
    console.print("  [bold green]  Points comparison — all teams[/bold green]")
    console.print("  [dim]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/dim]\n")
    time.sleep(0.2)

    max_pts = max(r["points"] for r in standings) if standings else 1
    bar_width = 35

    for row in standings:
        is_selected = row["team_name"] == team_name
        is_first = row["position"] == 1
        is_last = row["position"] == len(standings)

        filled = int((row["points"] / max_pts) * bar_width)
        empty = bar_width - filled

        if is_selected:
            bar_colour = "bold yellow"
            prefix = "▶ "
        elif is_first:
            bar_colour = "bold green"
            prefix = "🏆"
        elif is_last:
            bar_colour = "bold red"
            prefix = "⬇ "
        else:
            bar_colour = "green"
            prefix = "  "

        name_padded = row["team_name"][:18].ljust(18)

        console.print(f"  {prefix} [bold]{name_padded}[/bold] ", end="")
        for i in range(filled):
            console.print(f"[{bar_colour}]█[/{bar_colour}]", end="")
            time.sleep(0.01)
        console.print(f"[dim]{'░' * empty}[/dim] [bold]{row['points']}[/bold]")

    # points trend if available
    if len(history) >= 2:
        time.sleep(0.3)
        console.print("\n  [dim]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/dim]")
        console.print("  [bold green]  Points trend over time[/bold green]")
        console.print("  [dim]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/dim]\n")

        dates = [h["date"] for h in history]
        points = [h["points"] for h in history]
        positions = [h["position"] for h in history]
        max_pts_h = max(points)
        height = 8

        for row in range(height, 0, -1):
            threshold = (row / height) * max_pts_h
            line = f"  {int(threshold):>3} │"
            for pt in points:
                normalised = (pt / max_pts_h) * height
                if normalised >= row:
                    line += " [bold green]█[/bold green] "
                else:
                    line += "   "
            console.print(line)
            time.sleep(0.05)

        console.print("      └" + "───" * len(points))
        date_line = "       "
        for d in dates:
            date_line += d[-5:] + " "
        console.print(f"[dim]{date_line}[/dim]")

        console.print("\n  [dim]Position trend:[/dim]  ", end="")
        for i in range(1, len(positions)):
            diff = positions[i - 1] - positions[i]
            if diff > 0:
                console.print("[bold green]▲[/bold green] ", end="")
            elif diff < 0:
                console.print("[bold red]▼[/bold red] ", end="")
            else:
                console.print("[dim]─[/dim] ", end="")
            time.sleep(0.1)
        console.print()
    else:
        console.print(
            "\n  [dim]  run the scraper daily to unlock the points trend graph![/dim]"
        )

    console.print()
    input("  press enter to go back...")


def show_new_results_notification(new_results):
    """flashes up each new result one by one — impressive startup notification"""
    if not new_results:
        return

    clear_screen()
    time.sleep(0.2)

    header = "  ★  NEW RESULTS  ★"
    border = "  " + "═" * (len(header) - 2)

    for char in border:
        console.print(char, style="bold yellow", end="")
        time.sleep(0.01)
    console.print()
    for char in header:
        console.print(char, style="bold yellow", end="")
        time.sleep(0.03)
    console.print()
    for char in border:
        console.print(char, style="bold yellow", end="")
        time.sleep(0.01)
    console.print("\n")
    time.sleep(0.3)

    for i, r in enumerate(new_results):
        comp_name = r.get("competition", "")
        home = r["home"]
        away = r["away"]
        home_score = int(r["home_score"])
        away_score = int(r["away_score"])

        if home_score > away_score:
            home_style = "bold green"
            away_style = "dim white"
            result_char = "▶"
        elif away_score > home_score:
            home_style = "dim white"
            away_style = "bold green"
            result_char = "◀"
        else:
            home_style = "bold yellow"
            away_style = "bold yellow"
            result_char = "═"

        # flash effect
        for _ in range(2):
            clear_screen()
            time.sleep(0.06)
            console.print()
            for char in border:
                console.print(char, style="bold yellow", end="")
            console.print()
            for char in header:
                console.print(char, style="bold yellow", end="")
            console.print()
            for char in border:
                console.print(char, style="bold yellow", end="")
            console.print("\n")
            time.sleep(0.06)

        console.print(f"  [dim]{comp_name}[/dim]")
        console.print()
        console.print(
            f"  [{home_style}]{home:>22}[/{home_style}]  "
            f"[bold yellow]{home_score:>2} {result_char} {away_score:<2}[/bold yellow]  "
            f"[{away_style}]{away}[/{away_style}]"
        )
        console.print()

        bar = ""
        for _ in range(40):
            bar += "━"
            console.print(f"  [dim]{bar}[/dim]", end="\r")
            time.sleep(0.01)
        console.print()
        time.sleep(0.4)

    console.print(
        f"\n  [dim]{len(new_results)} new result{'s' if len(new_results) != 1 else ''} since last run[/dim]"
    )
    time.sleep(0.5)
    input("\n  press enter to continue...")


def show_results(competition_name, results, competition_key=None):
    """shows completed match results with dates"""
    colour = COMPETITION_COLOURS.get(competition_key or "", "bold white")

    clear_screen()
    console.print(f"\n[{colour}]  {competition_name} — Recent Results[/{colour}]\n")

    if not results:
        console.print("[dim]  no results found.[/dim]\n")
    else:
        table = Table(
            show_header=True,
            header_style=colour,
            box=box.SIMPLE,
            padding=(0, 2),
        )
        table.add_column("Date", style="dim", justify="left", width=12)
        table.add_column("Home", style="bold white", justify="right")
        table.add_column("Score", style="bold yellow", justify="center")
        table.add_column("Away", style="bold white", justify="left")

        for r in results:
            try:
                home_score = int(r["home_score"])
                away_score = int(r["away_score"])
            except (ValueError, KeyError):
                continue

            if home_score > away_score:
                home_style = "bold green"
                away_style = "dim white"
            elif away_score > home_score:
                home_style = "dim white"
                away_style = "bold green"
            else:
                home_style = "bold yellow"
                away_style = "bold yellow"

            table.add_row(
                r.get("date", ""),
                f"[{home_style}]{r['home']}[/{home_style}]",
                f"{r['home_score']} - {r['away_score']}",
                f"[{away_style}]{r['away']}[/{away_style}]",
            )

        console.print(table)
        console.print("[dim]  winner shown in green[/dim]")

    input("\n  press enter to go back...")


def show_fixtures(competition_name, fixtures, competition_key=None):
    """shows upcoming fixtures with form"""
    colour = COMPETITION_COLOURS.get(competition_key or "", "bold white")

    clear_screen()
    console.print(f"\n[{colour}]  {competition_name} — Upcoming Fixtures[/{colour}]\n")

    if not fixtures:
        console.print(
            "[dim]  no upcoming fixtures found — season may be complete.[/dim]\n"
        )
    else:
        table = Table(
            show_header=True,
            header_style=colour,
            box=box.SIMPLE,
            padding=(0, 2),
        )
        table.add_column("Date", style="dim", justify="left", width=14)
        table.add_column("Home", style="bold white", justify="right")
        table.add_column("Form", style="dim", justify="center", width=7)
        table.add_column("vs", style="dim", justify="center", width=4)
        table.add_column("Form", style="dim", justify="center", width=7)
        table.add_column("Away", style="bold white", justify="left")

        for f in fixtures:
            table.add_row(
                f.get("date", "TBC"),
                f["home"],
                f.get("home_form", ""),
                "vs",
                f.get("away_form", ""),
                f["away"],
            )

        console.print(table)

    input("\n  press enter to go back...")


def show_loading_spinner(message="fetching data..."):
    with Live(Spinner("dots", text=f"[green]{message}[/green]"), refresh_per_second=10):
        time.sleep(2)
