#!/usr/bin/env python3
"""
    File: window.py
    Basic curses window operations.
"""
import logging
from typing import Optional
import curses
from cursesFunctions import add_title_to_win, draw_border_on_win
from common import ROW, COL, HEIGHT, WIDTH, TOP, LEFT, BOTTOM, RIGHT, Focus
from typeError import __type_error__


class Window(object):
    """
    Base window class.
    """

#########################################
# Initialize:
#########################################
    def __init__(self,
                 std_screen: curses.window,
                 window,  # Type: curses._CursesWindow
                 title: Optional[str],
                 top_left: tuple[int, int],
                 window_attrs: int,
                 border_attrs: Optional[int],
                 border_focus_attrs: Optional[int],
                 border_chars: Optional[dict[str, str]],
                 title_attrs: Optional[int],
                 title_focus_attrs: Optional[int],
                 title_chars: Optional[dict[str, str]],
                 bg_char: str,
                 focus_id: Focus,
                 ) -> None:
        """
        Initialize the window.
        :param std_screen: curses.window: The std_screen window object.
        :param window: curses.window | curses._CursesWindow: The curses window object.
        :param title: Optional[str]: The title of the window, if None, no title.
        :param top_left: tuple[int, int]: The top left row, col of this window.
        :param window_attrs: int: The colours and attributes for this centre of this window.
        :param border_attrs: Optional[int]: The colours and attributes to use for the border of this window.
        :param border_focus_attrs: Optional[int]: The colours and attributes to use for the border when focused.
        :param border_chars: Optional[dict[str, str]]: The characters to use for the border of the window.
        :param title_attrs: Optional[int]: The colours and attributes to use for the title of this window.
        :param title_focus_attrs: Optional[int]: The colours and attributes to use for the title when focused.
        :param title_chars: Optional[dict[str, str]]: The dict of title start and end chars.
        :param bg_char: str: The background character.
        :param focus_id: Focus: The focus id of this window.
        """
        # Super init:
        object.__init__(self)

        # Set internal properties:
        self._std_screen: curses.window = std_screen
        """The std_screen window object."""
        self._window: curses.window = window
        """The curses window object to draw on."""
        self._window_attrs: int = window_attrs
        """The colour pair number and attributes for the centre of this window."""
        self._border_attrs: Optional[int] = border_attrs
        """The colour pair number and attributes for the border of this window."""
        self._border_focus_attrs: Optional[int] = border_focus_attrs
        """The colour pair number and attributes for the border when focused."""
        self._border_chars: Optional[dict[str, str]] = border_chars
        """The characters to use for the border of the window."""
        self._title_attrs: Optional[int] = title_attrs
        """The colour pair number and attributes for the title of this window."""
        self._title_focus_attrs: Optional[int] = title_focus_attrs
        """The colour pair number and attributes for the title when focused."""
        self._title_chars: Optional[dict[str, str]] = title_chars
        """The characters to use to start and end the title."""
        self._bg_char: str = bg_char
        """The character to use for drawing the center of the screen."""
        self._is_static_size: bool = True
        """Is this window of static size?"""
        self._is_focused: bool = False
        """If this window is focused, this is private because we use getter / setters for it."""
        self._is_visible: bool = False
        """Should this window be drawn?"""
        self._always_visible: bool = False
        """Is this window always visible?"""

        # Set external properties:
        self.title: str = title
        """The title of this window."""
        self.focus_id: Focus = focus_id
        """The focus ID of this window."""
        self.real_size: tuple[int, int] = window.getmaxyx()
        """The real size of the window, not taking the border into account. (rows, cols)."""
        self.size: tuple[int, int] = (self.real_size[HEIGHT] - 2, self.real_size[WIDTH] - 2)
        """The drawable size of the window, taking the border into account. (rows, cols)."""
        self.real_top_left: tuple[int, int] = top_left
        """The real top left of this window, not taking the border into account. (row, col)."""
        # self.top_left: tuple[int, int] = (self.real_top_left[ROW] + 1, self.real_top_left[COL] + 1)
        self.top_left: tuple[int, int] = (1, 1)
        """The drawable top left of this window, taking the border into account. (row, col)."""
        self.real_bottom_right: tuple[int, int] = (self.real_top_left[ROW] + self.real_size[HEIGHT] - 1,
                                                   self.real_top_left[COL] + self.real_size[WIDTH] - 1)
        """The real bottom right of the window, not taking the border into account. (row, col)."""
        self.bottom_right: tuple[int, int] = (self.top_left[ROW] + self.size[HEIGHT] - 1,
                                              self.top_left[COL] + self.size[WIDTH] - 1)
        """The drawable bottom right of the window, taking the border into account. (row, col)."""
        return

