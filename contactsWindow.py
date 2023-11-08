#!/usr/bin/env python3
"""
File: contactsWindow.py
Contacts window management.
"""
from typing import Optional
import curses
from common import ROW, COL, calc_attributes, STRINGS
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
                 theme: dict[str, dict[str, int | bool | Optional[str]]]
                 ) -> None:
        """
        Initialize the contacts' window.
        :param size: tuple[int, int]: The size of the window, (rows, cols).
        :param top_left: tuple[int, int]: The co-ords of the top left corner, (ROW, COL)
        :param theme: dict[str, dict[str, int | bool]]: The theme to use.
        :returns None
        """
        # Set the theme attrs:
        window_attrs: int = calc_attributes(ThemeColours.CONTACTS_WIN, theme['contWin'])
        border_attrs: int = calc_attributes(ThemeColours.CONTACT_WIN_BORDER, theme['contWinBorder'])
        border_focus_attrs: int = calc_attributes(ThemeColours.CONTACTS_WIN_FOCUS_BORDER, theme['contWinFBorder'])
        title_attrs: int = calc_attributes(ThemeColours.CONTACT_WIN_TITLE, theme['contWinTitle'])
        title_focus_attrs: int = calc_attributes(ThemeColours.CONTACTS_WIN_FOCUS_TITLE, theme['contWinFTitle'])
        # Make a curses window:
        window = curses.newwin(size[ROW], size[COL], top_left[ROW], top_left[COL])
        # Super the window.
        Window.__init__(self, window, STRINGS['titles']['contacts'], top_left, window_attrs, border_attrs,
                        border_focus_attrs, title_attrs, title_focus_attrs, theme, STRINGS['background']['contacts'])
        return
