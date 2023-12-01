#!/usr/bin/env python3
"""
File: bar.py
Base functions of the menu / status bar.
"""
import logging
from typing import Optional, Final
from enum import IntEnum
import curses
from themes import ThemeColours
from common import ROW, COL, WIDTH, HEIGHT, STRINGS, Focus, TOP, LEFT, BOTTOM, RIGHT
from typeError import __type_error__


class Bar(object):
    """
    Base class for the status and menu bars.
    """
    def __init__(self,
                 std_screen: curses.window,
                 top: int,
                 bg_attrs: int,
                 bg_char: str,
                 focus_id: Focus,
                 ) -> None:
        """
        Initialize the status bar.
        :param std_screen: curses.window: The window to draw on (Main window)
        :param top_left: tuple[int, int]: The top left corner of the status bar.
        :param bg_attrs: int: The attributes to use for empty spaces on the status bar.
        :param bg_char: str: The character to use for the background.
        """
        _, num_cols = std_screen.getmaxyx()
        width = num_cols - 2
        # Set internal vars:
        self._std_screen: curses.window = std_screen
        """The curses window object"""
        self._bg_attrs: int = bg_attrs
        """The attributes to use for the background of the bar."""
        self._bg_char: str = bg_char
        """The character to use for drawing the background. Usually space."""
        self._is_visible: bool = True
        """If this bar is visible."""
        self._window = curses.newwin(1, width, top, 1)
        """The window to draw on."""
        self._is_focused: bool = False
        """Is this bar focused?"""

        # Set external properties:
        self.focus_id: Final[Focus] = focus_id
        """The focus ID of this bar."""
        # self.real_top_left: tuple[int, int] = top_left
        self.real_top_left: tuple[int, int] = (top, 1)
        """The real top Left corner of the window on the std_screen."""
        self.top_left: tuple[int, int] = (0, 0)
        """The drawable top left corner of the window."""
        self.real_size: tuple[int, int] = (1, 10)
        """The real size of the window."""
        self.size: tuple[int, int] = self.real_size
        """The drawable size of the window."""
        self.real_bottom_right: tuple[int, int] = (self.real_top_left[ROW] + self.real_size[HEIGHT] - 1,
                                                   self.real_top_left[COL] + self.real_size[WIDTH] - 1)
        """The real bottom right of this window."""
        self.bottom_right: tuple[int, int] = (self.top_left[ROW] + self.size[HEIGHT] - 1,
                                              self.top_left[COL] + self.size[WIDTH] - 1)
        """The drawable bottom right of the window."""
        return

    def redraw(self) -> None:
        """
        Redraw the status bar.
        :return: None
        """
        logger: logging.Logger = logging.getLogger(__name__ + '.' + self.redraw.__name__)
        if not self.is_visible:
            return
        _, num_cols = self._window.getmaxyx()
        # logger.debug("num_rows: %i, num_cols %i" % (num_rows, num_cols))
        for col in range(0, num_cols - 1):
            # logger.debug("col = %i : max_col: %i" % (col, (self.width-1)))
            self._window.addstr(0, col, self._bg_char, self._bg_attrs)
        try:
            self._window.addstr(0, num_cols - 1, self._bg_char, self._bg_attrs)
        except curses.error:
            pass
        self._window.noutrefresh()
        return

    def resize(self, top_left: tuple[int, int]) -> None:
        """
        Resize the status bar.
        :param top_left: The new top_left corner.
        :return: None
        """
        _, width = self._std_screen.getmaxyx()
        width -= 2
        self._window.resize(1, width)
        self._window.mvwin(top_left[ROW], top_left[COL])
        num_rows, num_cols = self._window.getmaxyx()
        self.real_top_left: tuple[int, int] = top_left
        self.top_left: tuple[int, int] = (0, 0)
        self.real_size: tuple[int, int] = (1, width)
        self.size: tuple[int, int] = self.real_size
        self.real_bottom_right: tuple[int, int] = (self.real_top_left[ROW] + self.real_size[HEIGHT] - 1,
                                                   self.real_top_left[COL] + self.real_size[WIDTH] - 1)
        self.bottom_right: tuple[int, int] = (self.top_left[ROW] + self.size[HEIGHT] - 1,
                                              self.top_left[COL] + self.size[WIDTH] - 1)
        return

    def is_mouse_over(self, mouse_pos: tuple[int, int]) -> bool:
        """
        Is the mouse over this bar?
        :param mouse_pos: tuple[int, int]: The mouse position: (ROW, COL).
        :return: bool: True if the mouse is over this bar, False if not.
        """
        _, num_cols = self._window.getmaxyx()
        if mouse_pos[ROW] == self.real_top_left[ROW]:
            if self.real_top_left[COL] <= mouse_pos[COL] <= (self.real_top_left[COL] + num_cols - 1):
                return True
        return False

    def process_key(self, char_code: int) -> Optional[bool]:
        """
        Process a key press stub.
        :param char_code: int: The character code of the key pressed.
        :return: Optional[bool]: Return True, the character was processed and handling should stop, return False, the
            character was not handled, and processing should stop, return None the character wasn't handled, and
            processing should continue.
        """
        return None

    def process_mouse(self, mouse_pos: tuple[int, int], button_state: int) -> Optional[bool]:
        """
        Process the mouse stub.
        :param mouse_pos: tuple[int, int]: The current mouse position: (ROW, COL)
        :param button_state: int: The current button state.
        :return: Optional[bool]: Return True, and the mouse was handled, and processing should stop, return False, the
            mouse was not handled and processing should stop, return None, the mouse was not handled and processing
            should continue.
        """
        return None