#########################################
# External Methods that don't get overridden:
#########################################

    def is_mouse_over(self, mouse_pos: tuple[int, int]) -> bool:
        """
        Return True if the mouse position is over this window.
        :param mouse_pos: tuple[int, int]: The mouse position.
        :return: bool: True if the mouse is over this window, False if not.
        """
        if self.real_top_left[ROW] <= mouse_pos[ROW] <= self.real_bottom_right[ROW]:
            if self.real_top_left[COL] <= mouse_pos[COL] <= self.real_bottom_right[COL]:
                return True
        return False

    def show(self) -> None:
        """
        Make this window visible.
        :return: None
        """
        self.is_visible = True
        return

    def hide(self) -> None:
        """
        Make this window invisible.
        :return: None
        """
        self.is_visible = False
        return

#########################################
# External Methods that get overridden:
#########################################
    def redraw(self) -> None:
        """
        Redraw the window, but only if _is_visible is True.
        :return: None
        """
        if not self.is_visible and not self._always_visible:
            return
        # Clear the window without calling refresh.
        # self._window.erase()

        # Determine attributes:
        border_attrs: int
        title_attrs: int
        if self.is_focused:
            border_attrs = self._border_focus_attrs
            title_attrs = self._title_focus_attrs
        else:
            border_attrs = self._border_attrs
            title_attrs = self._title_attrs

        # Draw the border:
        draw_border_on_win(window=self._window, border_attrs=border_attrs,
                           ts=self._border_chars['ts'], bs=self._border_chars['bs'],
                           ls=self._border_chars['ls'], rs=self._border_chars['rs'],
                           tl=self._border_chars['tl'], tr=self._border_chars['tr'],
                           bl=self._border_chars['bl'], br=self._border_chars['br']
                           )

        # Add the title to the border:
        add_title_to_win(self._window, self.title, border_attrs, title_attrs,
                         self._title_chars['start'], self._title_chars['end'])

        # Fill the centre with background colour, and character:
        for row in range(1, self.size[HEIGHT] + 1):
            for col in range(1, self.size[WIDTH] + 1):
                self._window.addch(row, col, self._bg_char, self._window_attrs)

        # Refresh the window:
        self._window.noutrefresh()
        return

    def resize(self,
               size: tuple[int, int],
               real_top_left: tuple[int, int],
               do_resize: bool = True,
               do_move: bool = True,
               ) -> None:
        """
        Recalculate size variables when the window is resized.
        :param size: tuple[int, int]: The new size of the window: (ROWS, COLS).
        :param real_top_left: tuple[int, int]: The new top left corner of the window: (ROW, COL).
        :param do_resize: bool: Should we run the window resize method?
        :param do_move: bool: Should we run the window move method?
        :return: None
        """
        screen_size = self._std_screen.getmaxyx()
        logger: logging.Logger = logging.getLogger(__name__ + '.' + self.resize.__name__)
        logger.debug("New size: %s" % (str(size)))
        logger.debug("Screen size: %s" % str(screen_size))
        logger.debug("New top_left: %s" % str(real_top_left))
        # Resize and move the window if required:
        if do_resize:
            self._window.resize(size[HEIGHT], size[WIDTH])
        if do_move:
            self._window.mvwin(real_top_left[ROW], real_top_left[COL])

        num_rows, num_cols = self._window.getmaxyx()
        self.real_top_left = real_top_left
        self.top_left = (1, 1)
        self.real_size = (num_rows, num_cols)
        self.size = (num_rows - 2, num_cols - 2)
        self.real_bottom_right = (self.real_top_left[ROW] + self.real_size[ROW] - 1,
                                  self.real_top_left[COL] + self.real_size[COL] - 1)
        self.bottom_right = (self.top_left[ROW] + self.size[HEIGHT] - 1,
                             self.top_left[COL] + self.size[WIDTH] - 1)
        return

    def process_key(self, char_code: int) -> Optional[bool]:
        """
        Stub for process key.
        :param char_code: int: The character code of the key pressed.
        :return: bool: True key was processed, False, it was not.
        """
        return None

    def process_mouse(self, mouse_pos: tuple[int, int], button_state: int) -> Optional[bool]:
        """
        Stub for process mouse.
        :param mouse_pos: tuple[int, int]: The mouse position: (ROW, COL).
        :param button_state: int: The current button state.
        :return: bool: True the event was processed, False it was not.
        """
        return None

