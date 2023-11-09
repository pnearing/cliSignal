#!/usr/bin/env python3
"""
File: helpMenu.py
Handle the help menu.
"""
import curses
from typing import Optional, Callable, Any
from common import ROW, COL, ROWS, COLS, STRINGS, calc_attributes
from themes import ThemeColours
from menu import Menu, calc_size
from menuItem import MenuItem


class HelpMenu(Menu):
    """
    Handle the help menu.
    """
    def __init__(self,
                 window: curses.window,
                 top_left: tuple[int, int],
                 theme: dict[str, dict[str, int | bool | str]],
                 callbacks: dict[str, Optional[Callable]],
                 ) -> None:
        """
        Initialize the help menu.
        :param window: curses.window: The window to draw on.
        :param top_left: tuple[int, int]: The top left corner of this menu.
        :param theme: dict[str, dict[str, int | bool | str]: The current theme in use.
        """
        # Determine size:
        size: tuple[int, int] = calc_size(STRINGS['helpMenuNames'].values())
        border_attrs: int = calc_attributes(ThemeColours.HELP_MENU_BORDER, theme['helpMenuBorder'])
        border_chars: dict[str, str] = theme['helpMenuBorderChars']

        # Get the attributes from the theme:
        sel_attrs: int = calc_attributes(ThemeColours.HELP_MENU_SEL, theme['helpMenuSel'])
        sel_accel_attrs: int = calc_attributes(ThemeColours.HELP_MENU_SEL_ACCEL, theme['helpMenuSelAccel'])
        sel_lead_indicator: str = theme['helpMenuSelChars']['leadSel']
        sel_tail_indicator: str = theme['helpMenuSelChars']['tailSel']
        unsel_attrs: int = calc_attributes(ThemeColours.HELP_MENU_UNSEL, theme['helpMenuUnsel'])
        unsel_accel_attrs: int = calc_attributes(ThemeColours.HELP_MENU_UNSEL_ACCEL, theme['helpMenuUnselAccel'])
        unsel_lead_indicator: str = theme['helpMenuSelChars']['leadUnsel']
        unsel_tail_indicator: str = theme['helpMenuSelChars']['tailUnsel']

        # Build the menu items:
        shortcut_menu_item: MenuItem = MenuItem(window=window,
                                                width=size[COLS] - 2,
                                                top_left=(top_left[ROW] + 1, top_left[COL] + 1),
                                                label=STRINGS['helpMenuNames']['shortcuts'],
                                                sel_attrs=sel_attrs,
                                                sel_accel_attrs=sel_accel_attrs,
                                                sel_lead_indicator=sel_lead_indicator,
                                                sel_tail_indicator=sel_tail_indicator,
                                                unsel_attrs=unsel_attrs,
                                                unsel_accel_attrs=unsel_accel_attrs,
                                                unsel_lead_indicator=unsel_lead_indicator,
                                                unsel_tail_indicator=unsel_tail_indicator,
                                                callback=callbacks['shortcuts']
                                                )
        about_menu_item: MenuItem = MenuItem(window=window,
                                             width=size[COLS] - 2,
                                             top_left=(top_left[ROW] + 2, top_left[COL] + 1),
                                             label=STRINGS['helpMenuNames']['about'],
                                             sel_attrs=sel_attrs,
                                             sel_accel_attrs=sel_accel_attrs,
                                             sel_lead_indicator=sel_lead_indicator,
                                             sel_tail_indicator=sel_tail_indicator,
                                             unsel_attrs=unsel_attrs,
                                             unsel_accel_attrs=unsel_accel_attrs,
                                             unsel_lead_indicator=unsel_lead_indicator,
                                             unsel_tail_indicator=unsel_tail_indicator,
                                             callback=callbacks['about']
                                             )
        version_menu_item: MenuItem = MenuItem(window=window,
                                               width=size[COLS] - 2,
                                               top_left=(top_left[ROW] + 3, top_left[COL] + 1),
                                               label=STRINGS['helpMenuNames']['version'],
                                               sel_attrs=sel_attrs,
                                               sel_accel_attrs=sel_accel_attrs,
                                               sel_lead_indicator=sel_lead_indicator,
                                               sel_tail_indicator=sel_tail_indicator,
                                               unsel_attrs=unsel_attrs,
                                               unsel_accel_attrs=unsel_accel_attrs,
                                               unsel_lead_indicator=unsel_lead_indicator,
                                               unsel_tail_indicator=unsel_tail_indicator,
                                               callback=callbacks['version']
                                               )

        menu_items: list[MenuItem] = [shortcut_menu_item, about_menu_item, version_menu_item]

        # Call super:
        Menu.__init__(self, window, size, top_left, menu_items, border_chars, border_attrs)

        return
