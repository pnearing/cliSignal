#!/usr/bin/env python3
"""
File: accountsMenu.py
Handle the account menu.
"""
import curses
from typing import Optional, Callable, Any
from common import ROW, COL, HEIGHT, WIDTH, STRINGS, AccountsMenuSelection
from cursesFunctions import calc_attributes
from menu import Menu, calc_size
from themes import ThemeColours
from menuItem import MenuItem
from typeError import __type_error__


class AccountsMenu(Menu):
    """
    Handle the account menu.
    """
    def __init__(self,
                 std_screen: curses.window,
                 top_left: tuple[int, int],
                 theme: dict[str, dict[str, int | bool | str]],
                 callbacks: dict[str, tuple[Optional[Callable], Optional[Any]]],
                 ) -> None:
        """
        Initialize the account menu.
        :param std_screen: curses.window: The window to draw on.
        :param top_left: tuple[int, int]: The top left corner of the menu.
        :param theme: dict[str, dict[str, int | bool | str]]: The theme currently in use.
        """

        # Determine size:
        size = calc_size(STRINGS['acctMenuNames'].values())

        window = curses.newwin(size[HEIGHT], size[WIDTH], top_left[ROW], top_left[COL])

        # Create switch account menu item:
        switch_label: str = STRINGS['acctMenuNames']['switch']
        switch_menu_item: MenuItem = MenuItem(std_screen=std_screen,
                                              window=window,
                                              width=size[WIDTH] - 2,
                                              top_left=(1, 1),
                                              label=switch_label,
                                              theme=theme,
                                              callback=callbacks['switch'],
                                              char_codes=[ord('S'), ord('s')],
                                              )
        link_label: str = STRINGS['acctMenuNames']['link']
        link_menu_item: MenuItem = MenuItem(std_screen=std_screen,
                                            window=window,
                                            width=size[WIDTH] - 2,
                                            top_left=(2, 1),
                                            label=link_label,
                                            theme=theme,
                                            callback=callbacks['link'],
                                            char_codes=[ord('L'), ord('l')],
                                            )
        register_label: str = STRINGS['acctMenuNames']['register']
        register_menu_item: MenuItem = MenuItem(std_screen=std_screen,
                                                window=window,
                                                width=size[WIDTH] - 2,
                                                top_left=(3, 1),
                                                label=register_label,
                                                theme=theme,
                                                callback=callbacks['register'],
                                                char_codes=[ord('R'), ord('r')],
                                                )
        menu_items: list[MenuItem] = [switch_menu_item, link_menu_item, register_menu_item]

        # Call super:
        Menu.__init__(self, std_screen, window, size, top_left, menu_items, theme)

        # Internal Properties:
        self._selection = AccountsMenuSelection.SWITCH
        self._last_selection = None
        self._min_selection = AccountsMenuSelection.SWITCH
        self._max_selection = AccountsMenuSelection.REGISTER

        # Set initial selection:
        self._menu_items[self._selection].is_selected = True
        return
