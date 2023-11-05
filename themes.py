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


_THEMES: dict[str, dict[str, dict[str, int | bool | Optional[str]]]] = {
    'light': {
        # Window titles:
        'titles':        {'main': 'cliSignal', 'messages': 'Messages', 'contacts': 'Contacts & Groups', 'typing': None},
        # Border characters:
        'borderChars':   {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',    # Sides
                          'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},   # Corners
        # Title start and end characters:
        'titleChars':    {'start': '\u2561', 'end': '\u255E'},
        # Main window centre:
        'mainWin':       {'fg': 7, 'bg': 18, 'bold': False, 'underline': False, 'reverse': False},
        # Main window border:
        'mainWinBorder': {'fg': 15, 'bg': 18, 'bold': True, 'underline': False, 'reverse': False},
        # Main window title:
        'mainWinTitle':  {'fg': 15, 'bg': 18, 'bold': True, 'underline': True, 'reverse': False},
        # Contacts window centre:
        'contWin':       {'fg': 7, 'bg': 19, 'bold': False, 'underline': False, 'reverse': False},
        # Contacts window border:
        'contWinBorder': {'fg': 15, 'bg': 19, 'bold': True, 'underline': False, 'reverse': False},
        # Contacts window title:
        'contWinTitle':  {'fg': 15, 'bg': 19, 'bold': True, 'underline': True, 'reverse': False},
        # Contacts window unselected name:
        'contNameUnsel': {'fg': 0, 'bg': 19, 'bold': False, 'underline': False, 'reverse': False},
        # Contacts window selected name:
        'contNameSel':   {'fg': 0, 'bg': 19, 'bold': False, 'underline': True, 'reverse': True},
        # Messages window centre:
        'msgsWin':       {'fg': 7, 'bg': 20, 'bold': False, 'underline': False, 'reverse': False},
        # Messages window border:
        'msgsWinBorder': {'fg': 15, 'bg': 20, 'bold': True, 'underline': False, 'reverse': False},
        # Messages window Title:
        'msgsWinTitle':  {'fg': 15, 'bg': 20, 'bold': True, 'underline': True, 'reverse': False},
        # Typing window centre:
        'typeWin':       {'fg': 7, 'bg': 21, 'bold': False, 'underline': False, 'reverse': False},
        # The Typing window border:
        'typeWinBorder': {'fg': 15, 'bg': 21, 'bold': True, 'underline': False, 'reverse': False},
        # Typing window title:
        'typeWinTitle':  {'fg': 15, 'bg': 21, 'bold': True, 'underline': True, 'reverse': False},
    },
    'dark': {
        'titles': {'main': 'cliSignal', 'messages': 'Messages', 'contacts': 'Contacts & Groups', 'typing': None},
        'borderChars':   {'ts': '\u2550', 'bs': '\u2550', 'ls': '\u2551', 'rs': '\u2551',
                          'tl': '\u2554', 'tr': '\u2557', 'bl': '\u255A', 'br': '\u255D'},
        'titleChars': {'start': '\u2561', 'end': '\u255E'},
        'mainWin':       {'fg': 7, 'bg': 237, 'bold': False, 'underline': False, 'reverse': False},
        'mainWinBorder': {'fg': 7, 'bg': 237, 'bold': True, 'underline': False, 'reverse': False},
        'mainWinTitle':  {'fg': 7, 'bg': 237, 'bold': True, 'underline': True, 'reverse': False},
        'contWin':       {'fg': 7, 'bg': 238, 'bold': False, 'underline': False, 'reverse': False},
        'contWinBorder': {'fg': 7, 'bg': 238, 'bold': False, 'underline': False, 'reverse': False},
        'contWinTitle':  {'fg': 7, 'bg': 238, 'bold': True, 'underline': True, 'reverse': False},
        'contNameUnsel': {'fg': 7, 'bg': 238, 'bold': False, 'underline': False, 'reverse': False},
        'contNameSel':   {'fg': 7, 'bg': 238, 'bold': False, 'underline': True, 'reverse': True},
        'msgsWin':       {'fg': 7, 'bg': 239, 'bold': False, 'underline': False, 'reverse': False},
        'msgsWinBorder': {'fg': 7, 'bg': 239, 'bold': True, 'underline': False, 'reverse': False},
        'msgsWinTitle':  {'fg': 7, 'bg': 239, 'bold': True, 'underline': True, 'reverse': False},
        'typeWin':       {'fg': 7, 'bg': 240, 'bold': False, 'underline': False, 'reverse': False},
        'typeWinBorder': {'fg': 7, 'bg': 240, 'bold': True, 'underline': False, 'reverse': False},
        'typeWinTitle':  {'fg': 7, 'bg': 240, 'bold': True, 'underline': True, 'reverse': False},
    }
}
"""Light and dark theme definitions."""
_THEME_MAIN_KEYS: list[str] = ['mainWin', 'mainWinBorder', 'mainWinTitle', 'contWin', 'contWinBorder',
                               'contWinTitle', 'msgsWin', 'msgsWinBorder', 'msgsWinTitle', 'typeWin',
                               'typeWinBorder', 'typeWinTitle', 'contNameUnsel', 'contNameSel']
"""Main theme keys."""
_THEME_CHAR_KEYS: list[str] = ['borderChars', 'titleChars', 'titles']
"""Theme character keys."""
_THEME_ATTR_KEYS: list[str] = ['fg', 'bg', 'bold', 'underline', 'reverse']
"""Theme attribute keys."""
_THEME_BORDER_CHAR_KEYS: list[str] = ['ts', 'bs', 'ls', 'rs', 'tl', 'tr', 'bl', 'br']
"""Theme border character keys."""
_THEME_TITLE_CHAR_KEYS: list[str] = ['start', 'end']
"""Theme title character keys."""
_THEME_TITLE_KEYS: list[str] = ['main', 'messages', 'contacts', 'typing']


def verify_theme(theme: dict[str, dict[str, int | bool | Optional[str]]]) -> tuple[bool, str]:
    """
    Verify a theme dict is correct, has the right keys, and values.
    :param theme: The theme to check.
    :return: bool: True if this theme passes the test, False if not.
    """
    for main_key in _THEME_MAIN_KEYS:
        if main_key not in theme.keys():
            return False, "Key '%s' doesn't exist." % main_key
        for attr_key in _THEME_ATTR_KEYS:
            if attr_key not in theme[main_key].keys():
                return False, "Key '%s' missing from '%s'." % (attr_key, main_key)
            if attr_key in ('fg', 'bg'):
                if theme[main_key][attr_key] not in range(0, curses.COLORS + 1):
                    return False, "Value at ['%s']['%s'] out of range 0 -> %i." % (main_key, attr_key, curses.COLORS)
    for char_key in _THEME_CHAR_KEYS:
        if char_key not in theme.keys():
            return False, "Key '%s' doesn't exist." % char_key
        if char_key == 'borderChars':
            for border_key in _THEME_BORDER_CHAR_KEYS:
                if border_key not in theme[char_key].keys():
                    return False, "Key '%s' missing from 'borderChars'." % border_key
        elif char_key == 'titleChars':
            for title_char_key in _THEME_TITLE_CHAR_KEYS:
                if title_char_key not in theme[char_key].keys():
                    return False, "Key '%s' missing from 'titleChars'." % title_char_key
        elif char_key == 'titles':
            for title_key in _THEME_TITLE_KEYS:
                if title_key not in theme[char_key].keys():
                    return False, "Key '%s' missing from 'titles'." % title_key
    return True, 'PASS'


def load_theme() -> dict[str, dict[str, int | bool | Optional[str]]]:
    """
    Load the current theme.
    :return: dict[str, dict[str, int | bool]]:
    """
    theme: dict[str, dict[Optional[str], int | bool]]
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
    return
