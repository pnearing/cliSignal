#!/usr/bin/env python3
from typing import Optional, Callable, Any
from warnings import warn
import curses
from common import ROW, COL
from typeError import __type_error__
from fileMenu import FileMenu
from accountsMenu import AccountsMenu
from helpMenu import HelpMenu


class MenuBarItem(object):
    """
    Class to hold a single menu item.
    """

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
                 menu: Optional[FileMenu | AccountsMenu | HelpMenu],
                 callback: Optional[Callable] = None,
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
        :param menu: [FileMenu | AccountsMenu | HelpMenu]: The menu this item holds.
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
        self._callback: Optional[Callable] = callback
        """The callback to call when activated."""
        self._menu: [FileMenu | AccountsMenu | HelpMenu] = menu
        """The menu object this holds."""
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

    def redraw(self) -> None:
        """
        Redraw this menu item.
        :return: None
        """
        # Move the cursor to the top left corner:
        self._window.move(self.top_left[ROW], self.top_left[COL])
        # Write the leading indicator character:
        if self._is_selected:
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
                if self._is_selected and is_accel:
                    attrs = self._sel_accel_attrs
                elif self._is_selected and not is_accel:
                    attrs = self._sel_attrs
                elif not self._is_selected and is_accel:
                    attrs = self._unsel_accel_attrs
                else:  # Not self._is_selected and not is_accel:
                    attrs = self._unsel_attrs
                self._window.addstr(char, attrs)
        # Add the trailing selection indicator:
        if self._is_selected:
            self._window.addstr(self._sel_tail_indicator, self._sel_attrs)
        else:
            self._window.addstr(self._unsel_tail_indicator, self._unsel_attrs)
        return

    def activate(self, *args: list[Any]) -> Optional[Any]:
        """
        Activate this menu bar item.
        :param args: Any arguments to pass to the call back.
        :return: Optional[Any]: The return value of the callback
        """
        self.is_selected = False
        self._is_activated = True
        if self._callback is not None:
            try:
                return self._callback(*args)
            except TypeError as e:
                warn("Callback is not callable.", RuntimeWarning)
            except Exception as e:
                warn("Callback caused exception.", RuntimeWarning)
                raise e
        if self._menu is not None:
            self._menu.is_visible = True
        return None

    def deactivate(self) -> None:
        self.is_selected = False
        self._is_activated = False
        return

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
        old_value = self._is_selected
        self._is_selected = value
        if value != old_value:
            self.redraw()
        return