#########################################
# Properties:
#########################################
    @property
    def std_screen(self) -> curses.window:
        """
        The curses std_screen curses.window object.
        :return: curses.window: The std_screen object.
        """
        return self._std_screen

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
        # if value != old_value and value:
        #     self.is_visible = True
        return

    @property
    def is_static_size(self) -> bool:
        """
        Is this window of static size?
        :return: bool: True if static, False if dynamic.
        """
        return self._is_static_size

    @is_static_size.setter
    def is_static_size(self, value: bool) -> None:
        """
        Is this window of static size?
        Setter.
        :param value: bool: The value to set to.
        :return: None.
        """
        if not isinstance(value, bool):
            __type_error__("value", "bool", value)
        self._is_static_size = value
        return

    @property
    def is_visible(self) -> bool:
        """
        Is this window visible?
        :return: bool: True if visible, False if not.
        """
        return self._is_visible

    @is_visible.setter
    def is_visible(self, value: bool) -> None:
        """
        Is this window visible?
        Setter.
        :param value: bool: True this window is visible, False this window is not visible.
        :return: None.
        :raises TypeError: If value is not a bool.
        """
        if not isinstance(value, bool):
            __type_error__('value', 'bool', value)
        old_value: bool = self._is_visible
        self._is_visible = value
        if old_value != value and value:
            self.redraw()
        return

    @property
    def always_visible(self) -> bool:
        """
        Is this window always visible?
        :return: bool: True: The window is always drawn; False: it is not.
        """
        return self._always_visible

    @always_visible.setter
    def always_visible(self, value: bool) -> None:
        """
        Is this window always visible?
        Setter.
        :param value: bool: The value to set to.
        :return: None.
        """
        if not isinstance(value, bool):
            __type_error__("value", "bool", value)
        self._always_visible = value
        return

    @property
    def is_main_window(self) -> bool:
        """
        Is this the main window?
        :return: True this window is the main window, False it is not.
        """
        return self._std_screen == self._window

    @property
    def real_width(self) -> int:
        """
        The real width of the window.
        :return: int: The width.
        """
        return self.real_size[WIDTH]

    @property
    def real_height(self) -> int:
        """
        The real height of the window.
        :return: int: The real height.
        """
        return self.real_size[HEIGHT]

    @property
    def width(self) -> int:
        """
        The drawable width of the window.
        :return: int: The drawable width.
        """
        return self.size[WIDTH]

    @property
    def height(self) -> int:
        """
        The drawable height of the window.
        :return: int: The drawable height.
        """
        return self.size[HEIGHT]

    @property
    def top(self) -> int:
        """
        The top most drawable row of the window.
        :return: int: The top row.
        """
        return self.top_left[TOP]

    @property
    def left(self) -> int:
        """
        The left most drawable column of the window.
        :return: int: The left column.
        """
        return self.top_left[LEFT]

    @property
    def bottom(self) -> int:
        """
        The bottom most row of the drawable window.
        :return: int: The bottom row.
        """
        return self.bottom_right[BOTTOM]

    @property
    def right(self) -> int:
        """
        The right most column of the drawable window.
        :return: int: The right column.
        """
        return self.bottom_right[RIGHT]
