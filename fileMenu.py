#!/usr/bin/env python3
"""
File: fileMenu.py
Handle the file menu.
"""
from typing import Optional, Callable, Any
import curses
from enum import IntEnum
from common import ROW, COL, HEIGHT, WIDTH, STRINGS, FileMenuSelection, KEYS_ENTER
from cursesFunctions import calc_attributes
from typeError import __type_error__
from themes import ThemeColours
from menu import Menu, calc_size
from menuItem import MenuItem


class FileMenu(Menu):
    """
    Handle the file menu.
    """
###############################################
# Initialize:
###############################################
    def __init__(self,
                 std_screen: curses.window,
                 top_left: tuple[int, int],
                 theme: dict[str, dict[str, int | bool | str]],
                 callbacks: dict[str, tuple[Optional[Callable], Optional[list[Any]]]],
                 ) -> None:
        """
        Initialize the file menu.
        :param std_screen: curses.window: The window to draw on.
        :param top_left: tuple[int, int]: The top left corner of the file menu.
        :param theme: dict[str, dict[str, int | bool | str]]: The current theme in use.
        :param callbacks: dict[str, Optional[Callable]]: A dict with the callbacks for the file menu items.
        """

        # Determine size and create a window:
        size: tuple[int, int] = calc_size(STRINGS['fileMenuNames'].values())
        window = curses.newwin(size[HEIGHT], size[WIDTH], top_left[ROW], top_left[COL])
        # Create menu Items:
        settings_menu_item: MenuItem = MenuItem(std_screen=std_screen,
                                                window=window,
                                                width=size[WIDTH] - 2,
                                                top_left=(1, 1),
                                                label=STRINGS['fileMenuNames']['settings'],
                                                theme=theme,
                                                callback=callbacks['settings'],
                                                char_codes=[ord('S'), ord('s')],
                                                )
        quit_menu_item: MenuItem = MenuItem(std_screen=std_screen,
                                            window=window,
                                            width=size[WIDTH] - 2,
                                            top_left=(2, 1),
                                            label=STRINGS['fileMenuNames']['quit'],
                                            theme=theme,
                                            callback=callbacks['quit'],
                                            char_codes=[ord('Q'), ord('q')],
                                            )
        menu_items: list[MenuItem] = [settings_menu_item, quit_menu_item]
        #
        # # Call super:
        Menu.__init__(self, std_screen, window, size, top_left, menu_items, theme)
        #
        # # Private properties:
        self._selection = FileMenuSelection.SETTINGS
        self._last_selection = None
        self._min_selection = FileMenuSelection.SETTINGS
        self._max_selection = FileMenuSelection.QUIT

        # Set the initial selection:
        self._menu_items[self._selection].is_selected = True
        return
