#!/usr/bin/env python3
"""
File: fileMenu.py
Handle the file menu.
"""
from typing import Optional, Callable, Any
import curses
from enum import IntEnum
from common import ROW, COL, ROWS, COLS, STRINGS, calc_attributes, FileMenuSelection
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

        # Determine size and window attrs:
        size: tuple[int, int] = calc_size(STRINGS['fileMenuNames'].values())
        border_attrs: int = calc_attributes(ThemeColours.FILE_MENU_BORDER, theme['fileMenuBorder'])
        border_chars: dict[str, str] = theme['fileMenuBorderChars']

        # Determine attributes from theme:
        sel_attrs: int = calc_attributes(ThemeColours.FILE_MENU_SEL, theme['fileMenuSel'])
        sel_accel_attrs: int = calc_attributes(ThemeColours.FILE_MENU_SEL_ACCEL, theme['fileMenuSelAccel'])
        sel_lead_indicator: str = theme['fileMenuSelChars']['leadSel']
        sel_tail_indicator: str = theme['fileMenuSelChars']['tailSel']
        unsel_attrs: int = calc_attributes(ThemeColours.FILE_MENU_UNSEL, theme['fileMenuUnsel'])
        unsel_accel_attrs: int = calc_attributes(ThemeColours.FILE_MENU_UNSEL_ACCEL, theme['fileMenuUnselAccel'])
        unsel_lead_indicator: str = theme['fileMenuSelChars']['leadUnsel']
        unsel_tail_indicator: str = theme['fileMenuSelChars']['tailUnsel']

        # Create menu Items:
        settings_label: str = STRINGS['fileMenuNames']['settings']
        settings_bg_char: str = STRINGS['background']['settingsMenu']
        settings_menu_item: MenuItem = MenuItem(std_screen=std_screen,
                                                width=size[COLS] - 2,
                                                top_left=(top_left[ROW] + 1, top_left[COL] + 1),
                                                label=settings_label,
                                                bg_char=settings_bg_char,
                                                sel_attrs=sel_attrs,
                                                sel_accel_attrs=sel_accel_attrs,
                                                sel_lead_indicator=sel_lead_indicator,
                                                sel_tail_indicator=sel_tail_indicator,
                                                unsel_attrs=unsel_attrs,
                                                unsel_accel_attrs=unsel_accel_attrs,
                                                unsel_lead_indicator=unsel_lead_indicator,
                                                unsel_tail_indicator=unsel_tail_indicator,
                                                callback=callbacks['settings']
                                                )
        quit_label: str = STRINGS['fileMenuNames']['quit']
        quit_bg_char: str = STRINGS['background']['quitMenu']
        quit_menu_item: MenuItem = MenuItem(std_screen=std_screen,
                                            width=size[COLS] - 2,
                                            top_left=(top_left[ROW] + 2, top_left[COL] + 1),
                                            label=quit_label,
                                            bg_char=quit_bg_char,
                                            sel_attrs=sel_attrs,
                                            sel_accel_attrs=sel_accel_attrs,
                                            sel_lead_indicator=sel_lead_indicator,
                                            sel_tail_indicator=sel_tail_indicator,
                                            unsel_attrs=unsel_attrs,
                                            unsel_accel_attrs=unsel_accel_attrs,
                                            unsel_lead_indicator=unsel_lead_indicator,
                                            unsel_tail_indicator=unsel_tail_indicator,
                                            callback=callbacks['quit'],
                                            )
        menu_items: list[MenuItem] = [settings_menu_item, quit_menu_item]

        # Call super:
        Menu.__init__(self, std_screen, size, top_left, menu_items, border_chars, border_attrs)

        # Private properties:
        self._selection = FileMenuSelection.SETTINGS
        self._last_selection = None
        self._min_selection = FileMenuSelection.SETTINGS
        self._max_selection = FileMenuSelection.QUIT

        # Set the initial selection:
        self._menu_items[FileMenuSelection.SETTINGS].is_selected = True
        return
