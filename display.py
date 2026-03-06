import os
import time
from rich.console import Console
from rich.panel import Panel

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


if __name__ == "__main__":
    animate_logo()
    choice = animate_menu()
    console.print(f"you picked: {choice}")
