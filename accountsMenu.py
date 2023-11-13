#!/usr/bin/env python3
"""
File: accountsMenu.py
Handle the account menu.
"""
import curses
from typing import Optional, Callable, Any
from common import ROW, COL, ROWS, COLS, STRINGS, calc_attributes, AccountsMenuSelection
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

        # Determine border attrs and chars:
        border_attrs: int = calc_attributes(ThemeColours.ACCOUNTS_MENU_BORDER, theme['acctMenuBorder'])
        border_chars: dict[str, str] = theme['acctMenuBorderChars']

        # Determine attributes from the theme:
        sel_attrs: int = calc_attributes(ThemeColours.ACCOUNTS_MENU_SEL, theme['acctMenuSel'])
        sel_accel_attrs: int = calc_attributes(ThemeColours.ACCOUNTS_MENU_SEL_ACCEL, theme['acctMenuSelAccel'])
        sel_lead_indicator: str = theme['acctMenuSelChars']['leadSel']
        sel_tail_indicator: str = theme['acctMenuSelChars']['tailSel']
        unsel_attrs: int = calc_attributes(ThemeColours.ACCOUNTS_MENU_UNSEL, theme['acctMenuUnsel'])
        unsel_accel_attrs: int = calc_attributes(ThemeColours.ACCOUNTS_MENU_UNSEL_ACCEL, theme['acctMenuUnselAccel'])
        unsel_lead_indicator: str = theme['acctMenuSelChars']['leadUnsel']
        unsel_tail_indicator: str = theme['acctMenuSelChars']['tailUnsel']

        # Create switch account menu item:
        switch_label: str = STRINGS['acctMenuNames']['switch']
        switch_bg_char: str = STRINGS['background']['switchMenu']
        switch_menu_item: MenuItem = MenuItem(std_screen=std_screen,
                                              width=size[COLS] - 2,
                                              top_left=(top_left[ROW] + 1, top_left[COL] + 1),
                                              label=switch_label,
                                              bg_char=switch_bg_char,
                                              sel_attrs=sel_attrs,
                                              sel_accel_attrs=sel_accel_attrs,
                                              sel_lead_indicator=sel_lead_indicator,
                                              sel_tail_indicator=sel_tail_indicator,
                                              unsel_attrs=unsel_attrs,
                                              unsel_accel_attrs=unsel_accel_attrs,
                                              unsel_lead_indicator=unsel_lead_indicator,
                                              unsel_tail_indicator=unsel_tail_indicator,
                                              callback=callbacks['switch']
                                              )
        link_label: str = STRINGS['acctMenuNames']['link']
        link_bg_char: str = STRINGS['background']['linkMenu']
        link_menu_item: MenuItem = MenuItem(std_screen=std_screen,
                                            width=size[COLS] - 2,
                                            top_left=(top_left[ROW] + 2, top_left[COL] + 1),
                                            label=link_label,
                                            bg_char=link_bg_char,
                                            sel_attrs=sel_attrs,
                                            sel_accel_attrs=sel_accel_attrs,
                                            sel_lead_indicator=sel_lead_indicator,
                                            sel_tail_indicator=sel_tail_indicator,
                                            unsel_attrs=unsel_attrs,
                                            unsel_accel_attrs=unsel_accel_attrs,
                                            unsel_lead_indicator=unsel_lead_indicator,
                                            unsel_tail_indicator=unsel_tail_indicator,
                                            callback=callbacks['link']
                                            )
        register_label: str = STRINGS['acctMenuNames']['register']
        register_bg_char: str = STRINGS['background']['registerMenu']
        register_menu_item: MenuItem = MenuItem(std_screen=std_screen,
                                                width=size[COLS] - 2,
                                                top_left=(top_left[ROW] + 3, top_left[COL] + 1),
                                                label=register_label,
                                                bg_char=register_bg_char,
                                                sel_attrs=sel_attrs,
                                                sel_accel_attrs=sel_accel_attrs,
                                                sel_lead_indicator=sel_lead_indicator,
                                                sel_tail_indicator=sel_tail_indicator,
                                                unsel_attrs=unsel_attrs,
                                                unsel_accel_attrs=unsel_accel_attrs,
                                                unsel_lead_indicator=unsel_lead_indicator,
                                                unsel_tail_indicator=unsel_tail_indicator,
                                                callback=callbacks['register']
                                                )
        menu_items: list[MenuItem] = [switch_menu_item, link_menu_item, register_menu_item]

        # Call super:
        Menu.__init__(self, std_screen, size, top_left, menu_items, border_chars, border_attrs)

        # Internal Properties:
        self._selection = AccountsMenuSelection.SWITCH
        self._last_selection = None
        self._min_selection = AccountsMenuSelection.SWITCH
        self._max_selection = AccountsMenuSelection.REGISTER

        # Set initial selection:
        self._menu_items[AccountsMenuSelection.SWITCH].is_selected = True
        return
