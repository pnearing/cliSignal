#!/usr/bin/env python3
"""
File: menu.py
Handle basic menu display and control.
"""
from typing import Any
import curses
from common import ROW, COL, ROWS, COLS, draw_border_on_win
from menuItem import MenuItem
from typeError import __type_error__

def calc_size(menu_labels) -> tuple[int, int]:
    """
    Calculate the menu size given the menu keys and values.
    :param menu_labels: The list of the menu labels.
    :return: tuple[int, int]: The size: (ROWS, COLS).
    """
    # Determine size:
    width: int = 0
    for label in menu_labels:
        width = max(width, len(label))
    height: int = len(menu_labels)
    return height + 2, width + 2  # Add 2 for a border.


class Menu(object):
    """
    Handle basic menu display and control.
    """
########################################
# Initialize:
########################################
    def __init__(self,
                 window: curses.window,
                 size: tuple[int, int],
                 top_left: tuple[int, int],
                 menu_items: list[MenuItem],
                 border_chars: dict[str, str],
                 border_attrs: int,
                 ) -> None:
        """
        Initialize a basic menu.
        :param window: curses.window: The window to draw on.
        :param size: tuple[int, int]: The size of the menu: (ROWS, COLS).
        :param top_left: tuple[int, int]: The top left corner of the menu: (ROW, COL).
        :param menu_items: list[MenuItem]: The items in this menu.
        :param border_chars: dict[str, str]: The border character dict from the theme.
        :param border_attrs: int: The attributes to use for the border of this menu.
        """
        # Run super:
        object.__init__(self)

        # Internal Properties:
        self._window: curses.window = window
        """The curses window to draw on."""
        self._menu_items: list[MenuItem] = menu_items
        """The list of MenuItems for this menu."""
        self._is_activated: bool = False
        """Is this menu activated?"""
        self._border_chars: dict[str, str] = border_chars
        """The characters to use for the border."""
        self._border_attrs: int = border_attrs
        """The attributes to use for the border of this menu."""

        # External properties:
        self.size: tuple[int, int] = size
        """The size of the menu."""
        self.top_left: tuple[int, int] = top_left
        """The top left corner of this menu."""
        self.is_visible: bool = False
        """Is this menu visible?"""
        return

########################################
# Methods:
########################################
    def redraw(self) -> None:
        """
        Redraw the menu.
        :return: None:
        """
        if not self.is_visible:
            return
        # Draw a border:
        draw_border_on_win(window=self._window, border_attrs=self._border_attrs,
                           ts=self._border_chars['ts'], bs=self._border_chars['bs'], ls=self._border_chars['ls'],
                           rs=self._border_chars['rs'], tl=self._border_chars['tl'], tr=self._border_chars['tr'],
                           bl=self._border_chars['bl'], br=self._border_chars['br'], size=self.size,
                           top_left=self.top_left)
        # Draw the menu items:
        for menu_item in self._menu_items:
            menu_item.redraw()
        self._window.refresh()
        return

    def process_key(self, char_code: int) -> bool:
        """
        Process a key press.
        :param char_code: The character code.
        :return: bool: True, character handled, False, it was not handled.
        """
        return False

########################################
# Properties:
########################################
    @property
    def is_activated(self) -> bool:
        """
        Is this menu activated?
        :return: True if this menu is activated, False if not.
        """
        return self._is_activated

    @is_activated.setter
    def is_activated(self, value: bool) -> None:
        """
        Is this menu activated?
        :param value: bool: True, this window is activated, False if not.
        :return: None
        """
        if not isinstance(value, bool):
            __type_error__('value', 'bool', value)
        old_value = self._is_activated
        self._is_activated = value
        if old_value != value:
            self.is_visible = value
            if value:
                self.redraw()
        return
