#!/usr/bin/env python3
"""
File: common.py
-> Store common constants variables, Enums, etc.
"""
import playsound
import datetime
import logging
import os
import socket
from typing import Optional, Final, Callable, Any, TypeVar

import pytz

from SignalCliApi import SignalAccount, SignalReceiveThread, SignalGroup, SignalContact
from SignalCliApi.signalLinkThread import SignalLinkThread
from cliExceptions import CallbackCausedException
from enum import IntEnum, Enum

# from mainWindow import MainWindow
# from menuBar import MenuBar
from prettyPrint import print_coloured, print_debug, print_error, print_info, print_warning
# from window import Window

Window = TypeVar("Window", bound='window.Window')
MainWindow = TypeVar("MainWindow", bound='mainWindow.MainWindow')
MenuBar = TypeVar("MenuBar", bound='menuBar.MenuBar')

#####################################
# cliSignal version:
#####################################
APP_VERSION: Final[str] = '0.5.0'

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
        'qrcode': 'Scan QR-Code', 'contactsSubWin': 'Contacts', 'groupsSubWin': 'Groups'
    },
    # Group Item labels:
    'groupItemLabels': {
        'numMembers': 'Members',
        'lastSeen': 'Last seen',
        'expires': 'Expires',
        'groupId': 'Group ID',
        'description': 'Description',
        'unknown': 'Unknown',
        'notSet': 'Not set',

    },
    # Contact Item labels:
    'contactItemLabels': {
        'lastSeen': 'Last seen',
        'expires': 'Expires',
        'number': 'Number',
        'uuid': 'UUID',
        'emoji': 'Emoji',
        'about': 'About',
        'unknown': 'Unknown',
        'none': 'None',
        'notSet': 'Not set',
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
        'accountLabel': 'Account',
    },
    'msgsWin': {
        'endOfHist': 'End of history',
        'stickerLabel': 'Sticker',
        'attachLabel': 'Attachment',
        'thumbLabel': 'Thumbnail',
        'previewLabel': 'URL Preview',
        'quoteLabel': 'Quote',
        'replyText': 'said',
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
    'doExpunge': True,
    'theme': 'light',
    'themePath': None,
    'useMouse': False,
    'quitConfirm': True,
    'mouseMoveFocus': False,
    'defaultAccount': None,
    'useSound': True,
    'flashScreen': True,
    'hideUnknownContacts': True,
}
"""The settings for cliSignal."""

#####################################
# Minimum size of the terminal.
#####################################
MIN_SIZE: Final[tuple[int, int]] = (22, 80)
"""The minimum size of the terminal to display."""

#########################################
# Constants:
#########################################
WORKING_DIR_NAME: Final[str] = '.cliSignal'
"""Name of the working directory under $HOME."""
CONFIG_NAME: Final[str] = 'cliSignal'
"""Name to give our config file configuration."""
CONFIG_FILE_NAME: Final[str] = 'cliSignal.config'
"""Name of the cliSignal config file."""
SIGNAL_CONFIG_DIR_NAME: Final[str] = 'signal-cli'
"""Name to give the signal-cli config directory. (where signal-cli stores it's files)."""
SIGNAL_LOG_FILE_NAME: Final[str] = 'signal-cli.log'
"""Name of the signal-cli log file."""
CLI_SIGNAL_LOG_FILE_NAME: Final[str] = 'cliSignal.log'
"""Name of the cliSignal log file."""
WORKING_DIR: Final[str] = os.path.join(os.environ.get("HOME"), WORKING_DIR_NAME)
"""The full path to the working directory."""
SIGNAL_LOG_PATH: Final[str] = os.path.join(WORKING_DIR, SIGNAL_LOG_FILE_NAME)
"""The full path to the log file."""
SIGNAL_CONFIG_DIR: Final[str] = os.path.join(WORKING_DIR, SIGNAL_CONFIG_DIR_NAME)
"""The full path to the default signal-cli config directory."""
CLI_SIGNAL_CONFIG_FILE_PATH: Final[str] = os.path.join(WORKING_DIR, CONFIG_FILE_NAME)
"""The full path to the cliSignal config file."""
CLI_SIGNAL_LOG_PATH: Final[str] = os.path.join(WORKING_DIR, CLI_SIGNAL_LOG_FILE_NAME)
"""The full path to the cliSignal log file."""
HOST_NAME: Final[str] = socket.gethostname().split('.')[0]
"""The host name of the computer running cliSignal."""
DEVICE_NAME: Final[str] = HOST_NAME + '-cliSignal'

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
KEYS_PG_UP: Final[tuple[int, int]] = (339, 57)
"""Page up keys."""
KEYS_PG_DOWN: Final[tuple[int, int]] = (338, 51)
"""Page down keys."""

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


class ContactsFocus(IntEnum):
    """Contact sub window focus indexes"""
    CONTACTS = 0
    """The contact sub window."""
    GROUPS = 1
    """The groups sub window."""


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


