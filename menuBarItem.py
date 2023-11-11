#!/usr/bin/env python3
from typing import Optional, Callable, Any
from warnings import warn
import curses
from common import ROW, COL, CB_CALLABLE, CB_PARAM, CallbackStates
from typeError import __type_error__
from fileMenu import FileMenu
from accountsMenu import AccountsMenu
from helpMenu import HelpMenu


class MenuBarItem(object):
    """
    Class to hold a single menu item.
    """

#################################
# Initialize:
#################################
    def __init__(self,
                 window: curses.window,
                 top_left: tuple[int, int],
                 label: str,
                 sel_attrs: int,
                 sel_accel_attrs: int,
                 sel_lead_indicator: str,
                 sel_tail_indicator: str,
                 unsel_attrs: int,
                 unsel_accel_attrs: int,
                 unsel_lead_indicator: str,
                 unsel_tail_indicator: str,
                 menu: FileMenu | AccountsMenu | HelpMenu,
                 callback: tuple[Optional[Callable], Optional[list[Any]]],
                 ) -> None:
        """
        Initialize a menu item.
        :param window: curses.window: The window to draw on.
        :param top_left: tuple[int, int]: The top left corner of this menu item.
        :param label: str: The text of the menu item.
        :param sel_attrs: int: The attributes to use when selected.
        :param sel_accel_attrs: int: The attributes to use for the selected accelerator.
        :param sel_lead_indicator: str: The string to append to the beginning of the label when selected.
        :param sel_tail_indicator: str: The string to append to the end of the label when selected.
        :param unsel_attrs: int: The attributes to use when unselected.
        :param unsel_accel_attrs: int: The attributes to use for the unselected accelerator
        :param unsel_lead_indicator: str: The string to append to the beginning of the label when unselected.
        :param unsel_tail_indicator: str The string to append to the end of the label when unselected.
        :param menu: FileMenu | AccountsMenu | HelpMenu: The menu this item holds.
        :param callback: Optional[Callable]: The call back to call when activated.
        """
        # Super:
        object.__init__(self)
        # Private properties
        self._window: curses.window = window
        """The curses window object to draw on."""
        self._sel_attrs: int = sel_attrs
        """The attributes to use when this item is selected."""
        self._sel_accel_attrs: int = sel_accel_attrs
        """The attributes to use for the accelerator."""
        self._sel_lead_indicator: str = sel_lead_indicator
        """The string to append to the beginning of the label when selected."""
        self._sel_tail_indicator: str = sel_tail_indicator
        """The string to append to the end of the label when selected."""
        self._unsel_attrs: int = unsel_attrs
        """The attributes to use when this item is unselected."""
        self._unsel_accel_attrs: int = unsel_accel_attrs
        """The attributes to use for the accelerator when item is unselected."""
        self._unsel_lead_indicator: str = unsel_lead_indicator
        """The string to append to the beginning of the label when unselected."""
        self._unsel_tail_indicator: str = unsel_tail_indicator
        """The string to append to the end of the label when unselected."""
        self._callback: tuple[Optional[Callable], Optional[list[Any]]] = callback
        """The callback to call when activated."""
        self.menu: FileMenu | AccountsMenu | HelpMenu = menu
        """The menu object this menu bar item holds."""
        self._is_selected: bool = False
        """If this item is selected."""
        self._is_activated: bool = False
        """If this item is activated."""

        # Public properties:
        self.top_left: tuple[int, int] = top_left
        """This items top left corner."""
        self.width: int = len(label)  # This is 2 chars longer than the actual width of the title due to accel chars.
        """This items actual width, including leading and trailing spaces."""
        self.label: str = label
        """The label to display."""
        return

#################################
# Internal methods:
#################################
    def _run_callback(self, state: str) -> Optional[Any]:
        """
        Run the callback.
        :param state: str: The current state of the menu.
        :return: Optional[Any]: The return value of the callback.
        """
        return_value: Optional[Any] = None
        if self._callback[CB_CALLABLE] is not None:
            if self._callback[CB_PARAM] is not None:
                return_value = self._callback[CB_CALLABLE](state, self._window, self._callback[CB_PARAM])
            else:
                return_value = self._callback[CB_CALLABLE](state, self._window)
        return return_value

#################################
# Methods:
#################################
    def redraw(self) -> None:
        """
        Redraw this menu item.
        :return: None
        """
        # Move the cursor to the top left corner:
        self._window.move(self.top_left[ROW], self.top_left[COL])
        # Write the leading indicator character:
        if self.is_selected:
            self._window.addstr(self._sel_lead_indicator, self._sel_attrs)
        else:
            self._window.addstr(self._unsel_lead_indicator, self._unsel_attrs)
        # Write the label, parsing the _ as accel indicator start / stop char.
        is_accel: bool = False
        for char in self.label:
            if char == '_':  # If char is underscore flip is_accel
                is_accel = not is_accel
            else:
                # Select attributes for this character:
                attrs: int
                if self.is_selected and is_accel:
                    attrs = self._sel_accel_attrs
                elif self.is_selected and not is_accel:
                    attrs = self._sel_attrs
                elif not self.is_selected and is_accel:
                    attrs = self._unsel_accel_attrs
                else:  # Not self._is_selected and not is_accel:
                    attrs = self._unsel_attrs
                self._window.addstr(char, attrs)
        # Add the trailing selection indicator:
        if self.is_selected:
            self._window.addstr(self._sel_tail_indicator, self._sel_attrs)
        else:
            self._window.addstr(self._unsel_tail_indicator, self._unsel_attrs)

        # If the menu is active, redraw it:
        if self.is_activated:
            self.menu.redraw()
        return

    def activate(self) -> Optional[Any]:
        """
        Activate this menu bar item, show the menu and pass the keys to it.
        :return: Optional[Any]: The return value of the callback
        """
        self.is_activated = True
        self._run_callback(CallbackStates.ACTIVATED.value)
        self.menu.is_activated = True
        return None

    def deactivate(self) -> None:
        self.is_activated = False
        self._run_callback(CallbackStates.DEACTIVATED.value)
        self.menu.is_activated = False
        return

#################################
# Properties:
#################################
    @property
    def is_selected(self) -> bool:
        """
        Is this item selected?
        :return: bool: True item selected, False item is unselected.
        """
        return self._is_selected

    @is_selected.setter
    def is_selected(self, value: bool) -> None:
        """
        Is this item selected?
        Setter.
        :param value: bool: The value to set is_selected to.
        :raises TypeError: When value is not a bool.
        :return: None
        """
        if not isinstance(value, bool):
            __type_error__('value', 'bool', value)
        # old_value = self._is_selected
        self._is_selected = value
        # if value != old_value:
        #     self.redraw()
        return

    @property
    def is_activated(self) -> bool:
        """
        Is this menu bar item activated?
        :return: bool: True, this menu bar is activated, False, it is not.
        """
        return self._is_activated

    @is_activated.setter
    def is_activated(self, value: bool) -> None:
        """
        Is this menu bar item activated?
        Setter.
        :param value: bool: True, this menu bar item is activated, False, it is not.
        :return: None
        :raises TypeError: If value is not a bool.
        """
        if not isinstance(value, bool):
            __type_error__('value', 'bool', value)
        self._is_activated = value
        self.menu.is_activated = value
        return
