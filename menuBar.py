#!/usr/bin/env python3
"""
File: menuBar.py
Maintain and handle a curses menu bar.
"""
import time
from typing import Optional, Callable, Any
from enum import IntEnum
import curses

import common
from bar import Bar
from menu import Menu
from themes import ThemeColours
from common import ROW, COL, STRINGS, KEY_ESC, KEYS_ENTER, MenuBarSelections, KEY_TAB, KEY_SHIFT_TAB, KEY_BACKSPACE, \
    Focus
from cursesFunctions import calc_attributes, get_rel_mouse_pos, get_left_click, get_left_double_click, add_str
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
                 top_left: tuple[int, int],
                 theme: dict[str, dict[str, int | bool | str]],
                 callbacks: dict[str, dict[str, tuple[Optional[Callable], Optional[list[Any]]]]],
                 ) -> None:
        """
        Initialize the menu bar.
        :param std_screen: curses.window: The window to draw on.
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
        Bar.__init__(self, std_screen, top_left[ROW], empty_attrs, bg_char, Focus.MENU_BAR)

        # Set internal properties:
        self._acct_label_attrs: int = calc_attributes(ThemeColours.MENU_ACCT_LABEL, theme['menuBarAccountLabel'])
        """Account label attributes:"""
        self._acct_text_attrs: int = calc_attributes(ThemeColours.MENU_ACCT_TEXT, theme['menuBarAccountText'])
        """Account value attributes."""
        self._selection: Optional[MenuBarSelections] = None
        """What menu item is selected."""
        self._last_selection: Optional[MenuBarSelections] = None
        """What was last selected."""
        self._acct_label = STRINGS['menuBar']['accountLabel']
        """The account label."""

        # Build the menu items:
        labels: dict[str, str] = STRINGS['mainMenuNames']
        # # File menu:
        file_menu_item_top_left: tuple[int, int] = (self.top_left[ROW], self.top_left[COL] + 1)
        file_menu_top_left: tuple[int, int] = (self.real_top_left[ROW] + 1, self.real_top_left[COL] + 1)
        file_menu: FileMenu = FileMenu(std_screen=self._std_screen,
                                       top_left=file_menu_top_left,
                                       theme=theme,
                                       callbacks=callbacks['file'],
                                       )
        file_menu_item = MenuBarItem(std_screen=self._std_screen,
                                     window=self._window,
                                     top_left=file_menu_item_top_left,
                                     label=labels['file'],
                                     theme=theme,
                                     menu=file_menu,
                                     activate_char_codes=(curses.KEY_F1, ),
                                     deactivate_char_codes=(KEY_ESC, KEY_BACKSPACE)
                                     )
        # # Accounts menu:
        acct_menu_item_top_left: tuple[int, int] = (self.top_left[ROW],
                                                    file_menu_item.top_left[COL] + file_menu_item.width + 1)
        acct_menu_top_left: tuple[int, int] = (self.real_top_left[ROW] + 1,
                                               file_menu_item.top_left[COL] + file_menu_item.width + 1)
        acct_menu = AccountsMenu(std_screen=self._std_screen,
                                 top_left=acct_menu_top_left,
                                 theme=theme,
                                 callbacks=callbacks['accounts']
                                 )
        acct_menu_item = MenuBarItem(std_screen=self._std_screen,
                                     window=self._window,
                                     top_left=acct_menu_item_top_left,
                                     label=labels['accounts'],
                                     theme=theme,
                                     menu=acct_menu,
                                     activate_char_codes=(curses.KEY_F2, ),
                                     deactivate_char_codes=(KEY_ESC, KEY_BACKSPACE),
                                     )
        # # Help menu:
        help_menu_item_top_left: tuple[int, int] = (self.top_left[ROW],
                                                    acct_menu_item_top_left[COL] + acct_menu_item.width + 1)
        help_menu_top_left: tuple[int, int] = (top_left[ROW] + 1,
                                               acct_menu_item_top_left[COL] + acct_menu_item.width + 1)
        help_menu: HelpMenu = HelpMenu(std_screen=self._std_screen,
                                       top_left=help_menu_top_left,
                                       theme=theme,
                                       callbacks=callbacks['help']
                                       )
        help_menu_item = MenuBarItem(std_screen=self._std_screen,
                                     window=self._window,
                                     top_left=help_menu_item_top_left,
                                     label=labels['help'],
                                     theme=theme,
                                     menu=help_menu,
                                     activate_char_codes=(curses.KEY_F3, ),
                                     deactivate_char_codes=(KEY_ESC, KEY_BACKSPACE)
                                     )

        # # Build the menu item list:
        self.menu_bar_items: list[MenuBarItem] = [file_menu_item, acct_menu_item, help_menu_item]
        """The menu bar item list."""

        return

    def redraw(self) -> None:
        """
        Redraw the menu bar.
        :return:
        """
        # Return if not visible:
        if not self.is_visible:
            return
        # Draw background:
        super().redraw()
        # Draw the menu bar items:
        for menu_bar_item in self.menu_bar_items:
            menu_bar_item.redraw()
        # Draw the current account info:
        _, num_cols = self._window.getmaxyx()
        current_account: str = str(common.CURRENT_ACCOUNT)
        total_len = len(self._acct_label) + len(current_account)
        acct_col = (num_cols - 1) - total_len - 1
        self._window.move(0, acct_col)
        add_str(self._window, self._acct_label, self._acct_label_attrs)
        add_str(self._window, ': ', self._acct_text_attrs)
        add_str(self._window, current_account, self._acct_text_attrs)

        # Refresh the window:
        self._window.noutrefresh()
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
        # Make sure the selected item is not activated any more:
        next_selection = int(self.selection) - 1
        if next_selection < MenuBarSelections.FILE:
            next_selection = MenuBarSelections.HELP
        self.selection = MenuBarSelections(next_selection)
        return

    def process_key(self, char_code: int) -> Optional[bool]:
        """
        Process when a key is pressed.
        :param char_code: int: The character code of the key pressed.
        :return: bool: True if this character has been handled.
        """
        # Check for key in activate / deactivate keys:
        for i, menu_bar_item in enumerate(self.menu_bar_items):
            if not menu_bar_item.is_activated and char_code in menu_bar_item.activate_char_codes:
                self.selection = i
                menu_bar_item.is_activated = True
                return True
            elif menu_bar_item.is_activated and char_code in menu_bar_item.deactivate_char_codes:
                self.selection = i
                menu_bar_item.is_activated = False
                return True

        # Process the rest of the keys, only if we're focused since this is run every key press.
        if self.is_focused:
            # Pass the key code to the active menu before processing:
            return_value: Optional[bool] = None
            if self.is_menu_activated:
                return_value = self.active_menu.process_key(char_code)
                if return_value is not None:
                    return return_value

            # Handle Enter:
            if char_code in KEYS_ENTER:
                self.selected_menu_bar_item.is_activated = True
                return True
            # Handle KEY LEFT:
            elif char_code == curses.KEY_LEFT:
                self.dec_selection()
                return True
            # Handle KEY RIGHT
            elif char_code == curses.KEY_RIGHT:
                self.inc_selection()
                return True
        # Character wasn't handled:
        return None

    def process_mouse(self, mouse_pos: tuple[int, int], button_state: int) -> Optional[bool]:
        """
        Process the mouse when the mouse is over the menu bar.
        :param mouse_pos: tuple[int, int]: The current mouse position.
        :param button_state: int: The buttons pressed or not.
        :return: Optional[bool]: True the mouse event was handled and processing should stop, return False, and the
            mouse was not handled and processing should stop, return None, the mouse was not handled and processing
            should continue.
        """
        return_value: Optional[bool]
        # If a menu is active, pass the mouse there:
        if self.is_menu_activated and self.active_menu.is_mouse_over(mouse_pos):
            return_value = self.active_menu.process_mouse(mouse_pos, button_state)
            if return_value is not None:
                return return_value

        # If the mouse is over one of the menu bar items, process the click:
        rel_mouse_pos = get_rel_mouse_pos(mouse_pos, self.real_top_left)
        for i, menu_bar_item in enumerate(self.menu_bar_items):
            if menu_bar_item.is_mouse_over(rel_mouse_pos):
                if get_left_click(button_state):
                    if self.selection == i:
                        menu_bar_item.is_activated = not menu_bar_item.is_activated
                    else:
                        self.selection = i
                        menu_bar_item.is_activated = True
                    return True

        # If mouse hover is on, change the selected menu on move.
        if common.SETTINGS['mouseMoveFocus']:
            for i, menu_bar_item in enumerate(self.menu_bar_items):
                if menu_bar_item.is_mouse_over(rel_mouse_pos):
                    self.selection = i
        return None

    def is_mouse_over(self, mouse_pos: tuple[int, int]) -> bool:
        """
        Is the mouse over the menuBar or active menu.
        :param mouse_pos: tuple[int, int]: The mouse position: (ROW, COL).
        :return: bool: True the mouse is over the menuBar or active menu.
        """
        return_value: bool = super().is_mouse_over(mouse_pos)
        if return_value is True:
            return True

        if self.is_menu_activated:
            return_value = self.active_menu.is_mouse_over(mouse_pos)
            if return_value is True:
                return True
        return False

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

        # Set whether we should deactivate / activate the menus when changing selections:
        reactivate_menu: bool = False
        if self._selection is not None:
            reactivate_menu = self.menu_bar_items[self._selection].is_activated

        # Store the last selection:
        self._last_selection = self._selection

        # Set the value:
        if value is not None:
            self._selection = MenuBarSelections(value)
        else:
            self._selection = None

        # Set / Clear the selection bool, and activated state.:
        if self._selection != self.last_selection:
            if self._selection is not None:
                if reactivate_menu:
                    self.menu_bar_items[self._selection].is_activated = True
                self.menu_bar_items[self._selection].is_selected = True
            if self._last_selection is not None:
                if reactivate_menu:
                    self.menu_bar_items[self._last_selection].is_activated = False
                self.menu_bar_items[self._last_selection].is_selected = False
        return

    @property
    def is_menu_activated(self) -> bool:
        """
        Is a menu activated?; IE: Supposed to be showing.
        :return: bool: True a menu is activated, False if not.
        """
        for menu_bar_item in self.menu_bar_items:
            if menu_bar_item.is_activated:
                return True
        return False

    @property
    def active_menu(self) -> Optional[Menu]:
        """
        Get the active menu.
        :return: Menu: The active menu, or None if None active.
        """
        for menu_bar_item in self.menu_bar_items:
            if menu_bar_item.is_activated:
                return menu_bar_item.menu
        return None

    @property
    def selected_menu_bar_item(self) -> Optional[MenuBarItem]:
        """
        Return the selected menu bar item.
        :return: Optional[MenuBarItem]: The selected menu, or None if no menu selected.
        """
        for menu_bar_item in self.menu_bar_items:
            if menu_bar_item.is_selected:
                return menu_bar_item
        return None

    ######################################
    # Property Hooks:
    ######################################
    def __is_focused_hook__(self, is_get: bool, value: bool) -> None:
        if not is_get:  # The setter was run.
            if value:  # We are getting focus:
                if self.last_selection is not None:
                    self.selection = self.last_selection
                else:
                    self.selection = MenuBarSelections.FILE
            else:  # We are losing focus:
                self.selection = None
        self.redraw()
        return None
