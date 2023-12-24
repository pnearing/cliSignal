#!/usr/bin/env python3
"""
File: cursesFunctions.py
-> Store and handle basic curses functions.
"""
from typing import Optional
import curses

import common
from common import HEIGHT, WIDTH, ROW, COL, _ACCEL_INDICATOR, BUTTON_SCROLL_UP, BUTTON_SCROLL_DOWN, BUTTON_SCRAP

CURSOR_POS: tuple[int, int] = (0, 0)
"""The current known cursor position."""


#########################################
# Misc functions:
#########################################
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


def terminal_bell() -> None:
    """
    Ring the terminal bell, only if the current config allows it.
    :return: None
    """
    if common.SETTINGS['useSound']:
        curses.beep()
    if common.SETTINGS['flashScreen']:
        curses.flash()
    return


###########################################
# My versions of addstr and addch with cursor tracking.
###########################################
def move_cursor(window, row: int, col: int):
    global CURSOR_POS
    window.move(row, col)
    CURSOR_POS = (row, col)
    return


def add_str(window,  # Type _CursesWindow | curses.window
            string: str,
            attrs: int,
            row: Optional[int] = None,
            col: Optional[int] = None,
            ) -> None:
    """
    Sensible version of add str.
    :param window: _CursesWindow: The window or pad to add the string to.
    :param string: str: The string to add.
    :param attrs: int: The attributes to use.
    :param row: Optional[int]: The row to add string at.
    :param col: Optional[int]: The colum to add string at.
    :return: None
    """
    # Parameter checks:
    param_error_msg: str = "Either both 'row': %s and 'col': %s must be defined, or None." % (str(row), str(col))
    if row is not None and col is None:
        raise RuntimeError(param_error_msg)
    elif row is None and col is not None:
        raise RuntimeError(param_error_msg)

    # Add the string specifying the co-ords:
    if row is None and col is None:
        try:
            window.addstr(string, attrs)
        except curses.error as e:
            if e.args[0] != 'addwstr() returned ERR':
                raise e
    # Add the string not specifying co-ords
    else:
        try:
            window.addstr(row, col, string, attrs)
        except curses.error as e:
            if e.args[0] != 'addwstr() returned ERR':
                raise e
    return


def add_ch(window,  # Type: curses.window | _CursesWindow.
           char: str,
           attrs: int,
           row: Optional[int] = None,
           col: Optional[int] = None,
           ) -> None:
    """
    Sensible version of addch.
    :param window: _CursesWindow | curses.window: The window or pad to draw on.
    :param char: str: The character to add.
    :param attrs: int: The attributes to use.
    :param row: Optional[int]: The row to add the string at.
    :param col: Optional[int]: The col to add the string at.
    :return:
    """
    # window: curses.window = _window
    # Check parameters:
    param_error_message: str = "Either both 'row' and 'col' must defined, or both must be None."
    if row is None and col is not None:
        raise RuntimeError(param_error_message)
    elif row is not None and col is None:
        raise RuntimeError(param_error_message)
    # # DEBUG:
    # char = '\033[09m' + char
    # Add the string without doing the move:
    if row is None and col is None:
        try:
            window.addch(char, attrs)
        except curses.error as e:
            if e.args[0] != 'add_wch() returned ERR':
                raise e
    elif row is not None and col is not None:
        try:
            window.addch(row, col, char, attrs)
        except curses.error as e:
            if e.args[0] != 'add_wch() returned ERR':
                raise e
    return


