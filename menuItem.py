#!/usr/bin/env python3
from typing import Optional, Callable
import curses
from common import ROW, COL, STRINGS
from typeError import __type_error__

class MenuItem(object):
    """
    Store an handle a single menu item.
    """
#######################################
# Initialize:
#######################################
    def __init__(self,
                 window: curses.window,
                 width: int,
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
                 callback: Callable,
                 ) -> None:
        """
        Initialize a single menu item.
        :param window: curses.window: The window to draw on.
        :param width: int: The width of the menu item.
        :param top_left: tuple[int, int]: The top left corner of this item.
        :param label: str: The label to apply to this item.
        :param sel_attrs: int: The attributes to use when selected.
        :param sel_accel_attrs: int: The attributes to use for the accelerator when selected.
        :param sel_lead_indicator: str: The character to add before the label when selected.
        :param sel_tail_indicator: str: The character to add after the label when selected.
        :param unsel_attrs: int: The attributes to use when unselected.
        :param unsel_accel_attrs: int: The attributes to use for the accelerator when unselected.
        :param unsel_lead_indicator: str: The character to add before the label when unselected.
        :param unsel_tail_indicator: str: The character to add after the label when unselected.
        :param callback: Callable: The callback to call for this menu item.
        """
        # Internal properties:
        self._window: curses.window = window
        """The curses window to draw on."""
        self._sel_attrs: int = sel_attrs
        """Attributes to use when selected."""
        self._sel_accel_attrs: int = sel_accel_attrs
        """Attributes to use for the accelerator when selected."""
        self._sel_lead_indicator: str = sel_lead_indicator
        """Selection indicator character, added to the beginning of the label when selected."""
        self._sel_tail_indicator: str = sel_tail_indicator
        """Selection indicator character, added to the end of the label when selected."""
        self._unsel_attrs: int = unsel_attrs
        """Attributes to use when unselected."""
        self._unsel_accel_attrs: int = unsel_accel_attrs
        """Attributes to use for the accelerator when unselected."""
        self._unsel_lead_indicator: str = unsel_lead_indicator
        """Unselected lead indicator character, added to the beginning of the label when unselected."""
        self._unsel_tail_indicator: str = unsel_tail_indicator
        """Unselected tail indicator character, added to the end of the label when unselected."""
        self._callback: Optional[Callable] = callback
        """The call back to call when activated."""
        self._label: str = label
        """The label with accel indicators."""
        self._is_selected: bool = False
        """If this menu item is selected."""

        # External properties:
        self.top_left: tuple[int, int] = top_left
        """Top left corner of this menu item."""
        self.width: int = width
        """Width of this menu item."""
        return

#######################################
# Methods:
#######################################
    def redraw(self) -> None:
        """
        Redraw this menu item.
        :return: None
        """
        # draw background.
        bg_char = STRINGS['background']['menu']
        self._window.move(self.top_left[ROW], self.top_left[COL])
        bg_attrs: int
        if self.is_selected:
            bg_attrs = self._sel_attrs
        else:
            bg_attrs = self._unsel_attrs
        for col in range(self.top_left[COL], self.top_left[COL] + self.width):
            self._window.addstr(bg_char, bg_attrs)

        # Draw label, start by moving the cursor to start:
        self._window.move(self.top_left[ROW], self.top_left[COL])

        # Determine indicator attributes:
        indicator_attrs: int
        if self.is_selected:
            indicator_attrs = self._sel_attrs
        else:
            indicator_attrs = self._unsel_attrs

        # Put start selection indicator:
        indicator: str
        if self.is_selected:
            self._window.addstr(self._sel_lead_indicator, indicator_attrs)
        else:
            self._window.addstr(self._unsel_lead_indicator, indicator_attrs)

        # Put the label:
        is_accel: bool = False
        for char in self._label:
            if char == '_':  # Accel indicator.
                is_accel = not is_accel
            else:
                # Determine attributes:
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

        # Put the trailing selection indicator:
        if self.is_selected:
            self._window.addstr(self._sel_tail_indicator, indicator_attrs)
        else:
            self._window.addstr(self._unsel_tail_indicator, indicator_attrs)
        return

#######################################
# Properties:
#######################################
    @property
    def is_selected(self) -> bool:
        """
        Is this menu item selected?
        :return: bool: True, this menu item is selected, False, it is not.
        """
        return self._is_selected

    @is_selected.setter
    def is_selected(self, value: bool) -> None:
        """
        Is this menu item selected?
        Setter.
        :param value: bool: True if this item is selected, False if not.
        :return: None
        :raises TypeError: If value is not a bool.
        """
        if not isinstance(value, bool):
            __type_error__('value', 'bool', value)
        old_value = self._is_selected
        self._is_selected = value
        if old_value != value:
            self.redraw()
        return
