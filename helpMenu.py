#!/usr/bin/env python3
"""
File: helpMenu.py
Handle the help menu.
"""
import curses
from typing import Optional, Callable, Any
from common import ROW, COL, HEIGHT, WIDTH, STRINGS, HelpMenuSelection
from cursesFunctions import calc_attributes
from themes import ThemeColours
from menu import Menu, calc_size
from menuItem import MenuItem
from typeError import __type_error__


class HelpMenu(Menu):
    """
    Handle the help menu.
    """
    def __init__(self,
                 std_screen: curses.window,
                 top_left: tuple[int, int],
                 theme: dict[str, dict[str, int | bool | str]],
                 callbacks: dict[str, tuple[Optional[Callable], Optional[list[Any]]]],
                 ) -> None:
        """
        Initialize the help menu.
        :param std_screen: curses.window: The window to draw on.
        :param top_left: tuple[int, int]: The top left corner of this menu.
        :param theme: dict[str, dict[str, int | bool | str]: The current theme in use.
        """
        # Determine size:
        size: tuple[int, int] = calc_size(STRINGS['helpMenuNames'].values())
        window = curses.newwin(size[HEIGHT], size[WIDTH], top_left[ROW], top_left[COL])
        # Build the menu items:
        shortcut_label: str = STRINGS['helpMenuNames']['shortcuts']
        shortcut_menu_item: MenuItem = MenuItem(std_screen=std_screen,
                                                window=window,
                                                width=size[WIDTH] - 2,
                                                top_left=(1, 1),
                                                label=shortcut_label,
                                                theme=theme,
                                                callback=callbacks['shortcuts'],
                                                char_codes=[ord('S'), ord('s')],
                                                )
        about_label: str = STRINGS['helpMenuNames']['about']
        about_menu_item: MenuItem = MenuItem(std_screen=std_screen,
                                             window=window,
                                             width=size[WIDTH] - 2,
                                             top_left=(2, 1),
                                             label=about_label,
                                             theme=theme,
                                             callback=callbacks['about'],
                                             char_codes=[ord('A'), ord('a')],
                                             )
        version_label: str = STRINGS['helpMenuNames']['version']
        version_menu_item: MenuItem = MenuItem(std_screen=std_screen,
                                               window=window,
                                               width=size[WIDTH] - 2,
                                               top_left=(3, 1),
                                               label=version_label,
                                               theme=theme,
                                               callback=callbacks['version'],
                                               char_codes=[ord('V'), ord('v')]
                                               )

        menu_items: list[MenuItem] = [shortcut_menu_item, about_menu_item, version_menu_item]

        # Call super:
        Menu.__init__(self, std_screen, window, size, top_left, menu_items, theme)

        # Set internal properties:
        self._selection = HelpMenuSelection.KEYS
        self._last_selection = None
        self._min_selection = HelpMenuSelection.KEYS
        self._max_selection = HelpMenuSelection.VERSION

        # Set the initial selection.
        self._menu_items[self._selection].is_selected = True
        return
