#!/usr/bin/env python3
"""
File: contactsWindow.py
Contacts window management.
"""
from typing import Optional
import curses
from common import ROW, COL, STRINGS, Focus
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
                 std_screen: curses.window,
                 size: tuple[int, int],
                 top_left: tuple[int, int],
                 theme: dict[str, dict[str, int | bool | str]]
                 ) -> None:
        """
        Initialize the contacts' window.
        :param std_screen: curses.window: The std_screen window object.
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
        Window.__init__(self, std_screen, window, title, top_left, window_attrs, border_attrs, border_focus_attrs,
                        border_chars, title_attrs, title_focus_attrs, title_chars, bg_char, Focus.CONTACTS)

        # Set this window as always visible:
        self.always_visible = True
        self.is_static_size = False
        return

