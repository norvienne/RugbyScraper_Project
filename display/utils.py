import os
import platform
import time

from rich.console import Console
from rich.live import Live
from rich.spinner import Spinner

from display.constants import (
    DEFAULT_TERMINAL_WIDTH,
    LOADING_DELAY,
    NARROW_TERMINAL_WIDTH,
    SPINNER_REFRESH_RATE,
)

console = Console()


def clear_screen() -> None:
    os.system("cls" if platform.system() == "Windows" else "clear")


def get_terminal_width() -> int:
    try:
        return os.get_terminal_size().columns
    except OSError:
        return DEFAULT_TERMINAL_WIDTH


def is_narrow() -> bool:
    return get_terminal_width() < NARROW_TERMINAL_WIDTH


def get_result_styles(home_score: int, away_score: int) -> tuple:
    # returns (home_style, away_style) based on who won
    if home_score > away_score:
        return "bold green", "dim white"
    if away_score > home_score:
        return "dim white", "bold green"
    return "bold yellow", "bold yellow"


def show_loading_spinner(message: str = "fetching data...") -> None:
    with Live(
        Spinner("dots", text=f"[green]{message}[/green]"),
        refresh_per_second=SPINNER_REFRESH_RATE,
    ):
        time.sleep(LOADING_DELAY)
