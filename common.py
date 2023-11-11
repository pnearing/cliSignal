#!/usr/bin/env python3
from typing import Optional, Final
import curses
from enum import IntEnum, Enum

_VERSION: Final[str] = '1.0.0'

#####################################
# Strings:
#####################################
STRINGS: Final[dict[str, dict[str, Optional[str]]]] = {
    # Background characters:
    'background': {
        'mainWin': ' ', 'contactsWin': ' ', 'messagesWin': ' ', 'typingWin': ' ', 'settingsMenu': ' ', 'quitMenu': ' ',
        'switchMenu': ' ', 'linkMenu': ' ', 'registerMenu': ' ', 'shortcutsMenu': ' ', 'aboutMenu': ' ',
        'versionMenu': ' ', 'menuBar': ' ', 'statusBar': ' ', 'quitWin': ' ', 'linkWin': ' ',
    },
    # Window titles:
    'titles': {
        'main': 'cliSignal', 'messages': 'Messages', 'contacts': 'Contacts & Groups', 'typing': None,
        'settings': 'Settings', 'quit': 'Quit', 'switch': 'Switch Account', 'link': 'Link Account',
        'register': 'Register Account', 'keys': 'Shortcut Keys', 'about': 'About', 'version': 'Version'
    },
    # Main menu items:
    'mainMenuNames': {'file': 'File _F1_', 'accounts': 'Accounts _F2_', 'help': 'Help _F3_'},
    # File menu items:
    'fileMenuNames': {'settings': '_S_ettings', 'quit': '_Q_uit'},
    # Accounts menu items:
    'acctMenuNames': {'switch': '_S_witch account', 'link': '_L_ink account', 'register': '_R_egister account'},
    # Help menu items:
    'helpMenuNames': {'shortcuts': '_S_hortcut Keys', 'about': '_A_bout', 'version': '_V_ersion'},
    # Messages:
    'messages': {
        'quit': 'Are you sure you want to quit?',
    },
    # Other:
    'other': {
        'yesOrNo': '[ _Y_es / _N_ o ]',
    },
}

#####################################
# Settings:
#####################################
# Settings for configFile:
SETTINGS: dict[str, Optional[str | bool]] = {
    'signalExecPath': None,
    'signalConfigDir': None,
    'signalSocketPath': None,
    'startSignal': True,
    'workingDir': None,
    'theme': 'light',
    'themePath': None,
    'useMouse': False,
}
"""The settings for cliSignal."""
#####################################
# Key character code constants:
#####################################
KEY_ESC: int = 27
"""Escape key code."""
KEYS_ENTER: tuple[int, int] = (10, 77)
"""Main enter and keypad enter key codes."""
KEY_TAB: int = ord('\t')
"""TAB key code."""
KEY_SHIFT_TAB: int = 353
"""Shift TAB key code."""
KEY_BACKSPACE: int = 263
"""Backspace key code."""

#####################################
# Index Constants:
#####################################
ROW: Final[int] = 0
"""The tuple index for row.."""
ROWS: Final[int] = 0
"""The tuple index for rows."""
COL: Final[int] = 1
"""The tuple index for col."""
COLS: Final[int] = 1
"""The tuple index for cols."""
CB_CALLABLE: Final[int] = 0
"""The callback index for the callback tuple."""
CB_PARAM: Final[int] = 1
"""The callback parameter index for the callback tuple."""


###################################
# Enumerations:
###################################
class CallbackStates(Enum):
    """Strings to pass for the different call back states."""
    ACTIVATED = 'activated'
    DEACTIVATED = 'deactivated'


class MenuBarSelections(IntEnum):
    """Available menu selections, indexes self.menu_bar_items, and self.menus in MenuBar."""
    FILE = 0
    ACCOUNTS = 1
    HELP = 2


class FileMenuSelection(IntEnum):
    """Available file menu selections, indexes self._menu_items in FileMenu."""
    SETTINGS = 0
    QUIT = 1


class AccountsMenuSelection(IntEnum):
    """Available account menu selections, indexes self._menu_items in AccountsMenu."""
    SWITCH = 0
    LINK = 1
    REGISTER = 2


class HelpMenuSelection(IntEnum):
    """Available help menu selections, indexes self._menu_items in HelpMenu."""
    KEYS = 0
    ABOUT = 1
    VERSION = 2


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
                       size: Optional[tuple[int,int]] = None,
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
        num_rows: int = max_xy[ROWS]
        num_cols: int = max_xy[COLS]
    else:
        num_rows: int = size[ROWS]
        num_cols: int = size[COLS]

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
