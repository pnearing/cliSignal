#!/usr/bin/env python3
"""
File: common.py
-> Store common constants variables, Enums, etc.
"""
import logging
from typing import Optional, Final, Callable, Any

from SignalCliApi import Account
from cliExceptions import CallbackCausedException
from enum import IntEnum, Enum
APP_VERSION: Final[str] = '1.0.0'

#####################################
# String constants:
#####################################
_ACCEL_INDICATOR: Final[str] = '_'

#####################################
# Strings:
#####################################
STRINGS: Final[dict[str, dict[str, dict[str, str] | Optional[str]]]] = {
    # Window titles:
    'titles': {
        'main': 'cliSignal', 'messages': 'Messages', 'contacts': 'Contacts & Groups', 'typing': None,
        'settings': 'Settings', 'quit': 'Quit', 'switch': 'Switch Account', 'link': 'Link Account',
        'register': 'Register Account', 'keys': 'Shortcut Keys', 'about': 'About', 'version': 'Versions',
        'qrcode': 'Scan QR-Code',
    },
    # Button labels:
    'buttonLabels': {
        'okButton': f"{_ACCEL_INDICATOR}O{_ACCEL_INDICATOR}k",
        'cancelButton': f"{_ACCEL_INDICATOR}C{_ACCEL_INDICATOR}ancel"
    },
    # Main menu items:
    'mainMenuNames': {
        'file': f'File {_ACCEL_INDICATOR}F1{_ACCEL_INDICATOR}',
        'accounts': f'Accounts {_ACCEL_INDICATOR}F2{_ACCEL_INDICATOR}',
        'help': f'Help {_ACCEL_INDICATOR}F3{_ACCEL_INDICATOR}',
    },
    # File menu items:
    'fileMenuNames': {
        'settings': f'{_ACCEL_INDICATOR}S{_ACCEL_INDICATOR}ettings',
        'quit': f'{_ACCEL_INDICATOR}Q{_ACCEL_INDICATOR}uit'
    },
    # Accounts menu items:
    'acctMenuNames': {
        'switch': f'{_ACCEL_INDICATOR}S{_ACCEL_INDICATOR}witch account',
        'link': f'{_ACCEL_INDICATOR}L{_ACCEL_INDICATOR}ink account',
        'register': f'{_ACCEL_INDICATOR}R{_ACCEL_INDICATOR}egister account'
    },
    # Help menu items:
    'helpMenuNames': {
        'shortcuts': f'{_ACCEL_INDICATOR}S{_ACCEL_INDICATOR}hortcut Keys',
        'about': f'{_ACCEL_INDICATOR}A{_ACCEL_INDICATOR}bout',
        'version': f'{_ACCEL_INDICATOR}V{_ACCEL_INDICATOR}ersion'
    },
    # Messages:
    'messages': {
        'sizeError': 'Min window size: {cols:}x{rows:}',
        'quit': 'Are you sure you want to quit?',
    },
    'menuBar': {
        'accountLabel': 'Account:',
    },
    # Other:
    'other': {
        'yes': f'{_ACCEL_INDICATOR}Y{_ACCEL_INDICATOR}es',
        'no': f'{_ACCEL_INDICATOR}N{_ACCEL_INDICATOR}o',
    },
}
"""Common strings."""
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
    'logPath': None,
    'theme': 'light',
    'themePath': None,
    'useMouse': False,
    'quitConfirm': True,
    'mouseMoveFocus': False,
    'defaultAccount': None,
}
"""The settings for cliSignal."""

#####################################
# Minimum size of the terminal.
#####################################
MIN_SIZE: Final[tuple[int, int]] = (22, 80)
"""The minimum size of the terminal to display."""

#####################################
# Key character code constants:
#####################################
KEY_ESC: Final[int] = 27
"""Escape key code."""
KEYS_ENTER: Final[tuple[int, int]] = (10, 77)
"""Main enter and keypad enter key codes."""
KEY_TAB: Final[int] = ord('\t')
"""TAB key code."""
KEY_SHIFT_TAB: Final[int] = 353
"""Shift TAB key code."""
KEY_BACKSPACE: Final[int] = 263
"""Backspace key code."""

