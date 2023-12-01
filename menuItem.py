#!/usr/bin/env python3
import logging
from typing import Optional, Callable, Any
from warnings import warn
import curses
from common import ROW, COL, STRINGS, CBStates, CBIndex, WIDTH, HEIGHT
from cursesFunctions import calc_attributes, add_accel_text, get_left_click, get_left_double_click
from runCallback import __run_callback__, __type_check_callback__
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
                 window,  # Type: curses._CursesWindow
                 width: int,
                 top_left: tuple[int, int],
                 label: str,
                 theme: dict[str, dict[str, int | bool | str]],
                 callback: tuple[Optional[Callable], Optional[list[Any]]],
                 char_codes: list[int],
                 ) -> None:
        """
        Initialize a single menu item.
        :param std_screen: curses.window: The std_screen object.
        :param window: curses._CursesWindow: The window to draw on.
        :param width: int: The width of the menu item.
        :param top_left: tuple[int, int]: The top left corner of this item.
        :param label: str: The label to apply to this item.
        :param callback: Callable: The callback to call for this menu item.
        :param char_codes: list[int]: The character codes of the accelerator for this menu item.
        """

        # Internal properties:
        self._std_screen: curses.window = std_screen
        """The std_screen curses.window object."""
        self._window: curses.window = window  # Real Type curses._CursesWindow
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
        self.size: tuple[int, int] = (1, width)
        """The size of this menu item."""
        self.bottom_right: tuple[int, int] = (self.top_left[ROW] + self.size[HEIGHT] - 1,
                                              self.top_left[COL] + self.width - 1)
        """The bottom right of this menu item."""
        self.label: str = label
        """The label with accel indicators."""
        self.char_codes: list[int] = char_codes
        """The character codes this menu item should react to."""
        return

#######################################
# Methods:
#######################################
    def redraw(self) -> None:
        """
        Redraw this menu item.
        :return: None
        """
        logger: logging.Logger = logging.getLogger(__name__ + '.' + self.redraw.__name__)
        # Determine attrs and indicators:
        text_attrs: int
        accel_attrs: int
        lead_indicator: str
        tail_indicator: str
        if self.is_selected:
            text_attrs = self._sel_attrs
            accel_attrs = self._sel_accel_attrs
            lead_indicator = self._sel_lead_indicator
            tail_indicator = self._sel_tail_indicator
        else:
            text_attrs = self._unsel_attrs
            accel_attrs = self._unsel_accel_attrs
            lead_indicator = self._unsel_lead_indicator
            tail_indicator = self._unsel_tail_indicator

        # Move to start:
        self._window.move(self.top_left[ROW], self.top_left[COL])
        # Draw the background:
        num_row, num_col = self._window.getmaxyx()
        for col in range(self.top_left[COL], self.bottom_right[COL] + 1):
            self._window.addstr(self._bg_char, text_attrs)
        # Move back to the start:
        self._window.move(self.top_left[ROW], self.top_left[COL])
        # Put start selection indicator:
        self._window.addstr(lead_indicator, text_attrs)
        # Put the label:
        add_accel_text(self._window, self.label, text_attrs, accel_attrs)
        # Put the trailing selection indicator:
        self._window.addstr(tail_indicator, text_attrs)
        # Update the window:
        self._window.noutrefresh()
        return

    def activate(self) -> None:
        """
        Activate this menu item.
        :return: None
        """
        __run_callback__(self._callback, CBStates.ACTIVATED.value, self.std_screen)
        return

    def is_mouse_over(self, rel_mouse_pos: tuple[int, int]) -> bool:
        """
        Is the mouse over this menu item?
        :param rel_mouse_pos: tuple[int, int]: The relative mouse position: (ROW, COL)
        :return: bool: True if the mouse is over this menu item, False it is not.
        """
        if rel_mouse_pos[ROW] == self.top_left[ROW]:
            if self.top_left[COL] <= rel_mouse_pos[COL] <= self.bottom_right[COL]:
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

    @property
    def width(self) -> int:
        """
        The width of the menu item
        :return: int: The width.
        """
        return self.size[WIDTH]

    @property
    def height(self) -> int:
        """
        THe height of the menu item.
        :return: int: The height.
        """
        return self.size[HEIGHT]

    @property
    def std_screen(self) -> curses.window:
        """
        Get the std_screen curses.window object.
        :return: curses.window: The std_screen.
        """
        return self._std_screen