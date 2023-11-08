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


_THEMES: dict[str, dict[str, dict[str, int | bool | str]]] = {
    'light': {
        # Border characters:
        'borderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',  # Sides
                        'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},  # Corners
        # Title start and end characters:
        'titleChars': {'start': '\u2561', 'end': '\u255E'},
        # Menu selection indicator characters:
        'menuSelChars': {'leadSel': '\u2192', 'leadUnsel': ' ', 'tailSel': '\u2190', 'tailUnsel': ' '},
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
        # Menu bar empty spaces:
        'menuEmpty': {'fg': 15, 'bg': 18, 'bold': False, 'underline': False, 'reverse': False},
        # Menu bar item selected:
        'menuSel': {'fg': 15, 'bg': 18, 'bold': True, 'underline': False, 'reverse': False},
        # Menu bar accelerator indicator when selected:
        'menuSelAccel': {'fg': 15, 'bg': 18, 'bold': True, 'underline': True, 'reverse': False},
        # Menu bar item unselected:
        'menuUnsel': {'fg': 15, 'bg': 18, 'bold': False, 'underline': False, 'reverse': False},
        # Menu bar item accelerator indicator when unselected.
        'menuUnselAccel': {'fg': 15, 'bg': 18, 'bold': False, 'underline': True, 'reverse': False},
        # Status bar empty spaces:
        'statusEmpty': {'fg': 15, 'bg': 18, 'bold': False, 'underline': False, 'reverse': False},
    },
    'dark': {
        'titles': {'main': 'cliSignal', 'messages': 'Messages', 'contacts': 'Contacts & Groups', 'typing': None},
        'borderChars': {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',
                        'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},
        'titleChars': {'start': '\u2561', 'end': '\u255E'},
        'menuSelChars': {'leadSel': '\u2192', 'leadUnsel': ' ', 'tailSel': '\u2190', 'tailUnsel': ' '},
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
        'menuEmpty': {'fg': 7, 'bg': 236, 'bold': False, 'underline': False, 'reverse': False},
        'menuSel': {'fg': 7, 'bg': 0, 'bold': True, 'underline': False, 'reverse': True},
        'menuSelAccel': {'fg': 7, 'bg': 0, 'bold': True, 'underline': True, 'reverse': True},
        'menuUnsel': {'fg': 7, 'bg': 0, 'bold': False, 'underline': False, 'reverse': False},
        'menuUnselAccel': {'fg': 7, 'bg': 0, 'bold': False, 'underline': True, 'reverse': False},
        'statusEmpty': {'fg': 7, 'bg': 0, 'bold': False, 'underline': False, 'reverse': False},
    }
}
"""Light and dark theme definitions."""
_ATTRIBUTE_KEYS: list[str] = ['mainWin', 'mainWinBorder', 'mainWinTitle', 'contWin', 'contWinBorder',
                              'contWinTitle', 'msgsWin', 'msgsWinBorder', 'msgsWinTitle', 'typeWin',
                              'typeWinBorder', 'typeWinTitle', 'contNameUnsel', 'contNameSel',
                              'mainWinFBorder', 'msgsWinFBorder', 'contWinFBorder', 'typeWinFBorder',
                              'mainWinFTitle', 'contWinFTitle', 'msgsWinFTitle', 'typeWinFTitle',
                              'menuEmpty', 'statusEmpty', 'menuSel', 'menuSelAccel', 'menuUnsel', 'menuUnselAccel',]
"""Main theme keys."""
_CHAR_KEYS: list[str] = ['borderChars', 'titleChars', 'menuSelChars']
"""Keys with strings."""
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
    for main_key in _ATTRIBUTE_KEYS:
        if main_key not in theme.keys():
            return False, "Key '%s' doesn't exist." % main_key
        for attr_key in _ATTR_KEYS:
            if attr_key not in theme[main_key].keys():
                return False, "Key '%s' missing from '%s'." % (attr_key, main_key)
            elif attr_key in ('fg', 'bg'):
                if theme[main_key][attr_key] < 0 or theme[main_key][attr_key] >= curses.COLORS:
                    return False, "Value at ['%s']['%s'] out of range 0 -> %i." % (main_key, attr_key, curses.COLORS)
    for char_key in _CHAR_KEYS:
        if char_key not in theme.keys():
            return False, "Key '%s' doesn't exist." % char_key
        elif char_key == 'borderChars':
            for border_key in _BORDER_CHAR_KEYS:
                if border_key not in theme[char_key].keys():
                    return False, "Key '%s' missing from 'borderChars'." % border_key
        elif char_key == 'titleChars':
            for title_char_key in _TITLE_CHAR_KEYS:
                if title_char_key not in theme[char_key].keys():
                    return False, "Key '%s' missing from 'titleChars'." % title_char_key

        elif char_key == 'menuSelChars':
            for menu_key in _MENU_SEL_CHAR_KEYS:
                if menu_key not in theme[char_key].keys():
                    return False, "Key '%s' missing from 'menuSelChars'." % menu_key

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
    curses.init_pair(ThemeColours.MAIN_WIN_FOCUS_BORDER, theme['mainWinFBorder']['fg'], theme['mainWinFBorder']['bg'])
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
    curses.init_pair(ThemeColours.MENU_BAR_EMPTY, theme['menuEmpty']['fg'], theme['menuEmpty']['bg'])
    curses.init_pair(ThemeColours.STATUS_BAR_EMPTY, theme['statusEmpty']['fg'], theme['statusEmpty']['bg'])
    curses.init_pair(ThemeColours.MENU_SEL, theme['menuSel']['fg'], theme['menuSel']['bg'])
    curses.init_pair(ThemeColours.MENU_SEL_ACCEL, theme['menuSelAccel']['fg'], theme['menuSelAccel']['bg'])
    curses.init_pair(ThemeColours.MENU_UNSEL, theme['menuUnsel']['fg'], theme['menuUnsel']['bg'])
    curses.init_pair(ThemeColours.MENU_UNSEL_ACCEL, theme['menuUnselAccel']['fg'], theme['menuUnselAccel']['bg'])
    return
