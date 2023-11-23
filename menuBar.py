#!/usr/bin/env python3
"""
File: menuBar.py
Maintain and handle a curses menu bar.
"""
import time
from typing import Optional, Callable, Any
from enum import IntEnum
import curses
from bar import Bar
from themes import ThemeColours
from common import ROW, COL, STRINGS, KEY_ESC, KEYS_ENTER, MenuBarSelections, KEY_TAB, KEY_SHIFT_TAB, KEY_BACKSPACE
from cursesFunctions import calc_attributes
from typeError import __type_error__
from menuBarItem import MenuBarItem
from fileMenu import FileMenu
from accountsMenu import AccountsMenu
from helpMenu import HelpMenu


class MenuBar(Bar):
    """
    Maintain and handle a curses menu bar.
    """

    def __init__(self,
                 std_screen: curses.window,
                 width: int,
                 top_left: tuple[int, int],
                 theme: dict[str, dict[str, int | bool | str]],
                 callbacks: dict[str, dict[str, tuple[Optional[Callable], Optional[list[Any]]]]],
                 ) -> None:
        """
        Initialize the menu bar.
        :param std_screen: curses.window: The window to draw on.
        :param width: int: The width of the menu bar.
        :param top_left: tuple[int, int]: The top left corner of the menu bar.
        :param theme: dict[str, dict[str, int | bool | str]]: The current theme.
        :param callbacks: dict[str, Optional[Callable]]: The call back dict, keys 'file', 'account', 'help'.
        """
        # Set attributes:
        empty_attrs: int = calc_attributes(ThemeColours.MENU_BAR_EMPTY, theme['menuBarBG'])
        bg_char: str = theme['backgroundChars']['menuBar']
        sel_attrs: int = calc_attributes(ThemeColours.MENU_BAR_SEL, theme['menuBarSel'])
        sel_accel_attrs: int = calc_attributes(ThemeColours.MENU_BAR_SEL_ACCEL, theme['menuBarSelAccel'])
        unsel_attrs: int = calc_attributes(ThemeColours.MENU_BAR_UNSEL, theme['menuBarUnsel'])
        unsel_accel_attrs: int = calc_attributes(ThemeColours.MENU_BAR_UNSEL_ACCEL, theme['menuBarUnselAccel'])
        sel_lead_indicator: str = theme['menuBarSelChars']['leadSel']
        sel_tail_indicator: str = theme['menuBarSelChars']['tailSel']
        unsel_lead_indicator: str = theme['menuBarSelChars']['leadUnsel']
        unsel_tail_indicator: str = theme['menuBarSelChars']['tailUnsel']

        # Run super:
        Bar.__init__(self, std_screen, width, top_left, empty_attrs, bg_char)

        # Set internal properties:
        self._is_focused: bool = False
        """If this menu bar is focused."""
        self._selection: Optional[MenuBarSelections] = MenuBarSelections.FILE
        """What menu item is selected."""
        self._last_selection: Optional[MenuBarSelections] = None
        """What was last selected."""
        self._active_menu: Optional[FileMenu | AccountsMenu | HelpMenu] = None
        """What menu is active, None if not active."""

        # Build the menu items:
        labels: dict[str, str] = STRINGS['mainMenuNames']
        # File menu:
        file_menu_item_top_left: tuple[int, int] = (top_left[ROW], top_left[COL] + 1)
        file_menu_top_left: tuple[int, int] = (top_left[ROW] + 1, top_left[COL] + 1)
        file_menu: FileMenu = FileMenu(std_screen=self._std_screen,
                                       top_left=file_menu_top_left,
                                       theme=theme,
                                       callbacks=callbacks['file'],
                                       )
        file_menu_item = MenuBarItem(std_screen=self._std_screen,
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
                                     callback=callbacks['main']['file'],
                                     selection=MenuBarSelections.FILE
                                     )
        # Accounts menu:
        acct_menu_item_top_left: tuple[int, int] = (top_left[ROW],
                                                    file_menu_item.top_left[COL] + file_menu_item.width + 1)
        acct_menu_top_left: tuple[int, int] = (top_left[ROW] + 1,
                                               file_menu_item.top_left[COL] + file_menu_item.width + 1)
        acct_menu = AccountsMenu(std_screen=self._std_screen,
                                 top_left=acct_menu_top_left,
                                 theme=theme,
                                 callbacks=callbacks['accounts']
                                 )
        acct_menu_item = MenuBarItem(std_screen=self._std_screen,
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
                                     callback=callbacks['main']['accounts'],
                                     selection=MenuBarSelections.ACCOUNTS
                                     )
        # Help menu:
        help_menu_item_top_left: tuple[int, int] = (top_left[ROW],
                                                    acct_menu_item_top_left[COL] + acct_menu_item.width + 1)
        help_menu_top_left: tuple[int, int] = (top_left[ROW] + 1,
                                               acct_menu_item_top_left[COL] + acct_menu_item.width + 1)
        help_menu: HelpMenu = HelpMenu(std_screen=self._std_screen,
                                       top_left=help_menu_top_left,
                                       theme=theme,
                                       callbacks=callbacks['help']
                                       )
        help_menu_item = MenuBarItem(std_screen=self._std_screen,
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
                                     callback=callbacks['main']['help'],
                                     selection=MenuBarSelections.HELP
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
        self._std_screen.noutrefresh()
        return

    def inc_selection(self) -> None:
        """
        Increment the selection, wrapping if necessary.
        :return: None
        """
        next_selection = int(self.selection) + 1
        if next_selection > MenuBarSelections.HELP:
            next_selection = MenuBarSelections.FILE

        self.selection = MenuBarSelections(next_selection)
        return

    def dec_selection(self) -> None:
        """
        Decrement the selection wrapping if necessary.
        :return: None
        """
        next_selection = int(self.selection) - 1
        if next_selection < MenuBarSelections.FILE:
            next_selection = MenuBarSelections.HELP
        self.selection = MenuBarSelections(next_selection)
        return

    def process_key(self, char_code: int) -> bool:
        """
        Process when a key is pressed.
        :param char_code: int: The character code of the key pressed.
        :return: bool: True if this character has been handled.
        """
        # Pass the key code to the active menu before parsing:
        if self.is_menu_activated:
            handled: Optional[bool] = self._active_menu.process_key(char_code)
            self._std_screen.addstr(12, 10, str(handled))
            self._std_screen.refresh()
            if isinstance(handled, bool):
                return handled

        if char_code in KEYS_ENTER:  # ENTER key / keypad ENTER key.
            if self.selection is not None:
                self.menu_bar_items[self.selection].activate()
                self._active_menu = self.menus[self.selection]
                return True
        elif char_code in (KEY_ESC, KEY_TAB, KEY_SHIFT_TAB, KEY_BACKSPACE):  # Escape key.
            if self.is_menu_activated:
                self.menu_bar_items[self.selection].deactivate()
                self._active_menu = None
                if char_code in (KEY_TAB, KEY_SHIFT_TAB):
                    return False
                return True
        elif char_code == curses.KEY_LEFT:
            if self.is_menu_activated and self.selection is not None:
                self.menu_bar_items[self.selection].deactivate()
            self.dec_selection()
            if self.is_menu_activated:
                self.menu_bar_items[self.selection].activate()
                self._active_menu = self.menus[self.selection]
            return True
        elif char_code == curses.KEY_RIGHT:
            if self.is_menu_activated and self.selection is not None:
                self.menu_bar_items[self.selection].deactivate()
            self.inc_selection()
            if self.is_menu_activated:
                self.menu_bar_items[self.selection].activate()
                self._active_menu = self.menus[self.selection]
            return True
        # Character wasn't handled:
        return False

    def process_mouse(self, mouse_pos: tuple[int, int], button_state: int) -> bool:
        """
        Process the mouse when the mouse is over the menu bar.
        :param mouse_pos: tuple[int, int]: The current mouse position.
        :param button_state: int: The buttons pressed or not.
        :return: bool: True the mouse event was handled, False it was not.
        """
        if self.is_menu_activated:
            handled: bool = self._active_menu.process_mouse(mouse_pos, button_state)
            if handled:
                return True
        if button_state & curses.BUTTON1_CLICKED != 0 or button_state & curses.BUTTON1_DOUBLE_CLICKED != 0:
            # Check if the click is over the menu bar:
            for menu_bar_item in self.menu_bar_items:
                if menu_bar_item.is_mouse_over(mouse_pos):
                    if self.is_menu_activated and self.selection is not None:
                        self.menu_bar_items[self.selection].deactivate()
                    self.selection = menu_bar_item.selection
                    if self._active_menu == menu_bar_item.menu:
                        menu_bar_item.deactivate()
                        self._active_menu = None
                        self.selection = menu_bar_item.selection
                    else:
                        menu_bar_item.activate()
                        self._active_menu = menu_bar_item.menu
                    return True
            # if self.is_menu_activated:


        return

    ###################################
    # Properties:
    ###################################
    @property
    def last_selection(self) -> Optional[MenuBarSelections]:
        """
        What was the last item selected?; Will be None or one of MenuSelection enum.
        :return: Optional[MenuSelections]: The last selection.
        """
        return self._last_selection

    @property
    def selection(self) -> Optional[MenuBarSelections]:
        """
        What menu item is selected?; Will be one of MenuSelection enum or None.
        :return: Optional[MenuSelections]: The current selection.
        """
        return self._selection

    @selection.setter
    def selection(self, value: Optional[MenuBarSelections | int]) -> None:
        """
        What menu item is selected; Will be one of Selection Enum.
        :param value: MenuSelections | int: The value to set the selection to.
        :raises TypeError: If value is not a member of Selection Enum.
        :raises ValueError: If value is out of range.
        :return: None
        """
        # Value and type check:
        if value is not None:
            if not isinstance(value, (MenuBarSelections, int)):
                __type_error__("value", "Optional[Selections | int]", value)
            elif value < MenuBarSelections.FILE or value > MenuBarSelections.HELP:
                raise ValueError("value out of range. See MenuSelections enum for range.")
        # Store the last selection:
        self._last_selection = self._selection
        # Set the value:
        if value is not None:
            self._selection = MenuBarSelections(value)
        else:
            self._selection = None
        # Set / Clear the selection:
        if self._selection != self.last_selection:
            if self._selection is not None:
                self.menu_bar_items[self.selection].is_selected = True
            if self._last_selection is not None:
                self.menu_bar_items[self._last_selection].is_selected = False
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
        :return: bool: True a menu is activated, False if not.
        """
        return self._active_menu is not None

