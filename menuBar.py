#!/usr/bin/env python3
"""
File: menuBar.py
Maintain and handle a curses menu bar.
"""
import time
from typing import Optional, Callable
from enum import IntEnum
import curses
from bar import Bar
from themes import ThemeColours
from common import ROW, COL, calc_attributes, STRINGS
from typeError import __type_error__
from menuBarItem import MenuBarItem
from fileMenu import FileMenu
from accountsMenu import AccountsMenu
from helpMenu import HelpMenu


class MenuSelections(IntEnum):
    """Available menu selections, indexes self.menu_items, and self.menu."""
    FILE = 0
    ACCOUNTS = 1
    HELP = 2


class MenuBar(Bar):
    """
    Maintain and handle a curses menu bar.
    """

    def __init__(self,
                 window: curses.window,
                 width: int,
                 top_left: tuple[int, int],
                 theme: dict[str, dict[str, int | bool | str]],
                 callbacks: dict[str, dict[str, Optional[Callable]]],
                 ) -> None:
        """
        Initialize the menu bar.
        :param window: curses.window: The window to draw on.
        :param width: int: The width of the menu bar.
        :param top_left: tuple[int, int]: The top left corner of the menu bar.
        :param theme: dict[str, dict[str, int | bool | str]]: The current theme.
        :param callbacks: dict[str, Optional[Callable]]: The call back dict, keys 'file', 'account', 'help'.
        """
        # Set attributes:
        empty_attrs: int = calc_attributes(ThemeColours.MENU_BAR_EMPTY, theme['menuBG'])
        bg_char: str = STRINGS['background']['menuBar']
        sel_attrs: int = calc_attributes(ThemeColours.MENU_SEL, theme['menuSel'])
        sel_accel_attrs: int = calc_attributes(ThemeColours.MENU_SEL_ACCEL, theme['menuSelAccel'])
        unsel_attrs: int = calc_attributes(ThemeColours.MENU_UNSEL, theme['menuUnsel'])
        unsel_accel_attrs: int = calc_attributes(ThemeColours.MENU_UNSEL_ACCEL, theme['menuUnselAccel'])
        sel_lead_indicator: str = theme['menuSelChars']['leadSel']
        sel_tail_indicator: str = theme['menuSelChars']['tailSel']
        unsel_lead_indicator: str = theme['menuSelChars']['leadUnsel']
        unsel_tail_indicator: str = theme['menuSelChars']['tailUnsel']

        # Run super:
        Bar.__init__(self, window, width, top_left, empty_attrs, bg_char)

        # Set internal properties:
        self._is_focused: bool = False
        """If this menu bar is focused."""
        self._is_menu_activated: bool = False
        """If a menu has been activated."""
        self._selection: MenuSelections = MenuSelections.FILE
        """What menu item is selected."""
        self._active_menu: Optional[FileMenu | AccountsMenu | HelpMenu] = None
        """What menu is active, None if not active."""

        # Build the menu items:
        labels: dict[str, str] = STRINGS['mainMenuNames']
        # File menu:
        file_menu_item_top_left: tuple[int, int] = (top_left[ROW], top_left[COL] + 1)
        file_menu_top_left: tuple[int, int] = (top_left[ROW] + 1, top_left[COL] + 1)
        file_menu: FileMenu = FileMenu(window=self._window,
                                       top_left=file_menu_top_left,
                                       theme=theme,
                                       callbacks=callbacks['file'],
                                       )
        file_menu_item = MenuBarItem(window=self._window,
                                     top_left=file_menu_item_top_left,
                                     label=labels['file'],
                                     sel_attrs=sel_attrs,
                                     sel_accel_attrs=sel_accel_attrs,
                                     sel_lead_indicator=sel_lead_indicator,
                                     sel_tail_indicator=sel_tail_indicator,
                                     unsel_attrs=unsel_attrs,
                                     unsel_accel_attrs=unsel_accel_attrs,
                                     unsel_lead_indicator=unsel_lead_indicator,
                                     unsel_tail_indicator=unsel_tail_indicator,
                                     menu=file_menu,
                                     callback=callbacks['main']['file']
                                     )
        # Accounts menu:
        acct_menu_item_top_left: tuple[int, int] = (top_left[ROW],
                                                    file_menu_item.top_left[COL] + file_menu_item.width + 1)
        acct_menu_top_left: tuple[int, int] = (top_left[ROW] + 1,
                                               file_menu_item.top_left[COL] + file_menu_item.width + 1)
        acct_menu = AccountsMenu(window=self._window,
                                 top_left=acct_menu_top_left,
                                 theme=theme,
                                 callbacks=callbacks['accounts']
                                 )
        acct_menu_item = MenuBarItem(window=self._window,
                                     top_left=acct_menu_item_top_left,
                                     label=labels['accounts'],
                                     sel_attrs=sel_attrs,
                                     sel_accel_attrs=sel_accel_attrs,
                                     sel_lead_indicator=sel_lead_indicator,
                                     sel_tail_indicator=sel_tail_indicator,
                                     unsel_attrs=unsel_attrs,
                                     unsel_accel_attrs=unsel_accel_attrs,
                                     unsel_lead_indicator=unsel_lead_indicator,
                                     unsel_tail_indicator=unsel_tail_indicator,
                                     menu=acct_menu,
                                     callback=callbacks['main']['accounts']
                                     )
        # Help menu:
        help_menu_item_top_left: tuple[int, int] = (top_left[ROW],
                                                    acct_menu_item_top_left[COL] + acct_menu_item.width + 1)
        help_menu_top_left: tuple[int, int] = (top_left[ROW] + 1,
                                               acct_menu_item_top_left[COL] + acct_menu_item.width + 1)
        help_menu: HelpMenu = HelpMenu(window=self._window,
                                       top_left=help_menu_top_left,
                                       theme=theme,
                                       callbacks=callbacks['help']
                                       )
        help_menu_item = MenuBarItem(window=self._window,
                                     top_left=help_menu_item_top_left,
                                     label=labels['help'],
                                     sel_attrs=sel_attrs,
                                     sel_accel_attrs=sel_accel_attrs,
                                     sel_lead_indicator=sel_lead_indicator,
                                     sel_tail_indicator=sel_tail_indicator,
                                     unsel_attrs=unsel_attrs,
                                     unsel_accel_attrs=unsel_accel_attrs,
                                     unsel_lead_indicator=unsel_lead_indicator,
                                     unsel_tail_indicator=unsel_tail_indicator,
                                     menu=help_menu,
                                     callback=callbacks['main']['help']
                                     )

        # Build the menu item list:
        self.menu_bar_items: list[MenuBarItem] = [file_menu_item, acct_menu_item, help_menu_item]
        """The menu item list."""
        self.menus: tuple[FileMenu, AccountsMenu, HelpMenu] = (file_menu, acct_menu, help_menu)
        """The list of menus."""
        return

    def redraw(self) -> None:
        """
        Redraw the menu bar.
        :return:
        """
        if not self.is_visible:
            return
        super().redraw()
        for menu_item in self.menu_bar_items:
            menu_item.redraw()
        self._window.noutrefresh()
        return

    def inc_selection(self) -> None:
        """
        Increment the selection, wrapping if necessary.
        :return: None
        """
        next_selection = int(self.selection) + 1
        if next_selection > MenuSelections.HELP:
            next_selection = MenuSelections.FILE

        self.selection = MenuSelections(next_selection)
        return

    def dec_selection(self) -> None:
        """
        Decrement the selection wrapping if necessary.
        :return: None
        """
        next_selection = int(self.selection) - 1
        if next_selection < MenuSelections.FILE:
            next_selection = MenuSelections.HELP
        self.selection = MenuSelections(next_selection)
        return

    def process_key(self, char_code: int) -> bool:
        """
        Process when a key is pressed.
        :param char_code: int: The character code of the key pressed.
        :return: bool: True if this character has been handled.
        """
        self._window.addstr(11, 10, str(char_code))
        self._window.refresh()
        # time.sleep(1)
        if char_code == curses.KEY_LEFT:
            if self._is_menu_activated:
                self.menu_bar_items[self.selection].deactivate()
            self.dec_selection()
            if self._is_menu_activated:
                self.menu_bar_items[self.selection].activate()
            return True
        elif char_code == curses.KEY_RIGHT:
            if self._is_menu_activated:
                self.menu_bar_items[self.selection].deactivate()
            self.inc_selection()
            if self._is_menu_activated:
                self.menu_bar_items[self.selection].activate()
            return True
        elif char_code == 10 or char_code == 77:  # ENTER key / keypad ENTER key.
            self._active_menu = self.menu_bar_items[self.selection].menu
            self.menu_bar_items[self.selection].is_activated = not self.menu_bar_items[self.selection].is_activated

            return True

        return False

    def activate(self) -> None:
        return

    def deactivate(self) -> None:
        return

    ###################################
    # Properties:
    ###################################
    @property
    def selection(self) -> MenuSelections:
        """
        What menu item is selected; Will be one of Selection enum.
        :return: int: The current selection.
        """
        return self._selection

    @selection.setter
    def selection(self, value: MenuSelections | int) -> None:
        """
        What menu item is selected; Will be one of Selection Enum.
        :param value: MenuSelections | int: The value to set the selection to.
        :raises TypeError: If value is not a member of Selection Enum.
        :raises ValueError: If value is out of range.
        :return: None
        """
        if not isinstance(value, (MenuSelections, int)):
            __type_error__("value", "Selections | int", value)
        if value < MenuSelections.FILE or value > MenuSelections.HELP:
            raise ValueError("value out of range. See MenuSelections enum for range.")
        old_value = self._selection
        self._selection = MenuSelections(value)
        if old_value != value:
            self.menu_bar_items[old_value].is_selected = False
            self.menu_bar_items[value].is_selected = True
        return

    @property
    def is_focused(self) -> bool:
        """
        Is this menu bar focused?
        :return: bool: True if focused, False if not.
        """
        return self._is_focused

    @is_focused.setter
    def is_focused(self, value) -> None:
        """
        Is this menu bar focused?
        Setter.
        :param value: bool: value to set focus state to.
        :raises TypeError: If value is not a bool.
        :return: None
        """
        if not isinstance(value, bool):
            __type_error__("value", "bool", value)
        old_value = self._is_focused
        self._is_focused = value
        if value != old_value:
            if self._is_focused:
                self.menu_bar_items[self.selection].is_selected = True
            else:
                self.menu_bar_items[self.selection].is_selected = False
        return

    @property
    def is_menu_activated(self) -> bool:
        """
        Is a menu activated?; IE: Supposed to be showing.
        :return: bool: True a menu is actvated, False if not.
        """
        return self._is_menu_activated

    @is_menu_activated.setter
    def is_menu_activated(self, value: bool) -> None:
        if not isinstance(value, bool):
            __type_error__('value', 'bool', value)
        old_value = self._is_menu_activated
        self._is_menu_activated = value
        return
