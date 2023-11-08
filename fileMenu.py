#!/usr/bin/env python3
"""
File: fileMenu.py
Handle the file menu.
"""
from typing import Optional, Callable, Any
import curses

from common import ROW, COL, STRINGS
from menu import Menu
from menuItem import MenuItem


class FileMenu(Menu):
    """
    Handle the file menu.
    """
    def __init__(self,
                 window: curses.window,
                 top_left: tuple[int, int],
                 theme: dict[str, dict[str, int | bool | str]],
                 callbacks: dict[str, Optional[Callable]],
                 ) -> None:
        """
        Initialize the file menu.
        :param window: curses.window: The window to draw on.
        :param top_left: tuple[int, int]: The top left corner of the file menu.
        :param theme: dict[str, dict[str, int | bool | str]]: The current theme in use.
        :param callbacks: dict[str, Optional[Callable]]: A dict with the callbacks for the file menu items.
        """
        # Store internal properties:
        self._window: curses.window = window
        """The window to draw on."""

        # External properties:
        self.top_left = top_left

        # Determine size:
        width: int = 0
        for label in STRINGS['fileMenuNames'].values():
            width = max(width, len(label))
        height: int = len(STRINGS['fileMenuNames'].keys())
        self.size: tuple[int, int] = (height, width)
        return
