#!/usr/bin/env python3
"""
File: contactsWindow.py
Contacts window management.
"""
from typing import Optional
import curses
from common import ROW, COL, STRINGS
from cursesFunctions import calc_attributes
from themes import ThemeColours
from window import Window


class ContactsWindow(Window):
    """
    Class to store the contacts' window.
    """
    _CONTACTS: list[dict[str, str]] = []
    """List of contacts to show."""
    def __init__(self,
                 size: tuple[int, int],
                 top_left: tuple[int, int],
                 theme: dict[str, dict[str, int | bool | str]]
                 ) -> None:
        """
        Initialize the contacts' window.
        :param size: tuple[int, int]: The size of the window, (rows, cols).
        :param top_left: tuple[int, int]: The co-ords of the top left corner, (ROW, COL)
        :param theme: dict[str, dict[str, int | bool]]: The theme to use.
        :returns None
        """
        # Set title and background:
        title: str = STRINGS['titles']['contacts']
        bg_char: str = theme['backgroundChars']['contactsWin']

        # Set the theme attrs:
        window_attrs: int = calc_attributes(ThemeColours.CONTACTS_WIN, theme['contWin'])
        border_attrs: int = calc_attributes(ThemeColours.CONTACT_WIN_BORDER, theme['contWinBorder'])
        border_focus_attrs: int = calc_attributes(ThemeColours.CONTACTS_WIN_FOCUS_BORDER, theme['contWinFBorder'])
        border_chars: dict[str, str] = theme['contWinBorderChars']
        title_attrs: int = calc_attributes(ThemeColours.CONTACT_WIN_TITLE, theme['contWinTitle'])
        title_focus_attrs: int = calc_attributes(ThemeColours.CONTACTS_WIN_FOCUS_TITLE, theme['contWinFTitle'])
        title_chars: dict[str, str] = theme['contWinTitleChars']

        # Make a curses window:
        window = curses.newwin(size[ROW], size[COL], top_left[ROW], top_left[COL])

        # Super the window.
        Window.__init__(self, window, title, top_left, window_attrs, border_attrs, border_focus_attrs, border_chars,
                        title_attrs, title_focus_attrs, title_chars, bg_char)
        return

    def process_key(self, char_code: int) -> bool:
        """
        Process a key press.
        :param char_code: int: The character code.
        :return: bool: True, character handled, False, character not handled.
        """
        return False

    def process_mouse(self, mouse_pos: tuple[int, int], button_state: int) -> bool:
        """
        Process the mouse events.
        :param mouse_pos: tuple[int, int]: The mouse position: (ROW, COL).
        :param button_state: int: The button state.
        :return: bool: True, the mouse event was handled, False it was not.
        """
        return False