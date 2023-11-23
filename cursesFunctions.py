#!/usr/bin/env python3
"""
File: cursesFunctions.py
-> Store and handle basic curses functions.
"""
from typing import Optional
import curses
from common import HEIGHT, WIDTH, ROW, COL, _ACCEL_INDICATOR


##################################
# Curses Functions:
##################################
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
                       size: Optional[tuple[int, int]] = None,
                       top_left: Optional[tuple[int, int]] = None,
                       ) -> None:
    """
    Draw a border around a window.
    :param window: curses.window: The window to draw on.
    :param border_attrs: int: The border attributes, i.e. colour, bold, etc.
    :param ts: str: Top side character.
    :param bs: str: Bottom side character.
    :param ls: str: Left side character.
    :param rs: str: Right side character.
    :param tl: str: Top left character.
    :param tr: str: Top right character.
    :param bl: str: Bottom left character.
    :param br: str: Bottom right character.
    :param size: Optional[tuple[int, int]]: The Optional size of the border, if None uses the max size of the window.
    :param top_left: Optional[tuple[int, int]]: The Optional top left corner of the border, if None uses (0, 0).
    :return: None
    """
    # Determine the size of the box:
    if size is None:
        max_xy: tuple[int, int] = window.getmaxyx()
        num_rows: int = max_xy[HEIGHT]
        num_cols: int = max_xy[WIDTH]
    else:
        num_rows: int = size[HEIGHT]
        num_cols: int = size[WIDTH]

    # Determine the top left corner of the box:
    if top_left is None:
        start_row: int = 0
        start_col: int = 0
    else:
        start_row: int = top_left[ROW]
        start_col: int = top_left[COL]

    # Determine the bottom right of the box:
    end_row: int = start_row + num_rows - 1
    end_col: int = start_col + num_cols - 1

    # Top and bottom sides:
    for col in range(start_col + 1, end_col):
        window.addstr(start_row, col, ts, border_attrs)
        window.addstr(end_row, col, bs, border_attrs)

    # Left and right sides:
    for row in range(start_row + 1, end_row):
        window.addstr(row, start_col, ls, border_attrs)
        window.addstr(row, end_col, rs, border_attrs)

    # Top left corner:
    window.addstr(start_row, start_col, tl, border_attrs)

    # Top right corner:
    try:
        window.addstr(start_row, end_col, tr, border_attrs)
    except curses.error:
        pass

    # Bottom left corner:
    window.addstr(end_row, start_col, bl, border_attrs)

    # Bottom right corner, causes exception:
    try:
        window.addstr(end_row, end_col, br, border_attrs)
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
    :param window: curses.window: The curses window to draw on.
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


def center_string(window: curses.window,
                  row: int,
                  value: str,
                  attrs: int,
                  ) -> None:
    """
    Center a string on a window.
    :param window: curses.window: The window to draw on.
    :param row: int: The row to add the sting on.
    :param value: str: The string value to add
    :param attrs: int: The colour attributes to use.
    :return: None
    """
    _, num_cols = window.getmaxyx()
    col: int = int(num_cols / 2) - int(len(value) / 2)
    window.addstr(row, col, value, attrs)
    return


def add_accel_text(window: curses.window,
                   accel_text: str,
                   normal_attrs: int,
                   accel_attrs: int
                   ) -> None:
    """
    Add accelerator text to the given window, at the current position.
    :param window: curses.window: The window to draw on.
    :param accel_text: str: The text with accelerator indicators.
    :param normal_attrs: int: The attributes for the normal text.
    :param accel_attrs: int: The attributes for the accelerator text.
    :return: None
    """
    is_accel: bool = False
    for character in accel_text:
        if character == _ACCEL_INDICATOR:
            is_accel = not is_accel
        else:
            if is_accel:
                window.addstr(character, accel_attrs)
            else:
                window.addstr(character, normal_attrs)
    return


def calc_center_row(containing_height: int, element_height) -> int:
    """
    Calculate the centre row; Assumes top-most row = 0.
    :param containing_height: int: The containing height.
    :param element_height: int: The containing width.
    :return: int: The centre col.
    """
    return int(containing_height / 2) - int(element_height / 2)


def calc_center_col(containing_width: int, element_width: int) -> int:
    """
    Calculate the centre column; Assumes left-most col = 0.
    :param containing_width: int: The containing width.
    :param element_width: int: the containing height.
    :return: int: The centre column.
    """
    return int(containing_width / 2) - int(element_width / 2)


def calc_center_top_left(containing_size: tuple[int, int], window_size: tuple[int, int]) -> tuple[int, int]:
    """
    Calculate the top left corner, to centre a window in the containing window.
    :param containing_size: tuple[int, int]: The containing window size: (ROWS, COLS)
    :param window_size: tuple[int, int]: The display window size: (ROWS, COLS)
    :return: tuple[int, int]: The top left corner: (ROW, COL)
    """
    top: int = calc_center_row(containing_size[HEIGHT], window_size[HEIGHT]) - 1
    left: int = calc_center_col(containing_size[WIDTH], window_size[WIDTH]) - 1
    if top < 0:
        top = 0
    if left < 0:
        left = 0
    return top, left
