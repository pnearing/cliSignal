#!/usr/bin/env python3
"""
File: scrollBar.py
    Store and handle a curses scroll bar.
"""

import curses
from typing import Final, Optional

from common import TOP, LEFT, BOTTOM, RIGHT, HEIGHT, WIDTH
from cursesFunctions import calc_attributes
from themes import ThemeColours
from typeError import __type_error__

MIN_HEIGHT: Final[int] = 5
MIN_WIDTH: Final[int] = 5


class ScrollBar(object):
    """
    The base scroll bar base class. Do not use directly.
    """
    def __init__(self,
                 size: tuple[int, int],
                 top_left: tuple[int, int],
                 theme: dict[str, dict[str, int | bool | str]],
                 ) -> None:
        """
        Initialize the scroll bar.
        :param size: tuple[int, int]: The size of the scroll bar: (HEIGHT, WIDTH).
        :param top_left: tuple[int, int]: The top left of the scroll bar: (ROW, COL).
        :param theme: dict[str, dict[str, int | bool | str]]: The current theme.
        """
        super().__init__()
        # Set window properties and create the curses window:
        self._top_left = top_left
        """The top left corner of the scroll bar."""
        self._size = size
        """The size of the scroll bar."""
        self._window = curses.newwin(size[HEIGHT], size[WIDTH], top_left[TOP], top_left[LEFT])
        """The curses.window object for this scroll bar."""

        # Set the different attributes:
        self._enabled_bg_attrs: Final[int] = calc_attributes(ThemeColours.SCROLL_ENA_BG, theme['scrollBarEnaBg'])
        """The background attributes when enabled."""
        self._disabled_bg_attrs: Final[int] = calc_attributes(ThemeColours.SCROLL_DIS_BG, theme['scrollBarDisBg'])
        """The background attributes when disabled."""
        self._enabled_button_attrs: Final[int] = calc_attributes(ThemeColours.SCROLL_ENA_BTN, theme['scrollBarEnaBtn'])
        """The button attributes when enabled."""
        self._disabled_button_attrs: Final[int] = calc_attributes(ThemeColours.SCROLL_DIS_BTN, theme['scrollBarDisBtn'])
        """The button attributes when disabled."""
        self._enabled_handle_attrs: Final[int] = calc_attributes(ThemeColours.SCROLL_ENA_HAND,
                                                                 theme['scrollBarEnaHand'])
        """The handle attributes when enabled."""
        self._disabled_handle_attrs: Final[int] = calc_attributes(ThemeColours.SCROLL_DIS_HAND,
                                                                  theme['scrollBarDisHand'])
        """The handle attributes when disabled."""

        # Store the different chars from the theme:
        self.bg_char: Final[str] = theme['scrollBarChars']['bg']
        """The background character."""
        self._up_button_char: Final[str] = theme['scrollBarChars']['up']
        """The up button character."""
        self._pg_up_button_char: Final[str] = theme['scrollBarChars']['pgUp']
        """The page up button character."""
        self._down_button_char: Final[str] = theme['scrollBarChars']['down']
        """The down button character."""
        self._pg_down_button_char: Final[str] = theme['scrollBarChars']['pgDown']
        """The page down button character."""
        self._left_button_char: Final[str] = theme['scrollBarChars']['left']
        """The left button character."""
        self._pg_left_button_char: Final[str] = theme['scrollBarChars']['pgLeft']
        """The page left button characters."""
        self._right_button_char: Final[str] = theme['scrollBarChars']['right']
        """The right button characters."""
        self._pg_right_button_char: Final[str] = theme['scrollBarChars']['pgRight']
        """The page right button characters."""
        self._vertical_handle_char: Final[str] = theme['scrollBarChars']['vHandle']
        """The vertical handle character."""
        self._horizontal_handle_char: Final[str] = theme['scrollBarChars']['hHandle']
        """The horizontal handled character."""

        # Store the different states:
        self._is_visible: bool = False
        """Is this scroll bar visible?"""
        self._is_enabled: bool = False
        """Is this scroll bar enabled?"""
        self._position: Optional[float] = None
        """The position of the handle along the scroll bar, expressed as a value between 0.0 and 1.0, or None."""
        return

    ##############################################
    # External methods to override:
    ##############################################
    def resize(self, size: tuple[int, int], top_left: tuple[int, int]) -> None:
        self._window.resize(size[HEIGHT], size[WIDTH])
        self._window.mvwin(top_left[TOP], top_left[LEFT])
        self._top_left = top_left
        self._size = size
        return

    def redraw(self) -> None:
        """
        Redraw the scroll bar:
        :return: None
        """
        if not self._is_visible:
            return
        # Draw the background of the scroll bar:
        if self.is_vertical:
            for row in range(0, self._size[HEIGHT] - 1):
                self._window.addstr(row, 0, self.bg_char, self.bg_attrs)
        else:
            for col in range(0, self._size[WIDTH] - 1):
                self._window.addstr(0, col, self.bg_char, self.bg_attrs)
        try:
            self._window.addstr(self._size[HEIGHT], self._size[WIDTH], self.bg_char, self.bg_attrs)
        except curses.error:
            pass
        self._window.noutrefresh()
        return

    ##############################################
    # Properties:
    ##############################################
    @property
    def position(self) -> Optional[float]:
        """
        The position of the handle along the scroll bar, expressed as a float between 0.0 and 1.0, where 0.0 is all the
        way up, and 1.0 is all the way down; Or None, where the handled isn't displayed.
        :return: Optional[float]: The handle position, or None.
        """
        return_value: Optional[float] = self.__position_hook__(True, self._position)
        if isinstance(return_value, float):
            return return_value
        return self._position

    @position.setter
    def position(self, value: Optional[float]) -> None:
        """
        The position of the handle along the scroll bar, expressed as a float between 0.0 and 1.0, where 0.0 is all the
        way up, and 1.0 is all the way down; Or None, where the handled isn't displayed.
        :param value: Optional[float]: The value to set the position to.
        :return: None.
        """
        if value is not None and not isinstance(value, float):
            __type_error__("value", "float", value)
        if value < 0.0 or value > 1.0:
            raise ValueError("Position out of range: 0.0 -> 1.0")
        self._position = value
        self.__position_hook__(False, value)
        return

    @property
    def is_enabled(self) -> bool:
        """
        Is this scroll bar enabled?
        :return: bool: True the scroll bar is enabled, False it is disabled.
        """
        return_value: Optional[bool] = self.__is_enabled_hook__(True, self._is_enabled)
        if return_value is not None:
            return return_value
        return self._is_enabled

    @is_enabled.setter
    def is_enabled(self, value: bool) -> None:
        """
        Is this scroll bar enabled?
        Setter.
        :param value: bool: True the scroll bar is enabled, False, it is disabled.
        :return: None.
        """
        if not isinstance(value, bool):
            __type_error__('value', 'bool', value)
        self._is_enabled = value
        self.__is_enabled_hook__(False, value)
        return

    @property
    def is_visible(self) -> bool:
        """
        Is this scroll bar visible?
        :return: bool: True the scroll bar is visible, False it is not.
        """
        return_value: Optional[bool] = self.__is_visible_hook__(True, self._is_visible)
        if isinstance(return_value, bool):
            return return_value
        return self._is_visible

    @is_visible.setter
    def is_visible(self, value):
        """
        Is this scroll bar visible?
        Setter.
        :param value: bool: True the scroll bar is visible, False it is not.
        :return: None.
        """
        if not isinstance(value, bool):
            __type_error__('value', 'bool', value)
        self._is_visible = value
        self.__is_visible_hook__(False, value)
        return

    @property
    def is_vertical(self) -> bool:
        """
        Is this a vertical scroll bar?
        :return: bool: True if this is a vertical scroll bar.
        """
        return self._size[WIDTH] == 1

    @property
    def is_horizontal(self) -> bool:
        """
        Is this a horizontal scroll bar?
        :return: bool: True if this is a horizontal scroll bar.
        """
        return self._size[HEIGHT] == 1

    @property
    def bg_attrs(self) -> int:
        """
        The current background attributes.
        :return: int: The background attributes.
        """
        if self._is_enabled:
            return self._enabled_bg_attrs
        return self._disabled_bg_attrs

    @property
    def button_attrs(self) -> int:
        """
        The current button attributes.
        :return: int: The button attributes.
        """
        if self._is_enabled:
            return self._enabled_button_attrs
        return self._disabled_button_attrs

    @property
    def handle_attrs(self) -> int:
        """
        The current handle attributes.
        :return: int: The handle attributes.
        """
        if self._is_enabled:
            return self._enabled_handle_attrs
        return self._disabled_handle_attrs

    @property
    def top_left(self) -> tuple[int, int]:
        """
        The top left corner of the scroll bar.
        :return: tuple[int, int]: The top left corner: (ROW, COL).
        """
        return self._top_left

    @property
    def size(self) -> tuple[int, int]:
        """
        The size of the scroll bar.
        :return: tuple[int, int]: The size: (ROW, COL).
        """
        return self._size

    @property
    def bottom_right(self) -> tuple[int, int]:
        """
        The bottom right corner of the scroll bar.
        :return: tuple[int, int]: The bottom right: (ROW, COL).
        """
        return self._top_left[TOP] + self._size[HEIGHT] - 1, self._top_left[LEFT] + self._size[WIDTH] - 1

    @property
    def top(self) -> int:
        """
        The top most row of the scroll bar.
        :return: int: The top most row.
        """
        return self._top_left[TOP]

    @property
    def left(self) -> int:
        """
        The left most column of the scroll bar.
        :return: int: The left most column.
        """
        return self._top_left[LEFT]

    @property
    def bottom(self) -> int:
        """
        The bottom most row of the scroll bar.
        :return: int: The bottom most row.
        """
        return self._top_left[TOP] + self._size[HEIGHT] - 1

    @property
    def right(self) -> int:
        """
        The right most column of the scroll bar.
        :return: int: The right most column.
        """
        return self._top_left[LEFT] + self._size[WIDTH] - 1

    @property
    def height(self) -> int:
        """
        The height of the scroll bar.
        :return: int: The height.
        """
        return self._size[HEIGHT]

    @property
    def width(self) -> int:
        """
        The width of the scroll bar.
        :return: int: The width.
        """
        return self._size[WIDTH]

##################################################
# Property hooks:
##################################################
    def __is_enabled_hook__(self, is_get: bool, value: bool) -> Optional[bool]:
        """
        Hook stub for is_enabled Getter / Setter.
        :param is_get: bool: True: The Getter is being called; False: The Setter is being called.
        :param value: If 'is_get' is True, this is the current value of _enabled, if 'is_get' is False, this is the
            new value.
        :return: If 'is_get' is False, the return value is ignored; If 'is_get' is True, a return value of None will
            cause the Getter to return the current value of enabled, otherwise, the Getter will return the return value.
        """
        return None

    def __position_hook__(self, is_get, value: Optional[float]) -> Optional[float]:
        """
        Hook stub for position Getter / Setter.
        :param is_get: bool: True, and the Getter is being run, False, and the Setter is being run.
        :param value: Optional[float]: If 'is_get' is True, then this is the current value of _position, if 'is_get' is
            False, then this is the value that was set.
        :return: If 'is_get' is False, this value is ignored; If 'is_get' is True, then a return value of None will
            cause the Getter to return the current value of _position, otherwise if this is a float, then the Getter
            will return this value.
        """
        return None

    def __is_visible_hook__(self, is_get, value: bool) -> Optional[bool]:
        return None
