#!/usr/bin/env python3
from typing import Optional
import curses
from enum import IntEnum


# Settings for configFile:
SETTINGS: dict[str, Optional[str | bool]] = {
    'signalExecPath': None,
    'signalConfigDir': None,
    'signalSocketPath': None,
    'startSignal': True,
    'workingDir': '',
    'theme': 'light',
    'themePath': None,
}
"""The settings for cliSignal."""

ROW: int = 0
"""The tuple index for row / rows."""
COL: int = 1
"""The tuple index for col / cols."""


def calc_attributes(colour_pair: int, attrs: dict[str, int | bool]) -> int:
    """
    Calculate the int attribute given the theme and desired attributes in a dict.
    :param colour_pair: The colour pair to use.
    :param attrs: The attrs dict.
    :return: int: The attributes int.
    """
    attributes: int = curses.color_pair(colour_pair)
    if attrs['bold']:
        attributes |= curses.A_BOLD
    if attrs['underline']:
        attributes |= curses.A_UNDERLINE
    if attrs['reverse']:
        attributes |= curses.A_REVERSE
    return attributes


def draw_border_on_win(window: curses.window,
                       border_attrs: int,
                       ts: str, bs: str, ls: str, rs: str,
                       tl: str, tr: str, bl: str, br: str,
                       ) -> None:
    """
    Draw a border around a window.
    :param window: curses.window: The window to draw on.
    :param border_attrs: int: The border attributes, ie colour, bold, etc.
    :param ts: str: Top side character.
    :param bs: str: Bottom side character.
    :param ls: str: Left side character.
    :param rs: str: Right side character.
    :param tl: str: Top left character.
    :param tr: str: Top right character.
    :param bl: str: Bottom left character.
    :param br: str: Bottom right character.
    :return: None
    """
    num_rows, num_cols = window.getmaxyx()
    max_row = num_rows - 1
    max_col = num_cols - 1
    # Top and bottom sides:
    for col in range(1, num_cols - 1):
        window.addstr(0, col, ts, border_attrs)
        window.addstr(max_row, col, bs, border_attrs)
    # Left and right sides:
    for row in range(1, num_rows - 1):
        window.addstr(row, 0, ls, border_attrs)
        window.addstr(row, max_col, rs, border_attrs)
    # Top left corner:
    window.addstr(0, 0, tl, border_attrs)
    # Top right corner:
    window.addstr(0, max_col, tr, border_attrs)
    # Bottom left corner:
    window.addstr(max_row, 0, bl, border_attrs)
    # Bottom right corner, causes exception:
    try:
        window.addstr(max_row, max_col, br, border_attrs)
    except curses.error:
        pass
    return


def add_title_to_win(window: curses.window,
                     title: Optional[str],
                     border_attrs: int,
                     title_attrs: int,
                     start_char: str,
                     end_char: str
                     ) -> None:
    """
    Add a provided title to a given window.
    :param window: curses.window: The curser window to draw on.
    :param title: Optional[str]: The title to add, if None, no title is added.
    :param border_attrs: int: The attributes of the border.
    :param title_attrs: int: The attributes of the title.
    :param start_char: str: The start character.
    :param end_char: str: The end character.
    :return: None
    """
    if title is not None:
        # Set Vars:
        num_rows, num_cols = window.getmaxyx()
        col: int = int(num_cols / 2) - int((len(title) + 4) / 2)
        # Put the border start char:
        start_str: str = start_char + ' '
        window.addstr(0, col, start_str, border_attrs)
        # Put the title:
        window.addstr(title, title_attrs)
        # Put the end border char:
        end_str: str = ' ' + end_char
        window.addstr(end_str, border_attrs)
    return