#########################################
# Vars:
#########################################
TIME_STARTED: datetime.datetime = pytz.utc.localize(datetime.datetime.utcnow())
"""The time the app started."""
CURRENT_FOCUS: Focus = Focus.CONTACTS
"""The currently focused window."""
LAST_FOCUS: Focus = Focus.MENU_BAR
"""The last focused window."""
FOCUS_WINDOWS: Optional[tuple[Window | MenuBar]] = None
"""The list of windows that switch focus with tab / shift tab."""
MAIN_WINDOW: Optional[MainWindow] = None
"""The main window object."""
EXIT_ERROR: Optional[Exception] = None
"""If we're exiting due to an error, this is the error."""
DEBUG: bool = False
"""True if we should produce debug output."""
VERBOSE: bool = False
"""True if we should produce verbose output."""
RESIZING: bool = False
"""True if we are currently resizing the window."""

MOUSE_RESET_MASK: Optional[int] = None
"""The reset mouse mask."""
SIGNAL_LINK_THREAD: Optional[SignalLinkThread] = None
"""The signal link thread."""
RECEIVE_STARTED: bool = False
"""Has receive started?"""
IS_CURSES_STARTED: bool = False
"""Is curses started?"""
LOGGER: Optional[logging.Logger] = None
"""The logger for this module."""
LOG_LEVEL: Optional[int] = None
CURRENT_ACCOUNT: Optional[SignalAccount] = None
"""The current signal account."""
CURRENT_ACCOUNT_CHANGED: bool = False
"""Has the current account changed?"""
RECEIVE_THREAD: Optional[SignalReceiveThread] = None
"""Has the receive thread been started?"""
CURRENT_RECIPIENT: Optional[SignalGroup | SignalContact] = None
"""The current message recipient to display and send to."""
CURRENT_RECIPIENT_CHANGED: bool = False
"""Has the current recipient changed?"""

###################################
# Status bar variables:
###################################
CHAR_CODE: int = -1
"""The last pressed character code."""
MOUSE_POS: tuple[int, int] = (-1, -1)
"""The last known mouse position."""
BUTTON_STATE: int = -1
"""The last known button state."""


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


def out_info(message: str, force=False) -> None:
    """
    Output an info message to both the log file if logging started, and stdout if curses not started.
    :param message: The message to output
    :param force: Override _VERBOSE
    :return: None
    """
    global IS_CURSES_STARTED, LOGGER
    if not IS_CURSES_STARTED:
        print_info(message, force=True)
    if LOGGER is not None:
        LOGGER.info(message)
    return


def out_error(message) -> None:
    """
    Output an error message to both the log file if logging started and stdout if curses not started.
    :param message: The message to output.
    :return: None
    """
    global IS_CURSES_STARTED, LOGGER
    if not IS_CURSES_STARTED:
        print_error(message)
    if LOGGER is not None:
        LOGGER.error(message)
    return


def out_debug(message) -> None:
    """
    Output a debug message to both the log file if logging started, and stdout if curses not started.
    :param message: The message to output.
    :return: None
    """
    global IS_CURSES_STARTED, LOGGER
    if not IS_CURSES_STARTED:
        print_debug(message)
    if LOGGER is not None:
        LOGGER.debug(message)
    return


def out_warning(message) -> None:
    """
    Output a warning message to both the log file if logging started and stdout if curses is not started.
    :param message: The message to output.
    :return: None
    """
    global IS_CURSES_STARTED, LOGGER
    if not IS_CURSES_STARTED:
        print_warning(message)
    if LOGGER is not None:
        LOGGER.warning(message)
    return


def get_unread_char(num_unread: int) -> str:
    match num_unread:
        case 0: return ' '
        case 1: return '\u2460'
        case 2: return '\u2461'
        case 3: return '\u2462'
        case 4: return '\u2463'
        case 5: return '\u2464'
        case 6: return '\u2465'
        case 7: return '\u2466'
        case 8: return '\u2467'
        case 9: return '\u2468'
        case 10: return '\u2469'
        case 11: return '\u246A'
        case 12: return '\u246B'
        case 13: return '\u246C'
        case 14: return '\u246D'
        case 15: return '\u246E'
        case 16: return '\u246F'
        case 17: return '\u2470'
        case 18: return '\u2471'
        case 19: return '\u2472'
        case 20: return '\u2473'
        case 21: return '\u3251'
        case 22: return '\u3252'
        case 23: return '\u3253'
        case 24: return '\u3254'
        case 25: return '\u3255'
        case 26: return '\u3256'
        case 27: return '\u3257'
        case 28: return '\u3258'
        case 29: return '\u3259'
        case 30: return '\u325A'
        case 31: return '\u325B'
        case 32: return '\u325C'
        case 33: return '\u325D'
        case 34: return '\u325E'
        case 35: return '\u325F'
        case _: return '\u267E'


def get_subscript_char(num: int) -> str:
    match num:
        case 1: return '\u2081'
        case 2: return '\u2082'
        case 3: return '\u2083'
        case 4: return '\u2084'
        case 5: return '\u2085'
        case 6: return '\u2086'
        case 7: return '\u2087'
        case 8: return '\u2088'
        case 9: return '\u2089'
        case _: return '\u208A'

