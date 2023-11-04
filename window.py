#!/usr/bin/env python3
"""
    File: window.py
    Basic curses window operations.
"""
from typing import Optional
import curses
from common import add_title_to_win, draw_border_on_win
from common import ROW, COL

DEBUG: bool = True


class Window(object):
    """
    Base window class.
    """
    def __init__(self,
                 window,
                 title: Optional[str],
                 top_left: tuple[int, int],
                 window_attrs: int,
                 border_attrs: int,
                 title_attrs: int,
                 theme: dict[str, dict[str, int | bool | str]],
                 is_main_window: bool = False,
                 ) -> None:
        """
        Initialize the window.
        :param window: curses.window | curses._CursesWindow: The curses window object.
        :param title: Optional[str]: The title of the window, if None, no title.
        :param top_left: tuple[int, int]: The top left row, col of this window.
        :param window_attrs: int: The colours and attributes for this centre of this window.
        :param border_attrs: int: The colours and attributes to use for the border of this window.
        :param title_attrs: int: The colours and attributes to use for the title of this window.
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
        self._title_attrs: int = title_attrs
        """The colour pair number and attributes for the title of this window."""
        self._theme: dict[str, dict[str, int | bool | str]] = theme
        """Store a copy of theme for subclass use."""
        self._is_main_window: bool = is_main_window
        """True if this is the main window, means certain calls aren't made."""

        # Set external properties:
        self.title: str = title
        """The title of this window."""
        self.real_size: tuple[int, int] = window.getmaxyx()
        """The real size of the window, not taking the border into account. (rows, cols)."""
        self.size: tuple[int, int] = (self.real_size[ROW] - 2, self.real_size[COL] - 2)
        """The drawable size of the window, taking the border into account. (rows, cols)."""
        self.real_top_left: tuple[int, int] = top_left
        """The real top left of this window, not taking the border into account. (row, col)."""
        self.top_left: tuple[int, int] = (self.real_top_left[ROW] + 1, self.real_top_left[COL] + 1)
        """The drawable top left of this window, taking the border into account. (row, col)."""
        self.real_bottom_right: tuple[int, int] = (self.real_top_left[ROW] + self.real_size[ROW],
                                                   self.real_top_left[COL] + self.real_size[COL])
        """The real bottom right of the window, not taking the border into account. (row, col)."""
        self.bottom_right: tuple[int, int] = (self.top_left[ROW] + self.size[ROW],
                                              self.top_left[COL] + self.size[COL])
        """The drawable bottom right of the window, taking the border into account. (row, col)."""
        return

    def redraw(self) -> None:
        # Erase the window:
        self._window.clear()
        # Draw the border:

        draw_border_on_win(window=self._window, border_attrs=self._border_attrs,
                           ts=self._theme['borderChars']['ts'], bs=self._theme['borderChars']['bs'],
                           ls=self._theme['borderChars']['ls'], rs=self._theme['borderChars']['rs'],
                           tl=self._theme['borderChars']['tl'], tr=self._theme['borderChars']['tr'],
                           bl=self._theme['borderChars']['bl'], br=self._theme['borderChars']['br']
                           )
        # Add the title to the border:
        add_title_to_win(self._window, self.title, self._border_attrs, self._title_attrs,
                         self._theme['titleChars']['start'], self._theme['titleChars']['end'])
        # Fill the centre with background colour:
        for row in range(1, self.size[ROW] + 1):
            for col in range(1, self.size[COL] + 1):
                if DEBUG:
                    try:
                        self._window.addch(row, col, ' ', self._window_attrs)
                    except curses.error:
                        message = "R: %i, C: %i, size: %s" % (row, col, self.size)
                        raise RuntimeError(message)
                else:
                    self._window.addch(row, col, ' ', self._window_attrs)

        # Refresh the window:
        self._window.refresh()
        return

    def resize(self, size: tuple[int, int], top_left: tuple[int, int]) -> None:
        """
        Recalculate size variables when the window is resized.
        :return: None
        """
        # Set Vars:

        if not self._is_main_window:
            self._window.resize(size[ROW], size[COL])
            self._window.mvwin(top_left[ROW], top_left[COL])

        num_rows, num_cols = self._window.getmaxyx()
        self.real_top_left = top_left
        self.top_left = (self.real_top_left[ROW] + 1, self.real_top_left[COL] + 1)
        self.real_size = (num_rows, num_cols)
        self.size = (num_rows - 2, num_cols - 2)
        self.real_bottom_right = (self.real_top_left[ROW] + num_rows, self.real_top_left[COL] + num_cols)
        self.bottom_right = (self.real_bottom_right[ROW] - 1, self.real_bottom_right[COL] - 1)
        return
    #
    # def redraw(self) -> None:
    #     """
    #     Redraw this window.
    #     :return: None
    #     """
    #     # Clear the window:
    #     self._window.clear()
    #     # Draw a blue and white border:
    #     self._window.attron(curses.color_pair(1) | curses.A_BOLD)
    #     self._window.border()
    #     self._window.attroff(curses.color_pair(1) | curses.A_BOLD)
    #     # Add the title:
    #     add_title_to_win(self._window, self.title, (curses.color_pair(1) | curses.A_BOLD))
    #     # Fill the rest of the screen with a blue background.
    #     for row in range(self.min_row, self.max_row + 1):
    #         for col in range(self.min_col, self.max_col + 1):
    #             self._window.addch(row, col, ' ', curses.color_pair(1))
    #     return