def add_ch_with_attrs(window: curses.window,
                      char: str,
                      attrs: int,
                      row: Optional[int] = None,
                      col: Optional[int] = None,
                      bold: bool = False,
                      italics: bool = False,
                      strike_through: bool = False,
                      mono_space: bool = False,
                      spoiler: bool = False,
                      show_spoiler: bool = False,
                      ) -> None:
    """
    Add a character with signal attributes:
    :param window: _CursesWindow | curses.window: The window to draw on.
    :param char: str: The character to add.
    :param attrs: int: The colour attributes to use.
    :param row: Optional[int] = None: The row to add at, note: If row is not None, then col must not be None as well.
    :param col: Optional[int] = None: The column to add at, note: If col is not None, them row must not be None as well.
    :param bold: bool = False: Add bold attribute.
    :param italics: bool = False: Add Italics attribute.
    :param strike_through: bool = False: Add strike through attribute.
    :param mono_space: bool = False: Use monospace font.
    :param spoiler: bool: = False: Use the spoiler char.
    :param show_spoiler: = False: Should we show the spoiler char?
    :return: None.
    """
    attrs &= ~curses.A_BOLD
    attrs &= ~curses.A_REVERSE
    attrs &= ~curses.A_UNDERLINE

    new_char: int = -1
    if ord('A') <= ord(char) <= ord('Z'):
        if bold and italics:
            new_char = ord(char) + 0x1D5FB
        elif bold and mono_space:
            if ord(char) == ord('C'):
                new_char = 0x2102
            elif ord(char) == ord('H'):
                new_char = 0x210D
            elif ord(char) == ord('N'):
                new_char = 0x2115
            elif ord(char) == ord('P'):
                new_char = 0x2119
            elif ord(char) == ord('Q'):
                new_char = 0x211A
            elif ord(char) == ord('R'):
                new_char = 0x211D
            elif ord(char) == ord('Z'):
                new_char = 0x2124
            else:
                new_char = ord(char) + 0x1D4F7
        elif bold:
            new_char = ord(char) + 0x1D593
        elif italics:
            new_char = ord(char) + 0x1D5C7
        elif mono_space:
            new_char = ord(char) + 0x1D71F
        else:
            new_char = ord(char) + 0x1D55F
    elif ord('a') <= ord(char) <= ord('z'):
        if bold and italics:
            new_char = ord(char) + 0x1D5F5
        elif bold and mono_space:
            new_char = ord(char) + 0x1D4F1
        elif bold:
            new_char = ord(char) + 0x1D58D
        elif italics:
            new_char = ord(char) + 0x1D5C1
        elif mono_space:
            new_char = ord(char) + 0x1D629
        else:
            new_char = ord(char) + 0x1D559
    elif ord('0') <= ord(char) <= ord('9'):
        if mono_space and bold:
            new_char = ord(char) + 0x1D7A8
        elif bold:
            new_char = ord(char) + 0x1D7BC
        elif mono_space:
            new_char = ord(char) + 0x1D7C6
        else:
            new_char = ord(char) + 0x1D7B2

    real_char: str = char
    if new_char != -1:
        real_char = chr(new_char)
    if strike_through:
        real_char = '\033[09m' + real_char
    add_ch(window, real_char, attrs, row, col)
    return


