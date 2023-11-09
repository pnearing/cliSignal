#!/usr/bin/env python3
from typing import TextIO, Optional
from enum import IntEnum
import curses
import json
import common


class ThemeColours(IntEnum):
    """
    Theme colour pair numbers.
    """
    MAIN_WIN = 1
    MAIN_WIN_BORDER = 2
    MAIN_WIN_TITLE = 3
    CONTACTS_WIN = 4
    CONTACT_WIN_BORDER = 5
    CONTACT_WIN_TITLE = 6
    MESSAGES_WIN = 7
    MESSAGES_WIN_BORDER = 8
    MESSAGES_WIN_TITLE = 9
    TYPING_WIN = 10
    TYPING_WIN_BORDER = 11
    TYPING_WIN_TITLE = 12
    CONTACT_NAME_SEL = 13
    CONTACT_NAME_UNSEL = 14
    MAIN_WIN_FOCUS_BORDER = 15
    CONTACTS_WIN_FOCUS_BORDER = 16
    MESSAGES_WIN_FOCUS_BORDER = 17
    TYPING_WIN_FOCUS_BORDER = 18
    MAIN_WIN_FOCUS_TITLE = 19
    CONTACTS_WIN_FOCUS_TITLE = 20
    MESSAGES_WIN_FOCUS_TITLE = 21
    TYPING_WIN_FOCUS_TITLE = 22
    MENU_BAR_EMPTY = 23
    STATUS_BAR_EMPTY = 24
    MENU_UNSEL = 25
    MENU_SEL = 26
    MENU_UNSEL_ACCEL = 27
    MENU_SEL_ACCEL = 28
    FILE_MENU_BORDER = 29
    FILE_MENU_SEL = 30
    FILE_MENU_SEL_ACCEL = 31
    FILE_MENU_UNSEL = 32
    FILE_MENU_UNSEL_ACCEL = 33
    ACCOUNTS_MENU_BORDER = 34
    ACCOUNTS_MENU_SEL = 35
    ACCOUNTS_MENU_SEL_ACCEL = 36
    ACCOUNTS_MENU_UNSEL = 37
    ACCOUNTS_MENU_UNSEL_ACCEL = 38
    HELP_MENU_BORDER = 39
    HELP_MENU_SEL = 40
    HELP_MENU_SEL_ACCEL = 41
    HELP_MENU_UNSEL = 42
    HELP_MENU_UNSEL_ACCEL = 43


