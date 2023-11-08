#!/usr/bin/env python3
"""
File: accountsMenu.py
Handle the account menu.
"""
import curses
from typing import Optional, Callable, Any
from common import ROW, COL, STRINGS
from menu import Menu
from menuItem import MenuItem


class AccountsMenu(Menu):
    """
    Handle the account menu.
    """
    def __init__(self,
                 window: curses.window,
                 top_left: tuple[int, int],
                 theme: dict[str, dict[str, int | bool | str]],
                 ) -> None:
        """
        Initialize the account menu.
        :param window: curses.window: The window to draw on.
        :param top_left: The top left corner of the menu.
        :param theme: The theme currently in use.
        """
        return
