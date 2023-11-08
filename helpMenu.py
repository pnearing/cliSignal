#!/usr/bin/env python3
"""
File: helpMenu.py
Handle the help menu.
"""
import curses
from typing import Optional, Callable, Any
from menu import Menu
from menuItem import MenuItem


class HelpMenu(Menu):
    """
    Handle the help menu.
    """
    def __init__(self,
                 window: curses.window,
                 top_left: tuple[int, int],
                 theme: dict[str, dict[str, int | bool | str]],
                 ) -> None:
        """
        Initialize the help menu.
        :param window: curses.window: The window to draw on.
        :param top_left: tuple[int, int]: The top left corner of this menu.
        :param theme: dict[str, dict[str, int | bool | str]: The current theme in use.
        """
        return