###############################
# Properties:
###############################
    @property
    def is_visible(self) -> bool:
        """
        Is this bar visible?
        :return: bool: True, is visible, False is not visible.
        """
        return self._is_visible

    @is_visible.setter
    def is_visible(self, value: bool) -> None:
        """
        Is this bar visible?
        Setter.
        :param value: bool: True, this bar is visible, False, it is not.
        :return: None
        :raises TypeError: If value is not a bool.
        """
        if not isinstance(value, bool):
            __type_error__("value", "bool", value)
        old_value = self._is_visible
        self._is_visible = value
        if old_value != value and value:
            self.redraw()
        return

    @property
    def is_focused(self) -> bool:
        """
        Is this bar focused?
        :return: bool: Return True this bar is focused, False it is not.
        """
        self.__is_focused_hook__(True, self._is_focused)
        return self._is_focused

    @is_focused.setter
    def is_focused(self, value: bool) -> None:
        """
        Is this bar focused?
        :param value: bool: If True, this bar is focused, False it is not.
        :return: None.
        """
        if not isinstance(value, bool):
            __type_error__('value', 'bool', value)
        old_value: bool = self._is_focused
        self._is_focused = value
        if value != old_value:
            self.redraw()
            self.__is_focused_hook__(False, value)
        return

    @property
    def top(self) -> int:
        """
        Return the top most row of the drawable space.
        :return: int: The top row.
        """
        return self.top_left[TOP]

    @property
    def left(self) -> int:
        """
        Return the left most column of the drawable area.
        :return: int: The left most column.
        """
        return self.top_left[LEFT]

    @property
    def bottom(self) -> int:
        """
        Return the bottom most row of the drawable area.
        :return: int: The bottom row.
        """
        return self.bottom_right[BOTTOM]

    @property
    def right(self) -> int:
        """
        Return the right most column of the drawable area.
        :return: int: The right column.
        """
        return self.bottom_right[RIGHT]

    @property
    def height(self) -> int:
        """
        The height of the bar.
        :return: int: The height.
        """
        return self.size[HEIGHT]

    @property
    def width(self) -> int:
        """
        The width of the bar.
        :return: int: The width.
        """
        return self.size[WIDTH]

    ##################################
    # property hooks:
    ##################################
    def __is_focused_hook__(self, is_get: bool, value: bool) -> None:
        """
        setter
        :param is_get: bool: Is this the getter?
        :param value: bool: The value being set.
        :return: None.
        """
        return None