_THEMES: dict[str, dict[str, dict[str, int | bool | str]]] = {
    # LIGHT THEME:
    'light': {
        # BORDER CHARACTERS:
        # Main window border characters:
        'mainBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                            'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        # Contacts window border characters:
        'contWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                               'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        # Messages window border characters:
        'msgsWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                               'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        # Typing window border characters:
        'typeWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                               'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        # File menu border characters:
        'fileMenuBorderChars': {'ts': '\u2500', 'bs': '\u2500', 'ls': '\u2502', 'rs': '\u2502',  # Sides
                                'tl': '\u250C', 'tr': '\u2510', 'bl': '\u2514', 'br': '\u2518'},  # Corners
        # Accounts menu border characters:
        'acctMenuBorderChars': {'ts': '\u2500', 'bs': '\u2500', 'ls': '\u2502', 'rs': '\u2502',  # Sides
                                'tl': '\u250C', 'tr': '\u2510', 'bl': '\u2514', 'br': '\u2518'},  # Corners
        # Help menu border characters:
        'helpMenuBorderChars': {'ts': '\u2500', 'bs': '\u2500', 'ls': '\u2502', 'rs': '\u2502',  # Sides
                                'tl': '\u250C', 'tr': '\u2510', 'bl': '\u2514', 'br': '\u2518'},  # Corners

        # TITLE CHARACTERS:
        # Main window Title start and end characters:
        'mainWinTitleChars': {'start': '\u2561', 'end': '\u255E'},
        # Contacts window title start and end characters:
        'contWinTitleChars': {'start': '\u2561', 'end': '\u255E'},
        # Messages window title start and end characters:
        'msgsWinTitleChars': {'start': '\u2561', 'end': '\u255E'},
        # Typing window title start and end characters: NOTE: NOT USED.
        'typeWinTitleChars': {'start': '\u2561', 'end': '\u255E'},

        # MENU SELECTION INDICATOR CHARACTERS:
        # Menu bar selection indicator characters:
        'menuSelChars': {'leadSel': '\u2192', 'leadUnsel': ' ', 'tailSel': '\u2190', 'tailUnsel': ' '},
        # File menu selection indicator characters:
        'fileMenuSelChars': {'leadSel': '\u2192', 'leadUnsel': ' ', 'tailSel': '\u2190', 'tailUnsel': ' '},
        # Accounts menu selection indicator characters:
        'acctMenuSelChars': {'leadSel': '\u2192', 'leadUnsel': ' ', 'tailSel': '\u2190', 'tailUnsel': ' '},
        # Help menu selection indicator characters:
        'helpMenuSelChars': {'leadSel': '\u2192', 'leadUnsel': ' ', 'tailSel': '\u2190', 'tailUnsel': ' '},

        # MAIN WINDOW COLOUR ATTRIBUTES:
        # Main window centre:
        'mainWin': {'fg': 7, 'bg': 18, 'bold': False, 'underline': False, 'reverse': False},
        # Main window border:
        'mainWinBorder': {'fg': 15, 'bg': 18, 'bold': True, 'underline': False, 'reverse': False},
        # Main window focused border NOTE: NOT USED
        'mainWinFBorder': {'fg': 15, 'bg': 18, 'bold': True, 'underline': False, 'reverse': True},
        # Main window title:
        'mainWinTitle': {'fg': 15, 'bg': 18, 'bold': True, 'underline': True, 'reverse': False},
        # Main window focused title:
        'mainWinFTitle': {'fg': 15, 'bg': 19, 'bold': True, 'underline': True, 'reverse': True},

        # CONTACTS WINDOW COLOUR ATTRIBUTES:
        # Contacts window centre:
        'contWin': {'fg': 7, 'bg': 19, 'bold': False, 'underline': False, 'reverse': False},
        # Contacts window border:
        'contWinBorder': {'fg': 15, 'bg': 19, 'bold': True, 'underline': False, 'reverse': False},
        # Contacts window focused border:
        'contWinFBorder': {'fg': 15, 'bg': 19, 'bold': True, 'underline': False, 'reverse': True},
        # Contacts' window title:
        'contWinTitle': {'fg': 15, 'bg': 19, 'bold': True, 'underline': True, 'reverse': False},
        # Contacts window focused title:
        'contWinFTitle': {'fg': 15, 'bg': 19, 'bold': True, 'underline': True, 'reverse': True},
        # Contacts window unselected name:
        'contNameUnsel': {'fg': 0, 'bg': 19, 'bold': False, 'underline': False, 'reverse': False},
        # Contacts window selected name:
        'contNameSel': {'fg': 0, 'bg': 19, 'bold': False, 'underline': True, 'reverse': True},

        # MESSAGES WINDOW COLOUR ATTRIBUTES:
        # Messages window centre:
        'msgsWin': {'fg': 7, 'bg': 20, 'bold': False, 'underline': False, 'reverse': False},
        # Messages window border:
        'msgsWinBorder': {'fg': 15, 'bg': 20, 'bold': True, 'underline': False, 'reverse': False},
        # Messages window focused border:
        'msgsWinFBorder': {'fg': 15, 'bg': 20, 'bold': True, 'underline': False, 'reverse': True},
        # Messages window Title:
        'msgsWinTitle': {'fg': 15, 'bg': 20, 'bold': True, 'underline': True, 'reverse': False},
        # Messages window focused title:
        'msgsWinFTitle': {'fg': 15, 'bg': 20, 'bold': True, 'underline': True, 'reverse': True},

        # TYPING WINDOW COLOUR ATTRIBUTES:
        # The typing window centre:
        'typeWin': {'fg': 7, 'bg': 21, 'bold': False, 'underline': False, 'reverse': False},
        # The Typing window border:
        'typeWinBorder': {'fg': 15, 'bg': 21, 'bold': True, 'underline': False, 'reverse': False},
        # The typing window focused border:
        'typeWinFBorder': {'fg': 15, 'bg': 21, 'bold': True, 'underline': False, 'reverse': True},
        # Typing window title:
        'typeWinTitle': {'fg': 15, 'bg': 21, 'bold': True, 'underline': True, 'reverse': False},
        # Typing window focused title:
        'typeWinFTitle': {'fg': 15, 'bg': 21, 'bold': True, 'underline': True, 'reverse': True},

        # MENU BAR COLOUR ATTRIBUTES:
        # Menu bar background spaces:
        'menuBG': {'fg': 15, 'bg': 18, 'bold': False, 'underline': False, 'reverse': False},
        # Menu bar item selected:
        'menuSel': {'fg': 15, 'bg': 18, 'bold': True, 'underline': False, 'reverse': False},
        # Menu bar accelerator indicator when selected:
        'menuSelAccel': {'fg': 15, 'bg': 18, 'bold': True, 'underline': True, 'reverse': False},
        # Menu bar item unselected:
        'menuUnsel': {'fg': 15, 'bg': 18, 'bold': False, 'underline': False, 'reverse': False},
        # Menu bar item accelerator indicator when unselected.
        'menuUnselAccel': {'fg': 15, 'bg': 18, 'bold': False, 'underline': True, 'reverse': False},

        # STATUS BAR COLOUR ATTRIBUTES:
        # Status bar background spaces:
        'statusBG': {'fg': 15, 'bg': 18, 'bold': False, 'underline': False, 'reverse': False},

        # FILE MENU COLOUR ATTRIBUTES:
        # File menu border:
        'fileMenuBorder': {'fg': 7, 'bg': 20, 'bold': False, 'underline': False, 'reverse': False},
        # FIle menu selected item:
        'fileMenuSel': {'fg': 7, 'bg': 20, 'bold': False, 'underline': False, 'reverse': True},
        # File menu unselected item:
        'fileMenuUnsel': {'fg': 7, 'bg': 20, 'bold': False, 'underline': False, 'reverse': False},
        # File menu selected accelerator:
        'fileMenuSelAccel': {'fg': 7, 'bg': 20, 'bold': False, 'underline': True, 'reverse': True},
        # File menu unselected accelerator:
        'fileMenuUnselAccel': {'fg': 7, 'bg': 20, 'bold': False, 'underline': True, 'reverse': False},

        # ACCOUNTS MENU COLOUR ATTRIBUTES:
        # Accounts menu border:
        'acctMenuBorder': {'fg': 7, 'bg': 20, 'bold': False, 'underline': False, 'reverse': False},
        # Accounts menu selected item.
        'acctMenuSel': {'fg': 7, 'bg': 20, 'bold': False, 'underline': False, 'reverse': True},
        # Accounts menu unselected item.
        'acctMenuUnsel': {'fg': 7, 'bg': 20, 'bold': False, 'underline': False, 'reverse': False},
        # Accounts menu selected accelerator:
        'acctMenuSelAccel': {'fg': 7, 'bg': 20, 'bold': False, 'underline': True, 'reverse': True},
        # Accounts menu unselected accelerator:
        'acctMenuUnselAccel': {'fg': 7, 'bg': 20, 'bold': False, 'underline': True, 'reverse': False},

        # HELP MENU COLOUR ATTRIBUTES:
        # Help menu border:
        'helpMenuBorder': {'fg': 7, 'bg': 20, 'bold': False, 'underline': False, 'reverse': False},
        # Help menu selected item:
        'helpMenuSel': {'fg': 7, 'bg': 20, 'bold': False, 'underline': False, 'reverse': True},
        # Help menu unselected item:
        'helpMenuUnsel': {'fg': 7, 'bg': 20, 'bold': False, 'underline': False, 'reverse': False},
        # Help menu selected accelerator:
        'helpMenuSelAccel': {'fg': 7, 'bg': 20, 'bold': False, 'underline': True, 'reverse': True},
        # Help menu unselected accelerator:
        'helpMenuUnselAccel': {'fg': 7, 'bg': 20, 'bold': False, 'underline': True, 'reverse': False},
    },
    # DARK THEME:
    'dark': {
        'titles': {'main': 'cliSignal', 'messages': 'Messages', 'contacts': 'Contacts & Groups', 'typing': None},
        'mainBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                            'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'contWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                               'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'msgsWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                               'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'typeWinBorderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                               'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        'fileMenuBorderChars': {'ts': '\u2500', 'bs': '\u2500', 'ls': '\u2502', 'rs': '\u2502',  # Sides
                                'tl': '\u250C', 'tr': '\u2510', 'bl': '\u2514', 'br': '\u2518'},  # Corners
        'acctMenuBorderChars': {'ts': '\u2500', 'bs': '\u2500', 'ls': '\u2502', 'rs': '\u2502',  # Sides
                                'tl': '\u250C', 'tr': '\u2510', 'bl': '\u2514', 'br': '\u2518'},  # Corners
        'helpMenuBorderChars': {'ts': '\u2500', 'bs': '\u2500', 'ls': '\u2502', 'rs': '\u2502',  # Sides
                                'tl': '\u250C', 'tr': '\u2510', 'bl': '\u2514', 'br': '\u2518'},  # Corners
        'mainWinTitleChars': {'start': '\u2561', 'end': '\u255E'},
        'contWinTitleChars': {'start': '\u2561', 'end': '\u255E'},
        'msgsWinTitleChars': {'start': '\u2561', 'end': '\u255E'},
        'typeWinTitleChars': {'start': '\u2561', 'end': '\u255E'},
        'menuSelChars': {'leadSel': '\u2192', 'leadUnsel': ' ', 'tailSel': '\u2190', 'tailUnsel': ' '},
        'fileMenuSelChars': {'leadSel': '\u2192', 'leadUnsel': ' ', 'tailSel': '\u2190', 'tailUnsel': ' '},
        'acctMenuSelChars': {'leadSel': '\u2192', 'leadUnsel': ' ', 'tailSel': '\u2190', 'tailUnsel': ' '},
        'helpMenuSelChars': {'leadSel': '\u2192', 'leadUnsel': ' ', 'tailSel': '\u2190', 'tailUnsel': ' '},
        'mainWin': {'fg': 7, 'bg': 237, 'bold': False, 'underline': False, 'reverse': False},
        'mainWinBorder': {'fg': 7, 'bg': 237, 'bold': True, 'underline': False, 'reverse': False},
        'mainWinFBorder': {'fg': 7, 'bg': 237, 'bold': True, 'underline': False, 'reverse': True},
        'mainWinTitle': {'fg': 7, 'bg': 237, 'bold': True, 'underline': True, 'reverse': False},
        'mainWinFTitle': {'fg': 7, 'bg': 237, 'bold': True, 'underline': True, 'reverse': True},
        'contWin': {'fg': 7, 'bg': 238, 'bold': False, 'underline': False, 'reverse': False},
        'contWinBorder': {'fg': 7, 'bg': 238, 'bold': True, 'underline': False, 'reverse': False},
        'contWinFBorder': {'fg': 7, 'bg': 238, 'bold': True, 'underline': False, 'reverse': True},
        'contWinTitle': {'fg': 7, 'bg': 238, 'bold': True, 'underline': True, 'reverse': False},
        'contWinFTitle': {'fg': 7, 'bg': 238, 'bold': True, 'underline': True, 'reverse': True},
        'contNameUnsel': {'fg': 7, 'bg': 238, 'bold': False, 'underline': False, 'reverse': False},
        'contNameSel': {'fg': 7, 'bg': 238, 'bold': False, 'underline': True, 'reverse': True},
        'msgsWin': {'fg': 7, 'bg': 239, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinBorder': {'fg': 7, 'bg': 239, 'bold': True, 'underline': False, 'reverse': False},
        'msgsWinFBorder': {'fg': 7, 'bg': 239, 'bold': True, 'underline': False, 'reverse': True},
        'msgsWinTitle': {'fg': 7, 'bg': 239, 'bold': True, 'underline': True, 'reverse': False},
        'msgsWinFTitle': {'fg': 7, 'bg': 239, 'bold': True, 'underline': True, 'reverse': True},
        'typeWin': {'fg': 7, 'bg': 240, 'bold': False, 'underline': False, 'reverse': False},
        'typeWinBorder': {'fg': 7, 'bg': 240, 'bold': True, 'underline': False, 'reverse': False},
        'typeWinFBorder': {'fg': 7, 'bg': 240, 'bold': True, 'underline': False, 'reverse': True},
        'typeWinTitle': {'fg': 7, 'bg': 240, 'bold': True, 'underline': True, 'reverse': False},
        'typeWinFTitle': {'fg': 7, 'bg': 240, 'bold': True, 'underline': True, 'reverse': True},
        'menuBG': {'fg': 7, 'bg': 236, 'bold': False, 'underline': False, 'reverse': False},
        'menuSel': {'fg': 7, 'bg': 0, 'bold': True, 'underline': False, 'reverse': True},
        'menuSelAccel': {'fg': 7, 'bg': 0, 'bold': True, 'underline': True, 'reverse': True},
        'menuUnsel': {'fg': 7, 'bg': 0, 'bold': False, 'underline': False, 'reverse': False},
        'menuUnselAccel': {'fg': 7, 'bg': 0, 'bold': False, 'underline': True, 'reverse': False},
        'statusBG': {'fg': 7, 'bg': 0, 'bold': False, 'underline': False, 'reverse': False},
        'fileMenuBorder': {'fg': 7, 'bg': 237, 'bold': False, 'underline': False, 'reverse': False},
        'fileMenuSel': {'fg': 7, 'bg': 237, 'bold': True, 'underline': False, 'reverse': True},
        'fileMenuUnsel': {'fg': 7, 'bg': 237, 'bold': False, 'underline': False, 'reverse': False},
        'fileMenuSelAccel': {'fg': 7, 'bg': 237, 'bold': False, 'underline': True, 'reverse': True},
        'fileMenuUnselAccel': {'fg': 7, 'bg': 237, 'bold': False, 'underline': True, 'reverse': False},
        'acctMenuBorder': {'fg': 7, 'bg': 237, 'bold': False, 'underline': False, 'reverse': False},
        'acctMenuSel': {'fg': 7, 'bg': 237, 'bold': False, 'underline': False, 'reverse': True},
        'acctMenuUnsel': {'fg': 7, 'bg': 237, 'bold': False, 'underline': False, 'reverse': False},
        'acctMenuSelAccel': {'fg': 7, 'bg': 237, 'bold': False, 'underline': True, 'reverse': True},
        'acctMenuUnselAccel': {'fg': 7, 'bg': 237, 'bold': False, 'underline': True, 'reverse': False},
        'helpMenuBorder': {'fg': 7, 'bg': 237, 'bold': False, 'underline': False, 'reverse': False},
        'helpMenuSel': {'fg': 7, 'bg': 237, 'bold': False, 'underline': False, 'reverse': True},
        'helpMenuUnsel': {'fg': 7, 'bg': 237, 'bold': False, 'underline': False, 'reverse': False},
        'helpMenuSelAccel': {'fg': 7, 'bg': 237, 'bold': False, 'underline': True, 'reverse': True},
        'helpMenuUnselAccel': {'fg': 7, 'bg': 237, 'bold': False, 'underline': True, 'reverse': False},
    }
}
"""Light and dark theme definitions."""

# Primary Keys:
_ATTRIBUTE_PRIMARY_KEYS: list[str] = ['mainWin', 'mainWinBorder', 'mainWinTitle', 'contWin', 'contWinBorder',
                                      'contWinTitle', 'msgsWin', 'msgsWinBorder', 'msgsWinTitle', 'typeWin',
                                      'typeWinBorder', 'typeWinTitle', 'contNameUnsel', 'contNameSel',
                                      'mainWinFBorder', 'msgsWinFBorder', 'contWinFBorder', 'typeWinFBorder',
                                      'mainWinFTitle', 'contWinFTitle', 'msgsWinFTitle', 'typeWinFTitle',
                                      'menuBG', 'statusBG', 'menuSel', 'menuSelAccel', 'menuUnsel', 'menuUnselAccel',
                                      'fileMenuBorder', 'acctMenuBorder', 'helpMenuBorder',
                                      ]
"""Primary attribute theme keys."""
_TITLE_CHAR_PRIMARY_KEYS: list[str] = ['mainWinTitleChars', 'contWinTitleChars', 'msgsWinTitleChars',
                                       'typeWinTitleChars']
"""Title characters primary keys."""
_MENU_SEL_PRIMARY_KEYS: list[str] = ['menuSelChars', 'fileMenuSelChars', 'acctMenuSelChars', 'helpMenuSelChars']
"""Menu selection primary keys."""

_BORDER_PRIMARY_KEYS: list[str] = ['mainBorderChars', 'contWinBorderChars', 'msgsWinBorderChars', 'typeWinBorderChars',
                                   'fileMenuBorderChars', 'acctMenuBorderChars', 'helpMenuBorderChars']
"""Keys with border strings."""

# Sub keys:
_ATTR_KEYS: list[str] = ['fg', 'bg', 'bold', 'underline', 'reverse']
"""Attribute keys."""
_BORDER_CHAR_KEYS: list[str] = ['ts', 'bs', 'ls', 'rs', 'tl', 'tr', 'bl', 'br']
"""Border character keys."""
_TITLE_CHAR_KEYS: list[str] = ['start', 'end']
"""Title character keys."""
_MENU_SEL_CHAR_KEYS: list[str] = ['leadSel', 'leadUnsel', 'tailSel', 'tailUnsel']
"""Menu selection indicator character keys."""


def verify_theme(theme: dict[str, dict[str, int | bool | str]]) -> tuple[bool, str]:
    """
    Verify a theme dict is correct, has the right keys, and values.
    :param theme: The theme to check.
    :return: bool: True if this theme passes the test, False if not.
    """
    # Colour / font attribute keys:
    for main_key in _ATTRIBUTE_PRIMARY_KEYS:
        if main_key not in theme.keys():
            return False, "Primary key '%s' doesn't exist." % main_key
        for attr_key in _ATTR_KEYS:
            if attr_key not in theme[main_key].keys():
                return False, "Key '%s' missing from '%s'." % (attr_key, main_key)
            elif attr_key in ('fg', 'bg'):
                if theme[main_key][attr_key] < 0 or theme[main_key][attr_key] >= curses.COLORS:
                    return False, "Value at ['%s']['%s'] out of range 0 -> %i." % (main_key, attr_key, curses.COLORS)

    # Border character keys:
    for border_key in _BORDER_PRIMARY_KEYS:
        if border_key not in theme.keys():
            return False, "Primary key '%s' doesn't exist." % border_key
        for border_char_key in _BORDER_CHAR_KEYS:
            if border_char_key not in theme[border_key].keys():
                return False, "Key '%s' missing from '%s'." % (border_char_key, border_key)

    # Menu selection character keys:
    for menu_sel_primary_key in _MENU_SEL_PRIMARY_KEYS:
        if menu_sel_primary_key not in theme.keys():
            return False, "Primary key '%s' doesn't exist." % menu_sel_primary_key
        for menu_sel_key in _MENU_SEL_CHAR_KEYS:
            if menu_sel_key not in theme[menu_sel_primary_key].keys():
                return False, "Key '%s' missing from '%s'." % (menu_sel_key, menu_sel_primary_key)

    # Title character keys:
    for title_char_primary_key in _TITLE_CHAR_PRIMARY_KEYS:
        if title_char_primary_key not in theme.keys():
            return False, "Primary key '%s' doesn't exist." % title_char_primary_key
        for title_char_key in _TITLE_CHAR_KEYS:
            if title_char_key not in theme[title_char_primary_key].keys():
                return False, "Key '%s' missing from '%s'." % (title_char_key, title_char_primary_key)

    # Everything is good:
    return True, 'PASS'


def load_theme() -> dict[str, dict[str, int | bool | str]]:
    """
    Load the current theme.
    :return: dict[str, dict[str, int | bool]]:
    """
    theme: dict[str, dict[str, int | bool | str]]
    if common.SETTINGS['theme'] == 'light':
        theme = _THEMES['light']
    elif common.SETTINGS['theme'] == 'dark':
        theme = _THEMES['dark']
    elif common.SETTINGS['theme'] == 'custom':
        try:
            file_handle: TextIO = open(common.SETTINGS['themePath'], 'r')
            theme = json.loads(file_handle.read())
            file_handle.close()
        except (OSError, FileNotFoundError, PermissionError) as e:
            raise RuntimeError("Failed to open '%s' for reading: %s" % (common.SETTINGS['themePath'], str(e.args)))
        except json.JSONDecodeError as e:
            raise RuntimeError("Failed to load JSON from '%s': %s" % (common.SETTINGS['themePath'], e.msg))
    else:
        raise RuntimeError("Invalid theme: '%s' is not 'light', 'dark', or 'custom'.")
    # Verify the theme:
    result, message = verify_theme(theme)
    if result:
        return theme
    raise RuntimeError("Invalid theme: %s." % message)


def init_colours(theme: dict[str, dict[str, int | bool | Optional[str]]]) -> None:
    """
    Initialize the colour pairs:
    :param theme: The colour theme dict.
    :return: None
    """
    curses.init_pair(ThemeColours.MAIN_WIN, theme['mainWin']['fg'], theme['mainWin']['bg'])
    curses.init_pair(ThemeColours.MAIN_WIN_BORDER, theme['mainWinBorder']['fg'], theme['mainWinBorder']['bg'])
    curses.init_pair(ThemeColours.MAIN_WIN_TITLE, theme['mainWinTitle']['fg'], theme['mainWinTitle']['bg'])
    curses.init_pair(ThemeColours.CONTACTS_WIN, theme['contWin']['fg'], theme['contWin']['bg'])
    curses.init_pair(ThemeColours.CONTACT_WIN_BORDER, theme['contWinBorder']['fg'], theme['contWinBorder']['bg'])
    curses.init_pair(ThemeColours.CONTACT_WIN_TITLE, theme['contWinTitle']['fg'], theme['contWinTitle']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN, theme['msgsWin']['fg'], theme['msgsWin']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_BORDER, theme['msgsWinBorder']['fg'], theme['msgsWinBorder']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_TITLE, theme['msgsWinTitle']['fg'], theme['msgsWinTitle']['bg'])
    curses.init_pair(ThemeColours.TYPING_WIN, theme['typeWin']['fg'], theme['typeWin']['bg'])
    curses.init_pair(ThemeColours.TYPING_WIN_BORDER, theme['typeWinBorder']['fg'], theme['typeWinBorder']['bg'])
    curses.init_pair(ThemeColours.TYPING_WIN_TITLE, theme['typeWinTitle']['fg'], theme['typeWinTitle']['bg'])
    curses.init_pair(ThemeColours.CONTACT_NAME_SEL, theme['contNameSel']['fg'], theme['contNameSel']['bg'])
    curses.init_pair(ThemeColours.CONTACT_NAME_UNSEL, theme['contNameUnsel']['fg'], theme['contNameUnsel']['bg'])
    curses.init_pair(ThemeColours.MAIN_WIN_FOCUS_BORDER, theme['mainWinFBorder']['fg'],
                     theme['mainWinFBorder']['bg'])
    curses.init_pair(ThemeColours.CONTACTS_WIN_FOCUS_BORDER, theme['contWinFBorder']['fg'],
                     theme['contWinFBorder']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_FOCUS_BORDER, theme['msgsWinFBorder']['fg'],
                     theme['msgsWinFBorder']['bg'])
    curses.init_pair(ThemeColours.TYPING_WIN_FOCUS_BORDER, theme['typeWinFBorder']['fg'],
                     theme['typeWinFBorder']['bg'])
    curses.init_pair(ThemeColours.MAIN_WIN_FOCUS_TITLE, theme['mainWinFTitle']['fg'],
                     theme['mainWinFTitle']['bg'])
    curses.init_pair(ThemeColours.CONTACTS_WIN_FOCUS_TITLE, theme['contWinFTitle']['fg'],
                     theme['contWinFTitle']['bg'])
    curses.init_pair(ThemeColours.MESSAGES_WIN_FOCUS_TITLE, theme['msgsWinFTitle']['fg'],
                     theme['msgsWinFTitle']['bg'])
    curses.init_pair(ThemeColours.TYPING_WIN_FOCUS_TITLE, theme['typeWinFTitle']['fg'],
                     theme['typeWinFTitle']['bg'])
    curses.init_pair(ThemeColours.MENU_BAR_EMPTY, theme['menuBG']['fg'], theme['menuBG']['bg'])
    curses.init_pair(ThemeColours.STATUS_BAR_EMPTY, theme['statusBG']['fg'], theme['statusBG']['bg'])
    curses.init_pair(ThemeColours.MENU_SEL, theme['menuSel']['fg'], theme['menuSel']['bg'])
    curses.init_pair(ThemeColours.MENU_SEL_ACCEL, theme['menuSelAccel']['fg'], theme['menuSelAccel']['bg'])
    curses.init_pair(ThemeColours.MENU_UNSEL, theme['menuUnsel']['fg'], theme['menuUnsel']['bg'])
    curses.init_pair(ThemeColours.MENU_UNSEL_ACCEL, theme['menuUnselAccel']['fg'], theme['menuUnselAccel']['bg'])
    curses.init_pair(ThemeColours.FILE_MENU_BORDER, theme['fileMenuBorder']['fg'], theme['fileMenuBorder']['bg'])
    curses.init_pair(ThemeColours.FILE_MENU_SEL, theme['fileMenuSel']['fg'], theme['fileMenuSel']['bg'])
    curses.init_pair(ThemeColours.FILE_MENU_UNSEL, theme['fileMenuUnsel']['fg'], theme['fileMenuUnsel']['bg'])
    curses.init_pair(ThemeColours.ACCOUNTS_MENU_BORDER, theme['acctMenuBorder']['fg'], theme['acctMenuBorder']['bg'])
    curses.init_pair(ThemeColours.ACCOUNTS_MENU_SEL, theme['acctMenuSel']['fg'], theme['acctMenuSel']['bg'])
    curses.init_pair(ThemeColours.ACCOUNTS_MENU_UNSEL, theme['acctMenuUnsel']['fg'], theme['acctMenuUnsel']['bg'])
    curses.init_pair(ThemeColours.HELP_MENU_BORDER, theme['helpMenuBorder']['fg'], theme['helpMenuBorder']['bg'])
    curses.init_pair(ThemeColours.HELP_MENU_SEL, theme['helpMenuSel']['fg'], theme['helpMenuUnsel']['bg'])
    curses.init_pair(ThemeColours.HELP_MENU_UNSEL, theme['helpMenuUnsel']['fg'], theme['helpMenuUnsel']['bg'])
    curses.init_pair(ThemeColours.FILE_MENU_SEL_ACCEL, theme['fileMenuSelAccel']['fg'], theme['fileMenuSelAccel']['bg'])
    curses.init_pair(ThemeColours.FILE_MENU_UNSEL_ACCEL, theme['fileMenuUnselAccel']['fg'],
                     theme['fileMenuUnselAccel']['bg'])
    curses.init_pair(ThemeColours.ACCOUNTS_MENU_SEL_ACCEL, theme['acctMenuSelAccel']['fg'],
                     theme['acctMenuSelAccel']['bg'])
    curses.init_pair(ThemeColours.ACCOUNTS_MENU_UNSEL_ACCEL, theme['acctMenuUnselAccel']['fg'],
                     theme['acctMenuUnselAccel']['bg'])
    curses.init_pair(ThemeColours.HELP_MENU_SEL_ACCEL, theme['helpMenuSelAccel']['fg'], theme['helpMenuSelAccel']['bg'])
    curses.init_pair(ThemeColours.HELP_MENU_UNSEL_ACCEL, theme['helpMenuUnselAccel']['fg'],
                     theme['helpMenuUnselAccel']['bg'])
    return