#####################################
# Button code constants:
#####################################
BUTTON_SCROLL_UP: Final[int] = 0x00200000
"""Mouse scroll up button code."""
BUTTON_SCROLL_DOWN: Final[int] = 0x00010000
"""Mouse scroll down button code."""
BUTTON_SCRAP: Final[int] = 0x10000000
#####################################
# Index Constants:
#####################################
ROW: Final[int] = 0
"""The tuple index for row.."""
COL: Final[int] = 1
"""The tuple index for col."""
HEIGHT: Final[int] = ROW
"""The tuple index for height, or rows."""
WIDTH: Final[int] = COL
"""The tuple index for width, or cols."""
TOP: Final[int] = ROW
"""The tuple index for top, or row of top_left."""
LEFT: Final[int] = COL
"""The tuple index for left, or col of top_left."""
BOTTOM: Final[int] = ROW
"""The tuple index for bottom, or row of bottom_right."""
RIGHT: Final[int] = COL
"""The tuple index for right, or col of bottom_right."""

###################################
# Variables:
###################################
CURRENT_ACCOUNT: Optional[Account] = None
"""The current signal account."""


###################################
# Enumerations:
###################################
class Focus(IntEnum):
    """
    Focused windows / elements. Indexes focus_windows list.
    """
    MAIN = 0
    CONTACTS = 1
    MESSAGES = 2
    TYPING = 3
    MENU_BAR = 4
    STATUS_BAR = 5
    QUIT = 6
    LINK = 7
    QR_CODE = 8
    VERSION = 9


class ButtonCBKeys(Enum):
    """
    Button callback dict keys.
    """
    CLICK = 'on_click'
    """Dict key for clicked callback."""
    DOUBLE_CLICK = 'on_double_click'
    """Dict key for double clicked callback."""


class CBIndex(IntEnum):
    """Enum to hold callback index's."""
    CALLABLE = 0
    """The Callable portion index of the callback."""
    PARAMS = 1
    """The parameter list portion index of the callback."""


class CBStates(Enum):
    """Strings to pass for the different call back states."""
    ACTIVATED = 'activated'
    """Callback activated state."""
    DEACTIVATED = 'deactivated'
    """Callback deactivated state."""
    LEFT_CLICK = 'left_click'
    """Callback left click state."""
    LEFT_DOUBLE_CLICK = 'left_double_click'
    """Callback left double click state."""
    RIGHT_CLICK = 'right_click'
    """Callback right click state."""
    RIGHT_DOUBLE_CLICK = 'right_double_click'
    """Callback right double click state."""


class MenuBarSelections(IntEnum):
    """Available menu selections, indexes self.menu_bar_items, and self.menus in MenuBar."""
    FILE = 0
    """File menu."""
    ACCOUNTS = 1
    """Accounts menu."""
    HELP = 2
    """Help menu."""


class FileMenuSelection(IntEnum):
    """Available file menu selections, indexes self._menu_items in FileMenu."""
    SETTINGS = 0
    """Setting menu item."""
    QUIT = 1
    """Quit menu item."""


class AccountsMenuSelection(IntEnum):
    """Available account menu selections, indexes self._menu_items in AccountsMenu."""
    SWITCH = 0
    """Switch accounts menu item."""
    LINK = 1
    """Link existing account menu item."""
    REGISTER = 2
    """Register new account menu item."""


class HelpMenuSelection(IntEnum):
    """Available help menu selections, indexes self._menu_items in HelpMenu."""
    KEYS = 0
    """Shortcut keys menu item."""
    ABOUT = 1
    """About window menu item."""
    VERSION = 2
    """Version window menu item."""


def __type_check_position_or_size__(position: tuple[int, int]) -> bool:
    """
    Type-check a position tuple.
    :param position: tuple[int, int]: The position to check.
    :return: bool: True passes type-checks, False fails type-checks.
    """

    if not isinstance(position, tuple):
        return False
    if len(position) != 2:
        return False
    if not isinstance(position[0], int):
        return False
    if not isinstance(position[1], int):
        return False
    return True
