#!/usr/bin/env python3
"""
File: menu.py
Handle basic menu display and control.
"""
from typing import Optional, Callable
import curses
from common import ROW, COL
from menuItem import MenuItem


class Menu(object):
    """
    Handle basic menu display and control.
    """

    def __init__(self,
                 window: curses.window,
                 top_left: tuple[int, int],
                 menu_items: list[MenuItem],
                 theme: dict[str, dict[str, int | bool | str]],
                 ) -> None:
        """
        Initialize a basic menu.
        :param window: curses.window: The window to draw on.
        :param top_left: tuple[int, int]: The top left corner of the menu.
        :param menu_items: list[MenuItem]: The items in this menu.
        :param theme: dict[str, dict[str, int | bool | str]]: The theme in use.
        """
        # Run super:
        object.__init__(self)

        # Internal Properties:
        self._window: curses.window = window
        self._menu_items: list[MenuItem] = menu_items
        self.is_visible: bool = False

        # External properties:
        self.top_left: tuple[int, int] = top_left
        return

    def redraw(self) -> None:
        """
        Redraw the menu.
        :return: None:
        """
        if not self._is_visible:
            return
        for menu_item in self._menu_items:
            menu_item.redraw()
        self._window.noutrefresh()
        return
