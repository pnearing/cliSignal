#!/usr/bin/env python3
"""
    File: window.py
    Basic curses window operations.
"""
from typing import Optional
import curses
from cursesFunctions import add_title_to_win, draw_border_on_win
from common import ROW, COL, HEIGHT, WIDTH
from typeError import __type_error__


class Window(object):
    """
    Base window class.
    """

#########################################
# Initialize:
#########################################
    def __init__(self,
                 window,
                 title: Optional[str],
                 top_left: tuple[int, int],
                 window_attrs: int,
                 border_attrs: int,
                 border_focus_attrs: int,
                 border_chars: dict[str, str],
                 title_attrs: int,
                 title_focus_attrs: int,
                 title_chars: dict[str, str],
                 bg_char: str,
                 is_static_size: bool = False,
                 ) -> None:
        """
        Initialize the window.
        :param window: curses.window | curses._CursesWindow: The curses window object.
        :param title: Optional[str]: The title of the window, if None, no title.
        :param top_left: tuple[int, int]: The top left row, col of this window.
        :param window_attrs: int: The colours and attributes for this centre of this window.
        :param border_attrs: int: The colours and attributes to use for the border of this window.
        :param border_focus_attrs: int: The colours and attributes to use for the border when focused.
        :param border_chars: dict[str, str]: The characters to use for the border of the window.
        :param title_attrs: int: The colours and attributes to use for the title of this window.
        :param title_focus_attrs: int: The colours and attributes to use for the title when focused.
        :param title_chars: dict[str, str]: The dict of title start and end chars.
        :param bg_char: str: The background character.
        """
        # Super init:
        object.__init__(self)

        # Set internal properties:
        self._window: curses.window = window
        """The curses window object to use."""
        self._window_attrs: int = window_attrs
        """The colour pair number and attributes for the centre of this window."""
        self._border_attrs: int = border_attrs
        """The colour pair number and attributes for the border of this window."""
        self._border_focus_attrs: int = border_focus_attrs
        """The colour pair number and attributes for the border when focused."""
        self._border_chars: dict[str, str] = border_chars
        """The characters to use for the border of the window."""
        self._title_attrs: int = title_attrs
        """The colour pair number and attributes for the title of this window."""
        self._title_focus_attrs: int = title_focus_attrs
        """The colour pair number and attributes for the title when focused."""
        self._is_focused: bool = False
        """If this window is focused, this is private because we use getter / setters for it."""
        self._title_chars: dict[str, str] = title_chars
        """The characters to use to start and end the title."""
        self._bg_char: str = bg_char
        """The character to use for drawing the center of the screen."""

        # Set external properties:
        self.title: str = title
        """The title of this window."""
        self.real_size: tuple[int, int] = window.getmaxyx()
        """The real size of the window, not taking the border into account. (rows, cols)."""
        self.size: tuple[int, int] = (self.real_size[HEIGHT] - 2, self.real_size[WIDTH] - 2)
        """The drawable size of the window, taking the border into account. (rows, cols)."""
        self.real_top_left: tuple[int, int] = top_left
        """The real top left of this window, not taking the border into account. (row, col)."""
        self.top_left: tuple[int, int] = (self.real_top_left[ROW] + 1, self.real_top_left[COL] + 1)
        """The drawable top left of this window, taking the border into account. (row, col)."""
        self.real_bottom_right: tuple[int, int] = (self.real_top_left[ROW] + self.real_size[HEIGHT],
                                                   self.real_top_left[COL] + self.real_size[WIDTH])
        """The real bottom right of the window, not taking the border into account. (row, col)."""
        self.bottom_right: tuple[int, int] = (self.top_left[ROW] + self.size[HEIGHT],
                                              self.top_left[COL] + self.size[WIDTH])
        """The drawable bottom right of the window, taking the border into account. (row, col)."""
        self.is_visible: bool = True
        """If this window should be drawn."""
        return

#########################################
# Internal Methods:
#########################################
    def __get_relative_mouse_pos__(self, mouse_pos: tuple[int, int]) -> tuple[int, int]:
        """
        Get the relative mouse position over the window; IE: If the mouse is at top_left, then mouse_pos = (0, 0)
        :param mouse_pos: tuple[int, int]: The mouse position: (ROW, COL).
        :return: tuple[int, int]: The relative position: (ROW, COL).
        """
        relative_row: int = mouse_pos[ROW] - self.real_top_left[ROW]
        relative_col: int = mouse_pos[COL] - self.real_top_left[COL]
        return relative_row, relative_col

