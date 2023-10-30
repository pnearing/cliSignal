#!/usr/bin/env python3
from typing import Optional
import curses

# Settings for configFile:
SETTINGS: dict[str, Optional[str | bool]] = {
    'signalExecPath': None,
    'signalConfigDir': None,
    'signalLogPath': None,
    'signalSocketPath': None,
    'startSignal': True,
}


def add_title_to_win(window: curses.window, title: str, attrs: int = 0) -> None:
    """
    Add a provided title to a given window.
    :param window: curses.window: The curser window to draw on.
    :param title: str: The title to add.
    :param attrs: int: The attributes to add, defaults to 0
    :return: None
    """
    # Add start and end chars to the title.
    message: str = "\u2562 " + title + " \u255F"
    num_rows, num_cols = window.getmaxyx()
    col: int = int(num_cols / 2) - int(len(message) / 2)
    window.addstr(0, col, message, attrs)
    return
