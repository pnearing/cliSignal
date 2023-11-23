#!/usr/bin/env python3
from typing import Optional, Callable, Any
from warnings import warn
import curses
from common import ROW, COL, STRINGS, CBStates, CBIndex
from cursesFunctions import calc_attributes, add_accel_text
from themes import ThemeColours
from typeError import __type_error__


class MenuItem(object):
    """
    Store an handle a single menu item.
    """
#######################################
# Initialize:
#######################################
    def __init__(self,
                 std_screen: curses.window,
                 width: int,
                 top_left: tuple[int, int],
                 label: str,
                 theme: dict[str, dict[str, int | bool | str]],
                 callback: tuple[Optional[Callable], Optional[list[Any]]],
                 char_codes: list[int],
                 ) -> None:
        """
        Initialize a single menu item.
        :param std_screen: curses.window: The window to draw on.
        :param width: int: The width of the menu item.
        :param top_left: tuple[int, int]: The top left corner of this item.
        :param label: str: The label to apply to this item.
        :param callback: Callable: The callback to call for this menu item.
        :param char_codes: list[int]: The character codes of the accelerator for this menu item.
        """

        # Internal properties:
        self._std_screen: curses.window = std_screen
        """The curses window to draw on."""
        self._bg_char: str = theme['backgroundChars']['menuItem']
        """The character to use for drawing the background."""
        self._sel_attrs: int = calc_attributes(ThemeColours.MENU_SEL, theme['menuSel'])
        """Attributes to use when selected."""
        self._sel_accel_attrs: int = calc_attributes(ThemeColours.MENU_SEL_ACCEL, theme['menuSelAccel'])
        """Attributes to use for the accelerator when selected."""
        self._sel_lead_indicator: str = theme['menuSelChars']['leadSel']
        """Selection indicator character, added to the beginning of the label when selected."""
        self._sel_tail_indicator: str = theme['menuSelChars']['tailSel']
        """Selection indicator character, added to the end of the label when selected."""
        self._unsel_attrs: int = calc_attributes(ThemeColours.MENU_UNSEL, theme['menuUnsel'])
        """Attributes to use when unselected."""
        self._unsel_accel_attrs: int = calc_attributes(ThemeColours.MENU_UNSEL_ACCEL, theme['menuUnselAccel'])
        """Attributes to use for the accelerator when unselected."""
        self._unsel_lead_indicator: str = theme['menuSelChars']['leadUnsel']
        """Unselected lead indicator character, added to the beginning of the label when unselected."""
        self._unsel_tail_indicator: str = theme['menuSelChars']['tailUnsel']
        """Unselected tail indicator character, added to the end of the label when unselected."""
        self._callback: tuple[Optional[Callable], Optional[list[Any]]] = callback
        """The call back to call when activated."""
        self._is_selected: bool = False
        """If this menu item is selected."""

        # External properties:
        self.top_left: tuple[int, int] = top_left
        """Top left corner of this menu item."""
        self.width: int = width
        """Width of this menu item."""
        self.size: tuple[int, int] = (1, self.width)
        """The size of this menu item."""
        self.bottom_right: tuple[int, int] = (top_left[ROW], top_left[COL] + self.width)
        """The bottom right of this menu item."""
        self.label: str = label
        """The label with accel indicators."""
        self.char_codes: list[int] = char_codes
        """The character codes this menu item should react to."""
        return

#######################################
# Internal methods:
#######################################
    def _run_callback(self, state: str) -> None:
        """
        Run the callback.
        :param state: str: The status string.
        :return: None
        """
        if self._callback is not None:
            try:
                if self._callback[CBIndex.PARAMS] is not None:
                    self._callback[CBIndex.CALLABLE](state, self._std_screen, *self._callback[CBIndex.PARAMS])
                else:
                    self._callback[CBIndex.CALLABLE](state, self._std_screen)
            except KeyboardInterrupt as e:
                raise e
            except Exception as e:
                warning_message: str = "Callback caused Exception: %s(%s)." % (str(type(e)), str(e.args))
                warn(warning_message, RuntimeWarning)
                raise e
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
        self._std_screen.move(self.top_left[ROW], self.top_left[COL])
        bg_attrs: int
        if self.is_selected:
            bg_attrs = self._sel_attrs
        else:
            bg_attrs = self._unsel_attrs
        for col in range(self.top_left[COL], self.top_left[COL] + self.width):
            self._std_screen.addstr(self._bg_char, bg_attrs)

        # Draw label, start by moving the cursor to start:
        self._std_screen.move(self.top_left[ROW], self.top_left[COL])

        # Put start selection indicator:
        indicator: str
        if self.is_selected:
            self._std_screen.addstr(self._sel_lead_indicator, self._sel_attrs)
        else:
            self._std_screen.addstr(self._unsel_lead_indicator, self._unsel_attrs)

        # Put the label:
        if self.is_selected:
            add_accel_text(self._std_screen, self.label, self._sel_attrs, self._sel_accel_attrs)
        else:
            add_accel_text(self._std_screen, self.label, self._unsel_attrs, self._unsel_accel_attrs)

        # Put the trailing selection indicator:
        if self.is_selected:
            self._std_screen.addstr(self._sel_tail_indicator, self._sel_attrs)
        else:
            self._std_screen.addstr(self._unsel_tail_indicator, self._unsel_attrs)
        return

    def activate(self) -> None:
        """
        Activate this menu item.
        :return: None
        """
        self._run_callback(CBStates.ACTIVATED.value)
        return

    def is_mouse_over(self, mouse_pos: tuple[int, int]) -> bool:
        """
        Is the mouse over this menu item?
        :param mouse_pos: tuple[int, int]: The current mouse position: (ROW, COL)
        :return: bool: True if the mouse is over this menu item, False it is not.
        """
        if mouse_pos[ROW] == self.top_left[ROW]:
            if self.top_left[COL] <= mouse_pos[COL] <= self.bottom_right[COL]:
                return True
        return False

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