#########################################
# External Methods:
#########################################
    def redraw(self) -> None:
        """
        Redraw the window, but only if _is_visible is True.
        :return: None
        """
        if not self.is_visible:
            return
        # Clear the window without calling refresh.
        self._window.erase()
        # Draw the border:
        border_attrs: int
        if self._is_focused:
            border_attrs = self._border_focus_attrs
        else:
            border_attrs = self._border_attrs
        draw_border_on_win(window=self._window, border_attrs=border_attrs,
                           ts=self._border_chars['ts'], bs=self._border_chars['bs'],
                           ls=self._border_chars['ls'], rs=self._border_chars['rs'],
                           tl=self._border_chars['tl'], tr=self._border_chars['tr'],
                           bl=self._border_chars['bl'], br=self._border_chars['br']
                           )
        # Add the title to the border:
        title_attrs: int
        if self._is_focused:
            title_attrs = self._title_focus_attrs
        else:
            title_attrs = self._title_attrs
        add_title_to_win(self._window, self.title, border_attrs, title_attrs,
                         self._title_chars['start'], self._title_chars['end'])
        # Fill the centre with background colour, and character:
        for row in range(1, self.size[HEIGHT] + 1):
            for col in range(1, self.size[WIDTH] + 1):
                self._window.addch(row, col, self._bg_char, self._window_attrs)
        self._window.noutrefresh()
        return

    def resize(self, size: tuple[int, int], top_left: tuple[int, int]) -> None:
        """
        Recalculate size variables when the window is resized.
        :param size: tuple[int, int]: The new size of the window: (ROWS, COLS).
            NOTE: If ROWS or COLS is set to -1, size will be ignored, and the resize, function will not be called.
        :param top_left: tuple[int, int]: The new top left corner of the window: (ROW, COL).
            NOTE: If ROW or COL is set to -1, top_left will be ignored, and the mvwin function will not be called.
        :return: None
        """
        # Resize and move the window if required:
        if size[HEIGHT] != -1 and size[WIDTH] != -1:
            self._window.resize(size[HEIGHT], size[WIDTH])

        real_top_left: tuple[int, int] = top_left
        if top_left[ROW] != -1 and top_left[COL] != -1:
            self._window.mvwin(top_left[ROW], top_left[COL])
        else:
            real_top_left = (0, 0)  # This is the main window, real top_left is 0,0.
        num_rows, num_cols = self._window.getmaxyx()
        self.real_top_left = real_top_left
        self.top_left = (self.real_top_left[ROW] + 1, self.real_top_left[COL] + 1)
        self.real_size = (num_rows, num_cols)
        self.size = (num_rows - 2, num_cols - 2)
        self.real_bottom_right = (self.real_top_left[ROW] + num_rows, self.real_top_left[COL] + num_cols)
        self.bottom_right = (self.real_bottom_right[ROW] - 1, self.real_bottom_right[COL] - 1)
        return

    def is_mouse_over(self, mouse_pos: tuple[int, int]) -> bool:
        """
        Return True if the mouse position is over this window.
        :param mouse_pos: tuple[int, int]: The mouse position.
        :return: bool: True if the mouse is over this window, False if not.
        """
        if self.top_left[ROW] <= mouse_pos[ROW] <= (self.top_left[ROW] + self.size[HEIGHT]):
            if self.top_left[COL] <= mouse_pos[COL] <= (self.top_left[COL] + self.size[WIDTH]):
                return True
        return False

    def process_key(self, char_code: int) -> bool:
        """
        Stub for process key.
        :param char_code: int: The character code of the key pressed.
        :return: bool: True key was processed, False, it was not.
        """
        return False

    def process_mouse(self, mouse_pos: tuple[int, int], button_state: int) -> bool:
        """
        Stub for process mouse.
        :param mouse_pos: tuple[int, int]: The mouse position: (ROW, COL).
        :param button_state: int: The current button state.
        :return: bool: True the event was processed, False it was not.
        """
        return False

#########################################
# Properties:
#########################################
    @property
    def is_focused(self) -> bool:
        """
        True if the mouse is over this window. IE: Focused.
        :return: bool: True if this window is focused, False if not.
        """
        return self._is_focused

    @is_focused.setter
    def is_focused(self, value) -> None:
        """
        is_focused setter.
        :param value: bool: True if this is focused, False if not.
        :return: None
        """
        if not isinstance(value, bool):
            __type_error__("value", "bool", value)
        old_value: bool = self._is_focused
        self._is_focused = value
        if value != old_value:
            self.redraw()
        return

    @property
    def is_static_size(self) -> bool:
        """
        Is this window of static size?
        :return: bool: True if static, False if dynamic.
        """
        return self._is_static_size
