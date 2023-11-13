#!/usr/bin/env python3
"""
File: helpMenu.py
Handle the help menu.
"""
import curses
from typing import Optional, Callable, Any
from common import ROW, COL, ROWS, COLS, STRINGS, calc_attributes, HelpMenuSelection
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
        shortcut_label: str = STRINGS['helpMenuNames']['shortcuts']
        shortcut_bg_char: str = STRINGS['background']['shortcutsMenu']
        shortcut_menu_item: MenuItem = MenuItem(std_screen=std_screen,
                                                width=size[COLS] - 2,
                                                top_left=(top_left[ROW] + 1, top_left[COL] + 1),
                                                label=shortcut_label,
                                                bg_char=shortcut_bg_char,
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
        about_label: str = STRINGS['helpMenuNames']['about']
        about_bg_char: str = STRINGS['background']['aboutMenu']
        about_menu_item: MenuItem = MenuItem(std_screen=std_screen,
                                             width=size[COLS] - 2,
                                             top_left=(top_left[ROW] + 2, top_left[COL] + 1),
                                             label=about_label,
                                             bg_char=about_bg_char,
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
        version_label: str = STRINGS['helpMenuNames']['version']
        version_bg_char: str = STRINGS['background']['versionMenu']
        version_menu_item: MenuItem = MenuItem(std_screen=std_screen,
                                               width=size[COLS] - 2,
                                               top_left=(top_left[ROW] + 3, top_left[COL] + 1),
                                               label=version_label,
                                               bg_char=version_bg_char,
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
        Menu.__init__(self, std_screen, size, top_left, menu_items, border_chars, border_attrs)

        # Set internal properties:
        self._selection = HelpMenuSelection.KEYS
        self._last_selection = None
        self._min_selection = HelpMenuSelection.KEYS
        self._max_selection = HelpMenuSelection.VERSION

        # Set the initial selection.
        self._menu_items[self._selection].is_selected = True
        return