###########################################
# Drawing functions:
###########################################
def draw_border_on_win(window,  # Type: curses.window | curses._CursesWindow
                       border_attrs: int,
                       ts: str, bs: str, ls: str, rs: str,
                       tl: str, tr: str, bl: str, br: str,
                       size: Optional[tuple[int, int]] = None,
                       top_left: Optional[tuple[int, int]] = None,
                       ) -> None:
    """
    Draw a border on a window.
    :param window: curses.window | curses._CursesWindow: The window to draw on.
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
        height, width = window.getmaxyx()
    else:
        height: int = size[HEIGHT]
        width: int = size[WIDTH]

    # Determine the top left corner of the box:
    if top_left is None:
        top: int = 0
        left: int = 0
    else:
        top: int = top_left[ROW]
        left: int = top_left[COL]

    # Determine the bottom right of the box:
    bottom: int = top + height - 1
    right: int = left + width - 1

    # Top and bottom sides:
    for col in range(left + 1, right):
        add_ch(window, ts, border_attrs, top, col)
        add_ch(window, bs, border_attrs, bottom, col)

    # Left and right sides:
    for row in range(top + 1, bottom):
        add_ch(window, ls, border_attrs, row, left)
        add_ch(window, rs, border_attrs, row, right)

    # Top left corner:
    add_ch(window, tl, border_attrs, top, left)

    # Top right corner:
    add_ch(window, tr, border_attrs, top, right)

    # Bottom left corner:
    add_ch(window, bl, border_attrs, bottom, left)

    # Bottom right corner, causes exception:
    add_ch(window, br, border_attrs, bottom, right)
    return


def add_title_to_win(window: curses.window,
                     title: Optional[str],
                     lead_tail_attrs: int,
                     title_attrs: int,
                     lead_char: str,
                     tail_char: str,
                     justify: str = 'centre',
                     top_row: Optional[int] = None,
                     win_width: Optional[int] = None,
                     ) -> None:
    """
    Add a provided title to a given window.
    :param window: curses.window: The curses window to draw on.
    :param title: Optional[str]: The title to add, if None, no title is added.
    :param lead_tail_attrs: int: The attributes of the border.
    :param title_attrs: int: The attributes of the title.
    :param lead_char: str: The start character.
    :param tail_char: str: The end character.
    :param justify: str: Either 'centre', 'left', or 'right'
    :param top_row: Optional[int]: Override the row to put the title on.
    :param win_width: Optional[int]: Override the width of the window.
    :return: None
    """
    if title is None:
        return

    # Set Vars:
    if win_width is None:
        _, width = window.getmaxyx()
    else:
        width = win_width

    if top_row is None:
        row = 0
    else:
        row = top_row

    col: int
    if justify == 'center' or justify == 'centre':
        col = int(width / 2) - int((len(title) + 4) / 2)
    elif justify == 'left':
        col = 2
    elif justify == 'right':
        col = width - (len(title) + 4) - 3
    else:
        raise ValueError("'justify' must be one of 'centre', 'left', or 'right', not '%s'" % justify)
    # Put the border start char:
    start_str: str = lead_char + ' '
    add_str(window, start_str, lead_tail_attrs, row, col)
    # window.addstr(0, col, start_str, lead_tail_attrs)
    # Put the title:
    add_str(window, title, title_attrs)
    # window.addstr(title, title_attrs)
    # Put the end border char:
    end_str: str = ' ' + tail_char
    add_str(window, end_str, lead_tail_attrs)
    # window.addstr(end_str, lead_tail_attrs)
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


########################################
# Row / column calculations:
########################################
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


#######################################
# Mouse functions:
#######################################
def get_rel_mouse_pos(mouse_pos: tuple[int, int], real_top_left: tuple[int, int]) -> tuple[int, int]:
    """
    Get the relative mouse position over the window; IE: If the mouse is at top_left, then mouse_pos = (0, 0)
    :param mouse_pos: tuple[int, int]: The mouse position: (ROW, COL).
    :param real_top_left: tuple[int, int]: The real top left corner of the window: (ROW, COL).
    :return: tuple[int, int]: The relative position: (ROW, COL).
    """
    relative_row: int = mouse_pos[ROW] - real_top_left[ROW]
    relative_col: int = mouse_pos[COL] - real_top_left[COL]
    return relative_row, relative_col


def get_mouse() -> tuple[tuple[int, int], int]:
    """
    Get the mouse properties.
    :return: tuple[tuple[int, int], int]: The first element of the outer tuple is the mouse position, as a
        tuple[ROW, COL]; The second element of the outer tuple is an int representing the button state.
    """
    try:
        _, mouse_col, mouse_row, _, button_state = curses.getmouse()
    except curses.error:
        mouse_col = mouse_row = 0
        button_state = 0
    button_state &= ~BUTTON_SCRAP
    mouse_pos: tuple[int, int] = (mouse_row, mouse_col)
    return mouse_pos, button_state


def get_left_click(button_state: int) -> bool:
    """
    Return True if the left button was clicked.
    :param button_state: int: The current button state.
    :return: bool: True if the left button was clicked, False, it was not.
    """
    if (button_state & curses.BUTTON1_CLICKED != 0) or (button_state & curses.BUTTON1_PRESSED != 0):
        return True
    return False


def get_left_double_click(button_state: int) -> bool:
    """
    Return True if the left button was double-clicked.
    :param button_state: int: The current button state.
    :return: True if the left button was double-clicked, False it was not.
    """
    if button_state & curses.BUTTON1_DOUBLE_CLICKED != 0:
        return True
    return False


def get_middle_click(button_state: int) -> bool:
    """
    Return True if the middle button was clicked.
    :param button_state: int: The current button state.
    :return: bool: True the middle button was clicked, False it was not.
    """
    if (button_state & curses.BUTTON2_CLICKED != 0) or (button_state & curses.BUTTON2_PRESSED != 0):
        return True
    return False


def get_middle_double_click(button_state: int) -> bool:
    """
    Return True if the middle button was double-clicked.
    :param button_state: int: The current button state.
    :return: bool: True the middle button was double-clicked, False it was not.
    """
    if button_state & curses.BUTTON2_DOUBLE_CLICKED != 0:
        return True
    return False


def get_right_click(button_state: int) -> bool:
    """
    Return True if the right button was clicked.
    :param button_state: int: The current button state.
    :return:
    """
    if (button_state & curses.BUTTON3_CLICKED != 0) or (button_state & curses.BUTTON3_PRESSED != 0):
        return True
    return False


def get_right_double_click(button_state: int) -> bool:
    """
    Return True if the right button was double-clicked.
    :param button_state: int: The current button state.
    :return: bool: True the right button was double-clicked, False it was not.
    """
    if button_state & curses.BUTTON3_DOUBLE_CLICKED != 0:
        return True
    return False


def get_scroll_up(button_state: int) -> bool:
    """
    Return True if the scroll up has been hit.
    :param button_state: int: The current button state.
    :return: bool: True the scroll up button has been hit, False, it was not.
    """
    if button_state == BUTTON_SCROLL_UP:
        return True
    return False


def get_scroll_down(button_state: int) -> bool:
    """
    Return True if the scroll down was hit.
    :param button_state: int: The current button state.
    :return: bool: True scroll down was hit, False, it was not.
    """
    if button_state == BUTTON_SCROLL_DOWN:
        return True
    return False


def get_alt_pressed(button_state: int) -> bool:
    """
    Return True if ALT is being held down.
    :param button_state: int: The current button state.
    :return: bool: True alt is being pressed, False it is not.
    """
    return button_state & curses.BUTTON_ALT != 0


def get_ctrl_pressed(button_state: int) -> bool:
    """
    Return True if the CTRL key is being held down.
    :param button_state: int: The current button state.
    :return: bool: True if ctrl is being pressed, False, it is not.
    """
    return button_state & curses.BUTTON_CTRL != 0
