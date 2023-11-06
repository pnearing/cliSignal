#!/usr/bin/env python3
"""
File: menuBar.py
Maintain and handle a curses menu bar.
"""
from typing import Optional
import curses
from bar import Bar
from themes import ThemeColours
from common import ROW, COL, calc_attributes


class MenuItem(object):
    """
    Class to hold a single menu item.
    """

    def __init__(self,
                 col: int,
                 width: int,
                 label: str,
                 sel_attrs: int,
                 sel_accel_attrs: int,
                 unsel_attrs: int,
                 unsel_accel_attrs: int,
                 ) -> None:
        """
        Initialize a menu item.
        :param col: int: The column this menu starts at.
        :param width: int: The width of the menu item.
        :param label: str: The text of the menu item.
        :param sel_attrs: int: The attributes to use when selected.
        :param sel_accel_attrs: int: The attributes to use for the selected accelerator.
        :param unsel_attrs: int: The attributes to use when unselected.
        :param unsel_accel_attrs: int: The attributes to use for the unselected accelerator
        """
        object.__init__(self)
        self.col: int = col
        """This items start column."""
        self.width: int = width
        """This items actual width."""
        self.label: str = label
        """The label to display."""
        self.sel_attrs: int = sel_attrs
        """The attributes to use when this item is selected."""
        self.unsel_attrs: int = unsel_attrs
        """The attributes to use when this item is unselected."""
        self.is_selected: bool = False
        """If this item is selected."""


class MenuBar(Bar):
    """
    Maintain and handle a curses menu bar.
    """

    def __init__(self,
                 window: curses.window,
                 width: int,
                 top_left: tuple[int, int],
                 theme: dict[str, dict[str, int | bool | Optional[str]]]
                 ) -> None:
        """
        Initialize the menu bar.
        :param window: curses.window: The window to draw on.
        :param width: int: The width of the menu bar.
        :param top_left: tuple[int, int]: The top left corner of the menu bar.
        :param theme: dict[str, dict[str, int | bool | Optional[str]]]: The current theme.
        """
        # Set attributes:
        empty_attrs: int = calc_attributes(ThemeColours.MENU_BAR_EMPTY, theme['menuEmpty'])

        # Run super:
        Bar.__init__(self, window, width, top_left, empty_attrs, theme)
        # Build the menu:
        labels: dict[str, str] = theme['mainMenuNames']
        self._menu: list[MenuItem] = []
        file_menu_item_width = len(labels['file'])

        return

    def redraw(self) -> None:
        """
        Redraw the menu bar.
        :return:
        """
        if not self.is_visible:
            return
        super().redraw()
        self._window.refresh()
        return
